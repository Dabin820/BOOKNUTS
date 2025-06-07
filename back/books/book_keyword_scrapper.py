import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# ✅ 드라이버 생성 함수
def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ✅ ISBN 리스트 불러오기
with open("isbn_list.json", "r", encoding="utf-8") as f:
    raw_isbns = json.load(f)
    isbn_list = [isbn.strip().replace('"', '') for isbn in raw_isbns if isbn.strip()]

results = []

# ✅ 크롤링 시작
for isbn in isbn_list:
    try:
        print(f"📚 크롤링 중: {isbn}")
        driver = init_driver()

        search_url = f"https://search.kyobobook.co.kr/search?keyword={isbn}&gbCode=TOT&target=total"
        driver.get(search_url)

        # 검색 결과 링크 탐색
        try:
            first_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.prod_item a.prod_link"))
            )
        except TimeoutException:
            print(f"⚠️ 검색 결과 없음 (ISBN: {isbn})")
            results.append({"isbn": isbn, "title": None, "keywords": []})
            driver.quit()
            continue

        # 상세 페이지 열기
        first_result.click()
        driver.switch_to.window(driver.window_handles[-1])

        # 제목 가져오기
        try:
            title = driver.find_element(By.CSS_SELECTOR, "meta[property='og:title']").get_attribute("content").strip()
        except:
            title = None

        # 키워드 Pick 가져오기
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_keyword_pick span.tab_text"))
            )
            keyword_els = driver.find_elements(By.CSS_SELECTOR, "div.product_keyword_pick span.tab_text")
            keywords = [el.text.strip() for el in keyword_els]
        except:
            keywords = []

        results.append({
            "isbn": isbn,
            "title": title,
            "keywords": keywords
        })

        driver.quit()

    except WebDriverException as e:
        print(f"❌ WebDriver 에러 (ISBN: {isbn}): {e}")
        try:
            driver.quit()
        except:
            pass
        continue

# ✅ 결과 저장
with open("isbn_keywords.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ 크롤링 완료! isbn_keywords.json 저장됨.")
