from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

def place_orders():
    driver = webdriver.Firefox()
    driver.get("https://kite.zerodha.com/")
    time.sleep(5)

    inputs = driver.find_elements_by_tag_name("input")
    username = inputs[0]
    password = inputs[1]
    username.send_keys("ZP9970")
    password.send_keys("#PIKU747*")
    button = driver.find_elements_by_tag_name("button")
    button[0].click()

    time.sleep(5)
    dictionary={
            'What was your major during college? (e.g. Finance, IT, etc)':'Computer Science',
            'How many floors does your building have? (e.g. Five, Eleven, etc)':'2',
            'What is your shoe size? ( e.g. 5, 7 etc)':'10',
            'Name the previous company you worked for? ( e.g. TCS, Infosys, etc)':'Synopsys',
            'What is the first name of your grandmother? (e.g. Saraswati, Lata etc.)':'Lakshmi'
            }

    inputs = driver.find_elements_by_tag_name("input")
    input_labels = driver.find_elements_by_class_name("su-input-label")

    #Answer to question 1
    ans1=dictionary[input_labels[0].text]
    inputs[0].send_keys(ans1)

    #Answer to question 2
    ans2=dictionary[input_labels[1].text]
    inputs[1].send_keys(ans2)

    button = driver.find_elements_by_tag_name("button")
    button[0].click()

    time.sleep(7)
    search_field = driver.find_element_by_id('search-input')
    instruments = ['RELIANCE EQUITY NSE']

    search_field.send_keys(instruments[0])
    search_results = driver.find_elements_by_class_name('search-result-item')

    #Hover over the desired field.
    actions = ActionChains(driver)
    #Assuming that the instrument that we searched for is shown first in search results. Otherwise i'm fucked.
    #Add code for checking if the first field is infact of reliance equity by checking the exchange.
    actions.move_to_element(search_results[0])
    actions.perform()

    buy_button = driver.find_elements_by_class_name('button-blue')
    sell_button = driver.find_elements_by_class_name('button-orange')
    buy = True
    Sell = False
    if buy:
        buy_button[0].click()
    elif sell:
        sell_button[0].click()
