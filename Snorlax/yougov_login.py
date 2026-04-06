"""
YouGov 自動化登入腳本 v2
功能：
1. 開啟 YouGov 登入頁面
2. 輸入帳號密碼
3. 截圖記錄畫面
4. 彈窗通知用戶輸入驗證碼
"""

from playwright.sync_api import sync_playwright
import time
import os
import subprocess

# 設定
EMAIL = "pandaptc@gmail.com"
LOGIN_URL = "https://account.yougov.com/tw-zh/login/email"
SCREENSHOT_DIR = "yougov_screenshots"

def notify(message):
    """發送 Windows 通知"""
    script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show("{message}", "YouGov 自動化")
    '''
    subprocess.run(["powershell", "-Command", script], capture_output=True)

def setup():
    """建立截圖資料夾"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    # 清理舊截圖
    for f in os.listdir(SCREENSHOT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(SCREENSHOT_DIR, f))

def login_yougov():
    """執行 YouGov 登入流程"""
    setup()
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        try:
            # 1. 開啟登入頁面
            print("1. 開啟 YouGov 登入頁面...")
            page.goto(LOGIN_URL)
            page.wait_for_timeout(3000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/01_login_page.png")
            print(f"   已截圖: {SCREENSHOT_DIR}/01_login_page.png")
            
            # 2. 輸入 Email
            print("2. 輸入 Email...")
            # 嘗試多種選擇器
            selectors = [
                'input[type="email"]',
                'input[name="email"]',
                'input[placeholder*="email" i]',
                'input[id*="email"]',
                '#email'
            ]
            email_filled = False
            for selector in selectors:
                try:
                    email_input = page.locator(selector).first
                    if email_input.count() > 0:
                        email_input.fill(EMAIL)
                        page.screenshot(path=f"{SCREENSHOT_DIR}/02_email_filled.png")
                        print(f"   已輸入: {EMAIL}")
                        email_filled = True
                        break
                except:
                    continue
            
            if not email_filled:
                print("   找不到 Email 輸入框，請手動輸入")
            
            # 3. 點擊登入按鈕
            print("3. 點擊登入...")
            submit_selectors = [
                'button[type="submit"]',
                'button:has-text("登入")',
                'button:has-text("Sign in")',
                'input[type="submit"]'
            ]
            for selector in submit_selectors:
                try:
                    submit_btn = page.locator(selector).first
                    if submit_btn.count() > 0:
                        submit_btn.click()
                        print("   已點擊登入")
                        break
                except:
                    continue
            
            page.wait_for_timeout(5000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/03_after_submit.png")
            
            # 4. 通知用戶輸入驗證碼
            print("\n" + "="*50)
            print("請輸入驗證碼到瀏覽器視窗")
            print("="*50)
            notify("⚠️ 請在瀏覽器中輸入驗證碼，然後點擊確認\n完成後腳本會自動繼續...")
            
            # 等待用戶按 Enter鍵 後繼續
            input("\n✅ 輸入驗證碼並完成驗證後，按 Enter 鍵繼續...\n")
            
            # 5. 截圖最終狀態
            page.screenshot(path=f"{SCREENSHOT_DIR}/04_final_state.png")
            print("   已截圖最終狀態")
            
            # 6. 進入問卷頁面
            print("\n6. 進入問卷頁面...")
            page.goto("https://yougov.com/tw-zh/surveys")
            page.wait_for_timeout(3000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/05_survey_page.png")
            print("   已截圖問卷頁面")
            
            # 7. 嘗試截圖更多問卷題目
            print("\n7. 嘗試截圖問卷內容...")
            page.goto("https://yougov.com/tw-zh")
            page.wait_for_timeout(3000)
            page.screenshot(path=f"{SCREENSHOT_DIR}/06_homepage.png")
            
            print("\n✅ 完成！截圖已保存到:", SCREENSHOT_DIR)
            print("請上傳截圖資料夾到 Telegram，我幫你分析")
            notify("✅ 完成！截圖已保存，請上傳到 Telegram")
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            page.screenshot(path=f"{SCREENSHOT_DIR}/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    login_yougov()
