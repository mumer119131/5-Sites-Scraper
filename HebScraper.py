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
        burp0_cookies = {"HEB_AMP_DEVICE_ID": "h-9553dc8b-559c-4b78-ac9e-29473ea5147b", "USER_SELECT_STORE": "false", "CURR_SESSION_STORE": "92", "visid_incap_2302070": "vJO0L0njTA29eovhNqUWS1G6KmUAAAAAQUIPAAAAAACceG/mmByIIKugw3IJIqb7", "AMP_MKTG_760524e2ba": "JTdCJTdE", "_gcl_au": "1.1.317767528.1697299041", "_cs_mk": "0.2353851536637448_1697299041315", "AMP_TOKEN": "%24NOT_FOUND", "_gid": "GA1.2.534463307.1697299046", "__pdst": "81f3b640db914df78cc13cef62fcce3d", "_scid": "f840b179-6a37-41f0-98a9-74e3442ab044", "_fbp": "fb.1.1697299048562.502869888", "_pin_unauth": "dWlkPVl6azJNekF4TURJdFlXTXhZUzAwTmpaaUxXRmpNRFV0TURFeFpETm1aRGRrT1dFeQ", "_sctr": "1%7C1697223600000", "reese84": "3:wfp881qL7WdzRBcAU3ffYQ==:Lkz+p5QhQkIanJK16VH+0CKMWahxYgIwx42BwyynUW8cZUjk641sxSInJE7aSIw3xi3IOBQyCT54y6eJYl0T17bacdFZne2hKrPMyo6k2ohGhDzaRg7EGm5yWxYvsn8h89MgEz+Kskm9mbs6nRLoKvyZTfLk6AQ4HUhIE3vEaJzYGQxP3I3JTLQR+NH9d8QE4dwp3u0yUtO2FZprb5BLv/bn9Z9X15M8M34EhBK7F60PnuiBE7TfF/oKc8A2XWKE3cKTaiOfKaqjHgVXfoQqpjbx9v8TY97HI9e2YVsa3DdxMhjzi6nlAsnj3aibi4dwNjdPuCWWSpg/r/WCVJYrvkYBil3GEfc4Iu+dzSuelofSH3KbBgVJKsLDelHQdgs/0EKX8l+xUXEH11b4hgqzYEHZXippaIY4gOjPfIs8OgcYR+7KUcUs4I5PxzyFj5bAO6+LiQIJthnvaBlsksc/qRodhV1KG9Hf/2DY3aT0CT6+jJepJS2E8H+i5tlZui7J:MipVq/8PkcpW7eAucFY0CStRxOOSdYcckRoxs/6GKhE=", "incap_ses_7245_2302070": "SpfVMbfbJlWH8UP9qGmLZNO/KmUAAAAAQ6DdBaFAErdn71N1kOCBVQ==", "DYN_USER_ID": "16893314532", "DYN_USER_CONFIRM": "837ca6cfe35db1d6751dc9a494700b94", "sessionContext": "curbside", "JSESSIONID": "db-spVppjEPfOL2HNHGA9xXNNPz5yFqJofTA1P5P", "_ga": "GA1.2.1176000733.1697299042", "AWSALB": "OQekVYif9FJJBBWmjXGqmwTBJQk75g7DP2nIAKZ/Kav3wjkc/GF2PaqFCzQCRp+xlo9j2q7hh2dPzuSEgXisiQ5PH+m4uhcJjekqfPLQzZ21z1mfS+1V9oz2UP4s", "AMP_760524e2ba": "JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmgtOTU1M2RjOGItNTU5Yy00Yjc4LWFjOWUtMjk0NzNlYTUxNDdiJTIyJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE2OTczMDA0OTkyMTclMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjk3Mjk5MDQwMzIyJTdE", "_ga_WKSH6HYPT4": "GS1.1.1697299041.1.1.1697300503.0.0.0", "_scid_r": "f840b179-6a37-41f0-98a9-74e3442ab044", "_uetsid": "5e6a5f306aaa11eeb682912c91164f65", "_uetvid": "5e6a66c06aaa11eebfd5cfd70a56b55d"}
        burp0_headers = {"Pragma": "no-cache", "Cache-Control": "no-cache", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        response = requests.get(url, cookies=burp0_cookies)
        with open('heb.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        return response
    
    def parse_response(self, response, url):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            name = soup.find('h1').text
        except:
            name = ''
        product_id_pattern = r"/(\d+)$"
        #last digits of url are product id
        match = re.search(product_id_pattern, url)
        if match:
            product_id = match.group(1)
        else:
            product_id = ''
        print(url)
        # try:
        # Find the outer div with id "accordion-panel-productDetailAccordion-nutrition-ingredients"
        outer_ingredients = soup.find('div', {'id': 'accordion-panel-productDetailAccordion-nutrition-ingredients'})

        ingredients_section = soup.find('h4', text='Ingredients')

        # Extract the text within the following sibling `span` element
        if ingredients_section:
            ingredients_span = ingredients_section.find_next('span')
            if ingredients_span:
                ingredients = ingredients_span.get_text()
            else:
                ingredients = ''
        else:
            ingredients = ''
        # except:
        #     ingredients = ''
        return [name, product_id, ingredients]
    
    def search_category_pages(self, category):
        url = f"https://www.heb.com:443/search/?q={category}"
        cookies = {"HEB_AMP_DEVICE_ID": "h-9553dc8b-559c-4b78-ac9e-29473ea5147b", "USER_SELECT_STORE": "false", "CURR_SESSION_STORE": "92", "visid_incap_2302070": "vJO0L0njTA29eovhNqUWS1G6KmUAAAAAQUIPAAAAAACceG/mmByIIKugw3IJIqb7", "AMP_MKTG_760524e2ba": "JTdCJTdE", "_gcl_au": "1.1.317767528.1697299041", "_cs_mk": "0.2353851536637448_1697299041315", "AMP_TOKEN": "%24NOT_FOUND", "_gid": "GA1.2.534463307.1697299046", "__pdst": "81f3b640db914df78cc13cef62fcce3d", "_scid": "f840b179-6a37-41f0-98a9-74e3442ab044", "_fbp": "fb.1.1697299048562.502869888", "_pin_unauth": "dWlkPVl6azJNekF4TURJdFlXTXhZUzAwTmpaaUxXRmpNRFV0TURFeFpETm1aRGRrT1dFeQ", "_sctr": "1%7C1697223600000", "incap_ses_7245_2302070": "SpfVMbfbJlWH8UP9qGmLZNO/KmUAAAAAQ6DdBaFAErdn71N1kOCBVQ==", "DYN_USER_ID": "16893314532", "DYN_USER_CONFIRM": "837ca6cfe35db1d6751dc9a494700b94", "sessionContext": "curbside", "JSESSIONID": "db-spVppjEPfOL2HNHGA9xXNNPz5yFqJofTA1P5P", "_uetsid": "5e6a5f306aaa11eeb682912c91164f65", "_uetvid": "5e6a66c06aaa11eebfd5cfd70a56b55d", "_scid_r": "f840b179-6a37-41f0-98a9-74e3442ab044", "_ga": "GA1.2.1176000733.1697299042", "_dc_gtm_UA-26725300-5": "1", "AWSALB": "b1DIZXjB38LKdvzXrptoESB/gX95NzqAqHP+iHYgV2VRlMx39vMmZbjj1+3nehO6PJ261/X1VhyYY4fX/h6X0XCWnwahqqMS4ouwhzHiyT2gGlvNSaLlHr647Jgb", "_ga_WKSH6HYPT4": "GS1.1.1697299041.1.1.1697300936.0.0.0", "AMP_760524e2ba": "JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmgtOTU1M2RjOGItNTU5Yy00Yjc4LWFjOWUtMjk0NzNlYTUxNDdiJTIyJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE2OTczMDA5Mzc0NTAlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjk3Mjk5MDQwMzIyJTdE", "reese84": "3:MI9duruS5ddU/GvGLWwcRw==:wdq4U02M5AC5G6t9+QdHIEkgE3bYtn0KTF3BGxo2hot1ZthsfB5dYr+TXfLKq0HRxdj81COMZDeRwmfR/7tKp1BuMeZTbkmq/JqL/+V6lnu5QT5hO/9cqFny1JybiH68Siy0mk8dVFcyLQmiZfAY11gQmhlwGPo7CjnDKCirS0D6MifVE9HoZrSkjkm16VDGRDo1LyHQ1CgFQjeipvK5cuN63tK3E/r6y9GT/hDCp6hq0z5JJqZZ7UTdIvF5NmVdu6EBKpq6x2PJW440TCEDhmDN0JSrL4GRopfOu4Xb4ClPzeokv10RfZ+ZBj/SREDVNiwP1EEn2AJM9WPZE+l8eFWhDE55aBPPFJm3wsg6ggoAMb7JNc3rlSgH8ACVvtfU4u2sSkAYA+Pi4eFx6n8J3xJYJ2jU1AAMFsWyZAEOqTil0wqJMiBlOdrfskgEWNSIL7LjN9yhk4Otmwnhl3hoaHjPDn397nsgEbElrjmKIiXqSo/kuNG5A5AOKRsbnys/:0hMb0LNmXdkecUxwJtVPLkqqBNFhFcidBrSnXtWVWHw="}
        headers = {"Pragma": "no-cache", "Cache-Control": "no-cache", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        response = requests.get(url, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        total_pages = soup.find_all('a', {'data-qe-id': 'paginationListNum'})[-1].text
        print(total_pages)
        return int(total_pages)
    
    def get_urls_of_category_from_page(self, category, pages):
        all_urls = []
        for page in range(1, pages + 1):
            burp0_cookies = {"HEB_AMP_DEVICE_ID": "h-9553dc8b-559c-4b78-ac9e-29473ea5147b", "USER_SELECT_STORE": "false", "CURR_SESSION_STORE": "92", "visid_incap_2302070": "vJO0L0njTA29eovhNqUWS1G6KmUAAAAAQUIPAAAAAACceG/mmByIIKugw3IJIqb7", "AMP_MKTG_760524e2ba": "JTdCJTdE", "_gcl_au": "1.1.317767528.1697299041", "_cs_mk": "0.2353851536637448_1697299041315", "AMP_TOKEN": "%24NOT_FOUND", "_gid": "GA1.2.534463307.1697299046", "__pdst": "81f3b640db914df78cc13cef62fcce3d", "_scid": "f840b179-6a37-41f0-98a9-74e3442ab044", "_fbp": "fb.1.1697299048562.502869888", "_pin_unauth": "dWlkPVl6azJNekF4TURJdFlXTXhZUzAwTmpaaUxXRmpNRFV0TURFeFpETm1aRGRrT1dFeQ", "_sctr": "1%7C1697223600000", "incap_ses_7245_2302070": "SpfVMbfbJlWH8UP9qGmLZNO/KmUAAAAAQ6DdBaFAErdn71N1kOCBVQ==", "DYN_USER_ID": "16893314532", "DYN_USER_CONFIRM": "837ca6cfe35db1d6751dc9a494700b94", "sessionContext": "curbside", "JSESSIONID": "db-spVppjEPfOL2HNHGA9xXNNPz5yFqJofTA1P5P", "_uetsid": "5e6a5f306aaa11eeb682912c91164f65", "_uetvid": "5e6a66c06aaa11eebfd5cfd70a56b55d", "_scid_r": "f840b179-6a37-41f0-98a9-74e3442ab044", "_ga": "GA1.2.1176000733.1697299042", "_dc_gtm_UA-26725300-5": "1", "AWSALB": "b1DIZXjB38LKdvzXrptoESB/gX95NzqAqHP+iHYgV2VRlMx39vMmZbjj1+3nehO6PJ261/X1VhyYY4fX/h6X0XCWnwahqqMS4ouwhzHiyT2gGlvNSaLlHr647Jgb", "_ga_WKSH6HYPT4": "GS1.1.1697299041.1.1.1697300936.0.0.0", "AMP_760524e2ba": "JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMmgtOTU1M2RjOGItNTU5Yy00Yjc4LWFjOWUtMjk0NzNlYTUxNDdiJTIyJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE2OTczMDA5Mzc0NTAlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjk3Mjk5MDQwMzIyJTdE", "reese84": "3:MI9duruS5ddU/GvGLWwcRw==:wdq4U02M5AC5G6t9+QdHIEkgE3bYtn0KTF3BGxo2hot1ZthsfB5dYr+TXfLKq0HRxdj81COMZDeRwmfR/7tKp1BuMeZTbkmq/JqL/+V6lnu5QT5hO/9cqFny1JybiH68Siy0mk8dVFcyLQmiZfAY11gQmhlwGPo7CjnDKCirS0D6MifVE9HoZrSkjkm16VDGRDo1LyHQ1CgFQjeipvK5cuN63tK3E/r6y9GT/hDCp6hq0z5JJqZZ7UTdIvF5NmVdu6EBKpq6x2PJW440TCEDhmDN0JSrL4GRopfOu4Xb4ClPzeokv10RfZ+ZBj/SREDVNiwP1EEn2AJM9WPZE+l8eFWhDE55aBPPFJm3wsg6ggoAMb7JNc3rlSgH8ACVvtfU4u2sSkAYA+Pi4eFx6n8J3xJYJ2jU1AAMFsWyZAEOqTil0wqJMiBlOdrfskgEWNSIL7LjN9yhk4Otmwnhl3hoaHjPDn397nsgEbElrjmKIiXqSo/kuNG5A5AOKRsbnys/:0hMb0LNmXdkecUxwJtVPLkqqBNFhFcidBrSnXtWVWHw="}
            burp0_headers = {"Pragma": "no-cache", "Cache-Control": "no-cache", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
            burp0_url = f"https://www.heb.com:443/search/?q={category}&pageNumber={page}"
            response = requests.get(burp0_url, cookies=burp0_cookies)
            with open('heb.html', 'w', encoding='utf-8') as file:
                file.write(response.text)
            url_pattern = r'href="(/product-detail/[^"]+)"'
            matches = re.findall(url_pattern, response.text)
            urls = [f'https://www.heb.com{match}' for match in matches]
            print(urls)
            self.get_all_products_from_category_page(urls)
            
    def get_all_products_from_category_page(self, urls):
        for url in urls:
            response = self.get_response(url)
            product = self.parse_response(response, url=url)
            self.save_product_to_csv(product)
        return True

    def save_product_to_csv(self, product):
        with open('heb.csv', 'a+', encoding='utf-8', newline='') as file:
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
        pages = self.search_category_pages('health')
        self.get_urls_of_category_from_page('health', pages)
        print(f'Finished health')
        return True
if __name__ == "__main__":
    scraper = HebScraper()
    response = scraper.run()