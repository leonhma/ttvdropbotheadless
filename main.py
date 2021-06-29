# pylama:ignore=E501

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException


games = [
    'Apex Legends',
    'Goose Goose Duck'
]

print('starting')


options_headless = Options()  # idk doesnt work for some REASON
options_headless.add_argument(
    '--user-data-dir=chrome-profile/')
options = Options()
options.add_argument(
    '--user-data-dir=chrome-profile/')


def xpath(wait, path):
    return wait.until(
        EC.presence_of_element_located((By.XPATH, path)))


# -------- testing login and first time setup -------------
print('testing login')
try:
    logintest = webdriver.Chrome(options=options_headless)
    logintestwait = WebDriverWait(logintest, 2)
    logintest.get('https://www.twitch.tv/drops/campaigns/')
    xpath(
        logintestwait,
        '//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p')
    # user not logged in at this point
    print('first time setup. browser window will pop up. please complete the signin')
    logintest.quit()
    login = webdriver.Chrome(options=options)
    loginwait = WebDriverWait(login, 10)
    login.get('https://www.twitch.tv/')
    xpath(loginwait,
          '//*[@id="root"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button').click()
    while True:
        try:
            login.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/nav/div/div[3]/div[6]/div/div/div/div/button/div/figure')
            break
        except NoSuchElementException:
            pass
        sleep(1)
    login.quit()
except TimeoutException:
    pass
finally:
    logintest.quit()

# -------- setting up WebDriver for bot use ---------
print('gathering data..')

driver = webdriver.Chrome(options=options_headless)
driverwait = WebDriverWait(driver, 10)

""" # --------------- inventory check ------------------
print('inventory:')

driver.get('https://twitch.tv/drops/inventory/')

inv_name = driverwait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH,
         '//p[@data-test-selector="awarded-drop__drop-name"]')))

inv_game = driverwait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH,
         '//p[@data-test-selector="awarded-drop__game-name"]')))

inv = []
for i, name in enumerate(inv_name):
    inv.insert(i, (inv_name[i].text, inv_game[i].text))
print(inv) """

# --------------- scraping 'todo' list -------------
print('selected campaigns:')

driver.get('https://www.twitch.tv/drops/campaigns/')
sleep(2)
xpath(
    driverwait,
    '//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[4]/div[1]/div/button/div/div[2]/div/h3')
i = 0
els = []
while True:
    try:
        el = driver.find_element_by_xpath(
            f'//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div[4]/div[{i+1}]')
        sleep(0.1)
    except NoSuchElementException:
        break
    els.insert(i, el)
    i += 1

""" print([el.find_element_by_xpath(
    './div/button/div/div[2]/div/h3').get_attribute('title') if el.find_element_by_xpath(
    './div/button/div/div[2]/div/h3').get_attribute('title') in games else '' for el in els]) """

print('retrieving watchlist..')
watchlist = []
for x in els:
    if x.find_element_by_xpath(
            './div/button/div/div[2]/div/h3').get_attribute('title') not in games:
        continue
    print(x.find_element_by_xpath(
        './div/button/div/div[2]/div/h3').get_attribute('title'))
    for y in x.find_elements_by_xpath('./div/div/div'):
        watchlist.append(y.find_element_by_xpath(
            './div/div/div/div/div/ul/li/a[@target="_blank"]').href)


driver.quit()
