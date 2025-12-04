<template>
  <div style="min-height: 100vh; background: #f9fafb;">
    <!-- 頂部導航欄 -->
    <header style="
      background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
      padding: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #ffffff;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
      <button @click="goBack" style="
        background: rgba(255,255,255,0.2);
        border: none;
        color: #fff;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
      "
      @mouseover="$event.target.style.background='rgba(255,255,255,0.3)'"
      @mouseout="$event.target.style.background='rgba(255,255,255,0.2)'">
        <ChevronLeftIcon :size="24" />
      </button>
      
      <div style="flex: 1; text-align: center;">
        <h1 style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">行程詳情</h1>
        <p style="font-size: 14px; opacity: 0.9; margin: 0;">{{ itinerary.title }}</p>
      </div>
      
      <button @click="shareItinerary" style="
        background: rgba(255,255,255,0.2);
        border: none;
        color: #fff;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
      "
      @mouseover="$event.target.style.background='rgba(255,255,255,0.3)'"
      @mouseout="$event.target.style.background='rgba(255,255,255,0.2)'">
        <Share2Icon :size="20" />
      </button>
    </header>

    <!-- 主容器 -->
    <div style="max-width: 900px; margin: 0 auto; padding: 24px;">
      <!-- 行程概覽卡片 -->
      <div style="
        background: #ffffff;
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 32px;
        border: 2px solid #e0e7ff;
      ">
        <div style="
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 24px;
          flex-wrap: wrap;
          gap: 16px;
        ">
          <div style="display: flex; align-items: center; gap: 16px;">
            <MapPinIcon :size="32" style="color: #ec4899; flex-shrink: 0;" />
            <h2 style="font-size: 28px; font-weight: 700; color: #1f2937; margin: 0;">
              {{ itinerary.title }}
            </h2>
          </div>
          <span style="
            background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
            color: #fff;
            padding: 8px 16px;
            border-radius: 9999px;
            font-size: 14px;
            font-weight: 600;
          ">
            {{ itinerary.duration }}
          </span>
        </div>

        <!-- 行程特色 -->
        <div style="
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 16px;
          margin-bottom: 24px;
        ">
          <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
          ">
            <SparklesIcon :size="20" style="color: #6b7280;" />
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <span style="font-size: 12px; color: #9ca3af;">風格</span>
              <span style="font-size: 14px; color: #1f2937; font-weight: 600;">{{ itinerary.style }}</span>
            </div>
          </div>
          
          <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
          ">
            <UsersIcon :size="20" style="color: #6b7280;" />
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <span style="font-size: 12px; color: #9ca3af;">人流</span>
              <span style="font-size: 14px; color: #1f2937; font-weight: 600;">{{ itinerary.crowd }}</span>
            </div>
          </div>
          
          <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
          ">
            <WalletIcon :size="20" style="color: #6b7280;" />
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <span style="font-size: 12px; color: #9ca3af;">預算</span>
              <span style="font-size: 14px; color: #1f2937; font-weight: 600;">{{ itinerary.budget }}</span>
            </div>
          </div>
          
          <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
          ">
            <FootprintsIcon :size="20" style="color: #6b7280;" />
            <div style="display: flex; flex-direction: column; gap: 2px;">
              <span style="font-size: 12px; color: #9ca3af;">步數</span>
              <span style="font-size: 14px; color: #1f2937; font-weight: 600;">{{ itinerary.steps }}</span>
            </div>
          </div>
        </div>

        <!-- 精選景點 -->
        <div style="
          background: #eff6ff;
          padding: 12px;
          border-radius: 12px;
          margin-bottom: 24px;
        ">
          <p style="font-size: 14px; color: #1e40af; line-height: 1.6; margin: 0;">
            <span style="font-weight: 600;">精選景點：</span>{{ itinerary.highlights }}
          </p>
        </div>

        <button @click="scrollToSchedule" style="
          width: 100%;
          padding: 16px;
          background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
          color: #fff;
          border: none;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        "
        @mouseover="$event.target.style.transform='translateY(-2px)'; $event.target.style.boxShadow='0 10px 20px rgba(59, 130, 246, 0.3)'"
        @mouseout="$event.target.style.transform='translateY(0)'; $event.target.style.boxShadow='none'">
          查看完整行程
        </button>
      </div>

      <!-- 每日行程詳情 -->
      <div style="margin-bottom: 32px;" ref="scheduleSection">
        <h3 style="
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 20px;
          font-weight: 700;
          color: #1f2937;
          margin-bottom: 24px;
        ">
          <CalendarIcon :size="24" />
          詳細行程安排
        </h3>

        <div
          v-for="(day, index) in itinerary.dailySchedule"
          :key="index"
          style="
            background: #fff;
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-left: 4px solid #3b82f6;
          "
        >
          <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f3f4f6;
          ">
            <div style="font-size: 20px; font-weight: 700; color: #3b82f6;">
              Day {{ index + 1 }}
            </div>
            <div style="font-size: 14px; color: #6b7280;">
              {{ day.date }}
            </div>
          </div>

          <div style="
            display: flex;
            flex-direction: column;
            gap: 24px;
            margin-bottom: 24px;
          ">
            <div
              v-for="(activity, actIndex) in day.activities"
              :key="actIndex"
              style="
                display: flex;
                gap: 16px;
                padding-left: 12px;
                border-left: 2px solid #e5e7eb;
                position: relative;
                align-items: flex-start;
              "
            >
              <div style="
                width: 10px;
                height: 10px;
                background: #3b82f6;
                border-radius: 50%;
                margin-top: 6px;
                margin-right: 8px;
                position: absolute;
                left: -6px;
              "></div>
              
              <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
                font-weight: 600;
                color: #3b82f6;
                min-width: 80px;
                margin-top: 2px;
              ">
                <ClockIcon :size="16" />
                {{ activity.time }}
              </div>

              <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                  <component :is="getActivityIcon(activity.type)" :size="20" style="color: #6b7280;" />
                  <h4 style="font-size: 18px; font-weight: 700; color: #1f2937; margin: 0;">
                    {{ activity.name }}
                  </h4>
                </div>

                <p style="color: #6b7280; font-size: 14px; line-height: 1.6; margin-bottom: 12px;">
                  {{ activity.description }}
                </p>

                <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 8px;">
                  <span v-if="activity.duration" style="
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-size: 12px;
                    color: #6b7280;
                  ">
                    <TimerIcon :size="14" />
                    {{ activity.duration }}
                  </span>
                  <span v-if="activity.cost" style="
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    font-size: 12px;
                    color: #6b7280;
                  ">
                    <CoinsIcon :size="14" />
                    {{ activity.cost }}
                  </span>
                </div>

                <div v-if="activity.transport" style="
                  display: flex;
                  align-items: center;
                  gap: 8px;
                  padding: 8px 12px;
                  background: #f0fdf4;
                  border-radius: 8px;
                  font-size: 12px;
                  color: #15803d;
                  margin-top: 8px;
                  width: fit-content;
                ">
                  <BusIcon :size="14" />
                  <span>{{ activity.transport }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 每日統計 -->
          <div style="
            display: flex;
            gap: 32px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
            flex-wrap: wrap;
          ">
            <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: #4b5563;">
              <FootprintsIcon :size="16" />
              <span>{{ day.totalSteps }}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: #4b5563;">
              <WalletIcon :size="16" />
              <span>{{ day.totalCost }}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; font-size: 14px; color: #4b5563;">
              <ClockIcon :size="16" />
              <span>{{ day.totalTime }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 旅遊小貼士 -->
      <div style="
        background: #fff;
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 32px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      ">
        <h3 style="
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 20px;
          font-weight: 700;
          color: #1f2937;
          margin-bottom: 24px;
        ">
          <LightbulbIcon :size="24" />
          旅遊小貼士
        </h3>
        
        <div style="
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 16px;
        ">
          <div v-for="(tip, index) in tips" :key="index" style="
            display: flex;
            gap: 16px;
            padding: 12px;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
          ">
            <component :is="tip.icon" :size="24" :style="{ color: tip.iconColor }" />
            <div style="flex: 1;">
              <h4 style="font-size: 16px; font-weight: 600; color: #1f2937; margin-bottom: 4px;">
                {{ tip.title }}
              </h4>
              <p style="font-size: 14px; color: #6b7280; line-height: 1.5; margin: 0;">
                {{ tip.description }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部操作按鈕 -->
      <div style="
        display: flex;
        gap: 16px;
        position: sticky;
        bottom: 16px;
        background: #fff;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
      ">
        <button @click="modifyItinerary" style="
          flex: 1;
          padding: 16px;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          cursor: pointer;
          background: #fff;
          color: #3b82f6;
          border: 2px solid #3b82f6;
          transition: all 0.3s;
        "
        @mouseover="$event.target.style.background='#eff6ff'"
        @mouseout="$event.target.style.background='#fff'">
          <EditIcon :size="20" />
          修改行程
        </button>
        
        <button @click="startNavigation" style="
          flex: 1;
          padding: 16px;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          cursor: pointer;
          background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
          color: #fff;
          border: none;
          transition: all 0.3s;
        "
        @mouseover="$event.target.style.transform='translateY(-2px)'; $event.target.style.boxShadow='0 10px 20px rgba(59, 130, 246, 0.3)'"
        @mouseout="$event.target.style.transform='translateY(0)'; $event.target.style.boxShadow='none'">
          <NavigationIcon :size="20" />
          開始導航
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {
  ChevronLeft as ChevronLeftIcon,
  Share2 as Share2Icon,
  MapPin as MapPinIcon,
  Sparkles as SparklesIcon,
  Users as UsersIcon,
  Wallet as WalletIcon,
  Footprints as FootprintsIcon,
  Calendar as CalendarIcon,
  Clock as ClockIcon,
  Timer as TimerIcon,
  Coins as CoinsIcon,
  Bus as BusIcon,
  Edit as EditIcon,
  Navigation as NavigationIcon,
  Lightbulb as LightbulbIcon,
  Church as ChurchIcon,
  ShoppingBag as ShoppingBagIcon,
  UtensilsCrossed as UtensilsIcon,
  Coffee as CoffeeIcon,
  Camera as CameraIcon,
  TreePine as TreeIcon,
  Ticket as TicketIcon,
  Umbrella as UmbrellaIcon,
  Wifi as WifiIcon
} from 'lucide-vue-next';

const props = defineProps({
  itineraryId: {
    type: String,
    default: 'kyoto-3days'
  }
});

const emit = defineEmits(['go-back', 'start-navigation', 'modify', 'share']);

const scheduleSection = ref(null);

// 行程資料
const itinerary = ref({
  title: '京都三日古蹟巡禮',
  duration: '3天2夜',
  style: '古蹟文化深度遊',
  crowd: '避開熱門時段',
  budget: '中等消費',
  steps: '每日約8,000步',
  highlights: '清水寺、金閣寺、伏見稻荷、嵐山竹林...',
  
  dailySchedule: [
    {
      date: '2025-01-15 (三)',
      totalSteps: '7,500步',
      totalCost: 'NT$1,800',
      totalTime: '8小時',
      activities: [
        {
          time: '09:00',
          name: '清水寺',
          type: 'temple',
          description: '京都最著名的寺廟之一，以清水舞台聞名。建議早上前往避開人潮。',
          duration: '1.5小時',
          cost: '¥400',
          transport: '從飯店步行15分鐘'
        },
        {
          time: '11:00',
          name: '二年坂、三年坂',
          type: 'shopping',
          description: '充滿古都風情的石板坡道，兩旁有許多傳統工藝品店和茶屋。',
          duration: '1小時',
          cost: '¥500-1000',
          transport: '步行5分鐘'
        },
        {
          time: '12:30',
          name: '午餐 - 祇園豆腐料理',
          type: 'food',
          description: '品嚐京都傳統豆腐料理，推薦湯豆腐套餐。',
          duration: '1小時',
          cost: '¥1,500-2,500'
        },
        {
          time: '14:00',
          name: '八坂神社',
          type: 'temple',
          description: '祇園的守護神社，以美麗的朱紅色建築聞名。',
          duration: '45分鐘',
          cost: '免費',
          transport: '步行10分鐘'
        }
      ]
    },
    {
      date: '2025-01-16 (四)',
      totalSteps: '8,200步',
      totalCost: 'NT$2,000',
      totalTime: '9小時',
      activities: [
        {
          time: '08:30',
          name: '金閣寺',
          type: 'temple',
          description: '世界文化遺產，金碧輝煌的舍利殿倒映在鏡湖池中。',
          duration: '1.5小時',
          cost: '¥500',
          transport: '搭乘巴士30分鐘'
        },
        {
          time: '10:30',
          name: '龍安寺',
          type: 'temple',
          description: '以枯山水庭園聞名的禪寺。',
          duration: '1小時',
          cost: '¥500',
          transport: '搭乘巴士10分鐘'
        },
        {
          time: '13:30',
          name: '嵐山竹林小徑',
          type: 'nature',
          description: '穿梭在高聳的竹林間，感受寧靜與禪意。',
          duration: '45分鐘',
          cost: '免費'
        }
      ]
    },
    {
      date: '2025-01-17 (五)',
      totalSteps: '8,500步',
      totalCost: 'NT$1,600',
      totalTime: '7小時',
      activities: [
        {
          time: '08:00',
          name: '伏見稻荷大社',
          type: 'temple',
          description: '以千本鳥居聞名的神社，朱紅色的鳥居綿延數公里。',
          duration: '2小時',
          cost: '免費',
          transport: '搭乘JR 20分鐘'
        },
        {
          time: '13:30',
          name: '東福寺',
          type: 'temple',
          description: '以紅葉聞名的寺廟，通天橋是最佳觀景點。',
          duration: '1.5小時',
          cost: '¥600',
          transport: '搭乘JR 5分鐘'
        }
      ]
    }
  ]
});

// 旅遊小貼士
const tips = ref([
  {
    icon: TicketIcon,
    iconColor: '#3b82f6',
    title: '交通建議',
    description: '購買京都巴士一日券（¥700），可無限次搭乘市區巴士。'
  },
  {
    icon: UmbrellaIcon,
    iconColor: '#f97316',
    title: '天氣準備',
    description: '一月京都較冷，建議攜帶保暖衣物。'
  },
  {
    icon: CoffeeIcon,
    iconColor: '#8b4513',
    title: '用餐時間',
    description: '建議11:30前或13:30後用餐避開尖峰。'
  },
  {
    icon: WifiIcon,
    iconColor: '#10b981',
    title: '網路連線',
    description: '建議租用Wi-Fi機或購買上網SIM卡。'
  }
]);

// 獲取活動圖標
const getActivityIcon = (type) => {
  const iconMap = {
    temple: ChurchIcon,
    shopping: ShoppingBagIcon,
    food: UtensilsIcon,
    cafe: CoffeeIcon,
    sightseeing: CameraIcon,
    nature: TreeIcon
  };
  return iconMap[type] || MapPinIcon;
};

// 方法
const goBack = () => {
  emit('go-back');
};

const shareItinerary = () => {
  emit('share', itinerary.value);
};

const scrollToSchedule = () => {
  scheduleSection.value?.scrollIntoView({ behavior: 'smooth' });
};

const modifyItinerary = () => {
  emit('modify', itinerary.value);
};

const startNavigation = () => {
  emit('start-navigation', itinerary.value);
};
</script>

<style scoped>
/* 響應式 */
@media (max-width: 768px) {
  /* 行程特色改為單列 */
  div[style*="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))"] {
    grid-template-columns: 1fr !important;
  }
  
  /* 小貼士改為單列 */
  div[style*="grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))"] {
    grid-template-columns: 1fr !important;
  }
  
  /* 底部按鈕改為垂直排列 */
  div[style*="bottom: 16px"] {
    flex-direction: column !important;
  }
}
</style>