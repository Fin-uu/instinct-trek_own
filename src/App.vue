<template>
  <div id="app">
    <!-- 首頁 -->
    <HomePage 
      v-if="currentPage === 'home'"
      @start-chat="handleStartChat"
    />

    <!-- 聊天應用 -->
    <div v-else class="chat-app">
      <!-- 頂部導航欄 -->
      <header class="app-header">
        <div class="header-content">
          <button @click="currentPage = 'home'" class="back-to-home">
            <MapPinIcon :size="24" class="text-blue-500" />
          </button>
          <div class="header-title">
            <h1>AI 智慧導遊</h1>
            <p>全天候隨身助手</p>
          </div>
          <div class="header-nav">
            <button
              @click="currentPage = 'itinerary'"
              :class="['nav-btn', currentPage === 'itinerary' && 'active']"
            >
              <ClockIcon :size="18" />
              <span>行程</span>
            </button>
            <button
              @click="currentPage = 'chat'"
              :class="['nav-btn', currentPage === 'chat' && 'active']"
            >
              <MessageSquareIcon :size="18" />
              <span>聊天</span>
            </button>
            <button
              @click="currentPage = 'settings'"
              :class="['nav-btn', currentPage === 'settings' && 'active']"
            >
              <SettingsIcon :size="20" />
            </button>
          </div>
        </div>
      </header>

      <!-- 天氣警報 -->
      <WeatherAlert v-if="showAlert" @close="showAlert = false" />

      <!-- 主要內容區 -->
      <main class="app-main">
        <!-- 聊天介面 -->
        <ChatInterface
          v-if="currentPage === 'chat'"
          :messages="messages"
          :selected-image="selectedImage"
          @remove-image="selectedImage = null"
          @view-itinerary="handleViewItinerary"
        />
        
        <!-- 行程列表頁 -->
        <ItineraryPage 
          v-else-if="currentPage === 'itinerary'"
          @view-detail="handleViewItineraryDetail"
        />
        
        <!-- 行程詳細頁 -->
        <ItineraryDetailPage
          v-else-if="currentPage === 'itinerary-detail'"
          :itinerary-id="selectedItineraryId"
          @go-back="currentPage = 'itinerary'"
          @start-navigation="handleStartNavigation"
          @modify="handleModifyItinerary"
        />
        
        <!-- 設定頁 -->
        <SettingsPage
          v-else-if="currentPage === 'settings'"
          :preferences="userPreferences"
          @update-preferences="updatePreferences"
        />
      </main>

      <!-- 底部輸入區（僅在聊天頁顯示） -->
      <footer v-if="currentPage === 'chat'" class="app-footer">
        <div class="footer-content">
          <div v-if="selectedImage" class="selected-image">
            <img :src="selectedImage" alt="Selected" />
            <button @click="selectedImage = null" class="remove-image">×</button>
          </div>
          
          <div class="input-area">
            <input
              type="file"
              ref="fileInput"
              @change="handleImageUpload"
              accept="image/*"
              class="hidden"
            />
            <button @click="$refs.fileInput.click()" class="icon-btn">
              <CameraIcon :size="22" />
            </button>
            
            <input
              type="text"
              v-model="inputValue"
              @keypress.enter="handleSendMessage"
              placeholder="例如：我想去台南吃小吃，不要排隊"
              class="text-input"
            />
            
            <button @click="handleSendMessage" class="send-btn">
              <SendIcon :size="22" />
            </button>
          </div>
          
          <p class="footer-hint">💡 可上傳照片進行翻譯或辨識</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import {
  Send as SendIcon,
  MapPin as MapPinIcon,
  Clock as ClockIcon,
  Camera as CameraIcon,
  Settings as SettingsIcon,
  MessageSquare as MessageSquareIcon
} from 'lucide-vue-next';
import HomePage from './components/HomePage.vue';
import ChatInterface from './components/ChatInterface.vue';
import WeatherAlert from './components/WeatherAlert.vue';
import ItineraryPage from './components/ItineraryPage.vue';
import ItineraryDetailPage from './components/ItineraryDetailPage.vue';
import SettingsPage from './components/SettingsPage.vue';

const currentPage = ref('home');
const inputValue = ref('');
const selectedImage = ref(null);
const showAlert = ref(false);
const fileInput = ref(null);
const selectedItineraryId = ref(null);

const messages = ref([
  {
    type: 'assistant',
    content: '您好！我是您的 AI 智慧導遊助手。我可以幫您規劃行程、提供天氣警報、推薦景點。請告訴我您想去哪裡？',
    timestamp: new Date()
  }
]);

