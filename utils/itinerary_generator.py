from datetime import datetime, timedelta
import json

class ItineraryGenerator:
    """AI 行程生成器"""
    
    @staticmethod
    def generate_itinerary(client, location, duration, budget=None, preferences=None):
        """
        使用 AI 生成完整行程（支援 Gemini 和 vLLM）
        
        Args:
            client: Gemini GenerativeModel 或 OpenAI client
            location: 目的地
            duration: 天數
            budget: 預算（可選）
            preferences: 偏好列表（可選）
        """
        
        # 處理偏好
        pref_text = ""
        if preferences:
            if isinstance(preferences, list):
                pref_text = "、".join(preferences)
            else:
                pref_text = preferences
        
        # 簡化的 Prompt
        prompt = f"""
你是專業的台灣旅遊規劃師。請生成完整有效的 JSON 格式行程。

**用戶需求**：
- 目的地：{location}
- 天數：{duration}天
- 預算：{f'NT$ {budget:,}' if budget else '彈性預算'}
- 偏好：{pref_text if pref_text else '綜合旅遊'}

**重要**：
1. 只回傳完整的 JSON，不要任何其他文字
2. 確保 JSON 語法完全正確，所有括號、引號、逗號都要完整
3. 不要截斷，必須完整輸出到最後
4. 不要使用 markdown 標記

JSON 格式範例：
{{
  "trip_name": "{location}{duration}日遊",
  "location": "{location}",
  "duration": {duration},
  "total_budget": {budget if budget else duration * 10000},
  "budget_breakdown": {{
    "accommodation": {int((budget if budget else duration * 10000) * 0.3)},
    "food": {int((budget if budget else duration * 10000) * 0.3)},
    "transport": {int((budget if budget else duration * 10000) * 0.2)},
    "activities": {int((budget if budget else duration * 10000) * 0.2)}
  }},
  "daily_itinerary": [
    {{
      "day": 1,
      "theme": "抵達與市區探索",
      "activities": [
        {{
          "time": "09:00",
          "name": "活動名稱",
          "type": "景點",
          "location": "具體地點",
          "duration": "2小時",
          "cost": 0,
          "note": "簡短說明",
          "icon": "🗺️"
        }}
      ]
    }}
  ],
  "accommodation_suggestions": [
    {{
      "name": "住宿建議",
      "type": "飯店/民宿",
      "area": "區域",
      "price_range": "價格範圍",
      "reason": "推薦理由"
    }}
  ],
  "transport_tips": "交通方式建議",
  "packing_list": ["必備物品1", "必備物品2"],
  "important_notes": ["注意事項1", "注意事項2"]
}}

規劃原則：
- 每天安排 4-5 個活動
- 根據偏好「{pref_text}」設計特色行程
- 考慮地理位置和交通動線
- 包含早中晚餐建議
- 預算分配合理

現在請生成完整的 JSON："""

        try:
            # 檢測 client 類型
            if hasattr(client, 'generate_content'):
                # Gemini API - 根據天數調整輸出長度（增加容量避免截斷）
                max_tokens = min(8000, duration * 800)  # 增加到每天 800 tokens
                print(f"🤖 使用 Gemini 生成 {duration} 天行程，max_tokens: {max_tokens}")
                response = client.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.6,  # 降低溫度提高穩定性
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": max_tokens,
                        "response_mime_type": "application/json"  # 強制 JSON 輸出
                    }
                )
                content = response.text.strip()
                print(f"✅ Gemini 回應長度: {len(content)} 字元")
            else:
                # OpenAI compatible API (vLLM)
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "你是台灣旅遊專家。只回傳有效的 JSON 格式，不要其他內容。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=3000
                )
                content = response.choices[0].message.content.strip()
            
            # 更強力的清理
            # 移除可能的 markdown 標記
            content = content.replace("```json", "").replace("```", "").strip()
            
            # 更強力的清理
            # 移除可能的 markdown 標記
            content = content.replace("```json", "").replace("```", "").strip()
            
            # 移除開頭的非 JSON 字符
            if not content.startswith("{"):
                # 找到第一個 { 開始
                start_idx = content.find("{")
                if start_idx != -1:
                    content = content[start_idx:]
                else:
                    raise ValueError("找不到 JSON 開始標記")
            
            # 移除結尾的非 JSON 字符
            if not content.endswith("}"):
                # 找到最後一個 } 結束
                end_idx = content.rfind("}")
                if end_idx != -1:
                    content = content[:end_idx+1]
                else:
                    raise ValueError("找不到 JSON 結束標記")
            
            # 處理可能的截斷 JSON（移除不完整的最後一個屬性）
            # 如果 JSON 在解析時失敗，嘗試修復常見問題
            try:
                itinerary = json.loads(content)
            except json.JSONDecodeError as first_error:
                print(f"第一次解析失敗: {first_error}, 嘗試修復...")
                
                # 策略 1: 找到錯誤位置並截斷到最近的完整結構
                error_pos = first_error.pos
                
                # 截斷到錯誤位置之前
                truncated = content[:error_pos]
                
                # 向前尋找最後一個完整的 activity 或 day
                # 先找最後一個 }
                last_brace = truncated.rfind('}')
                if last_brace > 0:
                    truncated = truncated[:last_brace+1]
                    
                    # 補全必要的結構
                    # 檢查是否在 daily_itinerary 陣列中
                    if '"daily_itinerary"' in truncated:
                        # 確保 daily_itinerary 陣列結束
                        if truncated.count('[') > truncated.count(']'):
                            truncated += ']' * (truncated.count('[') - truncated.count(']'))
                        
                        # 補充缺失的欄位
                        if '"accommodation_suggestions"' not in truncated:
                            truncated += ', "accommodation_suggestions": []'
                        if '"transport_tips"' not in truncated:
                            truncated += ', "transport_tips": "建議使用大眾運輸工具"'
                        if '"packing_list"' not in truncated:
                            truncated += ', "packing_list": ["輕便服裝", "防曬用品"]'
                        if '"important_notes"' not in truncated:
                            truncated += ', "important_notes": ["注意天氣變化"]'
                    
                    # 補全最外層的 }
                    open_braces = truncated.count('{') - truncated.count('}')
                    truncated += '}' * open_braces
                    
                    try:
                        itinerary = json.loads(truncated)
                        print("截斷修復成功！")
                    except json.JSONDecodeError as second_error:
                        print(f"截斷修復失敗: {second_error}, 使用模板...")
                        raise first_error
                else:
                    print("找不到有效的結構，使用模板...")
                    raise first_error
            
            # 驗證必要欄位
            required_fields = ["trip_name", "location", "duration", "daily_itinerary"]
            missing_fields = [f for f in required_fields if f not in itinerary]
            
            if missing_fields:
                raise ValueError(f"缺少必要欄位: {missing_fields}")
            
            return {
                "success": True,
                "data": itinerary
            }
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON 解析錯誤: {e}")
            print(f"📍 錯誤位置: line {e.lineno} column {e.colno}")
            print(f"📏 原始內容長度: {len(content)} 字元")
            print(f"📖 內容開頭 (前300字): {content[:300]}")
            print(f"📖 內容結尾 (後300字): {content[-300:]}")
            print(f"\n💡 這通常表示 Gemini 生成的 JSON 不完整或格式錯誤")
            print(f"💡 系統將使用備用模板（來自 data/trip_templates.json）\n")
            
            # 儲存完整內容到檔案以便除錯
            try:
                with open("debug_json_error.txt", "w", encoding="utf-8") as f:
                    f.write(f"錯誤: {e}\n")
                    f.write(f"位置: line {e.lineno} column {e.colno}\n")
                    f.write(f"\n完整內容:\n{content}")
                print("完整錯誤內容已儲存至 debug_json_error.txt")
            except:
                pass
            
            return {
                "success": False,
                "error": f"JSON 解析失敗: {str(e)}",
                "fallback": ItineraryGenerator._create_fallback_itinerary(location, duration, budget)
            }
        except Exception as e:
            print(f"生成錯誤: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "fallback": ItineraryGenerator._create_fallback_itinerary(location, duration, budget)
            }
    
    @staticmethod
    def _create_fallback_itinerary(location, duration, budget):
        """
        備用方案：從模板載入高品質行程
        """
        import json
        import os
        
        # 載入行程模板
        template_path = "data/trip_templates.json"
        
        try:
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                
                # 尋找匹配的模板
                if location in templates:
                    duration_key = f"{duration}天"
                    
                    # 精確匹配
                    if duration_key in templates[location]:
                        template = templates[location][duration_key]
                        
                        # 調整預算
                        if budget:
                            template['total_budget'] = budget
                            template['budget_breakdown'] = {
                                "accommodation": int(budget * 0.3),
                                "food": int(budget * 0.3),
                                "transport": int(budget * 0.2),
                                "activities": int(budget * 0.2)
                            }
                        
                        return template
                    
                    # 尋找最接近的天數
                    available_durations = list(templates[location].keys())
                    if available_durations:
                        # 使用第一個可用模板
                        closest_template = templates[location][available_durations[0]]
                        
                        # 調整天數（簡單複製或刪減）
                        if duration > len(closest_template['daily_itinerary']):
                            # 需要更多天，複製最後一天
                            while len(closest_template['daily_itinerary']) < duration:
                                last_day = closest_template['daily_itinerary'][-1].copy()
                                last_day['day'] = len(closest_template['daily_itinerary']) + 1
                                closest_template['daily_itinerary'].append(last_day)
                        elif duration < len(closest_template['daily_itinerary']):
                            # 需要較少天，截取前N天
                            closest_template['daily_itinerary'] = closest_template['daily_itinerary'][:duration]
                        
                        closest_template['duration'] = duration
                        
                        if budget:
                            closest_template['total_budget'] = budget
                        
                        return closest_template
        
        except Exception as e:
            print(f"載入模板失敗: {e}")
        
        # 如果模板不存在或載入失敗，使用基本架構
        return ItineraryGenerator._create_basic_itinerary(location, duration, budget)
    
    @staticmethod
    def _create_basic_itinerary(location, duration, budget):
        """最基本的行程架構（終極備案）"""
        
        total_budget = budget if budget else duration * 5000
        
        daily_itinerary = []
        for day in range(1, duration + 1):
            daily_itinerary.append({
                "day": day,
                "theme": f"Day {day} - {location}探索",
                "activities": [
                    {
                        "time": "09:00",
                        "name": "早餐時光",
                        "type": "美食",
                        "location": location,
                        "duration": "1小時",
                        "cost": 150,
                        "note": "探索在地早餐小吃",
                        "icon": "🍳"
                    },
                    {
                        "time": "10:30",
                        "name": "上午景點",
                        "type": "景點",
                        "location": location,
                        "duration": "2小時",
                        "cost": 200,
                        "note": "參觀當地主要景點",
                        "icon": "🏛️"
                    },
                    {
                        "time": "13:00",
                        "name": "午餐時間",
                        "type": "美食",
                        "location": location,
                        "duration": "1.5小時",
                        "cost": 300,
                        "note": "品嚐當地特色料理",
                        "icon": "🍜"
                    },
                    {
                        "time": "15:00",
                        "name": "下午活動",
                        "type": "景點",
                        "location": location,
                        "duration": "2小時",
                        "cost": 150,
                        "note": "休閒漫遊或文化體驗",
                        "icon": "🎨"
                    },
                    {
                        "time": "18:30",
                        "name": "晚餐 & 夜市",
                        "type": "美食",
                        "location": location,
                        "duration": "2小時",
                        "cost": 400,
                        "note": "夜市美食巡禮",
                        "icon": "🌙"
                    }
                ]
            })
        
        return {
            "trip_name": f"{location}{duration}日遊",
            "location": location,
            "duration": duration,
            "total_budget": total_budget,
            "budget_breakdown": {
                "accommodation": int(total_budget * 0.3),
                "food": int(total_budget * 0.3),
                "transport": int(total_budget * 0.2),
                "activities": int(total_budget * 0.2)
            },
            "daily_itinerary": daily_itinerary,
            "accommodation_suggestions": [
                {
                    "name": f"{location}市中心旅館",
                    "type": "商務旅館",
                    "area": "市中心",
                    "price_range": f"NT$ {int(total_budget * 0.15):,}-{int(total_budget * 0.2):,}/晚",
                    "reason": "交通便利，近主要景點"
                }
            ],
            "transport_tips": "建議使用大眾運輸工具，可購買一日券較划算",
            "packing_list": ["防曬用品", "雨具", "舒適步鞋", "相機", "充電器"],
            "important_notes": ["注意天氣變化", "提前訂房享優惠", "夜市記得空腹去", "保持彈性調整行程"]
        }
    
    @staticmethod
    def convert_to_trip_format(itinerary_data):
        """將 AI 生成的行程轉換為系統格式"""
        from utils.trip_manager import TripManager
        from datetime import datetime, timedelta
        
        # 建立行程
        start_date = datetime.now() + timedelta(days=7)  # 預設一週後出發
        end_date = start_date + timedelta(days=itinerary_data['duration'] - 1)
        
        trip = TripManager.create_trip(
            name=itinerary_data['trip_name'],
            location=itinerary_data['location'],
            start_date=start_date,
            end_date=end_date,
            budget=itinerary_data['total_budget'],
            status="計劃中"
        )
        
        # 轉換每日行程格式
        trip['itinerary'] = []
        for day_plan in itinerary_data['daily_itinerary']:
            trip['itinerary'].append({
                "day": day_plan['day'],
                "date": (start_date + timedelta(days=day_plan['day']-1)).strftime("%Y-%m-%d"),
                "theme": day_plan.get('theme', ''),
                "activities": day_plan['activities']
            })
        
        # 加入其他資訊
        trip['accommodation_suggestions'] = itinerary_data.get('accommodation_suggestions', [])
        trip['transport_tips'] = itinerary_data.get('transport_tips', '')
        trip['packing_list'] = itinerary_data.get('packing_list', [])
        trip['notes'] = "\n".join(itinerary_data.get('important_notes', []))
        
        return trip
