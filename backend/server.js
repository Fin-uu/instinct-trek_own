// server.js - 後端 API 服務器
import express from 'express';
import OpenAI from 'openai';
import cors from 'cors';

const app = express();

// 中間件
app.use(cors()); // 允許跨域請求
app.use(express.json()); // 解析 JSON

// 連接到 vLLM 服務器
const openai = new OpenAI({
  baseURL: 'http://210.61.209.139:45014/v1', // vLLM 服務器地址
  apiKey: 'dummy-key',
  defaultHeaders: {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept-Charset': 'utf-8'
  }
});

// System prompt (define AI role)
const SYSTEM_PROMPT = `You are TravelMate, a professional and friendly travel guide. Provide helpful travel advice, attraction recommendations, and trip planning assistance. Keep responses clear, specific, and practical.`;

// Helper function to clean vLLM response
function cleanVLLMResponse(content) {
  if (!content) return '';
  
  // vLLM sometimes returns responses with "analysis...assistantfinal" prefix
  // Extract only the final assistant response
  const finalMarker = 'assistantfinal';
  const finalIndex = content.indexOf(finalMarker);
  
  if (finalIndex !== -1) {
    return content.substring(finalIndex + finalMarker.length).trim();
  }
  
  // If no marker found, return original content
  return content;
}

// ==================== API 端點 ====================

// 1. 健康檢查
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'AI Travel Guide Backend Running',
    vllm: 'http://210.61.209.139:45014/v1'
  });
});

// 2. Basic chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    console.log('📨 Received message:', message);
    console.log('📚 History length:', history.length);
    if (history.length > 0) {
      console.log('📚 Last history item:', history[history.length - 1]);
    }

    // Build conversation history
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...history.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      { role: 'user', content: message }
    ];

    // Call vLLM using native fetch with explicit UTF-8 encoding
    const requestBody = {
      model: 'openai/gpt-oss-120b',
      messages: messages,
      max_tokens: 1500,
      temperature: 0.8,
    };
    
    console.log('📤 Sending to vLLM:', JSON.stringify(requestBody).substring(0, 200));
    
    const vllmResponse = await fetch('http://210.61.209.139:45014/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });

    if (!vllmResponse.ok) {
      throw new Error(`vLLM returned ${vllmResponse.status}: ${vllmResponse.statusText}`);
    }

    const completion = await vllmResponse.json();
    let response = completion.choices[0].message.content;
    
    // Clean the response to remove vLLM's internal markers
    response = cleanVLLMResponse(response);
    
    console.log('✅ AI response:', response.substring(0, 100) + '...');

    res.json({
      success: true,
      content: response,
      usage: completion.usage
    });

  } catch (error) {
    console.error('❌ Chat error:', error.message);
    res.status(500).json({
      success: false,
      error: 'Cannot process request',
      details: error.message
    });
  }
});

// 3. 流式對話端點（逐字顯示）
app.post('/api/chat/stream', async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    console.log('📨 收到流式請求:', message);

    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...history.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      { role: 'user', content: message }
    ];

    // 設置 SSE 標頭
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // 流式呼叫
    const stream = await openai.chat.completions.create({
      model: 'openai/gpt-oss-120b',
      messages: messages,
      max_tokens: 1500,
      temperature: 0.8,
      stream: true
    });

    // 逐塊發送
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        res.write(`data: ${JSON.stringify({ content })}\n\n`);
      }
    }

    res.write('data: [DONE]\n\n');
    res.end();

    console.log('✅ 流式回應完成');

  } catch (error) {
    console.error('❌ Stream chat error:', error.message);
    res.status(500).json({
      success: false,
      error: 'Cannot process stream request',
      details: error.message
    });
  }
});

// 4. 智慧行程生成端點
app.post('/api/generate-itinerary', async (req, res) => {
  try {
    const { destination, days, preferences = {} } = req.body;

    console.log('📨 生成行程:', { destination, days });

    const prompt = `
請為以下旅遊需求生成詳細行程：

目的地：${destination}
天數：${days}天
偏好：${JSON.stringify(preferences)}

請以 JSON 格式返回，格式如下：
{
  "title": "行程標題",
  "style": "旅遊風格描述",
  "crowd": "人流建議",
  "budget": "預算範圍",
  "steps": "每日平均步數",
  "highlights": "精選景點（用頓號分隔）",
  "dailySchedule": [
    {
      "date": "第 1 天",
      "totalSteps": "8000步",
      "totalCost": "NT$2000",
      "totalTime": "8小時",
      "activities": [
        {
          "time": "09:00",
          "name": "景點名稱",
          "type": "temple",
          "description": "詳細描述，包含特色和注意事項",
          "duration": "1.5小時",
          "cost": "¥500",
          "transport": "交通方式和時間"
        }
      ]
    }
  ]
}

重要要求：
1. activities 的 type 只能是：temple, food, shopping, cafe, sightseeing, nature
2. 每天安排 3-5 個活動
3. 考慮交通時間和用餐時間
4. 費用使用當地貨幣
5. 確保返回有效的 JSON（不要包含其他文字）
`;

    const completion = await openai.chat.completions.create({
      model: 'openai/gpt-oss-120b',
      messages: [
        { role: 'system', content: '你是專業的旅遊規劃師，擅長生成結構化的行程資料。' },
        { role: 'user', content: prompt }
      ],
      max_tokens: 3000,
      temperature: 0.7
    });

    let response = completion.choices[0].message.content;
    response = cleanVLLMResponse(response);
    
    // 提取 JSON
    let itinerary;
    try {
      // 嘗試直接解析
      itinerary = JSON.parse(response);
    } catch {
      // 如果失敗，嘗試提取 JSON 塊
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        itinerary = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('無法解析 JSON');
      }
    }

    console.log('✅ 行程生成成功:', itinerary.title);

    res.json({
      success: true,
      itinerary: itinerary
    });

  } catch (error) {
    console.error('❌ 行程生成錯誤:', error.message);
    res.status(500).json({
      success: false,
      error: 'Cannot generate itinerary',
      details: error.message
    });
  }
});

// 5. 測試 vLLM 連接
app.get('/api/test-vllm', async (req, res) => {
  try {
    // 測試簡單對話
    const testResponse = await openai.chat.completions.create({
      model: 'openai/gpt-oss-120b',
      messages: [
        { role: 'user', content: 'Hello, please introduce yourself in one sentence.' }
      ],
      max_tokens: 100
    });

    const cleanedResponse = cleanVLLMResponse(testResponse.choices[0].message.content);

    res.json({
      success: true,
      message: 'vLLM connected successfully!',
      response: cleanedResponse,
      model: 'openai/gpt-oss-120b'
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'vLLM 連接失敗',
      error: error.message
    });
  }
});

// 啟動服務器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('╔══════════════════════════════════════╗');
  console.log('║   🚀 AI Travel Guide Backend Started ║');
  console.log('╚══════════════════════════════════════╝');
  console.log('');
  console.log(`✅ Server running at: http://localhost:${PORT}`);
  console.log(`📡 Connected to vLLM: http://210.61.209.139:45014/v1`);
  console.log('');
  console.log('Available endpoints:');
  console.log(`  GET  /health                 - Health check`);
  console.log(`  GET  /api/test-vllm          - Test vLLM connection`);
  console.log(`  POST /api/chat               - Basic chat`);
  console.log(`  POST /api/chat/stream        - Streaming chat`);
  console.log(`  POST /api/generate-itinerary - Generate itinerary`);
  console.log('');
  console.log('Press Ctrl+C to stop server');
  console.log('');
});

// export default app; // 註解掉以保持服務器運行
