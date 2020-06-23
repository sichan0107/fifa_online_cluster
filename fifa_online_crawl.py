### 피파 온라인 데이터 센터 크롤링
### 2019년 UEFA 출전 선수들의 스탯(능력치) 정보를 크롤링
### 이후 각 능력치별로 클러스터링 후 
### 능력치 별 적합 포지션을 군집화 시켜 알아본다.

# 선수 능력치는 다음과 같다.
# 스피드 / 슛 / 패스 / 드리블 / 수비 / 피지컬

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from pandas import DataFrame

url = "http://fifaonline4.nexon.com/datacenter/index?n1Confederation=0&n4LeagueId=0&strSeason=%2C221%2C&strPosition=&strPhysical=&n1LeftFootAblity=0&n1RightFootAblity=0&n1SkillMove=0&n1InterationalRep=0&n4BirthMonth=0&n4BirthDay=0&n4TeamId=0&n4NationId=0&strAbility1=&strAbility2=&strAbility3=&strTrait1=&strTrait2=&strTrait3=&strTraitNon1=&strTraitNon2=&strTraitNon3=&n1Strong=1&n1Grow=0&strSkill1=sprintspeed&strSkill2=acceleration&strSkill3=strength&strSkill4=stamina&strSearchStatus=off&strOrderby=&teamcolorid=0&strTeamColorCategory=&n1History=0&strPlayerName=&strTeamName=&strNationName=&n4OvrMin=0&n4OvrMax=150&n4SalaryMin=4&n4SalaryMax=34&n8PlayerGrade1Min=0&n8PlayerGrade1Max=1000&n1Ability1Min=40&n1Ability1Max=150&n1Ability2Min=40&n1Ability2Max=150&n1Ability3Min=40&n1Ability3Max=150&n4BirthYearMin=1900&n4BirthYearMax=2010&n4HeightMin=156&n4HeightMax=208&n4WeightMin=50&n4WeightMax=110&n4AvgPointMin=0&n4AvgPointMax=10"

def start_crawl(url):
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
    driver.implicitly_wait(2)
    driver.get(url)
    info = driver.find_element_by_class_name("tr")
    ref = driver.find_element_by_class_name("player_info")
    but = driver.find_element_by_class_name("btn_detail_link")
    action = webdriver.ActionChains(driver).move_to_element(info).click(ref).click(but)
    action.perform()
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    player_name = driver.find_elements_by_class_name("name")
    print(player_name[0].text)
    stats = driver.find_element_by_css_selector("div.content_middle").find_elements_by_class_name("ab")
    for stat in  stats: 
        print("스탯정보 : " + stat.find_element_by_class_name("value").text)
    # #middle > div > div > div:nth-child(2) > div.content.data_detail > div > div.content_middle > ul > li:nth-child(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    #time.sleep(3)
    
    print(driver.window_handles)
    #driver.close()
    print("왜 닫히고 지랄이지")

def start_crawl2(url):
    all_player = []
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(2)
    player_list = driver.find_elements_by_class_name("tr")
    for i in range(0, len(player_list)) :
        driver.implicitly_wait(3)
        player_info = driver.find_elements_by_class_name("player_info")[i]
        detail_button = driver.find_elements_by_class_name("btn_detail_link")[i]
        actions = webdriver.ActionChains(driver).move_to_element(player_info).click(detail_button)
        actions.perform()
        actions.reset_actions()
        info = get_player_name_stats(driver)
        print(info)
        all_player.append(info)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    print("----------첫번째 선수 ---------")
    print(all_player[0])
    print("----------두번째 선수 ---------")
    print(all_player[1])
    print("----------세번째 선수 ---------")
    print(all_player[2])
    print("----------네번째 선수 ---------")
    print(all_player[3])


    return all_player

def get_player_name_stats(driver):
    player_info_list = []
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    player_name = driver.find_element_by_class_name("name")
    player_info_list.append(player_name.text)
    stats = driver.find_element_by_css_selector("div.content_middle").find_elements_by_class_name("ab")
    for stat in  stats:
        player_info_list.append(stat.find_element_by_class_name("value").text) 
    #print(player_info_list)
    return player_info_list

def get_data(html):
    page = BeautifulSoup(html, "html.parser")
    divs = page.find_all("div")
    print(divs)




def make_dataFrame(data):
    players_info = pd.DataFrame(data, columns=['name','prefer_position','speed', 'shoot', 'pass', 'dribble', 'defense', 'physical'])
    return players_info

start_crawl2(url)

