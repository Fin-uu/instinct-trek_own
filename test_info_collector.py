"""
TripInfoCollector 測試套件

執行方式：
1. 基本測試：python test_info_collector.py
2. 詳細測試：python test_info_collector.py --verbose
3. 性能測試：python test_info_collector.py --performance
"""

import sys
import os
import time
from datetime import datetime

# 添加 utils 到路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

try:
    from info_collector import TripInfoCollector
    print("✅ 成功載入 TripInfoCollector")
except ImportError as e:
    print(f"❌ 無法載入 TripInfoCollector: {e}")
    print("請確保 utils/info_collector.py 存在")
    sys.exit(1)

# === 測試計數器 ===
class TestCounter:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.failed_tests = []
    
    def add_pass(self):
        self.total += 1
        self.passed += 1
    
    def add_fail(self, test_name, error):
        self.total += 1
        self.failed += 1
        self.failed_tests.append((test_name, error))
    
    def print_summary(self):
        print("\n" + "="*60)
        print("📊 測試摘要")
        print("="*60)
        print(f"總測試數：{self.total}")
        print(f"✅ 通過：{self.passed}")
        print(f"❌ 失敗：{self.failed}")
        
        if self.failed > 0:
            print(f"\n失敗率：{self.failed/self.total*100:.1f}%")
            print("\n失敗的測試：")
            for test_name, error in self.failed_tests:
                print(f"  • {test_name}: {error}")
        else:
            print("\n🎉 所有測試通過！")
        
        print("="*60)

counter = TestCounter()

# === 測試工具函數 ===
def assert_equal(actual, expected, test_name):
    """斷言相等"""
    if actual == expected:
        print(f"  ✅ {test_name}")
        counter.add_pass()
        return True
    else:
        error = f"期望 {expected}, 得到 {actual}"
        print(f"  ❌ {test_name}: {error}")
        counter.add_fail(test_name, error)
        return False

def assert_true(condition, test_name):
    """斷言為真"""
    if condition:
        print(f"  ✅ {test_name}")
        counter.add_pass()
        return True
    else:
        error = "條件為 False"
        print(f"  ❌ {test_name}: {error}")
        counter.add_fail(test_name, error)
        return False

def assert_in(item, container, test_name):
    """斷言包含"""
    if item in container:
        print(f"  ✅ {test_name}")
        counter.add_pass()
        return True
    else:
        error = f"{item} 不在 {container} 中"
        print(f"  ❌ {test_name}: {error}")
        counter.add_fail(test_name, error)
        return False

def assert_not_none(value, test_name):
    """斷言不為 None"""
    if value is not None:
        print(f"  ✅ {test_name}")
        counter.add_pass()
        return True
    else:
        error = "值為 None"
        print(f"  ❌ {test_name}: {error}")
        counter.add_fail(test_name, error)
        return False

# === 單元測試 ===
def test_extract_location():
    """測試地點提取"""
    print("\n📍 測試地點提取")
    
    test_cases = [
        ("我想去台北玩", "台北"),
        ("去台南吃美食", "台南"),
        ("花蓮好美", "花蓮"),
        ("想去墾丁度假", "墾丁"),
        ("台東很不錯", "台東"),
        ("日月潭風景", "日月潭"),
        ("阿里山看日出", "阿里山"),
    ]
    
    for message, expected_location in test_cases:
        result = TripInfoCollector._rule_extract(message)
        assert_equal(
            result.get("location"), 
            expected_location, 
            f"提取地點：{message}"
        )

def test_extract_duration():
    """測試天數提取"""
    print("\n⏱️ 測試天數提取")
    
    test_cases = [
        ("玩3天", 3),
        ("5天4夜", 5),
        ("兩天一夜", None),  # 中文數字暫不支援
        ("預計玩7天", 7),
        ("10日遊", 10),
    ]
    
    for message, expected_duration in test_cases:
        result = TripInfoCollector._rule_extract(message)
        assert_equal(
            result.get("duration"), 
            expected_duration, 
            f"提取天數：{message}"
        )

def test_extract_people():
    """測試人數提取"""
    print("\n👥 測試人數提取")
    
    test_cases = [
        ("2人", 2),
        ("4位", 4),
        ("一個人", 1),
        ("兩人", 2),
        ("10人團體", 10),
    ]
    
    for message, expected_people in test_cases:
        result = TripInfoCollector._rule_extract(message)
        actual_people = result.get("other_requirements", {}).get("people")
        assert_equal(
            actual_people, 
            expected_people, 
            f"提取人數：{message}"
        )

