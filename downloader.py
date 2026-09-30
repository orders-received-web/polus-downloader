import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # 1. GASから送られてきたURL（公開アドレス）を取得
    if len(sys.argv) < 2:
        print("エラー: URLが指定されていません。")
        return
    target_url = sys.argv[1]
    
    print(f"処理を開始します。対象URL: {target_url}")

    # 2. 画面を表示させずにブラウザを動かす設定（バックグラウンド処理）
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 3. 最初の公開アドレス（URL）にアクセス
        driver.get(target_url)
        time.sleep(3) # 画面が読み込まれるまで少し待つ
        
        # 4. メールアドレスを入力する欄を探して自動入力
        # ※Proselfの一般的な仕様に基づき、input要素を探します
        # 実際の画面構成に合わせて後ほど微調整する可能性があります
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        email_input.clear()
        email_input.send_keys("orders-received@okada-hd.co.jp")
        print("メールアドレスを入力しました。")

        # 5. 「パスワードを取得」ボタンをクリック
        # ※「パスワードを取得」という文字が含まれるボタンを探してクリックします
        buttons = driver.find_elements(By.TAG_NAME, "button")
        submit_button = None
        for btn in buttons:
            if "パスワード" in btn.text or "取得" in btn.text:
                submit_button = btn
                break
        
        if not submit_button:
            # input要素のボタン（submitタイプ）も探す
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                if inp.get_attribute("type") == "submit" or "取得" in inp.get_attribute("value"):
                    submit_button = inp
                    break

        if submit_button:
            submit_button.click()
            print("「パスワードを取得」ボタンをクリックしました。ワンタイムパスワードのを発行中...")
            time.sleep(5) # 発行処理を待つ
        else:
            print("エラー: パスワード取得ボタンが見つかりませんでした。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
