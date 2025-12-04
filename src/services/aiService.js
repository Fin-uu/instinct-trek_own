// src/services/aiService.js
// AI API 服務 - 連接到後端 vLLM

const API_BASE_URL = 'http://localhost:3000';

/**
 * 測試 API 連接
 */
export const testConnection = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error('連接測試失敗:', error);
    return { success: false, error: error.message };
  }
};

/**
 * 測試 vLLM 連接
 */
export const testVLLM = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/test-vllm`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('vLLM 測試失敗:', error);
    return { success: false, error: error.message };
  }
};

/**
 * 發送聊天訊息（基本版本）
 * @param {string} message - 用戶訊息
 * @param {Array} history - 對話歷史
 */
export const sendMessage = async (message, history = []) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message,
        history
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('發送訊息失敗:', error);
    return {
      success: false,
      error: error.message
    };
  }
};

/**
 * 發送聊天訊息（流式版本 - 逐字顯示）
 * @param {string} message - 用戶訊息
 * @param {Array} history - 對話歷史
 * @param {Function} onChunk - 收到每個文字塊時的回調
 */
export const sendMessageStream = async (message, history = [], onChunk) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message,
        history
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // 保留不完整的行

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') {
            return { success: true, done: true };
          }

          try {
            const parsed = JSON.parse(data);
            if (parsed.content && onChunk) {
              onChunk(parsed.content);
            }
          } catch (e) {
            // 忽略解析錯誤
          }
        }
      }
    }

    return { success: true, done: true };

  } catch (error) {
    console.error('流式訊息失敗:', error);
    return {
      success: false,
      error: error.message
    };
  }
};

/**
 * 生成行程
 * @param {string} destination - 目的地
 * @param {number} days - 天數
 * @param {Object} preferences - 偏好設定
 */
export const generateItinerary = async (destination, days, preferences = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-itinerary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        destination,
        days,
        preferences
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('生成行程失敗:', error);
    return {
      success: false,
      error: error.message
    };
  }
};

/**
 * 從用戶輸入中提取目的地
 * @param {string} input - 用戶輸入
 */
export const extractDestination = (input) => {
  // 常見目的地清單
  const places = [
    '京都', '東京', '大阪', '奈良', '北海道', '沖繩', '福岡', '名古屋',
    '台北', '台中', '台南', '高雄', '花蓮', '台東', '宜蘭',
    '首爾', '釜山', '濟州島',
    '曼谷', '清邁', '普吉島',
    '新加坡', '吉隆坡',
    '香港', '澳門',
    '上海', '北京', '成都', '西安', '杭州', '蘇州'
  ];

  for (const place of places) {
    if (input.includes(place)) {
      return place;
    }
  }

  // 如果沒有找到，返回 null
  return null;
};

/**
 * 從用戶輸入中提取天數
 * @param {string} input - 用戶輸入
 */
export const extractDays = (input) => {
  // 中文數字對應表
  const chineseNumbers = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '兩': 2, '倆': 2
  };
  
  // 1. 匹配阿拉伯數字 "3天" "5日"
  const arabicMatch = input.match(/(\d+)\s*[天日]/);
  if (arabicMatch) {
    return parseInt(arabicMatch[1]);
  }
  
  // 2. 匹配 "X天Y夜" 格式（取天數）
  const dayNightMatch = input.match(/([一二三四五六七八九十兩倆\d]+)\s*天\s*([一二三四五六七八九十兩倆\d]+)\s*夜/);
  if (dayNightMatch) {
    const dayPart = dayNightMatch[1];
    // 嘗試解析為數字
    if (/^\d+$/.test(dayPart)) {
      return parseInt(dayPart);
    }
    // 嘗試中文數字
    if (chineseNumbers[dayPart]) {
      return chineseNumbers[dayPart];
    }
  }
  
  // 3. 匹配中文數字 "三天" "五日"
  const chineseMatch = input.match(/([一二三四五六七八九十兩倆]+)\s*[天日]/);
  if (chineseMatch) {
    const chineseNum = chineseMatch[1];
    if (chineseNumbers[chineseNum]) {
      return chineseNumbers[chineseNum];
    }
  }

  // 預設 3 天
  console.log('⚠️ 無法提取天數，使用預設值 3 天');
  return 3;
};

/**
 * 判斷是否應該生成行程
 * @param {string} input - 用戶輸入
 */
export const shouldGenerateItinerary = (input) => {
  const lowerInput = input.toLowerCase();
  
  // 中文關鍵字
  const chineseKeywords = [
    '天', '日', '行程', '旅遊', '規劃', '安排',
    '去', '玩', '遊', '景點', '推薦'
  ];
  
  // 英文關鍵字
  const englishKeywords = [
    'day', 'days', 'trip', 'travel', 'itinerary', 'plan',
    'visit', 'tour', 'recommend', 'attraction', 'schedule'
  ];
  
  return chineseKeywords.some(keyword => input.includes(keyword)) ||
         englishKeywords.some(keyword => lowerInput.includes(keyword));
};

/**
 * 建立對話歷史（給 API 用）
 * @param {Array} messages - 前端訊息陣列
 */
export const buildHistory = (messages) => {
  return messages
    .filter(msg => msg.type === 'user' || msg.type === 'assistant')
    .map(msg => ({
      role: msg.type === 'user' ? 'user' : 'assistant',
      content: msg.content
    }));
};

export default {
  testConnection,
  testVLLM,
  sendMessage,
  sendMessageStream,
  generateItinerary,
  extractDestination,
  extractDays,
  shouldGenerateItinerary,
  buildHistory
};