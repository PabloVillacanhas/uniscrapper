from scrappers import CareerScrapper
from bs4 import BeautifulSoup
import urllib.request as request
from persistence.models import Career
from datetime import datetime
import utils


class USCCareerScrapper(CareerScrapper):

    def __init__(self, uniname="USC"):
        CareerScrapper.__init__(self, 'http://www.usc.es/graos/es/')
        self.uniname = uniname
        self.data = []

    def execute(self):
        self.year = datetime.now().year
        response = request.urlopen(self.baseurl)
        if(response.status == 200):
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, 'html.parser')
            careers = soup.select("#block-accordion-menu-1 div.view-graos div.panel")
            self.progressbar = utils.ScrapperProgressBar(len(careers), self.uniname)
            for career in careers:
                self.scheme['code'] = self.getCareerCode(career)
                self.scheme['name'] = career.select("div.panel-heading a")[0].string.strip()
                career = Career(self.scheme)
                self.data.append(career)
                print(career)
                self.progressbar.update()
                if len(self.data) == 5:
                    return self
        else:
            pass
        self.progressbar.finish()
        return self

    def getCareerCode(self, career):
        prefix = 'http://www.usc.es'
        subject_url = prefix + career.select(".views-field-field-show-link a")[0]['href']
        self.scheme['baseurl'] = subject_url
        response = request.urlopen(subject_url)
        if(response.status == 200):
            soup = BeautifulSoup(response, 'html.parser')
            url = soup.select("#ligazons a")[0]['href']
            soup = BeautifulSoup(request.urlopen(url), 'html.parser')
            return soup.select(".main-container h1")[0].string.split("-")[1]


    def getData(self):
        return self.data
