from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from bs4 import BeautifulSoup
import pandas as pd
import time

print("hello")
try:
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    models = []
    prices = []
    driver.get(
        "https://www.linsoul.com/collections/in-ear-monitors?sort_by=manual&filter.v.availability=1&filter.v.price.gte=&filter.v.price.lte=&filter.p.vendor=TinHiFi"
    )
    SCROLL_PAUSE_TIME = 10

    # Get scroll height
    """ last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(1, 100):
        iframe = driver.find_element(
            By.CSS_SELECTOR, ".mt-6.flex.flex-wrap.-mx-2 > :last-child"
        )
        ActionChains(driver).scroll_to_element(iframe).perform()
        time.sleep(4) """
    """A method for scrolling the page."""

    # Get scroll height.

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        listings = driver.find_elements(By.CSS_SELECTOR, ".sf__pcard")
        loc = listings[-1].location["y"]
        driver.execute_script(f"window.scrollTo(0, {loc} + 200);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Uses End key to scroll to bottom of page, page does not always automatically load new content after reaching bottom
    """ while True:
        body = driver.find_element(By.XPATH, "/html/body")
        body.send_keys(Keys.END)
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height """

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for element in soup.findAll("div", attrs={"class": "sf__col-item"}):
        model = element.find("a", attrs={"class": "sf__pcard-name"})
        price = element.find("span", attrs={"class": "money"})
        models.append(model.text.strip())
        prices.append(
            float(price.text.strip().translate({ord(i): None for i in "$USD,"}))
        )

    df = pd.DataFrame({"Product Name": models, "Price": prices})
    df.loc["Total"] = pd.Series(df["Price"].sum(), index=["Price"])
    df.to_csv("./TINHIFI.csv", index=False, encoding="utf-8")
    print("end")
except Exception as err:
    print(err)
    raise
