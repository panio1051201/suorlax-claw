# YouGov 自動化專案

## 目標
自動化 YouGov 問卷填寫流程：
1. 登入 YouGov
2. 截圖記錄問題和答案
3. 未來自動填寫問卷

## 帳號
- Email: pandaptc@gmail.com
- 登入網址: https://account.yougov.com/tw-zh/login/email

## 待完成
- [ ] 登入流程測試
- [ ] 擷取驗證碼機制
- [ ] 建立問題/答案資料庫
- [ ] 自動化填寫腳本

## 流程
1. 開啟 YouGov 登入頁面
2. 輸入 Email (pandaptc@gmail.com)
3. 用 Gmail API 讀取驗證碼（或手動輸入）
4. 完成登入
5. 進入問卷，截圖問題和答案
6. 存入資料庫供未來使用