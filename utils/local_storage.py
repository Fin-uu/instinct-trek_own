"""
本地儲存管理模組
用於儲存和讀取使用者的個人資訊和偏好設定
"""

import json
import os
from datetime import datetime
from pathlib import Path

class LocalStorage:
    """本地儲存管理器"""
    
    def __init__(self, storage_dir="user_data"):
        """
        初始化本地儲存
        
        Args:
            storage_dir: 儲存目錄名稱
        """
        # 建立儲存目錄
        self.base_dir = Path(__file__).parent.parent / storage_dir
        self.base_dir.mkdir(exist_ok=True)
        
        # 儲存檔案路徑
        self.user_profile_file = self.base_dir / "user_profile.json"
        self.preferences_file = self.base_dir / "preferences.json"
        self.history_file = self.base_dir / "history.json"
    
    # === 使用者資料管理 ===
    
    def save_user_profile(self, profile_data):
        """
        儲存使用者基本資料
        
        Args:
            profile_data: dict {
                "name": "使用者名稱",
                "email": "email@example.com",
                "phone": "0912345678",
                "preferences": {
                    "travel_style": ["美食", "自然"],
                    "budget_range": "中等",
                    "favorite_cities": ["台北", "台南"]
                }
            }
        """
        try:
            profile_data["last_updated"] = datetime.now().isoformat()
            
            with open(self.user_profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=2)
            
            return True, "使用者資料已儲存"
        except Exception as e:
            return False, f"儲存失敗: {str(e)}"
    
    def load_user_profile(self):
        """
        讀取使用者基本資料
        
        Returns:
            dict: 使用者資料，如果不存在則返回預設值
        """
        if not self.user_profile_file.exists():
            return {
                "name": "",
                "email": "",
                "phone": "",
                "preferences": {
                    "travel_style": [],
                    "budget_range": "中等",
                    "favorite_cities": []
                },
                "last_updated": None
            }
        
        try:
            with open(self.user_profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"讀取使用者資料失敗: {e}")
            return {}
    
    # === 偏好設定管理 ===
    
    def save_preferences(self, preferences):
        """
        儲存使用者偏好設定
        
        Args:
            preferences: dict {
                "alert_settings": {
                    "weather": True,
                    "crowd": True,
                    "budget": True,
                    ...
                },
                "notification": {
                    "email": False,
                    "line": False,
                    "frequency": "即時"
                },
                "display": {
                    "theme": "light",
                    "language": "zh-TW"
                }
            }
        """
        try:
            preferences["last_updated"] = datetime.now().isoformat()
            
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, ensure_ascii=False, indent=2)
            
            return True, "偏好設定已儲存"
        except Exception as e:
            return False, f"儲存失敗: {str(e)}"
    
    def load_preferences(self):
        """
        讀取使用者偏好設定
        
        Returns:
            dict: 偏好設定
        """
        if not self.preferences_file.exists():
            return {
                "alert_settings": {
                    "weather": True,
                    "crowd": True,
                    "budget": True,
                    "schedule": True,
                    "emergency": True,
                    "business": False
                },
                "notification": {
                    "email": False,
                    "line": False,
                    "frequency": "即時",
                    "quiet_hours": "無"
                },
                "display": {
                    "theme": "light",
                    "language": "zh-TW"
                },
                "last_updated": None
            }
        
        try:
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"讀取偏好設定失敗: {e}")
            return {}
    
    # === 歷史記錄管理 ===
    
    def save_history(self, history_type, data):
        """
        儲存歷史記錄
        
        Args:
            history_type: 記錄類型 ('search', 'alert', 'trip', 'chat')
            data: 記錄資料
        """
        try:
            # 讀取現有歷史
            history = self.load_history()
            
            # 確保類型存在
            if history_type not in history:
                history[history_type] = []
            
            # 添加時間戳記
            data["timestamp"] = datetime.now().isoformat()
            
            # 加入新記錄（保持在最前面）
            history[history_type].insert(0, data)
            
            # 限制每種類型最多保留 100 筆
            history[history_type] = history[history_type][:100]
            
            # 儲存
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return True, "歷史記錄已儲存"
        except Exception as e:
            return False, f"儲存失敗: {str(e)}"
    
    def load_history(self, history_type=None):
        """
        讀取歷史記錄
        
        Args:
            history_type: 指定類型，None 則返回全部
        
        Returns:
            dict or list: 歷史記錄
        """
        if not self.history_file.exists():
            return {} if history_type is None else []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            if history_type:
                return history.get(history_type, [])
            return history
        except Exception as e:
            print(f"讀取歷史記錄失敗: {e}")
            return {} if history_type is None else []
    
    def clear_history(self, history_type=None):
        """
        清除歷史記錄
        
        Args:
            history_type: 指定類型，None 則清除全部
        """
        try:
            if history_type is None:
                # 清除全部
                if self.history_file.exists():
                    self.history_file.unlink()
                return True, "所有歷史記錄已清除"
            else:
                # 清除指定類型
                history = self.load_history()
                if history_type in history:
                    del history[history_type]
                
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                
                return True, f"{history_type} 歷史記錄已清除"
        except Exception as e:
            return False, f"清除失敗: {str(e)}"
    
    # === 統計資訊 ===
    
    def get_storage_info(self):
        """
        取得儲存空間資訊
        
        Returns:
            dict: 儲存資訊
        """
        info = {
            "storage_path": str(self.base_dir),
            "files": {}
        }
        
        # 檢查各檔案大小
        for name, path in [
            ("使用者資料", self.user_profile_file),
            ("偏好設定", self.preferences_file),
            ("歷史記錄", self.history_file)
        ]:
            if path.exists():
                size = path.stat().st_size
                info["files"][name] = {
                    "exists": True,
                    "size": size,
                    "size_kb": f"{size / 1024:.2f} KB",
                    "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                }
            else:
                info["files"][name] = {
                    "exists": False
                }
        
        return info
    
    # === 資料匯出/匯入 ===
    
    def export_all_data(self, export_path=None):
        """
        匯出所有資料
        
        Args:
            export_path: 匯出檔案路徑，None 則使用預設
        
        Returns:
            tuple: (成功與否, 訊息, 檔案路徑)
        """
        try:
            if export_path is None:
                export_path = self.base_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            all_data = {
                "export_date": datetime.now().isoformat(),
                "user_profile": self.load_user_profile(),
                "preferences": self.load_preferences(),
                "history": self.load_history()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            return True, "資料匯出成功", str(export_path)
        except Exception as e:
            return False, f"匯出失敗: {str(e)}", None
    
    def import_data(self, import_path):
        """
        匯入資料
        
        Args:
            import_path: 匯入檔案路徑
        
        Returns:
            tuple: (成功與否, 訊息)
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 匯入各項資料
            if "user_profile" in data:
                self.save_user_profile(data["user_profile"])
            
            if "preferences" in data:
                self.save_preferences(data["preferences"])
            
            if "history" in data:
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump(data["history"], f, ensure_ascii=False, indent=2)
            
            return True, "資料匯入成功"
        except Exception as e:
            return False, f"匯入失敗: {str(e)}"
