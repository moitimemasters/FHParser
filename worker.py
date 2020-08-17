import requests
from bs4 import BeautifulSoup
from pprint import pprint


class FLHWorker:
    base = "https://freelancehunt.com/"
    def __init__(self, project_url):
        self.url = project_url

    @property
    def page_content(self):
        return requests.get(self.url).text

    @property
    def parser(self):
        return BeautifulSoup(self.page_content, "lxml")

    def find_by_class(self, worker: BeautifulSoup, tag, class_):
        return worker.find(tag, {"class": class_})

    def find_all_by_class(self, worker: BeautifulSoup, tag, class_):
        return worker.findAll(tag, {"class": class_})

    def get_description(self):
        well = self.find_by_class(self.parser, "div", "well")
        description_text = well.find("div").find("span").find("p").text
        return description_text

    def get_author(self):
        div = self.parser.find("div", string="Заказчик").parent
        a = self.find_by_class(div, "a", "profile-name")
        href = self.base + a["href"]
        name = a.text
        return "[%s](%s)" % (name, href)

    def get_price(self):
        span = self.find_by_class(self.parser, "span", "price-tag")
        return span.text.strip()
    
    def get_status(self):
        col_md = self.find_by_class(self.parser, "div", "col-md-12")
        span = list(col_md.findAll("span"))[-1]
        return span.text 
    
    def get_bids_count(self):
        span = self.parser.find("span", id="bids_count")
        return int(span.text)
    
# URL = "https://freelancehunt.com/project/prokonsultirovatsya-ckeditor-django-napisanie/735354.html"

# worker = FLHWorker(URL)
# print(worker.get_author())