<template>
  <div style="display: flex; justify-content: flex-start; margin: 16px 0;">
    <div style="
      background: white;
      padding: 16px 20px;
      border-radius: 24px;
      border-top-left-radius: 4px;
      max-width: 600px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border: 1px solid #e5e7eb;
    ">
      <div style="display: flex; align-items: flex-start; gap: 12px;">
        <!-- 機器人圖標 -->
        <div style="
          width: 32px;
          height: 32px;
          background: linear-gradient(135deg, #3b82f6, #9333ea);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        ">
          <BotIcon :size="16" style="color: white;" />
        </div>
        
        <!-- 訊息內容 -->
        <div style="flex: 1;">
          <p style="margin: 0; color: #1f2937; font-size: 14px; line-height: 1.5;">
            {{ message.content }}
          </p>
          <span style="
            display: block;
            margin-top: 4px;
            font-size: 12px;
            color: #9ca3af;
          ">
            {{ formatTime(message.timestamp) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Bot as BotIcon } from 'lucide-vue-next';

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' });
};
</script>