from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
import time

# 웹드라이버 설정
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.implicitly_wait(10) # 최대 10초 동안 요소를 찾기 위해 대기

# 네이버 접속 및 검색
driver.get("http://naver.com")
driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/div/div[3]/div/div/form/fieldset/div/input').send_keys("유시민 작가 인터뷰")
driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/div/div[3]/div/div/form/fieldset/button').click()
time.sleep(5)

# 블로그 탭 클릭
driver.find_element(By.XPATH,r'/html/body/div[3]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a').click()
time.sleep(5)

# 블로그 링크 수집 및 내용 추출
blog_links = driver.find_elements(By.XPATH, "//a[@class='title_link']")[:5]

# 텍스트 파일 생성
with open("유시민_작가_인터뷰.txt", "w", encoding="utf-8") as file:
    for i, link in enumerate(blog_links,1):
        blog_url = link.get_attribute('href')
        driver.get(blog_url)
        time.sleep(2)

        # iframe 전환
        driver.switch_to.frame('mainFrame')

        # 제목 추출
        title = driver.find_element(By.XPATH, "//div[contains(@class, 'se-module se-module-text se-title-text')]").text

        # 본문 추출
        content = driver.find_element(By.XPATH, "//div[@class='se-main-container']").text

        # 파일에 내용 쓰기
        file.write(f"===== 블로그 포스트 {i} =====\n")
        file.write(f"제목: {title}\n\n")
        file.write(f"내용:\n{content}\n\n")
        file.write("="*30 + "\n\n")

        driver.switch_to.default_content()

# 브라우저 종료
driver.quit()

print('PDF 파일이 생성되었습니다')