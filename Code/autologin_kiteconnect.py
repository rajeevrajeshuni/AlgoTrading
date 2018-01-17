from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect,KiteTicker
#from metaData import getApiKey,getApiSecret
from datetime import datetime
import time
import keys
import pickle

def create_access_token():
    options = webdriver.FirefoxOptions()
    options.set_headless(headless=True)
    # TODO Add error handling here. Webdriver might fail if firefox is updating.
    profile = webdriver.FirefoxProfile()
    profile.set_preference('app.update.auto', False)
    profile.set_preference('app.update.enabled', False)
    while True:
        try:
            driver = webdriver.Firefox(firefox_options=options,firefox_profile=profile)
            break
        except Exception as e:
            time.sleep(5)

    api_key = keys.getApiKey()
    print(api_key)
    app_login_url = 'https://kite.trade/connect/login?api_key=' + api_key + '&v=3'
    print(app_login_url)
    driver.get(app_login_url)
    time.sleep(5)

    inputs = driver.find_elements_by_tag_name("input")
    username = inputs[0]
    password = inputs[1]
    username.send_keys("YZ0647")
    password.send_keys("Wallstreet1")
    button = driver.find_elements_by_tag_name("button")
    #driver.save_screenshot('/Users/Rajeev/AlgoTrading/screen1.png')

    button[0].click()

    time.sleep(5)
    dictionary={
            'Which floor of the building do you live on?': 'yash',
            'Which fruit do you hate the most? ( e.g. Apple, Mango,.. etc)': 'yash',
            'What is your grandfather\'s name?':'yash',
            'What is the last name of your family Doctor? (e.g. Rathi, Khurana, etc.)':'yash',
            'What is your mother\'s name?':'yash'
            }

    inputs = driver.find_elements_by_tag_name("input")
    input_labels = driver.find_elements_by_class_name("su-input-label")
    #print(input_labels[0].text)

    #Answer to question 1
    ans1=dictionary[input_labels[0].text]
    inputs[0].send_keys(ans1)

    #Answer to question 2
    ans2=dictionary[input_labels[1].text]
    inputs[1].send_keys(ans2)

    #driver.save_screenshot('/Users/Rajeev/AlgoTrading/screen2.png')

    button = driver.find_elements_by_tag_name("button")
    button[0].click()

    time.sleep(5)
    #driver.save_screenshot('/Users/Rajeev/AlgoTrading/screen3.png')
    url=driver.current_url
    parse_url = urlparse(url)
    query = parse_qs(parse_url.query)
    #print(query)
    request_token=query['request_token'][0]
    api_key=keys.getApiKey()
    api_secret=keys.getApiSecret()
    kite=KiteConnect(api_key=api_key)

    data = kite.generate_session(request_token, api_secret)

    root_path = keys.getRootPath()
    token_file_path = root_path + 'AlgoTrading/Code/Secure/access_token.pickle'
    #access_token_file = open('Secure/access_token.pickle','wb')
    access_token_file = open(token_file_path,'wb')
    pickle.dump(datetime.now(),access_token_file)
    pickle.dump(data['access_token'],access_token_file)
    access_token_file.close()
    driver.quit()
    return data['access_token']
