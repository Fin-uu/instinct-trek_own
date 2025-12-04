<template>
  <div style="display: flex; justify-content: flex-end; margin: 16px 0;">
    <div style="
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      color: white;
      padding: 16px 20px;
      border-radius: 24px;
      border-top-right-radius: 4px;
      max-width: 28rem;
      box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
    ">
      <!-- 上傳的圖片 -->
      <img
        v-if="message.image"
        :src="message.image"
        alt="Uploaded"
        style="
          border-radius: 8px;
          margin-bottom: 8px;
          max-height: 160px;
          width: 100%;
          object-fit: cover;
        "
      />
      
      <!-- 訊息文字 -->
      <p style="font-size: 0.875rem; margin: 0; line-height: 1.5;">
        {{ message.content }}
      </p>
      
      <!-- 時間戳記 -->
      <span style="
        font-size: 0.75rem;
        color: #dbeafe;
        margin-top: 4px;
        display: block;
      ">
        {{ formatTime(message.timestamp) }}
      </span>
    </div>
  </div>
</template>

<script setup>
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