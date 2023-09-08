from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

#참고 (몇 개 설치했는데 뭘 했는지 기억 안나서 경고문 나오는 대로 설치)
#pip install selenium  셀레니움 모듈 설치
#pip install --upgrade pip  pip 최신버전 업그레이드
#pip install --upgrade selenium  셀레니움 모듈 최신버전 업그레이드
#pip install webdriver_manager  웹드라이버 매니저 설치

#브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#웹 드라이버 설정
driver = webdriver.Chrome(options = chrome_options)

#웹 페이지 접속
url = "https://www.jobplanet.co.kr/welcome/index"
driver.get(url)

login_page_bth = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/header/div[2]/div/a[1]/span')
login_page_bth.click()

#로그인 (이 계정으로해야 리뷰 보임.)
user_id = "kyjjhh1@g.skku.edu"
user_pw = "42524252comm!"

user_id_input = driver.find_element(By.ID, "user_email")
user_pw_input = driver.find_element(By.ID, "user_password")

user_id_input.send_keys(user_id)
user_pw_input.send_keys(user_pw)

#로그인 버튼 클릭
login_btn = driver.find_element(By.XPATH, '//*[@id="signInSignInCon"]/div[2]/div/section[3]/fieldset/button')
login_btn.click()


#웹 페이지 접속
adv_rev = [] #기업별 장점
dadv_rev = [] #기업별 단점
company_list = []


f = open('C:/Users/Jeonghwan Cho/Desktop/bank_financial_business_company_url.txt', 'r')  #텍스트 파일 이름 알아서 바꿔서 넣기.
data = f.read().splitlines() #url 리스트 정리

for url_m in data:
    url_m = url_m.replace('info', 'reviews')
    adv = []
    dadv = []

    for i in range(1, 1000): #페이지
            
            time.sleep(7)
            url = url_m + f"page={i}&year%5B%5D=2023&year%5B%5D=2022"
            driver.get(url)
 
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            company = soup.find('h1', 'name').text #기업 이름
            
            if i == 1:
                company_list.append(company)

            if "등록된 기업리뷰가 없습니다." in soup.find('p', 'txt').text : #예외처리
                break
            
            review_list = []
            
            rate_list = soup.find_all('dd', 'df1')
            for rev in rate_list:
                review_list.append(rev)

            for j in range(len(rate_list)//3):
                adv.append(review_list[3*j].text)
                dadv.append(review_list[3*j + 1].text)



    #리스트 하나의 문자열로 변환  #기업별 리뷰
    adv = ' '.join(map(str, adv))
    dadv = ' '.join(map(str, dadv))
    adv_rev.append(adv)
    dadv_rev.append(dadv)
    

#csv 파일
df = pd.DataFrame({"company": company_list,
                "pros": adv_rev,
                "cons":dadv_rev})
df = df.set_index("company")
df.to_csv("bank_financial_business_reviews.csv", encoding = 'cp949') #분야별 파일 이름 설정 


#드라이버 종료
driver.close()
