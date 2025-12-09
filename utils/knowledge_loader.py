import json
import os

class TaiwanKnowledgeBase:
    """台灣旅遊知識庫"""
    
    def __init__(self, json_path="data/taiwan_knowledge.json"):
        self.json_path = json_path
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self):
        """載入 JSON 知識庫"""
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ 知識庫檔案不存在: {self.json_path}")
                return {}
        except Exception as e:
            print(f"❌ 載入知識庫失敗: {str(e)}")
            return {}
    
    def search(self, keywords, location=None, category=None):
        """
        搜尋知識庫
        
        Args:
            keywords: 關鍵字列表
            location: 地點（台北、台南等）
            category: 分類（景點、美食、交通等）
        
        Returns:
            符合條件的知識內容
        """
        results = []
        
        # 如果指定地點，直接查詢
        if location and location in self.knowledge:
            location_data = self.knowledge[location]
            
            # 如果指定分類
            if category and category in location_data:
                item = location_data[category]
                results.append(f"### {item['標題']}\n\n{item['內容']}")
            else:
                # 搜尋所有分類
                for cat_name, item in location_data.items():
                    # 檢查關鍵字
                    if self._match_keywords(item, keywords):
                        results.append(f"### {item['標題']}\n\n{item['內容']}")
        else:
            # 全域搜尋
            for loc_name, location_data in self.knowledge.items():
                for cat_name, item in location_data.items():
                    if self._match_keywords(item, keywords):
                        results.append(f"### {item['標題']}\n\n{item['內容']}")
        
        return "\n\n---\n\n".join(results) if results else "未找到相關資訊"
    
    def _match_keywords(self, item, keywords):
        """檢查是否匹配關鍵字"""
        if not keywords:
            return True
        
        # 搜尋範圍：標題、內容、標籤
        search_text = item.get('標題', '') + item.get('內容', '') + ' '.join(item.get('標籤', []))
        
        # 只要有一個關鍵字匹配就返回
        return any(keyword in search_text for keyword in keywords)
    
    def get_location_info(self, location):
        """取得特定地點的所有資訊"""
        if location in self.knowledge:
            return self.knowledge[location]
        return None
    
    def get_category_info(self, location, category):
        """取得特定地點的特定分類資訊"""
        if location in self.knowledge:
            location_data = self.knowledge[location]
            if category in location_data:
                return location_data[category]
        return None
    
    def get_all_locations(self):
        """取得所有地點列表"""
        return list(self.knowledge.keys())
    
    def get_categories(self, location):
        """取得特定地點的所有分類"""
        if location in self.knowledge:
            return list(self.knowledge[location].keys())
        return []
