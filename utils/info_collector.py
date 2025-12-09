import json
import re

class TripInfoCollector:
    """旅遊資訊收集器"""
    
    # 必要欄位（只顯示必問的）
    REQUIRED_FIELDS = {
        "location": "目的地",
        "duration": "天數"
    }
    
    # 可選欄位（不強制問）
    OPTIONAL_FIELDS = {
        "date": "出發日期",
        "people": "人數",
        "budget": "預算",
        "preferences": "偏好"
    }
    
    @staticmethod
    def extract_info_from_message(message):
        """
        從用戶訊息中提取旅遊資訊
        
        Args:
            message: 用戶訊息
            
        Returns:
            dict: 提取到的資訊 {"location": ..., "duration": ..., ...}
        """
        extracted = {}
        
        # 1. 提取地點（擴充城市列表）
        cities = [
            "台北", "台南", "高雄", "花蓮", "台中", "墾丁", "台東", "宜蘭",
            "南投", "嘉義", "彰化", "新竹", "基隆", "桃園", "苗栗", "雲林",
            "屏東", "澎湖", "金門", "馬祖", "綠島", "蘭嶼"
        ]
        for city in cities:
            if city in message:
                extracted["location"] = city
                break
        
        # 2. 提取日期
        date_patterns = [
            r'(\d{1,2})月(\d{1,2})日',
            r'(\d{1,2})/(\d{1,2})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(今天|明天|後天)'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, message)
            if match:
                if match.group(0) in ['今天', '明天', '後天']:
                    from datetime import datetime, timedelta
                    days_offset = {'今天': 0, '明天': 1, '後天': 2}[match.group(0)]
                    date = datetime.now() + timedelta(days=days_offset)
                    extracted["date"] = date.strftime("%Y-%m-%d")
                elif len(match.groups()) == 2 and match.group(0).count('月') > 0:
                    from datetime import datetime
                    month, day = match.groups()
                    year = datetime.now().year
                    extracted["date"] = f"{year}-{int(month):02d}-{int(day):02d}"
                break
        
        # 3. 提取天數
        duration_patterns = [
            r'(\d+)\s*天',
            r'(\d+)\s*日'
        ]
        for pattern in duration_patterns:
            match = re.search(pattern, message)
            if match:
                extracted["duration"] = int(match.group(1))
                break
        
        # 4. 提取人數
        people_patterns = [
            r'(\d+)\s*人',
            r'(\d+)\s*位',
            r'(一|兩|二|三|四|五|六|七|八|九|十)人'
        ]
        chinese_numbers = {'一': 1, '兩': 2, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
        for pattern in people_patterns:
            match = re.search(pattern, message)
            if match:
                num = match.group(1)
                if num in chinese_numbers:
                    extracted["people"] = chinese_numbers[num]
                else:
                    extracted["people"] = int(num)
                break
        
        # 5. 提取預算
        if "萬" in message:
            budget_match = re.search(r'(\d+(?:\.\d+)?)\s*萬', message)
            if budget_match:
                extracted["budget"] = int(float(budget_match.group(1)) * 10000)
        else:
            budget_match = re.search(r'(\d{4,})', message)
            if budget_match:
                extracted["budget"] = int(budget_match.group(1))
        
        # 6. 提取偏好
        preference_keywords = {
            "美食": ["美食", "吃", "小吃", "餐廳", "夜市"],
            "自然": ["自然", "風景", "山", "海", "戶外", "大自然"],
            "文化": ["文化", "歷史", "古蹟", "博物館", "廟宇"],
            "放鬆": ["放鬆", "慢活", "悠閒", "休息", "度假"],
            "冒險": ["冒險", "刺激", "挑戰", "極限"],
            "購物": ["購物", "買", "逛街", "商圈"],
            "親子": ["親子", "小孩", "兒童", "家庭"]
        }
        
        preferences = []
        for pref, keywords in preference_keywords.items():
            if any(keyword in message for keyword in keywords):
                preferences.append(pref)
        
        if preferences:
            extracted["preferences"] = preferences
        
        return extracted
    
    @staticmethod
    def merge_info(current_info, new_info):
        """
        合併資訊
        
        Args:
            current_info: 目前已收集的資訊
            new_info: 新提取的資訊
            
        Returns:
            dict: 合併後的資訊
        """
        merged = {**current_info, **new_info}
        
        # 特殊處理：偏好列表合併（去重）
        if "preferences" in current_info and "preferences" in new_info:
            all_prefs = current_info["preferences"] + new_info["preferences"]
            merged["preferences"] = list(set(all_prefs))
        
        return merged
    
    @staticmethod
    def get_missing_fields(info):
        """
        取得缺少的必要欄位（只檢查 REQUIRED_FIELDS）
        
        Args:
            info: 已收集的資訊
            
        Returns:
            list: [(field_key, field_label), ...]
        """
        missing = []
        for field, label in TripInfoCollector.REQUIRED_FIELDS.items():
            if field not in info or not info[field]:
                missing.append((field, label))
        return missing
    
    @staticmethod
    def generate_follow_up_question(missing_fields, current_info, client=None):
        """生成追問問題（增強版）"""
        if not missing_fields or len(missing_fields) == 0:
            return None
        
        field, label = missing_fields[0]
        
        # === 備用靜態問題 ===
        fallback_questions = {
            "location": "請問您想去哪個城市旅遊呢？（例如：台北、台南、花蓮、台東）",
            "date": "請問預計什麼時候出發？（例如：12月15日、1月1日）",
            "duration": "預計玩幾天呢？（例如：2天、3天、4天）",
            "people": "請問有幾位要一起去呢？（例如：1人、2人、4人）",
            "budget": "預算大約多少呢？（例如：每人 1 萬、1.5 萬或 2 萬）",
            "preferences": "比較偏好哪種旅遊風格呢？（例如：美食、自然風光、文化體驗）"
        }
        
        # === 如果沒有提供 client，直接使用備用 ===
        if client is None:
            print("⚠️ 未提供 LLM client，使用備用問題")
            return fallback_questions.get(field, f"請提供您的{label}資訊")
        
        # === 嘗試使用 LLM 生成（但不是必須）===
        try:
            current_info_str = ", ".join([f"{v}" for k, v in current_info.items() if v])
            
            # 檢測客戶端類型
            if hasattr(client, 'generate_content'):
                # Gemini - 使用中文 prompt（Gemini 支援中文良好）
                prompt = f"""
你是旅遊助手。用**一句話**親切詢問用戶「{label}」。

已知：{current_info_str if current_info_str else "無"}
缺少：{label}

要求：
- 只問一個問題
- 給 2-3 個選項
- 不超過 40 字
- 語氣親切

例如：「預計玩幾天呢？（例如 2 天、3 天、4 天）」
"""
                response = client.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 80,
                    }
                )
                question = response.text.strip()
            else:
                # vLLM - 使用英文 prompt（vLLM 對英文更穩定）
                field_name_en = {
                    "location": "destination city",
                    "date": "departure date",
                    "duration": "trip duration (days)",
                    "people": "number of travelers",
                    "budget": "budget (NT$)",
                    "preferences": "travel preferences"
                }.get(field, "information")
                
                prompt = f"""
You are a friendly travel assistant. Generate ONE short question in Traditional Chinese to ask the user about "{field_name_en}".

Known info: {current_info_str if current_info_str else "None"}
Missing: {field_name_en}

Requirements:
- Ask in Traditional Chinese (繁體中文)
- One question only
- Provide 2-3 example options
- Keep under 40 characters
- Friendly tone

Example: "預計玩幾天呢？（例如 2 天、3 天、4 天）"

Generate the question:"""
                
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a helpful travel assistant that asks questions in Traditional Chinese."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=80
                )
                question = response.choices[0].message.content.strip()
            
            # 驗證回應
            if not question or len(question) < 5 or question.count('!') > 50:
                raise ValueError("LLM 回應異常")
            
            return question
            
        except Exception as e:
            print(f"⚠️ LLM 生成失敗: {e}，使用備用問題")
            return fallback_questions.get(field, f"請提供您的{label}資訊")
    
    @staticmethod
    def is_info_complete(info):
        """
        判斷資訊是否完整（極簡版）
        必要：目的地 + 天數
        其他自動填充
        """
        has_location = "location" in info and info["location"]
        has_duration = "duration" in info and info["duration"]
        
        if has_location and has_duration:
            # === 自動填充預設值 ===
            from datetime import datetime, timedelta
            
            # 自動填充出發日期
            if "date" not in info or not info["date"]:
                info["date"] = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            # 自動填充人數
            if "people" not in info or not info["people"]:
                info["people"] = 1
            
            # 自動填充預算（如果沒有）
            if "budget" not in info or not info["budget"]:
                info["budget"] = info["duration"] * 5000 * info.get("people", 1)
            
            # 偏好是可選的，不填也沒關係
            if "preferences" not in info:
                info["preferences"] = []
            
            return True
        
        return False
    
    @staticmethod
    def format_collected_info(info):
        """
        格式化顯示已收集的資訊
        
        Args:
            info: 已收集的資訊
            
        Returns:
            str: 格式化的字符串
        """
        lines = []
        
        if "location" in info and info["location"]:
            lines.append(f"📍 **目的地**：{info['location']}")
        
        if "date" in info and info["date"]:
            lines.append(f"📅 **出發日期**：{info['date']}")
        
        if "duration" in info and info["duration"]:
            lines.append(f"⏱️ **天數**：{info['duration']}天")
        
        if "people" in info and info["people"]:
            lines.append(f"👥 **人數**：{info['people']}人")
        
        if "budget" in info and info["budget"]:
            lines.append(f"💰 **預算**：NT$ {info['budget']:,}")
        
        if "preferences" in info and info["preferences"]:
            prefs = "、".join(info['preferences']) if isinstance(info['preferences'], list) else info['preferences']
            lines.append(f"🎯 **偏好**：{prefs}")
        
        return "\n".join(lines) if lines else "尚未收集資訊"
        """
        使用 vLLM 提取結構化資訊
        
        Args:
            vllm_client: OpenAI client（vLLM）
            message: 用戶訊息
            current_info: 目前已收集的資訊
        
        Returns:
            {
                "extracted_info": {...},  # 提取到的資訊
                "is_complete": bool,      # 是否完整
                "missing_fields": [...],  # 缺少的欄位
                "follow_up_question": str # 追問問題
            }
        """
        
        # 構建 Prompt
        current_info_str = json.dumps(current_info or {}, ensure_ascii=False)
        
        prompt = f"""
你是旅遊助手，正在收集用戶的旅遊需求。

**已收集資訊**：
{current_info_str}

**用戶新訊息**：
"{message}"

**任務**：
1. 從新訊息中提取旅遊資訊
2. 判斷資訊是否完整
3. 如果不完整，生成一個追問問題

**必要資訊**：
- location（目的地城市）
- duration（天數）

**可選資訊**：
- budget（預算，單位：NT$）
- preferences（偏好：美食/自然/文化/放鬆/冒險/購物/親子）

**回傳格式（只回傳 JSON）**：
{{
  "extracted_info": {{
    "location": "提取到的城市（台北/台南/高雄/花蓮/台中/墾丁/台東/宜蘭等）",
    "duration": 天數數字,
    "budget": 預算數字,
    "preferences": ["偏好1", "偏好2"]
  }},
  "is_complete": true/false,
  "missing_fields": ["缺少的欄位"],
  "follow_up_question": "追問問題（如果 is_complete 為 false）"
}}

**範例**：

用戶說「我想去台東玩」
→ {{"extracted_info": {{"location": "台東"}}, "is_complete": false, "missing_fields": ["duration"], "follow_up_question": "好的！預計玩幾天呢？（例如 2 天、3 天、4 天）"}}

用戶說「三天兩夜」
→ {{"extracted_info": {{"duration": 3}}, "is_complete": false, "missing_fields": ["budget"], "follow_up_question": "了解！預算大約多少呢？（例如每人 1 萬、1.5 萬）"}}

用戶說「預算一萬五」
→ {{"extracted_info": {{"budget": 15000}}, "is_complete": true, "missing_fields": [], "follow_up_question": ""}}

**注意**：
- 只回傳 JSON，不要其他文字
- 追問要親切自然
- 一次只問一個問題
"""

        try:
            response = vllm_client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            # 清理 JSON
            content = content.replace("```json", "").replace("```", "").strip()
            
            # 解析
            result = json.loads(content)
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            print(f"原始內容: {content[:200] if 'content' in locals() else 'N/A'}")
            
            # 備用：簡單規則提取
            return TripInfoCollector._fallback_extract(message, current_info)
        
        except Exception as e:
            print(f"vLLM 錯誤: {e}")
            return TripInfoCollector._fallback_extract(message, current_info)
    
    @staticmethod
    def _fallback_extract(message, current_info):
        """備用提取方案（規則匹配）"""
        extracted = {}
        
        # 提取地點
        cities = ["台北", "台南", "高雄", "花蓮", "台中", "墾丁", "台東", "宜蘭", "南投"]
        for city in cities:
            if city in message:
                extracted["location"] = city
                break
        
        # 提取天數
        duration_match = re.search(r'(\d+)\s*天', message)
        if duration_match:
            extracted["duration"] = int(duration_match.group(1))
        
        # 提取預算
        if "萬" in message:
            budget_match = re.search(r'(\d+)\s*萬', message)
            if budget_match:
                extracted["budget"] = int(budget_match.group(1)) * 10000
        else:
            budget_match = re.search(r'(\d{4,})', message)
            if budget_match:
                extracted["budget"] = int(budget_match.group(1))
        
        # 提取偏好
        pref_map = {
            "美食": ["美食", "吃", "小吃"],
            "自然": ["自然", "山", "海", "風景"],
            "文化": ["文化", "歷史", "古蹟"],
            "放鬆": ["放鬆", "慢活", "悠閒"]
        }
        
        prefs = []
        for pref, keywords in pref_map.items():
            if any(k in message for k in keywords):
                prefs.append(pref)
        
        if prefs:
            extracted["preferences"] = prefs
        
        # 合併資訊
        info = {**(current_info or {}), **extracted}
        
        # 判斷完整性
        is_complete = "location" in info and "duration" in info
        
        # 缺少的欄位
        missing = []
        if "location" not in info:
            missing.append("location")
        if "duration" not in info:
            missing.append("duration")
        
        # 生成追問
        follow_up = ""
        if not is_complete:
            if "location" not in info:
                follow_up = "請問想去哪個城市呢？（例如：台北、台南、花蓮、台東）"
            elif "duration" not in info:
                follow_up = "預計玩幾天呢？（例如：2天、3天、4天）"
        
        return {
            "extracted_info": extracted,
            "is_complete": is_complete,
            "missing_fields": missing,
            "follow_up_question": follow_up
        }
    
    @staticmethod
    def merge_info(existing_info, new_info):
        """合併資訊"""
        merged = (existing_info or {}).copy()
        merged.update(new_info)
        return merged
    
    @staticmethod
    def format_info_display(info):
        """格式化顯示已收集資訊"""
        lines = []
        
        if info.get("location"):
            lines.append(f"📍 **目的地**：{info['location']}")
        
        if info.get("duration"):
            lines.append(f"📅 **天數**：{info['duration']}天")
        
        if info.get("budget"):
            lines.append(f"💰 **預算**：NT$ {info['budget']:,}")
        
        if info.get("preferences"):
            prefs = "、".join(info['preferences'])
            lines.append(f"🎯 **偏好**：{prefs}")
        
        return "\n".join(lines) if lines else "（尚無資訊）"