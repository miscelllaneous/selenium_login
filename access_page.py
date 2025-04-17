from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import logging
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# ログの設定
logging.basicConfig(
    filename='log.log',
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
        # 指定されたURLにアクセス
        url = "http://10.1.1.1/"
        driver.get(url)
        logging.info(f"URL {url} にアクセスしました")
        
        # ページが読み込まれるのを待つ
        time.sleep(5)
        
        # ユーザー名とパスワードを入力
        username_field = driver.find_element(By.NAME, "USERNAME")
        password_field = driver.find_element(By.NAME, "PASSWORD")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        logging.info("認証情報を入力しました")
        
        # ログインボタンをクリック
        login_button = driver.find_element(By.NAME, "ACTION")
        login_button.click()
        logging.info("ログインボタンをクリックしました")
        
        # ログイン後のページが読み込まれるのを待つ
        time.sleep(5)
        logging.info("ログインに成功しました")
        return driver
        
    except Exception as e:
        logging.error(f"ログイン中にエラーが発生しました: {e}")
        return None

def logout(driver):
    try:
        logging.info("ログアウト処理を開始します")
        # 指定されたURLにアクセス
        url = "http://10.1.1.1/"
        driver.get(url)
        logging.info(f"URL {url} にアクセスしました")
        
        # ページが読み込まれるのを待つ
        time.sleep(5)
        # ログアウトボタンをクリック
        logout_button = driver.find_element(By.CSS_SELECTOR, "input[name='ACTION'][value='logout']")
        logout_button.click()
        logging.info("ログアウトボタンをクリックしました")
        
        # ログアウト後のページが読み込まれるのを待つ
        time.sleep(5)
        
        logging.info("ログアウトが完了しました")
        
    except Exception as e:
        logging.error(f"ログアウト中にエラーが発生しました: {e}")
    
    finally:
        # ブラウザを閉じる
        if driver:
            driver.quit()
            logging.info("ドライバーを解放しました")

if __name__ == "__main__":
    # 環境変数からユーザー名とパスワードを取得
    logging.info("プログラムを開始します")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    # ドライバーを作成してログイン
    driver = create_driver()
    logout(driver)
    driver = create_driver()
    login(driver, username, password)
    logging.info("プログラムを終了します")
