from undetected_chromedriver import Chrome, ChromeOptions
import time


url = "https://www.sallybeauty.com/on/demandware.store/Sites-SA-Site/default/Search-UpdateGrid?cgid=shop-all-hair-color&selectedUrl=https%3A%2F%2Fwww.sallybeauty.com%2Fon%2Fdemandware.store%2FSites-SA-Site%2Fdefault%2FSearch-UpdateGrid%3Fcgid%3Dshop-all-hair-color%26start%3D24%26sz%3D24&start=0&sz=1000"

driver = Chrome()
driver.get(url)
time.sleep(1000)
driver.quit()