def test_extract_budget():
    """測試預算提取"""
    print("\n💰 測試預算提取")
    
    test_cases = [
        ("預算1萬", 10000),
        ("2萬元", 20000),
        ("1.5萬", 15000),
        ("預算15000", 15000),
    ]
    
    for message, expected_budget in test_cases:
        result = TripInfoCollector._rule_extract(message)
        actual_budget = result.get("other_requirements", {}).get("budget")
        assert_equal(
            actual_budget, 
            expected_budget, 
            f"提取預算：{message}"
        )

def test_extract_trip_type():
    """測試旅遊類型提取"""
    print("\n🎯 測試旅遊類型提取")
    
    test_cases = [
        ("和家人去玩", "家族旅遊"),
        ("畢業旅行", "畢業旅行"),
        ("和男友出遊", "情侶出遊"),
        ("跟朋友一起", "朋友聚會"),
        ("一個人旅行", "一個人旅行"),
        ("蜜月旅行", "蜜月旅行"),
        ("帶小孩去", "親子旅遊"),
    ]
    
    for message, expected_type in test_cases:
        result = TripInfoCollector._rule_extract(message)
        actual_type = result.get("other_requirements", {}).get("trip_type")
        assert_equal(
            actual_type, 
            expected_type, 
            f"提取類型：{message}"
        )

def test_extract_preferences():
    """測試偏好提取"""
    print("\n❤️ 測試偏好提取")
    
    test_cases = [
        ("想吃美食", ["美食"]),
        ("看風景", ["自然"]),
        ("參觀古蹟", ["文化"]),
        ("放鬆度假", ["放鬆"]),
        ("想吃美食和逛街", ["美食", "購物"]),
    ]
    
    for message, expected_prefs in test_cases:
        result = TripInfoCollector._rule_extract(message)
        actual_prefs = result.get("other_requirements", {}).get("preferences", [])
        
        # 檢查是否包含預期的偏好
        all_found = all(pref in actual_prefs for pref in expected_prefs)
        assert_true(
            all_found,
            f"提取偏好：{message}"
        )

def test_extract_special_needs():
    """測試特殊需求提取"""
    print("\n⚠️ 測試特殊需求提取")
    
    test_cases = [
        ("需要無障礙", ["需要無障礙設施"]),
        ("我吃素", ["素食"]),
        ("帶寵物", ["攜帶寵物"]),
        ("有小孩", ["有小孩同行"]),
    ]
    
    for message, expected_needs in test_cases:
        result = TripInfoCollector._rule_extract(message)
        actual_needs = result.get("other_requirements", {}).get("special_needs", [])
        
        all_found = all(need in actual_needs for need in expected_needs)
        assert_true(
            all_found,
            f"提取特殊需求：{message}"
        )

# === 整合測試 ===
def test_complete_extraction():
    """測試完整提取"""
    print("\n🔄 測試完整提取")
    
    message = "我想和家人去台南玩3天，預算2萬，想吃美食"
    result = TripInfoCollector._rule_extract(message)
    
    assert_equal(result.get("location"), "台南", "完整提取：地點")
    assert_equal(result.get("duration"), 3, "完整提取：天數")
    
    other = result.get("other_requirements", {})
    assert_equal(other.get("budget"), 20000, "完整提取：預算")
    assert_equal(other.get("trip_type"), "家族旅遊", "完整提取：類型")
    assert_in("美食", other.get("preferences", []), "完整提取：偏好")

def test_merge_info():
    """測試資訊合併"""
    print("\n🔀 測試資訊合併")
    
    current = {
        "location": "台北",
        "other_requirements": {
            "trip_type": "家族旅遊"
        }
    }
    
    new = {
        "duration": 3,
        "other_requirements": {
            "budget": 15000
        }
    }
    
    merged = TripInfoCollector.merge_info(current, new)
    
    assert_equal(merged.get("location"), "台北", "合併：地點保留")
    assert_equal(merged.get("duration"), 3, "合併：天數新增")
    assert_equal(
        merged.get("other_requirements", {}).get("trip_type"), 
        "家族旅遊", 
        "合併：類型保留"
    )
    assert_equal(
        merged.get("other_requirements", {}).get("budget"), 
        15000, 
        "合併：預算新增"
    )

