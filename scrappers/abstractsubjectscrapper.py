from . import Scrapper


class SubjectScrapper(Scrapper):

    progressbar = None
    baseurl = None
    scheme = {
        "name": "",
        "credits": "",
        "course": "",
        "period": "",
        "type": "",
        "code": "",
        "docencia": ""
    }

    def __init__(self, baseurl):
        super(Scrapper, self).__init__()
        self.baseurl = baseurl
