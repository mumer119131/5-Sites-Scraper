import requests
from bs4 import BeautifulSoup
import re
import csv
from undetected_chromedriver import Chrome
import time
from selenium.webdriver.common.action_chains import ActionChains

class HebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ',
        }

    def get_response(self, url):
        id_pattern = pattern = r'-(P\d+)\?'
        match = re.search(pattern, url)
        if match:
            product_id = match.group(1)
        else:
            return False
        burp0_url = f"https://www.sephora.com:443/api2/catalog/products/{product_id}?addCurrentSkuToProductChildSkus=true&includeRegionsMap=true&showContent=true&includeConfigurableSku=true&countryCode=US&removePersonalizedData=true&includeReviewFilters=true&includeReviewImages=true&sentiments=6"
        burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "X-Ufe-Request": "true", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "X-Dtpc": "5$505172501_268h23vBLLCMFBNGOLFAPFGHKUDBVTGKMEPJULD-0e0", "X-Dtreferer": "https://www.sephora.com/shop/makeup-cosmetics?currentPage=2", "Exclude_personalized_content": "true", "X-Requested-Source": "rwd", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.sephora.com/product/sephora-collection-total-coverage-blending-sponge-set-60-plant-based-P482303?skuId=2497220&icid2=products%20grid:p482303:product", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        response = requests.get(burp0_url, headers=burp0_headers)
        return response.json()
    
    def parse_response(self, response, url):
        name = response['productDetails']['displayName']
        product_id = response['productDetails']['productId']
        try:
            ingredients = response['currentSku']['ingredientDesc']
        except:
            ingredients = ''

        return [name, product_id, ingredients]
    
    def search_category_total_results(self, category):
        # burp0_url = f"https://www.sallybeauty.com:443/{category}"
        # burp0_headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Dest": "document", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Referer": "https://www.sallybeauty.com/on/demandware.store/Sites-SA-Site/default/PX-Show?url=aHR0cHM6Ly93d3cuc2FsbHliZWF1dHkuY29tL29uL2RlbWFuZHdhcmUuc3RvcmUvU2l0ZXMtU0EtU2l0ZS9kZWZhdWx0L1NlYXJjaC1TaG93P2NnaWQ9c2hvcC1hbGwtaGFpci1jb2xvcg%3d%3d", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        # response = requests.get(burp0_url, headers=burp0_headers)
        # with open('test.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # total_results = soup.find('span', {'class': 'result-count-search-suggestions'}).text
        # pattern = r'\d+'
        # match = re.search(pattern, total_results)
        # extracted_number = match.group()
        return 10000
    
    def get_urls_of_category_from_all_results(self, category, total_results):

        all_urls = []
        burp0_url = f"https://www.sallybeauty.com:443/on/demandware.store/Sites-SA-Site/default/Search-UpdateGrid?cgid={category}&start=0&sz={total_results}&selectedUrl=https%3A%2F%2Fwww.sallybeauty.com%2Fon%2Fdemandware.store%2FSites-SA-Site%2Fdefault%2FSearch-UpdateGrid%3Fcgid%3Dshop-all-hair-color%26start%3D24%26sz%3D24"
        print(burp0_url)
        burp0_cookies = {"dwanonymous_4a9e5b8a33ad3045e7872fce95e7ad07": "abslIXqlGjascjPGaQMWAMJRe0", "_pxhd": "YxTrj7sekNsUMSnMFuZD/hE2ISaon4YNeUBIFfoHcAkY0P-fUmRrqI8mgO1pYLm4vF8IraXgJD1bNS0URweUJA==:XVXatt04oy4jYHPldCK2sLb3KzCPsLjLV6OYfoT3E1Fpej-WpJY9ZS-s83e6D34991xZ45RfzCnMexWGMiIAWDJotE5VMKCHUh441GvBQbc=", "_pxvid": "ec41d93c-6ac1-11ee-83dd-50ea5afd0ac0", "__pxvid": "f0047934-6ac1-11ee-bbf9-0242ac120003", "dwac_196b05238959e64d786b987e0d": "KMZk1oJvb_bU-700PGvwOETZex8Yer70mGs%3D|dw-only|||USD|false|US%2FCentral|true", "cqcid": "abslIXqlGjascjPGaQMWAMJRe0", "cquid": "||", "sid": "KMZk1oJvb_bU-700PGvwOETZex8Yer70mGs", "dwsid": "cKMNPN1fASbTYCGFkAV5lxy8EvVHStAkn_CNBk9kahThG8_ytMW-plIr6cm9gXz4vTukHSfHbXjdyzfJeZeCIw==", "__cq_dnt": "0", "dw_dnt": "0", "pxcts": "342a51ef-6b2a-11ee-9420-881ec3267458", "mt.v": "2.2130695091.1697354110464", "liveagent_oref": "https://www.sallybeauty.com/on/demandware.store/Sites-SA-Site/default/PX-Show?url=aHR0cHM6Ly93d3cuc2FsbHliZWF1dHkuY29tL29uL2RlbWFuZHdhcmUuc3RvcmUvU2l0ZXMtU0EtU2l0ZS9kZWZhdWx0L1NlYXJjaC1TaG93P2NnaWQ9aGFpci1jb2xvcg%3d%3d", "yotpo_pixel": "dcd69391-27b0-42e9-95e9-6d0eb4ac1761", "_sp_ses.3ed8": "*", "liveagent_sid": "a9262d4e-7af1-4bd1-970a-f7d32fb94aed", "liveagent_vc": "2", "liveagent_ptid": "a9262d4e-7af1-4bd1-970a-f7d32fb94aed", "__cq_uuid": "abslIXqlGjascjPGaQMWAMJRe0", "__cq_seg": "0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00", "_gcl_au": "1.1.715011637.1697354119", "_gid": "GA1.2.41649245.1697354121", "_etr_s_sallybeauty.com": "~0~~~1~0~1~6~", "_etr_p_sallybeauty.com": "6se715cysj~0~-1~1697357084517~2", "OptanonConsent": "isGpcEnabled=0&datestamp=Sun+Oct+15+2023+13%3A04%3A46+GMT%2B0500+(Pakistan+Standard+Time)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A0%2CC0004%3A0%2CC0005%3A0&AwaitingReconsent=false", "_ga": "GA1.2.2092079075.1697354120", "_sp_id.3ed8": "fa33fdaa37764325.1697354118.1.1697357092.1697354118", "_px3": "1f8221ce11799a7baf600eb9160882eba1b6a6ea5f9824472f24ea785d06cae6:C+gG1S5BysCzCe6XRB+5M6HN9kpmLuwSuuE3pBT6klvru3Ggm+ElWn0yrCJQB7gxk1S9REOnoB310wTwMmVzLg==:1000:snu3rJQSzp2TpvGqUGT143nyFj/uYaZovfXT0keOnw8HLmpzusv21IlbdqhVZHsRXuel2nuS8w+/TtS3vV7hDe+So/+P5F4JA36dAiOJgN76sQTYGVzgQ0p8uLjnbMMmxiClV2vTy9PUPWiCblGjnSgzO7aVK1O4QNSP+f6zDXSrVCMgkwqgzkb+fC3qCPhf2MHegwlvuORObNDDMkIeaNlCo/BV6GdMZL+sVY1IJW8=", "_gat_UA-3986609-1": "1", "_ga_QV4GNBRMPC": "GS1.1.1697354119.1.1.1697357457.0.0.0"}
        burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Accept": "*/*", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.sallybeauty.com/hair-color/shop-all-hair-color/", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        # response = requests.get(burp0_url, headers=burp0_headers)
        driver = Chrome()
        driver.get(burp0_url)
        response = driver.page_source
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(response)
        actions = ActionChains(driver)
        press_and_hold_button = driver.find_element(by='xpath', value='/html/body/div/div')
        actions.click_and_hold(press_and_hold_button)
        actions.perform()
        time.sleep(10)
        # Release the button
        actions.release(press_and_hold_button)
        actions.perform()


        time.sleep(1000)
        # self.get_all_products_from_category_page(urls)
        # self.get_all_products_from_category_page(all_urls)
            
    def get_all_products_from_category_page(self, urls):
        for url in urls:
            response = self.get_response(url)
            product = self.parse_response(response, url=url)
            self.save_product_to_csv(product)
        return True

    def save_product_to_csv(self, product):
        with open('sep.csv', 'a+', encoding='utf-8', newline='') as file:
            #check if the product is already in the csv
            file.seek(0) # move the file pointer to the beginning of the file
            reader = csv.reader(file)
            product_ids = [row[1] for row in reader]
            print(product_ids)
            if product[1] in product_ids:
                return False
            
            writer = csv.writer(file)
            writer.writerow(product)
            file.close()
    
    def run(self):
        total_results = self.search_category_total_results('hair-color/shop-all-hair-color/')
        print(total_results)
        self.get_urls_of_category_from_all_results('shop-all-hair-color', total_results)
        # print(f'Finished health')
        # return True
if __name__ == "__main__":
    scraper = HebScraper()
    response = scraper.run()