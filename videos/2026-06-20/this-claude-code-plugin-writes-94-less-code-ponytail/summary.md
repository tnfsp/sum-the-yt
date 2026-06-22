# This Claude Code Plugin Writes 94% Less Code (ponytail)

> https://www.youtube.com/watch?v=2xuFcmUAQUc&t=84s

## 一句話總結
Ponytail 是一款 Claude Code 外掛，透過把「YAGNI（你不會需要它）」原則注入 AI 編碼代理，逼它寫出最精簡的解法，實測可省下約 50% 成本並產生更少卻更貼合需求的程式碼。

## 重點摘要
- Ponytail 的核心理念是 YAGNI（You Ain't Gonna Need It），這是源自 1990 年代的軟體工程觀念：在真正需要之前，不要建立抽象層、不要裝套件、不要寫多餘的類別。
- 它給 AI 代理一個「決策階梯」：這東西真的需要存在嗎？標準函式庫能解決嗎？有原生平台功能嗎？已安裝的相依套件能用嗎？能不能寫成一行？只有全部答「否」時，才允許寫新程式碼。
- 經典範例：要做刪除確認的 modal，一般代理會去裝 Radix UI 等套件（30 行＋相依套件），Ponytail 則改用瀏覽器原生的 `<dialog>` 元素，只要 8 行、零相依，並留下註解說明「省略了什麼、為什麼」。
- 官方宣稱可降低 47～77% 成本，且 benchmark 有同時檢查「正確性」，避免為了少寫程式碼而產生壞掉的一行解。
- benchmark 因每次都重送完整規則集而被自我懲罰；實際使用中規則只在每個 session 載入一次並被快取，所以真實省下的成本其實更高。
- 有質疑聲音（Colin Eberhart 的部落格）：只要在系統提示寫「follow YAGNI principles」三個字，效果就幾乎追平 Ponytail；加到七個字甚至超越。作者反駁：Ponytail 的價值在於「打包」——自動跨代理注入規則，還附帶 audit、review、技術債帳本等功能。
- 實測天氣儀表板：Ponytail 版不到 1 分鐘完成、單一 HTML 檔、零相依；預設版花 2 分半、三個檔案、需 Python server，較為過度設計。
- 功能面 Ponytail 反而更好：它確實依指示自動偵測使用者位置，預設版卻只顯示倫敦當預設值。
- 用量證實 Ponytail 版比預設版便宜約 50%、程式碼行數更少。
- 作者另測「Caveman ＋ Ponytail」併用，結果與單用 Ponytail 差異不大，甚至略貴，顯示疊加沒有明顯好處。

## 關鍵結論／takeaways
- 想精簡 AI 產出又省 token，可直接安裝 Ponytail 外掛；它的賣點是「自動化、跨代理地強制套用 YAGNI」，而非單純省字。
- 若不想裝外掛，光在系統提示加上「follow YAGNI principles and one-liner solutions」就能拿到接近的效果，可作為輕量替代方案。
- 別把 Caveman 和 Ponytail 疊加使用——成效幾乎相同甚至更貴，擇一即可，作者偏好 Ponytail。
- 精簡不等於草率：Ponytail 在範例中反而更精準地達成需求（自動定位），印證「很多解法其實被過度設計，少即是多」。
- 真實工作流程中，規則集成本會被整個 session 攤提，所以實際省下的成本通常比 benchmark 數字更高。
