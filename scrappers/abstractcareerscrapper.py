from . import Scrapper


class CareerScrapper(Scrapper):

    progressbar = None
    baseurl = None
    scheme = {
        "id": "",
        "name": "",
        "code": "",
        "year": "",
        "baseurl": ""
    }

    def __init__(self, baseurl):
        super(Scrapper, self).__init__()
        self.baseurl = baseurl