def test_missing_fields():
    """測試缺少欄位檢測"""
    print("\n🔍 測試缺少欄位檢測")
    
    # 完整資訊
    complete_info = {"location": "台北", "duration": 3}
    missing = TripInfoCollector.get_missing_fields(complete_info)
    assert_equal(len(missing), 0, "完整資訊：無缺少欄位")
    
    # 缺少地點
    no_location = {"duration": 3}
    missing = TripInfoCollector.get_missing_fields(no_location)
    assert_equal(len(missing), 1, "缺少地點：1個缺少欄位")
    assert_equal(missing[0][0], "location", "缺少地點：正確識別")
    
    # 缺少天數
    no_duration = {"location": "台北"}
    missing = TripInfoCollector.get_missing_fields(no_duration)
    assert_equal(len(missing), 1, "缺少天數：1個缺少欄位")
    assert_equal(missing[0][0], "duration", "缺少天數：正確識別")
    
    # 都缺少
    empty_info = {}
    missing = TripInfoCollector.get_missing_fields(empty_info)
    assert_equal(len(missing), 2, "都缺少：2個缺少欄位")

def test_is_complete():
    """測試完整性判斷"""
    print("\n✅ 測試完整性判斷")
    
    # 完整
    complete_info = {"location": "台北", "duration": 3}
    result = TripInfoCollector.is_info_complete(complete_info)
    assert_true(result, "完整資訊：判斷為完整")
    
    # 檢查自動填充
    assert_not_none(
        complete_info.get("other_requirements", {}).get("date"),
        "完整資訊：自動填充日期"
    )
    assert_not_none(
        complete_info.get("other_requirements", {}).get("people"),
        "完整資訊：自動填充人數"
    )
    assert_not_none(
        complete_info.get("other_requirements", {}).get("budget"),
        "完整資訊：自動填充預算"
    )
    
    # 不完整
    incomplete_info = {"location": "台北"}
    result = TripInfoCollector.is_info_complete(incomplete_info)
    assert_true(not result, "不完整資訊：判斷為不完整")

def test_follow_up_question():
    """測試追問生成"""
    print("\n❓ 測試追問生成")
    
    # 缺少地點
    missing = [("location", "目的地")]
    question = TripInfoCollector.generate_follow_up_question(
        missing, {}, client=None
    )
    assert_not_none(question, "缺少地點：生成追問")
    assert_in("城市", question, "缺少地點：包含關鍵字")
    
    # 缺少天數
    missing = [("duration", "天數")]
    question = TripInfoCollector.generate_follow_up_question(
        missing, {}, client=None
    )
    assert_not_none(question, "缺少天數：生成追問")
    assert_in("天", question, "缺少天數：包含關鍵字")
    
    # 無缺少
    missing = []
    question = TripInfoCollector.generate_follow_up_question(
        missing, {}, client=None
    )
    assert_equal(question, None, "無缺少：不生成追問")

def test_format_display():
    """測試格式化顯示"""
    print("\n🎨 測試格式化顯示")
    
    info = {
        "location": "台南",
        "duration": 3,
        "other_requirements": {
            "people": 2,
            "budget": 15000,
            "trip_type": "情侶出遊",
            "preferences": ["美食", "文化"]
        }
    }
    
    formatted = TripInfoCollector.format_collected_info(info)
    
    assert_in("台南", formatted, "格式化：包含地點")
    assert_in("3天", formatted, "格式化：包含天數")
    assert_in("2人", formatted, "格式化：包含人數")
    assert_in("15,000", formatted, "格式化：包含預算（格式化）")
    assert_in("情侶出遊", formatted, "格式化：包含類型")
    assert_in("美食", formatted, "格式化：包含偏好")

# === 邊界測試 ===
def test_edge_cases():
    """測試邊界情況"""
    print("\n🔬 測試邊界情況")
    
    # 空字串
    result = TripInfoCollector._rule_extract("")
    assert_equal(result.get("location"), None, "空字串：無地點")
    assert_equal(result.get("duration"), None, "空字串：無天數")
    
    # 超長輸入
    long_message = "我想去台北" + "玩" * 1000 + "3天"
    result = TripInfoCollector._rule_extract(long_message)
    assert_equal(result.get("location"), "台北", "超長輸入：提取地點")
    assert_equal(result.get("duration"), 3, "超長輸入：提取天數")
    
    # 多個城市（取第一個）
    result = TripInfoCollector._rule_extract("台北台南高雄")
    assert_equal(result.get("location"), "台北", "多個城市：取第一個")
    
    # 多個天數（取第一個）
    result = TripInfoCollector._rule_extract("3天5天7天")
    assert_equal(result.get("duration"), 3, "多個天數：取第一個")
    
    # 無效預算
    result = TripInfoCollector._rule_extract("預算100")
    budget = result.get("other_requirements", {}).get("budget")
    assert_equal(budget, None, "無效預算：不提取")

