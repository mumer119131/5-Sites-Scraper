import requests
from bs4 import BeautifulSoup
import re
import csv


class UltaScraper:

  def __init__(self):
    self.headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    self.base_url = "https://www.ulta.com/"
    self.categories = [
        'make-up', 'skin-care', 'hair', 'body-care', 'fragrance',
        'tools-brushes', 'luxury-beauty', 'gifts', 'men'
    ]

  def product_detail(self, url):
    response = requests.get(url, headers=self.headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_name = soup.find('h1').find('span', {
        'class': 'Text-ds--title-5'
    }).text

    product_id_pattern = r'(\d+)\?'
    product_id = re.search(product_id_pattern, url).group(1)
    try:
      ingridient_summary = ingredients_element = soup.find(id="Ingredients")
      ingridients = ingridient_summary.find_next_sibling().text
    except:
      ingridients = ''

    return [product_name, product_id, ingridients]

  def get_number_of_results(self, category):
    """
    Get the number of results for a given category.
    """
    url = f"{self.base_url}shop/{category}/all"
    print(url)
    response = requests.get(url, headers=self.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    total_results_text = soup.find(
        "div", {
            "class": "ProductListingWrapper__resultslabel"
        }).text
    print(total_results_text)
    result = re.search(r'\d+', total_results_text)
    return int(result.group())

  def get_product_urls(self, category, total_results):
    """
    Get product urls from category
    """

    total_pages = total_results // 96 + 1
    for page in range(1, total_pages + 1):
      url = f"{self.base_url}shop/{category}/all?page={page}"
      print(url)
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        products_ul = soup.find(
            "ul", {"class": "ProductListingResults__productList"})
        all_links = products_ul.find_all('a', href=True)
        urls = []
        for link in all_links:
          if link['href'].startswith('https://www.ulta.com/p/'):
            print(link['href'])
            product = self.product_detail(link['href'])
            print(product)
            self.save_product_to_csv(product)
            urls.append(link['href'])

        if len(urls) == 0:
          break
        page += 1

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
    total_results = self.get_number_of_results('makeup')
    self.get_product_urls("makeup", total_results)


if __name__ == "__main__":
  scraper = UltaScraper()
  scraper.run()
