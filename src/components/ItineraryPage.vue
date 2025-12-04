<template>
  <div style="height: 100%; overflow-y: auto; padding: 24px; background: #f9fafb;">
    <div style="max-width: 896px; margin: 0 auto;">
      <!-- 頂部標題和按鈕 -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
        <h2 style="font-size: 24px; font-weight: 700; color: #111827; margin: 0;">我的行程</h2>
        <button
          @click="handleAddItinerary"
          style="
            background: linear-gradient(135deg, #3b82f6, #9333ea);
            color: white;
            padding: 8px 16px;
            border-radius: 9999px;
            display: flex;
            align-items: center;
            gap: 8px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s;
          "
          @mouseover="$event.target.style.boxShadow='0 10px 15px -3px rgba(59, 130, 246, 0.4)'"
          @mouseout="$event.target.style.boxShadow='none'"
        >
          <PlusIcon :size="18" />
          新增行程
        </button>
      </div>
      
      <!-- 行程列表 -->
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div
          v-for="itinerary in itineraries"
          :key="itinerary.id"
          style="
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
          "
          @click="handleViewItinerary(itinerary)"
          @mouseover="$event.currentTarget.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)'"
          @mouseout="$event.currentTarget.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.1)'"
        >
          <div style="display: flex; flex-direction: column;">
            <!-- 行程圖片（手機版全寬，桌面版固定寬度） -->
            <img
              :src="itinerary.image"
              :alt="itinerary.title"
              style="width: 100%; height: 128px; object-fit: cover;"
            />
            
            <!-- 行程內容 -->
            <div style="flex: 1; padding: 16px;">
              <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div>
                  <h3 style="font-weight: 700; font-size: 18px; color: #111827; margin: 0 0 4px 0;">
                    {{ itinerary.title }}
                  </h3>
                  <p style="font-size: 14px; color: #6b7280; margin: 0; display: flex; align-items: center; gap: 4px;">
                    <CalendarIcon :size="14" />
                    {{ itinerary.date }}
                  </p>
                </div>
                
                <!-- 狀態標籤 -->
                <span :style="{
                  padding: '4px 12px',
                  borderRadius: '9999px',
                  fontSize: '12px',
                  fontWeight: 500,
                  background: itinerary.status === 'active' ? '#d1fae5' : '#dbeafe',
                  color: itinerary.status === 'active' ? '#047857' : '#1d4ed8'
                }">
                  {{ itinerary.status === 'active' ? '進行中' : '已規劃' }}
                </span>
              </div>
              
              <!-- 地點標籤 -->
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
                <span
                  v-for="(place, idx) in itinerary.places"
                  :key="idx"
                  style="
                    font-size: 12px;
                    background: #f3f4f6;
                    color: #4b5563;
                    padding: 4px 8px;
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                  "
                >
                  <MapPinIcon :size="12" />
                  {{ place }}
                </span>
              </div>
              
              <!-- 底部操作區 -->
              <div style="margin-top: 12px; display: flex; align-items: center; justify-content: space-between;">
                <button
                  @click.stop="handleViewItinerary(itinerary)"
                  style="
                    color: #3b82f6;
                    font-size: 14px;
                    font-weight: 500;
                    background: none;
                    border: none;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    padding: 0;
                    transition: color 0.3s;
                  "
                  @mouseover="$event.target.style.color='#2563eb'"
                  @mouseout="$event.target.style.color='#3b82f6'"
                >
                  查看詳情
                  <ChevronRightIcon :size="16" />
                </button>
                
                <div style="display: flex; gap: 8px;">
                  <button
                    @click.stop="handleEditItinerary(itinerary)"
                    style="
                      padding: 8px;
                      color: #6b7280;
                      background: none;
                      border: none;
                      border-radius: 8px;
                      cursor: pointer;
                      transition: all 0.3s;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                    "
                    @mouseover="$event.target.style.color='#3b82f6'; $event.target.style.background='#eff6ff'"
                    @mouseout="$event.target.style.color='#6b7280'; $event.target.style.background='none'"
                  >
                    <EditIcon :size="16" />
                  </button>
                  <button
                    @click.stop="handleShareItinerary(itinerary)"
                    style="
                      padding: 8px;
                      color: #6b7280;
                      background: none;
                      border: none;
                      border-radius: 8px;
                      cursor: pointer;
                      transition: all 0.3s;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                    "
                    @mouseover="$event.target.style.color='#10b981'; $event.target.style.background='#d1fae5'"
                    @mouseout="$event.target.style.color='#6b7280'; $event.target.style.background='none'"
                  >
                    <ShareIcon :size="16" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 空狀態 -->
      <div v-if="itineraries.length === 0" style="text-align: center; padding: 48px 0;">
        <CalendarIcon :size="48" style="margin: 0 auto 16px auto; color: #d1d5db;" />
        <p style="color: #6b7280; margin-bottom: 16px; font-size: 16px;">還沒有任何行程</p>
        <button
          @click="handleAddItinerary"
          style="
            background: linear-gradient(135deg, #3b82f6, #9333ea);
            color: white;
            padding: 12px 24px;
            border-radius: 9999px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s;
          "
          @mouseover="$event.target.style.boxShadow='0 10px 15px -3px rgba(59, 130, 246, 0.4)'"
          @mouseout="$event.target.style.boxShadow='none'"
        >
          開始規劃第一個行程
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {
  Calendar as CalendarIcon,
  MapPin as MapPinIcon,
  Plus as PlusIcon,
  ChevronRight as ChevronRightIcon,
  Edit as EditIcon,
  Share as ShareIcon
} from 'lucide-vue-next';

const emit = defineEmits(['view-detail', 'edit', 'share', 'add']);

const itineraries = ref([
  {
    id: 1,
    title: '京都三日古蹟巡禮',
    date: '2025-01-15 至 2025-01-17',
    status: 'active',
    places: ['清水寺', '金閣寺', '伏見稻荷', '嵐山'],
    image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&q=80'
  },
  {
    id: 2,
    title: '台南美食一日遊',
    date: '2025-01-20',
    status: 'planned',
    places: ['國華街', '赤崁樓', '安平老街', '花園夜市'],
    image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&q=80'
  },
  {
    id: 3,
    title: '東京購物之旅',
    date: '2025-02-01 至 2025-02-03',
    status: 'planned',
    places: ['銀座', '澀谷', '原宿', '新宿'],
    image: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80'
  }
]);

const handleAddItinerary = () => {
  emit('add');
};

const handleViewItinerary = (itinerary) => {
  emit('view-detail', itinerary.id);
};

const handleEditItinerary = (itinerary) => {
  emit('edit', itinerary);
};

const handleShareItinerary = (itinerary) => {
  emit('share', itinerary);
};
</script>

<style scoped>
/* 響應式設計 */
@media (min-width: 640px) {
  /* 桌面版：圖片在左側，內容在右側 */
  div[style*="flex-direction: column"] > img {
    width: 128px !important;
    height: 128px !important;
  }
  
  div[style*="flex-direction: column"] {
    flex-direction: row !important;
  }
}
</style>