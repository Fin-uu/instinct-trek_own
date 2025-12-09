from datetime import datetime, timedelta
import json

class TripManager:
    """行程管理器"""
    
    @staticmethod
    def create_trip(name, location, start_date, end_date, budget, status="計劃中"):
        """建立新行程"""
        return {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "name": name,
            "location": location,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "days": (end_date - start_date).days + 1,
            "budget": budget,
            "spent": 0,
            "status": status,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "itinerary": [],  # 每日行程
            "notes": "",
            "adjustments": []  # 即時調整記錄
        }
    
    @staticmethod
    def add_day_itinerary(trip, day, activities):
        """新增每日行程"""
        if not trip.get("itinerary"):
            trip["itinerary"] = []
        
        trip["itinerary"].append({
            "day": day,
            "date": trip["start_date"],
            "activities": activities
        })
        return trip
    
    @staticmethod
    def update_budget(trip, spent):
        """更新花費"""
        trip["spent"] = spent
        trip["remaining"] = trip["budget"] - spent
        return trip
    
    @staticmethod
    def add_adjustment(trip, adjustment):
        """記錄行程調整"""
        if not trip.get("adjustments"):
            trip["adjustments"] = []
        
        trip["adjustments"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": adjustment
        })
        return trip
    
    @staticmethod
    def get_trip_summary(trip):
        """取得行程摘要"""
        return {
            "總天數": trip["days"],
            "預算": f"NT$ {trip['budget']:,}",
            "已花費": f"NT$ {trip.get('spent', 0):,}",
            "剩餘": f"NT$ {trip['budget'] - trip.get('spent', 0):,}",
            "狀態": trip["status"]
        }
