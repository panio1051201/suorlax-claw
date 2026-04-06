"""
YouGov 自動化登入腳本
功能：
1. 開啟 YouGov 登入頁面
2. 輸入帳號密碼
3. 截圖記錄畫面
4. 讀取 Gmail 驗證碼
"""

from playwright.sync_api import sync_playwright
import time
import os

# 設定
EMAIL = "pandaptc@gmail.com"
LOGIN_URL = "https://account.yougov.com/tw-zh/login/email"
SCREENSHOT_DIR = "yougov_screenshots"

def setup():
    """建立截圖資料夾"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

def login_yougov():
    """執行 YouGov 登入流程"""
    setup()
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)  # 顯示瀏覽器視窗
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        try:
            # 1. 開啟登入頁面
            print("1. 開啟 YouGov 登入頁面...")
            page.goto(LOGIN_URL)
            page.wait_for_timeout(3000)  # 等待3秒
            page.screenshot(path=f"{SCREENSHOT_DIR}/01_login_page.png")
            print(f"   已截圖: {SCREENSHOT_DIR}/01_login_page.png")
            
            # 2. 輸入 Email
            print("2. 輸入 Email...")
            email_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]')
            if email_input.count() > 0:
                email_input.first.fill(EMAIL)
                page.screenshot(path=f"{SCREENSHOT_DIR}/02_email_filled.png")
                print(f"   已輸入: {EMAIL}")
            else:
                print("   找不到 Email 輸入框，請手動截圖確認")
            
            # 3. 點擊登入按鈕
            print("3. 點擊登入...")
            submit_btn = page.locator('button[type="submit"], button:has-text("登入" i), button:has-text("Sign" i)')
            if submit_btn.count() > 0:
                submit_btn.first.click()
                page.wait_for_timeout(5000)  # 等待驗證碼發送
                page.screenshot(path=f"{SCREENSHOT_DIR}/03_after_submit.png")
                print("   已點擊，等待驗證碼...")
            else:
                print("   找不到登入按鈕")
            
            # 4. 提示用戶手動輸入驗證碼
            print("\n" + "="*50)
            print("請手動輸入驗證碼到瀏覽器視窗")
            print("="*50)
            
            # 等待用戶手動完成驗證（最多60秒）
            page.wait_for_timeout(60)
            
            # 5. 截圖最終狀態
            page.screenshot(path=f"{SCREENSHOT_DIR}/04_final_state.png")
            print(f"   已截圖最終狀態")
            
            # 6. 進入問卷頁面測試
            print("\n6. 測試進入問卷...")
            page.goto("https://yougov.com/tw-zh/surveys")
            page.wait_for_timeout(3000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/05_survey_page.png")
            print("   已截圖問卷頁面")
            
            print("\n✅ 流程完成！截圖已保存到:", SCREENSHOT_DIR)
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    login_yougov()