# === 性能測試 ===
def test_performance():
    """測試性能"""
    print("\n⚡ 測試性能")
    
    test_messages = [
        "我想去台北玩3天",
        "和家人去台南吃美食，預算2萬",
        "一個人去花蓮放鬆5天",
        "畢業旅行想去墾丁4天3夜，10個人",
        "帶小孩去宜蘭玩，需要親子友善景點",
    ]
    
    # 測試規則提取速度
    start_time = time.time()
    for _ in range(100):
        for message in test_messages:
            TripInfoCollector._rule_extract(message)
    elapsed = time.time() - start_time
    
    avg_time = elapsed / (100 * len(test_messages)) * 1000  # 毫秒
    
    print(f"  ⏱️ 平均提取時間：{avg_time:.2f}ms")
    assert_true(avg_time < 10, "性能：單次提取 < 10ms")
    
    # 測試完整流程速度
    start_time = time.time()
    for _ in range(100):
        for message in test_messages:
            result = TripInfoCollector._rule_extract(message)
            TripInfoCollector.is_info_complete(result)
            TripInfoCollector.format_collected_info(result)
    elapsed = time.time() - start_time
    
    avg_time = elapsed / (100 * len(test_messages)) * 1000
    
    print(f"  ⏱️ 平均完整流程時間：{avg_time:.2f}ms")
    assert_true(avg_time < 20, "性能：完整流程 < 20ms")

# === 實際場景測試 ===
def test_real_scenarios():
    """測試實際場景"""
    print("\n🌍 測試實際場景")
    
    scenarios = [
        {
            "name": "簡單規劃",
            "messages": [
                "我想去台北玩",
                "3天"
            ],
            "expected": {
                "location": "台北",
                "duration": 3
            }
        },
        {
            "name": "完整輸入",
            "messages": [
                "我想和家人去台南玩3天，預算2萬，想吃美食"
            ],
            "expected": {
                "location": "台南",
                "duration": 3,
                "budget": 20000,
                "trip_type": "家族旅遊",
                "preferences": ["美食"]
            }
        },
        {
            "name": "分次輸入",
            "messages": [
                "想去花蓮",
                "玩5天",
                "預算1.5萬"
            ],
            "expected": {
                "location": "花蓮",
                "duration": 5,
                "budget": 15000
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"\n  場景：{scenario['name']}")
        
        collected_info = {}
        
        for message in scenario["messages"]:
            extracted = TripInfoCollector._rule_extract(message)
            collected_info = TripInfoCollector.merge_info(collected_info, extracted)
        
        # 驗證結果
        expected = scenario["expected"]
        
        if "location" in expected:
            assert_equal(
                collected_info.get("location"),
                expected["location"],
                f"{scenario['name']}：地點"
            )
        
        if "duration" in expected:
            assert_equal(
                collected_info.get("duration"),
                expected["duration"],
                f"{scenario['name']}：天數"
            )
        
        other = collected_info.get("other_requirements", {})
        
        if "budget" in expected:
            assert_equal(
                other.get("budget"),
                expected["budget"],
                f"{scenario['name']}：預算"
            )
        
        if "trip_type" in expected:
            assert_equal(
                other.get("trip_type"),
                expected["trip_type"],
                f"{scenario['name']}：類型"
            )
        
        if "preferences" in expected:
            assert_in(
                expected["preferences"][0],
                other.get("preferences", []),
                f"{scenario['name']}：偏好"
            )

# === 主測試函數 ===
def run_all_tests():
    """執行所有測試"""
    print("\n" + "="*60)
    print("🧪 開始測試 TripInfoCollector")
    print("="*60)
    
    # 單元測試
    print("\n📦 單元測試")
    test_extract_location()
    test_extract_duration()
    test_extract_people()
    test_extract_budget()
    test_extract_trip_type()
    test_extract_preferences()
    test_extract_special_needs()
    
    # 整合測試
    print("\n🔄 整合測試")
    test_complete_extraction()
    test_merge_info()
    test_missing_fields()
    test_is_complete()
    test_follow_up_question()
    test_format_display()
    
    # 邊界測試
    print("\n🔬 邊界測試")
    test_edge_cases()
    
    # 實際場景測試
    print("\n🌍 實際場景測試")
    test_real_scenarios()
    
    # 性能測試
    if "--performance" in sys.argv:
        test_performance()
    
    # 顯示摘要
    counter.print_summary()
    
    # 返回結果
    return counter.failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    
    # 退出碼
    sys.exit(0 if success else 1)
