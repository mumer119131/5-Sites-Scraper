import requests
from bs4 import BeautifulSoup
import re
import csv

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
        burp0_url = f"https://www.sephora.com:443/api/v2/catalog/categories/{category}/seo?targetSearchEngine=NLP&currentPage=2&pageSize=60&content=true&includeRegionsMap=true&headers=%5Bobject%20Object%5D&pickupRampup=true&sddRampup=true&loc=en-US&ch=rwd"
        burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "X-Dtpc": "5$505172501_268h16vBLLCMFBNGOLFAPFGHKUDBVTGKMEPJULD-0e0", "X-Dtreferer": "https://www.sephora.com/shop/makeup-cosmetics", "X-Timestamp": "1697306065014", "Exclude_personalized_content": "true", "X-Requested-Source": "rwd", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.sephora.com/shop/makeup-cosmetics?currentPage=2", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        response = requests.get(burp0_url, headers=burp0_headers)
        data = response.json()

        return data['totalProducts']
    
    def get_urls_of_category_from_all_results(self, category, total_results):

        all_urls = []
        pages = total_results // 60 + 1
        for page in range(1, pages+1):
            burp0_url = f"https://www.sephora.com:443/api/v2/catalog/categories/{category}/seo?targetSearchEngine=NLP&currentPage={page}&pageSize=60&content=true&includeRegionsMap=true&headers=%5Bobject%20Object%5D&pickupRampup=true&sddRampup=true&loc=en-US&ch=rwd"
            burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "X-Dtpc": "5$505172501_268h16vBLLCMFBNGOLFAPFGHKUDBVTGKMEPJULD-0e0", "X-Dtreferer": "https://www.sephora.com/shop/makeup-cosmetics", "X-Timestamp": "1697306065014", "Exclude_personalized_content": "true", "X-Requested-Source": "rwd", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.sephora.com/shop/makeup-cosmetics?currentPage=2", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
            response = requests.get(burp0_url, headers=burp0_headers)
            data = response.json()
            products = data['products']
            urls = []
            for product in products:
                urls.append(f'https://www.sephora.com{product["targetUrl"]}')
            print(urls)
            self.get_all_products_from_category_page(urls)
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
        total_results = self.search_category_total_results('makeup-cosmetics')
        self.get_urls_of_category_from_all_results('makeup-cosmetics', total_results)
        print(f'Finished health')
        return True
if __name__ == "__main__":
    scraper = HebScraper()
    response = scraper.run()