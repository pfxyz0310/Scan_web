from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PyPDF2 import PdfMerger
from PIL import Image
import time
import os
import re
import sys

# ================= 設定區 =================
# 翻頁後的等待秒數
WAIT_TIME = 2.5 
# ==========================================

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def init_driver():
    print("正在嘗試連接已開啟的 Chrome (Port 9222)...")
    options = webdriver.ChromeOptions()
    # 這一行是關鍵：告訴 Selenium 不要開新視窗，而是去連這個位址
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ 成功連接到 Chrome！")
        return driver
    except Exception as e:
        print("\n❌ 連接失敗！")
        print("請確認你是否已經執行了 start_chrome.bat？")
        print(f"錯誤訊息: {e}")
        sys.exit()

def prepare_book(driver):
    """
    確認使用者已經準備好
    """
    print("==================================================")
    print("【模式】接管已開啟的瀏覽器")
    print("請確認：")
    print("1. 你已經在 Chrome 中開啟了電子書")
    print("2. 目前停留在「第一頁」")
    print("3. 請點擊一下電子書畫面中央 (確保鍵盤焦點在書上)")
    print("==================================================")
    
    # 自動切換到最新分頁 (通常是閱讀器)
    try:
        handles = driver.window_handles
        if len(handles) > 0:
            driver.switch_to.window(handles[-1])
            print(f"已鎖定分頁：{driver.title}")
    except:
        pass

    try:
        input(">>> 準備好後，請按下 [Enter] 鍵開始截圖...")
    except KeyboardInterrupt:
        sys.exit()

def capture_pages(driver):
    pdf_directory = 'pdf'
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
    
    # 清空舊檔
    for f in os.listdir(pdf_directory):
        try: os.remove(os.path.join(pdf_directory, f))
        except: pass

    try:
        total_pages = int(input(">>> 請輸入總頁數 (例如 200): "))
    except ValueError:
        total_pages = 10

    print(f"\n開始截圖 (共 {total_pages} 頁)...")

    for i in range(1, total_pages + 1):
        filename = f"{pdf_directory}/{i}.png"
        pdf_filename = f"{pdf_directory}/{i}.pdf"
        
        # 1. 截圖
        try:
            driver.save_screenshot(filename)
        except Exception as e:
            if "window already closed" in str(e):
                print("錯誤：視窗已關閉")
                return
            print(f"Page {i} 截圖失敗，重試中...")
            time.sleep(1)
            try:
                driver.find_element(By.TAG_NAME, 'body').screenshot(filename)
            except:
                print("略過此頁")
                continue

        # 2. 轉檔
        try:
            img = Image.open(filename)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(pdf_filename, 'PDF')
            img.close()
            os.remove(filename)
            print(f"Page {i} saved.")
        except:
            pass

        if i == total_pages:
            break

        # 3. 翻頁
        try:
            # 使用鍵盤右方向鍵
            ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
            time.sleep(WAIT_TIME)
        except Exception as e:
            print(f"翻頁失敗: {e}")
            try:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
                time.sleep(WAIT_TIME)
            except:
                pass

    print("截圖結束")

def merge_pdf_file():
    print("合併 PDF...")
    pdf_merger = PdfMerger()
    if not os.path.exists('pdf'): return
    
    files = sorted([f for f in os.listdir('pdf') if f.endswith('.pdf')], key=natural_sort_key)
    if not files: return
    
    for f in files:
        pdf_merger.append(os.path.join('pdf', f))
    
    with open('result.pdf', 'wb') as output:
        pdf_merger.write(output)
    print("✅ 完成！檔案為 result.pdf")

if __name__ == '__main__':
    driver = init_driver()
    try:
        prepare_book(driver)
        capture_pages(driver)
    finally:
        # 這裡不執行 quit()，以免把使用者還在看的視窗關掉
        print("程式結束。")
    
    merge_pdf_file()