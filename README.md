# 📈 股票看盤 Dashboard Web

一個功能完整的股票看盤軟體網頁版，支援即時股價、技術分析指標、自選股管理。

## ✨ 功能特色

- **即時股價** - 透過 Yahoo Finance API 取得即時報價
- **K線圖** - 互動式 K線圖表，支援縮放
- **技術分析指標**
  - MA (移動平均線) - 5日、20日均線
  - RSI (相對強弱指數)
  - MACD (指數平滑異同移動平均線)
  - KDJ (隨機指標)
  - 布林帶 (Bollinger Bands)
- **自選股管理** - 新增、刪除、持久化存儲
- **響應式設計** - 支援桌面和移動設備
- **深色主題** - 專業級深色界面

## 🛠️ 技術棧

- **前端框架**: 純 HTML/CSS/JavaScript（無需後端）
- **圖表庫**: ECharts 5.4.3
- **數據源**: Yahoo Finance API（免費、無需 API Key）
- **部署**: Vercel

## 🚀 本地運行

```bash
# 簡單的 HTTP 服務器
python -m http.server 3000

# 或使用 npx
npx serve .
```

然後在瀏覽器中打開 `http://localhost:3000`

## 📊 部署到 Vercel

1. Fork 或 Clone 此倉庫
2. 在 Vercel 中導入項目
3. 部署（無需額外配置）

或使用 Vercel CLI：

```bash
npm i -g vercel
vercel
```

## 📱 使用說明

1. **添加股票** - 點擊側邊欄的「+ 添加」按鈕
2. **快速添加** - 點擊常用股票代碼晶片（AAPL, GOOGL 等）
3. **切換股票** - 點擊自選股列表中的股票
4. **刪除股票** - 滑鼠懸停後點擊 × 按鈕
5. **查看技術分析** - 在圖表下方查看各種指標
6. **切換時間範圍** - 點擊 1天/5天/1月/3月/6月/1年

## 🔧 開發

項目結構：

```
stock-dashboard/
├── index.html      # 主頁面（包含所有 HTML/CSS/JS）
├── fetch_stock.py  # Python 版數據獲取腳本
├── indicators.py   # 技術指標計算模組
└── package.json    # NPM 配置
```

## 📄 License

MIT