const userPreferences = ref({
  language: 'zh-TW',
  walkingPace: 'normal',
  budget: 'medium',
  notifications: {
    weather: true,
    itinerary: true,
    recommendations: false
  }
});

onMounted(() => {
  setTimeout(() => {
    if (currentPage.value === 'chat') {
      showAlert.value = true;
    }
  }, 5000);
});

const handleStartChat = (topic) => {
  currentPage.value = 'chat';
  if (topic) {
    inputValue.value = topic;
    handleSendMessage();
  }
};

const handleSendMessage = () => {
  if (!inputValue.value.trim() && !selectedImage.value) return;

  const newMessage = {
    type: 'user',
    content: inputValue.value,
    image: selectedImage.value,
    timestamp: new Date()
  };

  messages.value.push(newMessage);
  const userInput = inputValue.value;
  inputValue.value = '';
  selectedImage.value = null;

  setTimeout(() => {
    messages.value.push({
      type: 'assistant',
      content: '好的！正在為您規劃行程...',
      timestamp: new Date()
    });

    setTimeout(() => {
      messages.value.push({
        type: 'itinerary',
        data: {
          title: generateItineraryTitle(userInput),
          style: '精選推薦',
          crowd: '避開熱門時段',
          budget: '中等消費',
          steps: '每日約8,000步',
          highlights: '清水寺、金閣寺、伏見稻荷、嵐山竹林...'
        },
        timestamp: new Date()
      });
    }, 1500);
  }, 1000);
};

const generateItineraryTitle = (input) => {
  if (input.includes('京都')) return '京都三日古蹟巡禮';
  if (input.includes('台南')) return '台南美食一日遊';
  if (input.includes('東京')) return '東京購物之旅';
  return '精選旅遊行程';
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onloadend = () => {
      selectedImage.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

const updatePreferences = (newPreferences) => {
  userPreferences.value = { ...userPreferences.value, ...newPreferences };
};

const handleViewItinerary = (itineraryData) => {
  selectedItineraryId.value = itineraryData.id || 'kyoto-3days';
  currentPage.value = 'itinerary-detail';
};

const handleViewItineraryDetail = (itineraryId) => {
  selectedItineraryId.value = itineraryId;
  currentPage.value = 'itinerary-detail';
};

const handleStartNavigation = (itinerary) => {
  console.log('開始導航:', itinerary);
  alert('導航功能開發中...');
};

const handleModifyItinerary = (itinerary) => {
  currentPage.value = 'chat';
  inputValue.value = `我想修改「${itinerary.title}」的行程`;
  setTimeout(() => {
    handleSendMessage();
  }, 100);
};
</script>

<style scoped>
/* 全局容器 */
#app {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 聊天應用容器 */
.chat-app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background-color: #f9fafb;
}

/* 頂部導航欄 */
.app-header {
  background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
  color: white;
  padding: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.back-to-home {
  background: white;
  padding: 0.5rem;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.back-to-home:hover {
  transform: scale(1.05);
}

.header-title {
  flex: 1;
  text-align: center;
}

.header-title h1 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.header-title p {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0;
}

.header-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 9999px;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.875rem;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.4);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.5);
}

.nav-btn span {
  display: none;
}

@media (min-width: 640px) {
  .nav-btn span {
    display: inline;
  }
}

/* 主要內容區 */
.app-main {
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* 底部輸入區 */
.app-footer {
  background: white;
  border-top: 1px solid #e5e7eb;
  padding: 1rem;
  flex-shrink: 0;
}

.footer-content {
  max-width: 1000px;
  margin: 0 auto;
}

.selected-image {
  margin-bottom: 1rem;
  position: relative;
  display: inline-block;
}

.selected-image img {
  height: 5rem;
  width: 5rem;
  object-fit: cover;
  border-radius: 0.5rem;
}

.remove-image {
  position: absolute;
  top: -0.5rem;
  right: -0.5rem;
  background: #ef4444;
  color: white;
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
}

.remove-image:hover {
  background: #dc2626;
}

.input-area {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hidden {
  display: none;
}

.icon-btn {
  padding: 0.75rem;
  color: #3b82f6;
  background: transparent;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: #eff6ff;
}

.text-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 9999px;
  outline: none;
  transition: all 0.3s;
}

.text-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.send-btn {
  padding: 0.75rem;
  background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
  color: white;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.footer-hint {
  text-align: center;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.5rem;
  margin-bottom: 0;
}

/* 響應式 */
@media (max-width: 640px) {
  .header-content {
    gap: 0.5rem;
  }
  
  .header-title h1 {
    font-size: 1rem;
  }
  
  .header-title p {
    display: none;
  }
}
</style>