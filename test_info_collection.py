"""
測試資訊收集流程
"""

import sys
sys.path.insert(0, '.')

from utils.info_collector import TripInfoCollector

print("=" * 60)
print("🧪 測試資訊收集流程")
print("=" * 60)

# 測試 1: 第一輪 - 我想去台東玩
print("\n📝 第一輪輸入：我想去台東玩")
message1 = "我想去台東玩"
info1 = TripInfoCollector.extract_info_from_message(message1)
print(f"提取結果：{info1}")

collected_info = {}
collected_info = TripInfoCollector.merge_info(collected_info, info1)
print(f"當前資訊：{collected_info}")

is_complete = TripInfoCollector.is_info_complete(collected_info)
print(f"是否完整：{is_complete}")

if not is_complete:
    missing = TripInfoCollector.get_missing_fields(collected_info)
    print(f"缺少欄位：{missing}")

# 測試 2: 第二輪 - 2天
print("\n" + "=" * 60)
print("📝 第二輪輸入：2天")
message2 = "2天"
info2 = TripInfoCollector.extract_info_from_message(message2)
print(f"提取結果：{info2}")

collected_info = TripInfoCollector.merge_info(collected_info, info2)
print(f"當前資訊：{collected_info}")

is_complete = TripInfoCollector.is_info_complete(collected_info)
print(f"是否完整：{is_complete}")

if not is_complete:
    missing = TripInfoCollector.get_missing_fields(collected_info)
    print(f"缺少欄位：{missing}")

# 測試 3: 第三輪 - 一萬五，喜歡自然
print("\n" + "=" * 60)
print("📝 第三輪輸入：一萬五，喜歡自然")
message3 = "一萬五，喜歡自然"
info3 = TripInfoCollector.extract_info_from_message(message3)
print(f"提取結果：{info3}")

collected_info = TripInfoCollector.merge_info(collected_info, info3)
print(f"當前資訊：{collected_info}")

is_complete = TripInfoCollector.is_info_complete(collected_info)
print(f"是否完整：{is_complete}")

# 最終格式化顯示
print("\n" + "=" * 60)
print("✅ 最終收集資訊：")
print("=" * 60)
formatted = TripInfoCollector.format_collected_info(collected_info)
print(formatted)

print("\n" + "=" * 60)
print("🎯 測試完成！")
print("=" * 60)
