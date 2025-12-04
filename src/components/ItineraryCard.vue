<template>
  <div style="display: flex; justify-content: flex-start;">
    <div style="
      background: white;
      border-radius: 16px;
      max-width: 42rem;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
      border: 1px solid #dbeafe;
      overflow: hidden;
      transition: all 0.3s;
    "
    @mouseover="$event.currentTarget.style.boxShadow='0 20px 25px -5px rgba(0, 0, 0, 0.1)'"
    @mouseout="$event.currentTarget.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'">
      <div style="padding: 20px;">
        <!-- 標題區 -->
        <div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px;">
          <MapPinIcon style="color: #ec4899; margin-top: 4px; flex-shrink: 0;" :size="24" />
          <div>
            <h3 style="font-size: 1.125rem; font-weight: 700; color: #111827; margin: 0;">
              {{ data.title }}
            </h3>
          </div>
        </div>
        
        <!-- 詳細資訊 -->
        <div style="margin-bottom: 16px;">
          <!-- 風格 -->
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <SparklesIcon :size="16" style="color: #eab308;" />
            <span style="font-size: 0.875rem; color: #374151;">風格：{{ data.style }}</span>
          </div>
          
          <!-- 人流 -->
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <UsersIcon :size="16" style="color: #a855f7;" />
            <span style="font-size: 0.875rem; color: #374151;">人流：{{ data.crowd }}</span>
          </div>
          
          <!-- 預算 -->
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <WalletIcon :size="16" style="color: #10b981;" />
            <span style="font-size: 0.875rem; color: #374151;">預算：{{ data.budget }}</span>
          </div>
          
          <!-- 步數 -->
          <div style="display: flex; align-items: center; gap: 8px;">
            <FootprintsIcon :size="16" style="color: #3b82f6;" />
            <span style="font-size: 0.875rem; color: #374151;">步數：{{ data.steps }}</span>
          </div>
        </div>
        
        <!-- 精選景點 -->
        <div style="
          background: #eff6ff;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 16px;
        ">
          <p style="font-size: 0.75rem; color: #4b5563; font-style: italic; margin: 0;">
            <span style="font-weight: 600;">精選景點：</span>{{ data.highlights }}
          </p>
        </div>
        
        <!-- 查看按鈕 -->
        <button
          @click="handleViewDetails"
          style="
            width: 100%;
            background: linear-gradient(135deg, #3b82f6, #9333ea);
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
          @mouseover="$event.target.style.boxShadow='0 10px 15px -3px rgba(59, 130, 246, 0.4)'"
          @mouseout="$event.target.style.boxShadow='none'"
        >
          <EyeIcon :size="18" />
          查看完整行程
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  MapPin as MapPinIcon,
  Sparkles as SparklesIcon,
  Users as UsersIcon,
  Wallet as WalletIcon,
  Footprints as FootprintsIcon,
  Eye as EyeIcon
} from 'lucide-vue-next';

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['view-details']);

const handleViewDetails = () => {
  console.log('查看行程詳情:', props.data);
  emit('view-details', props.data);
};
</script>