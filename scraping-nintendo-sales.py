from bs4 import BeautifulSoup
from selenium import webdriver

def percentile(ori_price,sale_price):
    return (1-(sale_price/ori_price))*100

sale_url = 'https://www.nintendo.com/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals'

driver = webdriver.Chrome()
driver.get(sale_url)

res = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = BeautifulSoup(res, 'html.parser')
game_list = soup.find_all('ul',{'class':'game-list-results-container'})

filename = 'table.csv'
f = open(filename,'w')

header = 'Title, release_date, sale_price, ori_price, off %'

f.write(header+ '\n')

for ul in game_list:
    for li in ul.find_all('li'):
        game_title = li.find('h3').text
        game_release_date = li.find('p',{'class':'row-date'}).text
        game_sale_price = li.find('strong',{'class':'sale-price'}).text
        game_ori_price = li.find('s',{'class':'strike'}).text
        game_discount = percentile(float(game_ori_price.replace('$','')),float(game_sale_price.replace('$','')))
        f.write(game_title + ',' + game_release_date.replace(',','') + ',' + game_sale_price + ',' + game_ori_price + ',' + str(game_discount) + '\n')

f.close()