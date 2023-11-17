from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Specify the path to chromedriver
chrome_path = '/Users/bhagyashreerane/Documents/chrome-headless-shell-mac-arm64'

# Set up the Selenium webdriver with options
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

product_url = "https://www.amazon.in/ref=nav_logo"
driver.get(product_url)
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys("mobile under 10000")
driver.find_element(By.XPATH,'//*[@id="nav-search-submit-button"]').click()
time.sleep(2)

reviews = driver.find_elements(By.CSS_SELECTOR, '.puis-price-instructions-style .a-price-whole , .a-spacing-none.s-line-clamp-2')

data=""""""
for review in reviews:
     data+=review.text
     data+="\n"
# Splitting data into mobile names and prices
lines = data.split('\n')
mobile_names = []
prices = []

i = 0
while i < len(lines):
    mobile_name = lines[i]
    i += 1

    while i < len(lines) and not lines[i].replace(",", "").isdigit():
        mobile_name += " " + lines[i]
        i += 1

    if i < len(lines) and lines[i].replace(",", "").isdigit():
        price = lines[i]
        i += 1
    else:
        price = None

    mobile_names.append(mobile_name)
    prices.append(price)

# Creating a DataFrame
df = pd.DataFrame({"Mobile Name": mobile_names, "Price": prices})
df = df.drop(df.index[-1])
df.to_csv('amazon_mobile.csv')
driver.quit()
