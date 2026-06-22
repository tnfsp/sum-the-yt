# Every Frontend System Design Pattern w/ Senior Engineer (Microfrontend, BFF, CDN etc)

> https://www.youtube.com/watch?v=KuClyhvSzXk

## 一句話總結
隨著 AI 越來越會寫前端程式碼，前端工程師唯一的生存之道是升級系統設計與架構能力，這支影片完整拆解了從微前端、BFF、CDN 到渲染策略等所有前端系統設計的核心概念。

## 重點摘要
- **微前端（Micro-frontend）**：將前端單體拆成多個可獨立部署的應用，由一個「shell」負責全域功能（auth、路由、語言、全域狀態），各微前端可掛在不同子網域獨立載入；對應後端的微服務，兩者結合形成由單一團隊垂直擁有的「垂直切片（vertical slice）」。
- **AI 與團隊演進**：依 Conway's Law，組織決定架構；AI 讓「兩個披薩團隊」縮成「一個披薩團隊」，工程師應朝「全端垂直整合工程師」轉型。AI 把實作時間壓到趨近零，但拉高了「驗證時間」，因此架構重點從「寫得快」轉為「容易驗證、降低風險爆炸半徑」。
- **API Gateway**：統一處理邊緣功能（HTTPS、快取、認證、限流），客戶端只需實作一次，後端服務專注自身邏輯；對外用 HTTPS、VPC 內部用 HTTP 以提升效能與安全。
- **Backend for Frontend（BFF）**：每個客戶端（桌面/行動）擁有專屬後端層，前端團隊得以全端方式自主開發、不被後端團隊的 backlog 卡住，並避免 over-fetching / under-fetching。GraphQL 是建構 BFF 的好技術。
- **負載平衡與容器化**：單一 Node.js 伺服器約可撐 2,000～10,000 並發，超過需用 Load Balancer 水平擴展；用 Docker 打包應用（程式+runtime+OS），再交由 Kubernetes/ECS 等編排系統部署。前端工程師需「理解」而非精通這些。
- **CDN**：以全球邊緣節點就近提供靜態資源，解決光速造成的跨洲延遲（約 200～250ms），同時負責壓縮與快取策略，是最便宜有效的效能優化手段；涉及 cache hit、cache invalidation、cache busting 等概念。
- **設計系統（Design System）**：以 design tokens（CSS 自訂屬性）+ 可複用元件確保視覺一致與 DRY，並能集中處理無障礙與單元測試。對 AI 編碼尤其關鍵——有設計系統才能讓 coding agent 跨 session 產出一致 UI。Tailwind 即 Atomic CSS 的實作。
- **Monorepo 與 AI 工作流**：單一倉庫統一程式風格、依賴與品質標準，並讓 coding agent 能跨服務邊界取得完整 context；搭配 Figma 等 design-to-code MCP server 可快速組裝功能。微前端 + 微服務 + monorepo 是與 AI 協作的最有效組合。
- **MCP UI**：把傳統網頁與 LLM 應用結合，讓聊天回應能直接渲染 UI 元件（如地圖、產品卡），由前端解析 LLM 回傳的渲染指令；作者認為這是前端與 LLM 融合的重要方向，UI 不會消失。
- **效能與 Core Web Vitals**：三大指標 LCP（載入）、INP（互動）、CLS（視覺穩定），對應關鍵渲染路徑；過多 JS/CSS、慢伺服器、過度 re-render 都會拖垮分數。
- **Code Splitting 與懶載入**：用 Webpack/Vite 依路由切分 JS，只載入當前頁面所需，配合 lazy loading（捲動、點擊、進頁才載）優化 Core Web Vitals。
- **渲染策略**：CSR（白屏問題、不利 SEO）→ 靜態預渲染 / ISG（只重建變動頁面）→ SSR（解決白屏但需 hydration、複雜度高）。作者警告別過度工程化，SSR 像「開 F1 去買菜」，僅在極致效能或 SEO 需求時才用。
- **即時通訊資料層**：Polling（簡單但耗伺服器）、WebSocket（雙向、適合聊天）、Server-Sent Events（單向、適合 LLM 串流回傳 token）。SSE 正是 OpenAI/Claude 等 LLM 應用串流回應的底層機制。

## 關鍵結論／takeaways
- 別只當純前端或純後端，盡快朝「能與 coding agent 協作、跨全端的垂直整合工程師」轉型，這是當前市場的生存關鍵。
- 設計架構時，目標應是「降低驗證時間、縮小變更的爆炸半徑」——微前端 + 微服務能縮小 PR、降低風險，讓 AI 編碼更有效率。
- 前端工程師不需精通 Kubernetes、Load Balancer、Docker，但**必須能在高層次理解它們在架構中的位置**，並能在面試中說明。
- 至少要會在後端「做點事」：懂 API 設計、能擴充微服務、能用 GraphQL 建 BFF，這是大公司前端職位的基本要求。
- 開新專案時，第一件事是先萃取出 design system 餵給 coding agent，才能跨 session 得到一致、可靠的 UI 產出。
- 微前端 + 微服務 + monorepo 是與 AI 協作最有效率的組合，因為能給 agent 完整跨服務 context。
- CDN 是最便宜、最快見效的效能優化；效能問題先從 Core Web Vitals（LCP/INP/CLS）著手診斷。
- 渲染策略以簡單為先，別盲目上 SSR；靜態網站用預渲染/ISG 即可。
- 想做 LLM 串流 UI，用的是 Server-Sent Events，不是 WebSocket 也不是 polling——務必去了解 SSE API。
