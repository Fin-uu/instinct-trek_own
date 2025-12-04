<template>
  <div style="
    background: #ef4444;
    color: white;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    animation: slideDown 0.3s ease-out;
  ">
    <div style="max-width: 1200px; margin: 0 auto; padding: 16px;">
      <!-- 標題和關閉按鈕 -->
      <div style="display: flex; align-items: flex-start; justify-content: space-between;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
          <CloudRainIcon :size="24" style="margin-top: 4px; flex-shrink: 0; animation: pulse 2s infinite;" />
          <div>
            <h3 style="font-weight: 700; font-size: 1.125rem; margin: 0;">天氣警報</h3>
            <p style="font-size: 0.875rem; margin-top: 4px; margin-bottom: 0;">偵測到未來1小時有豪大雨</p>
          </div>
        </div>
        <button 
          @click="$emit('close')" 
          style="
            color: white;
            background: transparent;
            border: none;
            font-size: 2rem;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            width: 32px;
            height: 32px;
          "
        >
          ×
        </button>
      </div>
      
      <!-- 原定行程受影響 -->
      <div style="
        margin-top: 16px;
        background: #fef3c7;
        border: 2px solid #fbbf24;
        border-radius: 8px;
        padding: 16px;
      ">
        <div style="display: flex; align-items: flex-start; gap: 8px;">
          <AlertTriangleIcon style="color: #d97706; margin-top: 4px; flex-shrink: 0;" :size="20" />
          <div>
            <h4 style="font-weight: 700; color: #1f2937; margin: 0;">原定行程受影響</h4>
            <div style="font-size: 0.875rem; color: #374151; margin-top: 8px;">
              <div style="display: flex; align-items: flex-start; gap: 8px;">
                <XIcon :size="16" style="color: #ef4444; margin-top: 2px; flex-shrink: 0;" />
                <div>
                  <span style="font-weight: 500;">伏見稻荷大社（戶外）</span>
                  <p style="font-size: 0.75rem; color: #6b7280; margin: 0;">預計淋雨，不適合前往</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 建議替代方案 -->
      <div style="
        margin-top: 16px;
        background: #d1fae5;
        border: 2px solid #34d399;
        border-radius: 8px;
        padding: 16px;
      ">
        <div style="display: flex; align-items: flex-start; gap: 8px;">
          <CheckCircleIcon style="color: #059669; margin-top: 4px; flex-shrink: 0;" :size="20" />
          <div style="flex: 1;">
            <h4 style="font-weight: 700; color: #1f2937; margin: 0;">建議替代方案</h4>
            <div style="margin-top: 8px; background: white; border-radius: 8px; padding: 12px;">
              <div style="display: flex; align-items: flex-start; gap: 8px;">
                <BuildingIcon :size="16" style="color: #3b82f6; margin-top: 2px; flex-shrink: 0;" />
                <div style="font-size: 0.875rem; color: #374151;">
                  <p style="font-weight: 500; margin: 0;">方案一：錦市場</p>
                  <ul style="font-size: 0.75rem; color: #6b7280; margin: 4px 0 0 0; padding-left: 16px; list-style: none;">
                    <li>• 室內環境，完全不受天氣影響</li>
                    <li>• 距離您目前位置：步行12分鐘</li>
                    <li>• 可品嚐京都傳統小吃</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 按鈕 -->
      <div style="margin-top: 16px; display: flex; flex-direction: column; gap: 12px;">
        <button
          @click="handleConfirmChange"
          style="
            flex: 1;
            background: #10b981;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s;
          "
          @mouseover="$event.target.style.background='#059669'"
          @mouseout="$event.target.style.background='#10b981'"
        >
          <CheckIcon :size="18" />
          確認變更 → 前往錦市場
        </button>
        <button
          @click="$emit('close')"
          style="
            flex: 1;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-weight: 500;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s;
          "
          @mouseover="$event.target.style.background='rgba(255, 255, 255, 0.3)'"
          @mouseout="$event.target.style.background='rgba(255, 255, 255, 0.2)'"
        >
          <RouteIcon :size="18" />
          繼續原定行程
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  CloudRain as CloudRainIcon,
  AlertTriangle as AlertTriangleIcon,
  CheckCircle as CheckCircleIcon,
  X as XIcon,
  Building as BuildingIcon,
  Check as CheckIcon,
  Route as RouteIcon
} from 'lucide-vue-next';

const emit = defineEmits(['close']);

const handleConfirmChange = () => {
  console.log('確認變更行程');
  emit('close');
};
</script>

<style scoped>
@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@media (min-width: 640px) {
  div[style*="flex-direction: column"]:last-of-type {
    flex-direction: row !important;
  }
}
</style>