# pylama:ignore=E501

from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver_location = "./chromedriver.exe"

games = [
    'Apex Legends',
    'Goose Goose Duck'
]


checkdelay = 150


print('starting')

options = Options()
options.add_argument(
    '--user-data-dir=chrome-profile/')
options.add_argument('--mute-audio')

options_headless = options  # idk doesnt work for some REASON


def xpath(wait, path):
    return wait.until(
        EC.presence_of_element_located((By.XPATH, path)))


def checkprogress(driv, returnurl):
    driv.get('https://www.twitch.tv/drops/inventory')
    hsh = hash(driv.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div/div/div[2]').get_attribute('innerHTML'))
    driv.get(returnurl)
    return hsh


# -------- testing login and first time setup -------------
print('testing login')
logintest = webdriver.Chrome(
    executable_path=driver_location, options=options_headless)
try:
    logintestwait = WebDriverWait(logintest, 2)
    logintest.get('https://www.twitch.tv/drops/campaigns/')
    xpath(
        logintestwait,
        '//*[@id="root"]/div/div[2]/div[2]/main/div[2]/div[3]/div/div/div/div/div[2]/p')
    # user not logged in at this point
    print('first time setup. browser window will pop up. please complete the signin')
    logintest.quit()
    login = webdriver.Chrome(executable_path=driver_location, options=options)
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

driver = webdriver.Chrome(
    executable_path=driver_location, options=options_headless)
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


print('retrieving watchlist..')
watchlist = []
for x in els:
    gamename = x.find_element_by_xpath(
        './div/button/div/div[2]/div/h3').get_attribute('title')
    if gamename not in games:
        continue
    for y in x.find_elements_by_xpath('./div/div/div')[:-1]:
        itemnames = [el.text for el in y.find_elements_by_xpath(
            './div/div/div/div/div/div/div/div/div/div/p')]
        watchlist.append((gamename, itemnames, y.find_element_by_xpath(
            './div/div/div/div/div/ul/li/a[@target="_blank"]').get_attribute('href')))
print(watchlist)


# --------------- watch the channels ------------------


print('leaning back and watching some streams. where my popcorn at?!')

while len(watchlist) > 0:
    entry = watchlist.pop()
    driver.get(entry[2])
    xpath(driverwait, '//*[contains(@data-a-target, "form-tag-Drops")]')
    print(f'starting watching {driver[2]}')
    starttime = time.time()
    try:
        streamerurl = driver.find_element_by_xpath(
            '//*[contains(@data-a-target, "preview-card-title-link")]').get_attribute('href')
    except NoSuchElementException:
        print(f'no streamer online for: {entry[0]} - {[e for e in entry[1]]}')
        continue
    driver.get(streamerurl)
    sleep(checkdelay)
    oldhash = None
    exitflag = True
    while exitflag:
        newhash = checkprogress(driver, checkdelay)
        if newhash == oldhash:
            exitflag = False
        oldhash = newhash
        sleep(checkdelay)
    print(f'finished watching {driver[2]} in {time.time() - starttime} time.')


driver.quit()
