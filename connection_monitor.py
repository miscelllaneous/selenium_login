from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

# ログの設定
log_handler = RotatingFileHandler(
    'connection_monitor.log',
    maxBytes=2*1024*1024,  # 2MB
    backupCount=5
)
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def create_driver():
    logging.info("ドライバーの作成を開始します")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logging.info("ドライバーの作成が完了しました")
    return driver

def login(driver, username, password):
    try:
        logging.info("ログイン処理を開始します")
        url = "http://10.1.1.1/"
        driver.get(url)
        logging.info(f"URL {url} にアクセスしました")
        
        time.sleep(5)
        
        username_field = driver.find_element(By.NAME, "USERNAME")
        password_field = driver.find_element(By.NAME, "PASSWORD")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        logging.info("認証情報を入力しました")
        
        login_button = driver.find_element(By.NAME, "ACTION")
        login_button.click()
        logging.info("ログインボタンをクリックしました")
        
        time.sleep(5)
        logging.info("ログインに成功しました")
        return True
        
    except Exception as e:
        logging.error(f"ログイン中にエラーが発生しました: {e}")
        return False

def check_connection():
    try:
        response = requests.get("https://www.google.com", timeout=10)
        logging.info(f"Googleへの接続テスト: {response.status_code}")
        return response.status_code == 200
    except:
        return False

def main():
    logging.info("接続監視プログラムを開始します")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    while True:
        if not check_connection():
            logging.warning("インターネット接続が切断されました")
            retry_count = 0
            max_retries = 10
            
            while retry_count < max_retries:
                driver = create_driver()
                if login(driver, username, password):
                    logging.info("接続が回復しました")
                    driver.quit()
                    break
                else:
                    retry_count += 1
                    logging.warning(f"ログインに失敗しました。リトライ {retry_count}/{max_retries}")
                    driver.quit()
                    time.sleep(180)  # 3分待機
                    
            if retry_count >= max_retries:
                logging.error("最大リトライ回数を超えました")
        
        time.sleep(60)  # 1分待機

if __name__ == "__main__":
    main() 
