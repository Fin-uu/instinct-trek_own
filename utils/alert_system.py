from datetime import datetime, timedelta
import random

class AlertSystem:
    """即時提醒系統"""
    
    @staticmethod
    def check_weather_alerts(location, current_weather=None):
        """檢查天氣預警"""
        alerts = []
        
        # 模擬天氣資料（實際可接 API）
        weather_conditions = {
            "台北": {"condition": "🌧️ 午後雷陣雨", "temp": 28, "rain_prob": 80},
            "台南": {"condition": "☀️ 晴天", "temp": 32, "rain_prob": 10},
            "高雄": {"condition": "☀️ 炎熱", "temp": 34, "rain_prob": 5},
            "花蓮": {"condition": "🌦️ 多雲時晴", "temp": 26, "rain_prob": 30},
            "台中": {"condition": "☁️ 多雲", "temp": 29, "rain_prob": 20},
        }
        
        weather = weather_conditions.get(location, {"condition": "☀️ 晴天", "temp": 28, "rain_prob": 10})
        
        # 下雨警報
        if weather["rain_prob"] > 60:
            alerts.append({
                "type": "weather",
                "level": "warning",
                "icon": "🌧️",
                "title": "降雨機率高",
                "message": f"未來2小時降雨機率 {weather['rain_prob']}%，建議攜帶雨具或調整為室內行程",
                "suggestion": "建議前往：博物館、購物中心、室內景點",
                "time": datetime.now().strftime("%H:%M")
            })
        
        # 高溫警報
        if weather["temp"] > 33:
            alerts.append({
                "type": "weather",
                "level": "caution",
                "icon": "🌡️",
                "title": "高溫警示",
                "message": f"目前氣溫 {weather['temp']}°C，請注意防曬與補充水分",
                "suggestion": "建議避開中午時段戶外活動，多待在有冷氣的地方",
                "time": datetime.now().strftime("%H:%M")
            })
        
        return alerts
    
    @staticmethod
    def check_crowd_alerts(location, time_of_day):
        """檢查人流擁擠狀況"""
        alerts = []
        
        # 模擬人流資料
        crowded_times = {
            "週末": ["10:00-12:00", "14:00-17:00"],
            "平日": ["12:00-13:00", "18:00-19:00"]
        }
        
        # 熱門景點人流預測
        popular_spots = ["台北101", "故宮", "夜市", "老街"]
        
        if any(spot in location for spot in popular_spots):
            current_hour = datetime.now().hour
            
            # 假日或尖峰時段
            if current_hour in [11, 12, 15, 16, 17]:
                alerts.append({
                    "type": "crowd",
                    "level": "info",
                    "icon": "👥",
                    "title": "人潮擁擠提醒",
                    "message": f"{location} 目前人流較多，建議錯開尖峰時段",
                    "suggestion": "建議時段：早上9:00前 或 下午5:00後",
                    "time": datetime.now().strftime("%H:%M")
                })
        
        return alerts
    
    @staticmethod
    def check_business_hours(location, attraction):
        """檢查景點營業狀態"""
        alerts = []
        
        # 模擬營業時間資料
        business_hours = {
            "故宮": {"open": "09:00", "close": "17:00", "rest_day": "週一"},
            "台北101": {"open": "09:00", "close": "22:00", "rest_day": None},
            "夜市": {"open": "17:00", "close": "24:00", "rest_day": None},
        }
        
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime("%A")
        
        for place, hours in business_hours.items():
            if place in attraction:
                # 檢查是否休息日
                if hours["rest_day"] and hours["rest_day"] in current_day:
                    alerts.append({
                        "type": "business",
                        "level": "warning",
                        "icon": "🚫",
                        "title": "景點休館提醒",
                        "message": f"{place} 今日休館（{hours['rest_day']}）",
                        "suggestion": "建議改訪其他景點或調整日期",
                        "time": datetime.now().strftime("%H:%M")
                    })
                
                # 檢查即將閉館
                close_hour = int(hours["close"].split(":")[0])
                if current_hour >= close_hour - 2:
                    alerts.append({
                        "type": "business",
                        "level": "caution",
                        "icon": "⏰",
                        "title": "即將閉館",
                        "message": f"{place} 將於 {hours['close']} 閉館，請注意時間",
                        "suggestion": "建議提早離開或改天再訪",
                        "time": datetime.now().strftime("%H:%M")
                    })
        
        return alerts
    
    @staticmethod
    def check_traffic_alerts(from_location, to_location):
        """檢查交通狀況"""
        alerts = []
        
        # 模擬交通狀況
        current_hour = datetime.now().hour
        
        # 尖峰時段
        if current_hour in [7, 8, 9, 17, 18, 19]:
            alerts.append({
                "type": "traffic",
                "level": "info",
                "icon": "🚗",
                "title": "交通尖峰時段",
                "message": "目前為交通尖峰時段，預計車程時間較長",
                "suggestion": "建議搭乘捷運或提早出發",
                "time": datetime.now().strftime("%H:%M")
            })
        
        return alerts
    
    @staticmethod
    def check_budget_alerts(trip):
        """檢查預算狀況"""
        alerts = []
        
        if not trip:
            return alerts
        
        budget = trip.get("budget", 0)
        spent = trip.get("spent", 0)
        
        if budget > 0:
            usage_rate = (spent / budget) * 100
            
            # 預算使用超過 80%
            if usage_rate >= 80:
                alerts.append({
                    "type": "budget",
                    "level": "warning",
                    "icon": "💰",
                    "title": "預算即將用完",
                    "message": f"已使用 {usage_rate:.0f}% 預算（NT$ {spent:,} / NT$ {budget:,}）",
                    "suggestion": "建議調整後續消費或增加預算",
                    "time": datetime.now().strftime("%H:%M")
                })
            
            # 預算超支
            elif spent > budget:
                over_budget = spent - budget
                alerts.append({
                    "type": "budget",
                    "level": "danger",
                    "icon": "⚠️",
                    "title": "預算超支",
                    "message": f"已超支 NT$ {over_budget:,}",
                    "suggestion": "建議減少非必要支出",
                    "time": datetime.now().strftime("%H:%M")
                })
        
        return alerts
    
    @staticmethod
    def check_schedule_alerts(trip):
        """檢查行程時間提醒"""
        alerts = []
        
        if not trip or not trip.get("itinerary"):
            return alerts
        
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # 檢查今日行程
        for day_plan in trip["itinerary"]:
            if day_plan.get("activities"):
                for activity in day_plan["activities"]:
                    activity_time = activity.get("time", "")
                    if activity_time:
                        try:
                            hour, minute = map(int, activity_time.split(":"))
                            
                            # 提前30分鐘提醒
                            if hour == current_hour and minute - current_minute <= 30 and minute - current_minute > 0:
                                alerts.append({
                                    "type": "schedule",
                                    "level": "info",
                                    "icon": "📅",
                                    "title": "行程提醒",
                                    "message": f"30分鐘後：{activity.get('name', '活動')}",
                                    "suggestion": f"地點：{activity.get('note', '請確認地點')}",
                                    "time": current_time.strftime("%H:%M")
                                })
                        except:
                            pass
        
        return alerts
    
    @staticmethod
    def get_all_alerts(location=None, trip=None):
        """取得所有提醒"""
        all_alerts = []
        
        # 天氣提醒
        if location:
            all_alerts.extend(AlertSystem.check_weather_alerts(location))
        
        # 人流提醒
        if location:
            all_alerts.extend(AlertSystem.check_crowd_alerts(location, datetime.now().hour))
        
        # 預算提醒
        if trip:
            all_alerts.extend(AlertSystem.check_budget_alerts(trip))
            all_alerts.extend(AlertSystem.check_schedule_alerts(trip))
        
        return all_alerts
