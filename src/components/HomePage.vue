<template>
  <div class="home-container">
    <!-- 頂部英雄區 -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-overlay"></div>
        <div class="floating-elements">
          <div class="float-element" v-for="i in 6" :key="i"></div>
        </div>
      </div>
      
      <div class="hero-content">
        <div class="hero-icon">
          <MapPinIcon :size="64" class="text-white" />
        </div>
        
        <h1 class="hero-title">AI 智慧導遊</h1>
        <p class="hero-subtitle">您的全天候旅遊隨身助手</p>
        <p class="hero-description">
          結合 AI 人工智慧，為您量身打造完美行程<br />
          即時天氣預警 • 個人化推薦 • 智能路線規劃
        </p>
        
        <div class="hero-buttons">
          <button @click="startChat" class="btn-hero btn-primary">
            <SparklesIcon :size="20" />
            開始規劃行程
          </button>
          <button @click="scrollToFeatures" class="btn-hero btn-outline">
            <InfoIcon :size="20" />
            了解更多
          </button>
        </div>
        
        <div class="hero-stats">
          <div class="stat-item">
            <UsersIcon :size="24" />
            <div class="stat-number">10,000+</div>
            <div class="stat-label">活躍用戶</div>
          </div>
          <div class="stat-item">
            <MapIcon :size="24" />
            <div class="stat-number">5,000+</div>
            <div class="stat-label">行程規劃</div>
          </div>
          <div class="stat-item">
            <StarIcon :size="24" />
            <div class="stat-number">4.9</div>
            <div class="stat-label">用戶評分</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能特色區 -->
    <section class="features-section" ref="featuresSection">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">核心功能</span>
          <h2 class="section-title">為什麼選擇我們？</h2>
          <p class="section-description">
            運用最先進的 AI 技術，打造最貼心的旅遊體驗
          </p>
        </div>
        
        <div class="features-grid">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="feature-card"
          >
            <div class="feature-icon" :class="feature.colorClass">
              <component :is="feature.icon" :size="32" />
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
            <ul class="feature-list">
              <li v-for="(item, idx) in feature.items" :key="idx">
                <CheckIcon :size="16" />
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- 使用流程區 -->
    <section class="process-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">簡單三步驟</span>
          <h2 class="section-title">開始您的智慧旅程</h2>
        </div>
        
        <div class="process-timeline">
          <div 
            v-for="(step, index) in processSteps" 
            :key="index"
            class="process-step"
          >
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <div class="step-icon" :class="step.colorClass">
                <component :is="step.icon" :size="28" />
              </div>
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 應用場景區 -->
    <section class="examples-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">實際應用</span>
          <h2 class="section-title">適用各種旅遊場景</h2>
        </div>
        
        <div class="examples-grid">
          <div 
            v-for="(example, index) in examples" 
            :key="index"
            class="example-card"
            @click="selectExample(example)"
          >
            <div class="example-image">
              <img :src="example.image" :alt="example.title" />
              <div class="example-overlay">
                <component :is="example.icon" :size="48" class="text-white" />
              </div>
            </div>
            <div class="example-content">
              <h3 class="example-title">{{ example.title }}</h3>
              <p class="example-description">{{ example.description }}</p>
              <div class="example-tags">
                <span v-for="tag in example.tags" :key="tag" class="example-tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 用戶評價區 -->
    <section class="testimonials-section">
      <div class="section-container">
        <div class="section-header">
          <span class="section-badge">用戶好評</span>
          <h2 class="section-title">聽聽他們怎麼說</h2>
        </div>
        
        <div class="testimonials-grid">
          <div class="testimonial-card" v-for="(testimonial, index) in testimonials" :key="index">
            <div class="testimonial-rating">
              <StarIcon 
                v-for="i in 5" 
                :key="i" 
                :size="16" 
                :class="i <= testimonial.rating ? 'star-filled' : 'star-empty'"
              />
            </div>
            <p class="testimonial-text">"{{ testimonial.text }}"</p>
            <div class="testimonial-author">
              <div class="author-avatar">
                {{ testimonial.name.charAt(0) }}
              </div>
              <div class="author-info">
                <div class="author-name">{{ testimonial.name }}</div>
                <div class="author-location">{{ testimonial.location }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA 區 -->
    <section class="cta-section">
      <div class="cta-content">
        <div class="cta-icon">
          <RocketIcon :size="64" class="text-white" />
        </div>
        <h2 class="cta-title">準備好開始您的旅程了嗎？</h2>
        <p class="cta-description">
          立即體驗 AI 智慧導遊，讓每一次旅行都充滿驚喜
        </p>
        <button @click="startChat" class="btn-cta">
          <SparklesIcon :size="24" />
          立即開始使用
          <ArrowRightIcon :size="24" />
        </button>
        <p class="cta-note">完全免費，無需註冊</p>
      </div>
    </section>

    <!-- 頁腳 -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-columns">
          <div class="footer-column">
            <div class="footer-logo">
              <MapPinIcon :size="32" />
              <span>AI 智慧導遊</span>
            </div>
            <p class="footer-description">
              運用 AI 技術，為全球旅行者提供最智慧的旅遊規劃服務
            </p>
          </div>
          
          <div class="footer-column">
            <h4 class="footer-title">產品</h4>
            <ul class="footer-links">
              <li><a href="#">功能介紹</a></li>
              <li><a href="#">使用教學</a></li>
              <li><a href="#">常見問題</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 class="footer-title">公司</h4>
            <ul class="footer-links">
              <li><a href="#">關於我們</a></li>
              <li><a href="#">聯絡我們</a></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 class="footer-title">法律</h4>
            <ul class="footer-links">
              <li><a href="#">服務條款</a></li>
              <li><a href="#">隱私政策</a></li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2025 AI 智慧導遊. 保留所有權利.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import {
  MapPin as MapPinIcon,
  Sparkles as SparklesIcon,
  Info as InfoIcon,
  Users as UsersIcon,
  Map as MapIcon,
  Star as StarIcon,
  MessageSquare as MessageSquareIcon,
  Calendar as CalendarIcon,
  CloudRain as CloudRainIcon,
  Camera as CameraIcon,
  Heart as HeartIcon,
  Settings as SettingsIcon,
  Check as CheckIcon,
  Rocket as RocketIcon,
  ArrowRight as ArrowRightIcon,
  Mountain as MountainIcon,
  UtensilsCrossed as UtensilsIcon,
  Building as BuildingIcon,
  Palmtree as PalmtreeIcon
} from 'lucide-vue-next';

const emit = defineEmits(['start-chat']);

const featuresSection = ref(null);

// 功能特色
const features = [
  {
    icon: MessageSquareIcon,
    title: 'AI 智能對話',
    description: '自然語言交流，像與朋友聊天一樣規劃旅程',
    colorClass: 'bg-blue-gradient',
    items: ['24/7 即時回應', '多語言支援', '語音輸入辨識']
  },
  {
    icon: CalendarIcon,
    title: '智能行程規劃',
    description: '根據個人喜好自動生成最佳旅遊路線',
    colorClass: 'bg-purple-gradient',
    items: ['個性化推薦', '景點優化排序', '時間智能分配']
  },
  {
    icon: CloudRainIcon,
    title: '即時天氣預警',
    description: '提前預知天氣變化，自動調整行程安排',
    colorClass: 'bg-orange-gradient',
    items: ['精準天氣預報', '自動替代方案', '推播即時通知']
  },
  {
    icon: CameraIcon,
    title: '照片智能辨識',
    description: '上傳照片即可識別景點、翻譯文字',
    colorClass: 'bg-green-gradient',
    items: ['AI 圖像識別', '多語言翻譯', '景點資訊查詢']
  },
  {
    icon: HeartIcon,
    title: '個人偏好學習',
    description: '記住您的喜好，每次推薦都更精準',
    colorClass: 'bg-pink-gradient',
    items: ['智能學習系統', '興趣標籤管理', '歷史行程分析']
  },
  {
    icon: SettingsIcon,
    title: '高度可自訂',
    description: '靈活設定步行速度、預算、興趣等',
    colorClass: 'bg-cyan-gradient',
    items: ['多種偏好設定', '彈性調整方案', '即時更新行程']
  }
];

// 使用流程
const processSteps = [
  {
    icon: MessageSquareIcon,
    title: '告訴我們您的需求',
    description: '輸入想去的地方、旅行天數、興趣偏好等資訊',
    colorClass: 'bg-blue-gradient'
  },
  {
    icon: SparklesIcon,
    title: 'AI 智能分析',
    description: '系統自動分析並生成最適合您的旅遊方案',
    colorClass: 'bg-purple-gradient'
  },
  {
    icon: MapIcon,
    title: '開始您的旅程',
    description: '跟隨智能導航，享受無憂的旅行體驗',
    colorClass: 'bg-green-gradient'
  }
];

// 應用場景
const examples = [
  {
    title: '城市深度遊',
    description: '探索城市的每個角落，發現隱藏的寶藏',
    image: 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600&q=80',
    icon: BuildingIcon,
    tags: ['文化', '歷史', '美食']
  },
  {
    title: '自然生態之旅',
    description: '親近大自然，體驗戶外探險的樂趣',
    image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80',
    icon: MountainIcon,
    tags: ['登山', '健行', '生態']
  },
  {
    title: '美食饕客行',
    description: '品嚐當地特色美食，尋找米其林餐廳',
    image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80',
    icon: UtensilsIcon,
    tags: ['美食', '小吃', '餐廳']
  },
  {
    title: '海島度假風',
    description: '享受陽光沙灘，體驗悠閒的島嶼生活',
    image: 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=600&q=80',
    icon: PalmtreeIcon,
    tags: ['海灘', '潛水', '度假']
  }
];

// 用戶評價
const testimonials = [
  {
    name: '王小明',
    location: '台北，台灣',
    rating: 5,
    text: '太方便了！去京都玩的時候，AI 幫我規劃了完美的三天行程，還在下雨前提醒我改去室內景點，真的很貼心！'
  },
  {
    name: '李美麗',
    location: '高雄，台灣',
    rating: 5,
    text: '作為一個路痴，這個 APP 簡直是救星。不僅幫我找到最佳路線，還推薦了很多在地人才知道的美食，超讚！'
  },
  {
    name: '陳大偉',
    location: '台中，台灣',
    rating: 5,
    text: '帶著爸媽出國旅遊，設定了慢步調和低步數模式，AI 自動調整行程，讓全家都玩得很開心。五顆星推薦！'
  },
  {
    name: '林小芳',
    location: '台南，台灣',
    rating: 5,
    text: '照片翻譯功能超實用！在日本看不懂菜單的時候，拍照就能翻譯，還能查詢景點資訊，出國必備！'
  }
];

// 方法
const startChat = () => {
  emit('start-chat');
};

const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({ behavior: 'smooth' });
};

