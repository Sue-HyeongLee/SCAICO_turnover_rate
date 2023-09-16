from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

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

#로그인
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
review_list = []
adv = [] #장점
dadv = [] #단점

for i in range(1,2000):
    try:
        time.sleep(5)
        url = f"https://www.jobplanet.co.kr/companies/30139/reviews/삼성전자?page={i}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        company = soup.find('h1', 'name').text

        rate_list = soup.find_all('dd', 'df1')


        for rev in rate_list:
            review_list.append(rev)

        for i in range(len(rate_list)//3):
            adv.append(review_list[3*i].text)
            dadv.append(review_list[3*i + 1].text)
    except:
        pass



#리스트 하나의 문자열로 변환
adv = ' '.join(map(str, adv))
dadv = ' '.join(map(str, dadv))

File = open("기업 리뷰_장점.txt", "w")
File.write(company)
File.write(adv)
File.close()

File = open("기업 리뷰_단점.txt", "w")
File.write(company)
File.write(adv)
File.close()


#드라이버 종
driver.close()
