# 09 - 27 Su-Hyeong Lee

import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pyautogui # 이건 자동으로 엔터를 쳐줄 것임.
from selenium.common.exceptions import NoSuchElementException  # 에러 발생할 때 대비시키기 위해.

result_o = open("error.txt", "r", encoding = 'utf-8')
company_name_list = []
for i in result_o:
  company_name_list.append(i)

for j in range(len(company_name_list)):
    if '\n' in company_name_list[j]:
        company_name_list[j] = company_name_list[j][:-1]

chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options = chrome_options)
average_salary_list = [] # 평균 연봉.
total_sale_list = [] # 총 매출액.
for company_name in company_name_list: # company_name 뽑기.
  driver.get(url="https://insight.wanted.co.kr/")
  time.sleep(5) # 페이지 렌더링 되는 시간 줄거임.

  driver.find_element(By.CSS_SELECTOR, '#__next > div:nth-child(1) > main > div > div > div.sc-a1c834fc-2.jjVsPe > button').click() # 클릭할 것임.
  time.sleep(5)
  
  driver.find_element(By.CSS_SELECTOR, '#__next > div.sc-fd88cdc9-0.koKcEa > div > div > form > div > div > input').send_keys(company_name) # company_name 검색.
  time.sleep(5)
    

  try: # 검색 결과가 있다면
    driver.find_element(By.CSS_SELECTOR,'#__next > div.sc-fd88cdc9-0.koKcEa > div > div > form > div.sc-572e6719-0.bGoNnq > ul > li > a').click() # 맨 위의 검색 결과를 클릭.
    time.sleep(10)
    company = driver.find_element(By.CSS_SELECTOR, "#__next > div > main > section > section > div.sc-f57504e-4.cTZuoU > div > div.sc-2815c9a5-0.esIFkh > div.sc-2815c9a5-3.bEDlck > h1").text # 클릭 후, 회사 이름을 가져올 것임.
    
    if company_name != company: # 만약 클릭은 했지만 찾으려는 회사 이름과 맨 위의 검색 결과 회사 이름이 같지 않다면,
        average_salary_list.append('회사없음1')
        total_sale_list.append('회사없음1')
        print('선택된 기업이 wanted sight에 없습니다.', company_name) # 우리는 선택된 기업이 없음으로 판단할 것임.
        continue
    
    try:
        average_salary = driver.find_element(By.CSS_SELECTOR, '#summary > div.sc-b1bcd09b-2.iFdoBk > div > div:nth-child(2) > div.sc-f33d0827-14.boPJph > div.sc-f33d0827-12.isyksU > span').text
        total_sale = driver.find_element(By.CSS_SELECTOR, '#summary > div.sc-b1bcd09b-2.iFdoBk > div > div:nth-child(4) > div.sc-f33d0827-14.boPJph > div.sc-f33d0827-12.isyksU > span').text
        average_salary_list.append(average_salary)
        total_sale_list.append(total_sale)
        print('wanted insight에 있습니다.', company_name)
        
    except NoSuchElementException: 
      average_salary_list.append('회사없음')
      total_sale_list.append('회사없음')
      print('선택된 기업이 wanted sight에 없습니다.', company_name)        
  except NoSuchElementException:
    average_salary_list.append('회사없음')
    total_sale_list.append('회사없음')
    print('선택된 기업이 wanted sight에 없습니다.', company_name) 
df = pd.DataFrame({"company_name": company_name_list, "average_salary": average_salary_list, "total_sale" : total_sale_list})
df.to_csv("./output/media_design_financial_variable.csv", encoding= 'utf-8-sig') # utf-8로 할 경우, 파일이 깨짐.
print("종료되었습니다.")