const selectExample = (example) => {
  emit('start-chat', example.title);
};
</script>

<style scoped>
/* 基礎樣式 */
.home-container {
  width: 100%;
  overflow-x: hidden;
}

/* 英雄區 */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.1) 0%, rgba(0,0,0,0.3) 100%);
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
}

.float-element {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
}

.float-element:nth-child(1) { width: 80px; height: 80px; top: 20%; left: 10%; animation-delay: 0s; }
.float-element:nth-child(2) { width: 60px; height: 60px; top: 60%; left: 80%; animation-delay: 2s; }
.float-element:nth-child(3) { width: 100px; height: 100px; top: 80%; left: 20%; animation-delay: 4s; }
.float-element:nth-child(4) { width: 40px; height: 40px; top: 30%; left: 70%; animation-delay: 6s; }
.float-element:nth-child(5) { width: 70px; height: 70px; top: 50%; left: 50%; animation-delay: 8s; }
.float-element:nth-child(6) { width: 90px; height: 90px; top: 10%; left: 90%; animation-delay: 10s; }

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-30px) translateX(30px); }
  50% { transform: translateY(-60px) translateX(-30px); }
  75% { transform: translateY(-30px) translateX(30px); }
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 2rem;
  margin-bottom: 2rem;
  animation: float 3s ease-in-out infinite;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1rem;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: 1.75rem;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 1rem;
}

