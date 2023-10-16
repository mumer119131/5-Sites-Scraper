import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import time

class HebScraper:
    def __init__(self):
        self.ac = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers = {"Referer":"https://www.google.com","Connection":"Keep-Alive","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":self.ac,"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
        self.session = requests.Session()
        self.categories = [
            'health', 'beauty', 'personal care'
        ]
    def get_product_detail(self, url):
        response = self.session.get(
            url, headers=self.headers)
        with open('test.html', 'w+', encoding='utf-8') as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'}).text
        # convert scraipt tag json to dict
        script_tag_json = json.loads(script_tag)
        try:
            ingridents = script_tag_json['props']['pageProps']['initialData'][
                'data']['idml']['ingredients']['ingredients']['value']
        except:
            ingridents = ''
        # x.props.pageProps.initialData.data.product.name
        product_name = script_tag_json['props']['pageProps']['initialData']['data']['product']['name']
        # x.props.pageProps.initialData.data.product.usItemId
        product_id = script_tag_json['props']['pageProps']['initialData']['data']['product']['usItemId']
        return [product_name, product_id, ingridents]

    def get_no_of_pages_of_sub_category(self, url):
        # burp0_headers = {"Dpr": "1", "Downlink": "10", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://www.walmart.com/cp/health/976760?q=health", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        # response = requests.get(url, headers=burp0_headers)

        # # try:
        # pattern = r'"maxPage":\s*(\d+)'
        # match = re.search(pattern, response.text)
        # total_pages = match.group(1)

        # print(total_pages)
        return 25
        # except:
        #     print('No pagination found')
        #     return 1

    def get_category_browse_urls(self, category):
        url = f'https://www.walmart.com/cp/health/976760?q={category}'
        response = self.session.get(
            url, headers=self.headers)
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        url_pattern = re.compile(
            r'https://www.walmart.com/browse/[^/]+/[^/]+/\d+_\d+\?povid=.*')
        url_matches = url_pattern.findall(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all anchor (a) tags in the HTML
        all_links = soup.find_all("a")

        # Extract and print the href attribute of each anchor tag matching the pattern
        for link in all_links:
            href = link.get("href")
            if href and url_pattern.match(href):
                print(href)
                try:
                    total_pages = self.get_no_of_pages_of_sub_category(href)
                    urls = self.get_product_urls(href, int(total_pages))
                except Exception as e:
                    print(e)
                    pass
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

    def get_product_urls(self, url, pages):
        urls = []
        for i in range(1, pages + 1):
            print(i)

            request_url = f'{url}&page={i}'
            print(request_url)
            response = self.session.get(
                request_url, headers=self.headers)
            with open('test.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('div', {'class': 'b--near-white'})
            for item in items:
                a_tag = item.find('a')
                if a_tag:
                    if a_tag['href'].startswith('/ip'):
                        a_tag['href'] = 'https://www.walmart.com' + \
                            a_tag['href']
                    product = self.get_product_detail(a_tag['href'])
                    time.sleep(2)
                    print(product)
                    self.save_product_to_csv(product)
        print(urls)
        return urls

    def save_product_to_csv(self, product):
        with open('wallmart.csv', 'a+', encoding='utf-8', newline='') as file:
            # check if the product is already in the csv
            file.seek(0)  # move the file pointer to the beginning of the file
            reader = csv.reader(file)
            product_ids = [row[1] for row in reader]
            if product[1] in product_ids:
                return False

            writer = csv.writer(file)
            writer.writerow(product)
            file.close()

    def run(self):
        browse_urls = self.get_category_browse_urls('health')

        return True


if __name__ == "__main__":
    print('Starting...')
    scraper = HebScraper()
    response = scraper.run()
