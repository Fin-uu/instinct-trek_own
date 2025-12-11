import json
import re
from datetime import datetime, timedelta

class TripInfoCollector:
    """旅遊資訊收集器（規則 + LLM 混合版）"""
    
    # === 必要欄位：只有地點和天數 ===
    REQUIRED_FIELDS = {
        "location": "目的地",
        "duration": "天數"
    }
    
    # === 其他需求類型 ===
    TRIP_TYPES = [
        "家族旅遊", "畢業旅行", "情侶出遊", "朋友聚會", 
        "一個人旅行", "蜜月旅行", "親子旅遊", "員工旅遊"
    ]
    
    @staticmethod
    def extract_info_from_message(message, vllm_client=None):
        """
        智能提取：規則優先，LLM 輔助
        
        Args:
            message: 用戶訊息
            vllm_client: vLLM client（可選）
            
        Returns:
            dict: 提取的資訊
        """
        # === 第一步：規則提取（快速掃描）===
        rule_extracted = TripInfoCollector._rule_extract(message)
        
        # === 判斷是否需要 LLM ===
        has_location = rule_extracted.get("location") is not None
        has_duration = rule_extracted.get("duration") is not None
        
        # 如果規則已經提取完整，直接返回
        if has_location and has_duration:
            print("✅ 規則提取完整，不需要 LLM")
            return rule_extracted
        
        # 如果沒有 LLM client，只能用規則
        if vllm_client is None:
            print("⚠️ 規則提取不完整，但沒有 LLM client")
            return rule_extracted
        
        # === 第二步：LLM 輔助（理解複雜句子）===
        print("🤖 規則提取不完整，使用 LLM 輔助...")
        
        try:
            llm_result = TripInfoCollector._llm_extract(
                vllm_client, 
                message, 
                rule_extracted
            )
            
            # 合併結果：規則優先
            final_result = {**llm_result, **rule_extracted}
            
            # 確保 other_requirements 合併
            if "other_requirements" in llm_result or "other_requirements" in rule_extracted:
                final_result["other_requirements"] = {
                    **llm_result.get("other_requirements", {}),
                    **rule_extracted.get("other_requirements", {})
                }
            
            print("✅ LLM 輔助完成")
            return final_result
            
        except Exception as e:
            print(f"❌ LLM 失敗: {e}，使用規則結果")
            return rule_extracted
    
    @staticmethod
    def _rule_extract(message):
        """純規則提取（快速、穩定）"""
        extracted = {
            "other_requirements": {}
        }
        
        # === 1. 提取地點 ===
        cities = [
            "台北", "台南", "高雄", "花蓮", "台中", "墾丁", "台東", "宜蘭",
            "南投", "嘉義", "彰化", "新竹", "基隆", "桃園", "苗栗", "雲林",
            "屏東", "澎湖", "金門", "馬祖", "綠島", "蘭嶼", "日月潭", "阿里山",
            "九份", "太魯閣", "清境", "合歡山"
        ]
        
        for city in cities:
            if city in message:
                extracted["location"] = city
                break
        
        # === 2. 提取天數 ===
        duration_patterns = [
            r'(\d+)\s*天',
            r'(\d+)\s*日'
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, message)
            if match:
                extracted["duration"] = int(match.group(1))
                break
        
        # 特殊處理：X天Y夜
        if "天" in message and "夜" in message:
            match = re.search(r'(\d+)\s*天\s*(\d+)\s*夜', message)
            if match:
                extracted["duration"] = int(match.group(1))
        
        # === 3. 提取人數 ===
        people_patterns = [
            r'(\d+)\s*人',
            r'(\d+)\s*位',
            r'(一|兩|二|三|四|五|六|七|八|九|十)人'
        ]
        
        chinese_numbers = {
            '一': 1, '兩': 2, '二': 2, '三': 3, '四': 4, 
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        
        for pattern in people_patterns:
            match = re.search(pattern, message)
            if match:
                num = match.group(1)
                if num in chinese_numbers:
                    extracted["other_requirements"]["people"] = chinese_numbers[num]
                else:
                    extracted["other_requirements"]["people"] = int(num)
                break
        
        # === 4. 提取預算 ===
        if "萬" in message:
            budget_match = re.search(r'(\d+(?:\.\d+)?)\s*萬', message)
            if budget_match:
                extracted["other_requirements"]["budget"] = int(float(budget_match.group(1)) * 10000)
        elif re.search(r'\d{4,}', message):
            budget_match = re.search(r'(\d{4,})', message)
            if budget_match:
                extracted["other_requirements"]["budget"] = int(budget_match.group(1))
        
        # === 5. 提取旅遊類型 ===
        trip_type_keywords = {
            "家族旅遊": ["家族", "家人", "爸媽", "父母", "長輩"],
            "畢業旅行": ["畢業", "畢旅", "同學"],
            "情侶出遊": ["情侶", "男友", "女友", "兩個人", "約會"],
            "朋友聚會": ["朋友", "好友", "閨蜜", "兄弟"],
            "一個人旅行": ["一個人", "自己", "solo", "獨自"],
            "蜜月旅行": ["蜜月", "新婚", "結婚"],
            "親子旅遊": ["親子", "小孩", "孩子", "寶寶", "兒童"],
            "員工旅遊": ["員工", "公司", "團體", "員旅"]
        }
        
        for trip_type, keywords in trip_type_keywords.items():
            if any(keyword in message for keyword in keywords):
                extracted["other_requirements"]["trip_type"] = trip_type
                break
        
        # === 6. 提取偏好 ===
        preference_keywords = {
            "美食": ["美食", "吃", "小吃", "餐廳", "夜市", "美味"],
            "自然": ["自然", "風景", "山", "海", "戶外", "大自然", "風光"],
            "文化": ["文化", "歷史", "古蹟", "博物館", "廟宇", "老街"],
            "放鬆": ["放鬆", "慢活", "悠閒", "休息", "度假", "舒壓"],
            "冒險": ["冒險", "刺激", "挑戰", "極限", "運動"],
            "購物": ["購物", "買", "逛街", "商圈", "百貨"],
            "拍照": ["拍照", "打卡", "網美", "攝影", "IG"]
        }
        
        preferences = []
        for pref, keywords in preference_keywords.items():
            if any(keyword in message for keyword in keywords):
                preferences.append(pref)
        
        if preferences:
            extracted["other_requirements"]["preferences"] = preferences
        
        # === 7. 提取特殊需求 ===
        special_needs = []
        
        if any(word in message for word in ["輪椅", "行動不便", "無障礙"]):
            special_needs.append("需要無障礙設施")
        
        if any(word in message for word in ["素食", "吃素", "vegetarian"]):
            special_needs.append("素食")
        
        if any(word in message for word in ["寵物", "狗", "貓", "毛小孩"]):
            special_needs.append("攜帶寵物")
        
        if any(word in message for word in ["小孩", "孩子", "baby", "寶寶", "嬰兒"]):
            special_needs.append("有小孩同行")
        
        if special_needs:
            extracted["other_requirements"]["special_needs"] = special_needs
        
        # === 8. 保存原始輸入 ===
        extracted["other_requirements"]["raw_input"] = message
        
        return extracted
    
    @staticmethod
    def _llm_extract(vllm_client, message, rule_result):
        """
        LLM 輔助提取（只提取規則沒找到的）
        
        重要：讓 LLM 專注於「理解意圖」，不要做結構化輸出
        """
        
        # 構建簡單的 Prompt
        has_location = rule_result.get("location") is not None
        has_duration = rule_result.get("duration") is not None
        
        if not has_location and not has_duration:
            # 都沒有，問 LLM：用戶想去哪裡玩幾天？
            prompt = f"""User says: "{message}"

Extract ONLY:
1. Location (city name in Taiwan)
2. Duration (number of days)

Reply in this EXACT format:
Location: [city name or "unknown"]
Duration: [number or "unknown"]

Example:
User: "想去南部玩個三天"
Location: unknown
Duration: 3

User: "台東好像不錯"
Location: 台東
Duration: unknown

Now extract from: "{message}"
"""
        
        elif not has_location:
            # 有天數，沒地點
            prompt = f"""User says: "{message}"
They want to travel for {rule_result['duration']} days.

What is the destination city?
Reply ONLY the city name in Traditional Chinese, or "unknown".

Examples:
"不知道去哪" → unknown
"可能去南部" → unknown
"台東好像不錯" → 台東
"去海邊玩" → unknown

City name:"""
        
        else:  # not has_duration
            # 有地點，沒天數
            prompt = f"""User says: "{message}"
They want to go to {rule_result['location']}.

How many days do they want to travel?
Reply ONLY a number, or "unknown".

Examples:
"想去走走" → unknown
"週末去" → 2
"玩個三四天" → 3

Number of days:"""
        
        try:
            response = vllm_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": "You extract travel information. Reply briefly and directly."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=50,
                stop=["\n\n"]
            )
            
            content = response.choices[0].message.content.strip()
            print(f"[LLM 回應] {content}")
            
            # 驗證回應是否有效（不是全是特殊字符）
            if not content or len(content) < 1 or content.count('!') > len(content) * 0.5:
                print(f"\n⚠️  vLLM 回應無效（返回了 {content.count('!')} 個驚嘆號）")
                print(f"💡 可能原因：")
                print(f"   - vLLM 模型資源不足或過載")
                print(f"   - 模型配置錯誤")
                print(f"   - 需要重啟 vLLM 服務")
                print(f"✅ 系統將使用基於規則的提取結果\n")
                return {}
            
            # 解析回應
            extracted = {}
            
            if not has_location and not has_duration:
                # 解析 Location: ... / Duration: ...
                for line in content.split('\n'):
                    if 'Location:' in line or 'location:' in line:
                        loc = line.split(':')[1].strip()
                        if loc.lower() not in ['unknown', 'none', '']:
                            extracted["location"] = loc
                    
                    if 'Duration:' in line or 'duration:' in line:
                        dur = line.split(':')[1].strip()
                        if dur.isdigit():
                            extracted["duration"] = int(dur)
            
            elif not has_location:
                # 解析城市名稱
                if content.lower() not in ['unknown', 'none', '']:
                    # 清理可能的格式
                    city = content.replace('City name:', '').replace('Location:', '').strip()
                    if city and len(city) <= 10:  # 合理的城市名長度
                        extracted["location"] = city
            
            else:  # not has_duration
                # 解析天數
                # 可能的回應："3", "Number of days: 3", "3 days"
                import re
                numbers = re.findall(r'\d+', content)
                if numbers:
                    extracted["duration"] = int(numbers[0])
            
            return extracted
            
        except Exception as e:
            print(f"❌ LLM 提取錯誤: {e}")
            return {}
    
    @staticmethod
    def merge_info(current_info, new_info):
        """合併資訊"""
        merged = current_info.copy() if current_info else {}
        
        # 合併基本欄位
        if "location" in new_info:
            merged["location"] = new_info["location"]
        
        if "duration" in new_info:
            merged["duration"] = new_info["duration"]
        
        # 合併 other_requirements
        if "other_requirements" not in merged:
            merged["other_requirements"] = {}
        
        if "other_requirements" in new_info:
            for key, value in new_info["other_requirements"].items():
                if key == "preferences" and key in merged["other_requirements"]:
                    existing = merged["other_requirements"]["preferences"]
                    merged["other_requirements"]["preferences"] = list(set(existing + value))
                elif key == "special_needs" and key in merged["other_requirements"]:
                    existing = merged["other_requirements"]["special_needs"]
                    merged["other_requirements"]["special_needs"] = list(set(existing + value))
                else:
                    merged["other_requirements"][key] = value
        
        return merged
    
    @staticmethod
    def get_missing_fields(info):
        """取得缺少的必要欄位"""
        missing = []
        
        if not info.get("location"):
            missing.append(("location", "目的地"))
        
        if not info.get("duration"):
            missing.append(("duration", "天數"))
        
        return missing
    
    @staticmethod
    def generate_follow_up_question(missing_fields, current_info, client=None):
        """
        生成追問問題
        
        可以選擇性使用 LLM 生成更自然的追問
        """
        if not missing_fields:
            return None
        
        field, label = missing_fields[0]
        
        # === 預設問題（規則）===
        default_questions = {
            "location": "請問您想去哪個城市旅遊呢？\n\n💡 熱門選擇：\n• 台北：都市風光、美食購物\n• 台南：古蹟美食、文化巡禮\n• 花蓮：山海美景、太魯閣\n• 墾丁：海灘度假、水上活動",
            
            "duration": "請問預計玩幾天呢？\n\n💡 常見選擇：\n• 2天1夜：週末小旅行\n• 3天2夜：經典行程\n• 4天3夜：深度體驗"
        }
        
        default_question = default_questions.get(field, f"請提供您的{label}資訊")
        
        # === 如果有 LLM，生成更自然的追問 ===
        if client is not None:
            try:
                # 根據已知資訊生成個性化追問
                context = []
                if current_info.get("location"):
                    context.append(f"目的地是{current_info['location']}")
                if current_info.get("duration"):
                    context.append(f"玩{current_info['duration']}天")
                
                other = current_info.get("other_requirements", {})
                if other.get("trip_type"):
                    context.append(f"是{other['trip_type']}")
                
                context_str = "、".join(context) if context else "還沒有資訊"
                
                prompt = f"""You are a friendly travel assistant.

Known: {context_str}
Missing: {label}

Generate ONE friendly question in Traditional Chinese asking for the {label}.
Keep it under 30 characters. Be warm and encouraging.

Question:"""
                
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a friendly assistant. Reply in Traditional Chinese."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=80,
                    stop=["\n"]
                )
                
                llm_question = response.choices[0].message.content.strip()
                
                # 驗證回應（檢查是否為垃圾輸出）
                if llm_question and 5 <= len(llm_question) <= 100:
                    # 檢查是否全是特殊字符
                    if llm_question.count('!') > len(llm_question) * 0.5:
                        print(f"⚠️ LLM 追問無效（特殊字符過多），使用預設問題")
                    else:
                        print(f"✅ LLM 生成追問：{llm_question}")
                        return llm_question
                
            except Exception as e:
                print(f"⚠️ LLM 追問生成失敗: {e}")
        
        # 返回預設問題
        return default_question
    
    @staticmethod
    def is_info_complete(info):
        """判斷資訊是否完整"""
        has_location = info.get("location") is not None
        has_duration = info.get("duration") is not None
        
        if has_location and has_duration:
            # 自動填充
            if "other_requirements" not in info:
                info["other_requirements"] = {}
            
            other = info["other_requirements"]
            
            if "date" not in other:
                other["date"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            if "people" not in other:
                trip_type = other.get("trip_type", "")
                if trip_type == "一個人旅行":
                    other["people"] = 1
                elif trip_type in ["情侶出遊", "蜜月旅行"]:
                    other["people"] = 2
                elif trip_type in ["家族旅遊", "朋友聚會"]:
                    other["people"] = 4
                else:
                    other["people"] = 1
            
            if "budget" not in other:
                people = other.get("people", 1)
                duration = info.get("duration", 3)
                other["budget"] = duration * 5000 * people
            
            return True
        
        return False
    
    @staticmethod
    def format_collected_info(info):
        """格式化顯示已收集的資訊"""
        lines = []
        
        if info.get("location"):
            lines.append(f"📍 **目的地**：{info['location']}")
        
        if info.get("duration"):
            lines.append(f"⏱️ **天數**：{info['duration']}天")
        
        other = info.get("other_requirements", {})
        
        if other.get("people"):
            lines.append(f"👥 **人數**：{other['people']}人")
        
        if other.get("budget"):
            lines.append(f"💰 **預算**：NT$ {other['budget']:,}")
        
        if other.get("trip_type"):
            lines.append(f"🎯 **類型**：{other['trip_type']}")
        
        if other.get("preferences"):
            prefs = "、".join(other['preferences'])
            lines.append(f"❤️ **偏好**：{prefs}")
        
        if other.get("special_needs"):
            needs = "、".join(other['special_needs'])
            lines.append(f"⚠️ **特殊需求**：{needs}")
        
        return "\n".join(lines) if lines else "（尚未收集資訊）"
    
    @staticmethod
    def get_summary_for_generation(info):
        """取得用於生成行程的摘要"""
        other = info.get("other_requirements", {})
        
        return {
            "location": info.get("location"),
            "duration": info.get("duration"),
            "budget": other.get("budget"),
            "people": other.get("people", 1),
            "trip_type": other.get("trip_type"),
            "preferences": other.get("preferences", []),
            "special_needs": other.get("special_needs", []),
            "date": other.get("date")
        }