.hero-description {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 3rem;
  line-height: 1.8;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.btn-hero {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: 9999px;
  transition: all 0.3s;
  cursor: pointer;
  border: none;
}

.btn-hero.btn-primary {
  background: white;
  color: #667eea;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.btn-hero.btn-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.btn-hero.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-hero.btn-outline:hover {
  background: white;
  color: #667eea;
}

.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: white;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

/* 通用區塊 */
.section-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-description {
  font-size: 1.125rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

/* 功能特色 */
.features-section {
  background: #f9fafb;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 1.5rem;
}

.bg-blue-gradient { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
.bg-purple-gradient { background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%); }
.bg-orange-gradient { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
.bg-green-gradient { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.bg-pink-gradient { background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); }
.bg-cyan-gradient { background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); }

.feature-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.feature-description {
  color: #6b7280;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4b5563;
  font-size: 0.875rem;
}

.feature-list li svg {
  color: #10b981;
  flex-shrink: 0;
}

/* 使用流程 */
.process-section {
  background: white;
}

.process-timeline {
  display: flex;
  gap: 2rem;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
}

.process-step {
  flex: 1;
  min-width: 280px;
  max-width: 350px;
  text-align: center;
}

.step-number {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1.5rem;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.step-content {
  background: #f9fafb;
  border-radius: 1.5rem;
  padding: 2rem;
}

.step-icon {
  width: 64px;
  height: 64px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1rem;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.step-description {
  color: #6b7280;
  line-height: 1.6;
}

/* 應用場景 */
.examples-section {
  background: #f9fafb;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.example-card {
  background: white;
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  cursor: pointer;
}

.example-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.example-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.example-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.example-card:hover .example-image img {
  transform: scale(1.1);
}

.example-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.example-card:hover .example-overlay {
  opacity: 1;
}

.example-content {
  padding: 1.5rem;
}

.example-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.example-description {
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.example-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.example-tag {
  padding: 0.25rem 0.75rem;
  background: #f3f4f6;
  color: #4b5563;
  border-radius: 9999px;
  font-size: 0.75rem;
}

/* 用戶評價 */
.testimonials-section {
  background: white;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: #f9fafb;
  border-radius: 1.5rem;
  padding: 2rem;
  transition: all 0.3s;
}

.testimonial-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.testimonial-rating {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.star-filled { color: #fbbf24; }
.star-empty { color: #d1d5db; }

.testimonial-text {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
}

.author-name {
  font-weight: 600;
  color: #1f2937;
}

.author-location {
  font-size: 0.875rem;
  color: #6b7280;
}

/* CTA 區 */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 5rem 2rem;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  color: white;
}

.cta-icon {
  display: inline-flex;
  margin-bottom: 2rem;
  animation: bounce 2s infinite;
}

.cta-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-description {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.95;
}

.btn-cta {
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 3rem;
  font-size: 1.25rem;
  font-weight: 600;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.btn-cta:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
}

.cta-note {
  margin-top: 1rem;
  font-size: 0.875rem;
  opacity: 0.8;
}

/* 頁腳 */
.footer {
  background: #1f2937;
  color: #d1d5db;
  padding: 4rem 2rem 2rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.footer-description {
  color: #9ca3af;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.footer-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-links a {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

.footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid #374151;
  text-align: center;
}

/* 響應式 */
@media (max-width: 768px) {
  .hero-title { font-size: 2.5rem; }
  .hero-subtitle { font-size: 1.25rem; }
  .section-title { font-size: 2rem; }
  .cta-title { font-size: 2rem; }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>