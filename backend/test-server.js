// test-server.js - 最小測試版本
import express from 'express';
import cors from 'cors';

const app = express();

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Test server running' });
});

const PORT = 3000;
const server = app.listen(PORT, () => {
  console.log(`✅ Test server running on port ${PORT}`);
});

// 保持服務器運行
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server');
  server.close(() => {
    process.exit(0);
  });
});

console.log('Server setup complete, waiting for requests...');
