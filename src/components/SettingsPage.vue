<template>
  <div :style="rootStyle">
    <div :style="containerStyle">
      <h2 :style="headingStyle">設定與偏好</h2>

      <div style="display:block; gap:16px">
        <!-- 語言設定 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <LanguagesIcon :size="24" :style="{ color: '#3b82f6' }" />
            <h3 :style="sectionTitleStyle">語言設定</h3>
          </div>
          <select
            :value="preferences.language"
            @change="updateLanguage"
            :style="selectStyle"
          >
            <option value="zh-TW">繁體中文</option>
            <option value="zh-CN">简体中文</option>
            <option value="en">English</option>
            <option value="ja">日本語</option>
            <option value="ko">한국어</option>
          </select>
        </div>

        <!-- 步行速度 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <FootprintsIcon :size="24" :style="{ color: '#10b981' }" />
            <h3 :style="sectionTitleStyle">步行速度</h3>
          </div>
          <div style="display:block; gap:12px">
            <label
              v-for="option in walkingPaceOptions"
              :key="option.value"
              :style="[optionBaseStyle, preferences.walkingPace === option.value ? optionSelectedStyle : optionUnselectedStyle]"
            >
              <input
                type="radio"
                :value="option.value"
                :checked="preferences.walkingPace === option.value"
                @change="updateWalkingPace"
                :style="radioStyle"
              />
              <div style="margin-left:12px">
                <p :style="optionLabelStyle">{{ option.label }}</p>
                <p :style="optionDescStyle">{{ option.description }}</p>
              </div>
            </label>
          </div>
        </div>

        <!-- 預算偏好 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <WalletIcon :size="24" :style="{ color: '#8b5cf6' }" />
            <h3 :style="sectionTitleStyle">預算偏好</h3>
          </div>
          <div style="display:block; gap:12px">
            <label
              v-for="option in budgetOptions"
              :key="option.value"
              :style="[optionBaseStyle, preferences.budget === option.value ? budgetSelectedStyle : optionUnselectedStyle]"
            >
              <input
                type="radio"
                :value="option.value"
                :checked="preferences.budget === option.value"
                @change="updateBudget"
                :style="radioStyle"
              />
              <div style="margin-left:12px; flex:1">
                <p :style="optionLabelStyle">{{ option.label }}</p>
                <p :style="optionDescStyle">{{ option.description }}</p>
              </div>
              <span :style="budgetIconStyle">{{ option.icon }}</span>
            </label>
          </div>
        </div>

        <!-- 通知設定 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <BellIcon :size="24" :style="{ color: '#f97316' }" />
            <h3 :style="sectionTitleStyle">通知設定</h3>
          </div>
          <div style="display:block; gap:12px">
            <label
              v-for="option in notificationOptions"
              :key="option.key"
              :style="notificationRowStyle"
            >
              <div style="display:flex; align-items:center; gap:12px">
                <component :is="option.icon" :size="20" :style="{ color: option.iconColor }" />
                <div>
                  <p :style="optionLabelStyle">{{ option.label }}</p>
                  <p :style="optionDescStyle">{{ option.description }}</p>
                </div>
              </div>
              <div @click.prevent="toggleNotification(option.key)" :style="{ cursor: 'pointer' }">
                <div :style="getToggleTrackStyle(option.key)"></div>
                <div :style="getToggleKnobStyle(option.key)"></div>
              </div>
            </label>
          </div>
        </div>

        <!-- 個人偏好 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <HeartIcon :size="24" :style="{ color: '#ef4444' }" />
            <h3 :style="sectionTitleStyle">個人偏好</h3>
          </div>
          <div style="display:block; gap:12px">
            <div>
              <label :style="labelBlockStyle">興趣標籤</label>
              <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:8px">
                <button
                  v-for="tag in interestTags"
                  :key="tag"
                  @click="toggleInterestTag(tag)"
                  :style="selectedInterests.includes(tag) ? tagSelectedStyle : tagUnselectedStyle"
                >
                  {{ tag }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 關於 -->
        <div :style="cardStyle">
          <div :style="cardHeaderStyle">
            <InfoIcon :size="24" :style="{ color: '#6b7280' }" />
            <h3 :style="sectionTitleStyle">關於應用</h3>
          </div>
          <div :style="aboutTextStyle">
            <p>版本：1.0.0</p>
            <p>© 2025 AI 智慧導遊</p>
            <div style="display:flex; gap:12px; margin-top:12px">
              <button :style="linkButtonStyle">使用條款</button>
              <button :style="linkButtonStyle">隱私政策</button>
              <button :style="linkButtonStyle">聯絡我們</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {
  Languages as LanguagesIcon,
  Footprints as FootprintsIcon,
  Wallet as WalletIcon,
  Bell as BellIcon,
  Heart as HeartIcon,
  Info as InfoIcon,
  CloudRain as CloudRainIcon,
  Calendar as CalendarIcon,
  Star as StarIcon
} from 'lucide-vue-next';

const props = defineProps({
  preferences: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update-preferences']);

const walkingPaceOptions = [
  { value: 'slow', label: '慢速', description: '適合老人、兒童或悠閒散步' },
  { value: 'normal', label: '正常速度', description: '一般步行速度' },
  { value: 'fast', label: '快速', description: '快速步行，適合趕時間' }
];

const budgetOptions = [
  { value: 'low', label: '經濟實惠', description: '每日 $500-1000 TWD', icon: '💰' },
  { value: 'medium', label: '中等消費', description: '每日 $1000-3000 TWD', icon: '💳' },
  { value: 'high', label: '高端享受', description: '每日 $3000+ TWD', icon: '💎' }
];

// Inline-color notification options
const notificationOptions = [
  {
    key: 'weather',
    label: '天氣警報',
    description: '接收即時天氣變化通知',
    icon: CloudRainIcon,
    iconColor: '#3b82f6'
  },
  {
    key: 'itinerary',
    label: '行程提醒',
    description: '在景點開始前提醒您',
    icon: CalendarIcon,
    iconColor: '#10b981'
  },
  {
    key: 'recommendations',
    label: '景點推薦',
    description: '根據您的位置推薦附近景點',
    icon: StarIcon,
    iconColor: '#f59e0b'
  }
];

const interestTags = [
  '美食', '古蹟', '自然', '購物', '藝術', '攝影',
  '登山', '海灘', '夜生活', '咖啡廳', '博物館', '寺廟'
];

const selectedInterests = ref(['美食', '古蹟', '攝影']);

// Inline style objects
const rootStyle = {
  height: '100%',
  overflowY: 'auto',
  padding: '24px',
  backgroundColor: '#f9fafb'
};

const containerStyle = {
  maxWidth: '42rem',
  margin: '0 auto'
};

const headingStyle = {
  fontSize: '20px',
  fontWeight: 700,
  color: '#111827',
  marginBottom: '24px'
};

const cardStyle = {
  backgroundColor: '#ffffff',
  borderRadius: '16px',
  boxShadow: '0 4px 6px rgba(0,0,0,0.08)',
  padding: '24px',
  marginBottom: '16px'
};

const cardHeaderStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '12px',
  marginBottom: '16px'
};

const sectionTitleStyle = {
  fontWeight: 700,
  fontSize: '16px',
  color: '#111827'
};

const selectStyle = {
  width: '100%',
  padding: '12px 16px',
  border: '1px solid #d1d5db',
  borderRadius: '12px',
  outline: 'none',
  fontSize: '14px',
  background: '#ffffff'
};

const optionBaseStyle = {
  display: 'flex',
  alignItems: 'center',
  padding: '12px',
  borderRadius: '12px',
  cursor: 'pointer',
  transition: 'all 0.15s',
  border: '2px solid #e5e7eb'
};

const optionSelectedStyle = {
  borderColor: '#3b82f6',
  backgroundColor: '#eff6ff'
};

const optionUnselectedStyle = {
  borderColor: '#e5e7eb',
  backgroundColor: '#ffffff'
};

const radioStyle = {
  width: '16px',
  height: '16px'
};

const optionLabelStyle = { fontWeight: 600, color: '#111827' };
const optionDescStyle = { fontSize: '12px', color: '#6b7280' };

const budgetSelectedStyle = { borderColor: '#8b5cf6', backgroundColor: '#f3e8ff' };
const budgetIconStyle = { fontSize: '20px', marginLeft: '8px' };

const notificationRowStyle = { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', borderRadius: '12px', transition: 'background 0.15s' };

const labelBlockStyle = { display: 'block', fontSize: '14px', fontWeight: 500, color: '#374151', marginBottom: '8px' };
const tagSelectedStyle = { padding: '6px 12px', borderRadius: '999px', fontSize: '13px', backgroundColor: '#3b82f6', color: '#ffffff', border: 'none', cursor: 'pointer' };
const tagUnselectedStyle = { padding: '6px 12px', borderRadius: '999px', fontSize: '13px', backgroundColor: '#f3f4f6', color: '#4b5563', border: 'none', cursor: 'pointer' };

const aboutTextStyle = { fontSize: '14px', color: '#4b5563' };
const linkButtonStyle = { color: '#3b82f6', background: 'transparent', border: 'none', padding: 0, cursor: 'pointer' };

// Toggle styles helpers
const getToggleTrackStyle = (key) => {
  const on = props.preferences.notifications && props.preferences.notifications[key];
  return {
    width: '44px',
    height: '24px',
    borderRadius: '999px',
    backgroundColor: on ? '#3b82f6' : '#e5e7eb',
    position: 'relative',
    transition: 'background 0.15s'
  };
};

const getToggleKnobStyle = (key) => {
  const on = props.preferences.notifications && props.preferences.notifications[key];
  return {
    width: '20px',
    height: '20px',
    borderRadius: '50%',
    backgroundColor: '#ffffff',
    position: 'relative',
    transform: `translateX(${on ? '20px' : '0px'})`,
    transition: 'transform 0.15s',
    boxShadow: '0 1px 3px rgba(0,0,0,0.2)',
    marginTop: '-22px',
    marginLeft: on ? '24px' : '2px'
  };
};

const toggleNotification = (key) => {
  const value = !!(props.preferences.notifications && props.preferences.notifications[key]);
  updateNotification(key, !value);
};

const updateLanguage = (event) => {
  emit('update-preferences', { language: event.target.value });
};

const updateWalkingPace = (event) => {
  emit('update-preferences', { walkingPace: event.target.value });
};

const updateBudget = (event) => {
  emit('update-preferences', { budget: event.target.value });
};

const updateNotification = (key, value) => {
  const newNotifications = { ...(props.preferences.notifications || {}), [key]: value };
  emit('update-preferences', { notifications: newNotifications });
};

const toggleInterestTag = (tag) => {
  const index = selectedInterests.value.indexOf(tag);
  if (index > -1) {
    selectedInterests.value.splice(index, 1);
  } else {
    selectedInterests.value.push(tag);
  }
};
</script>