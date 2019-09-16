from scrappers import SubjectScrapper
from bs4 import BeautifulSoup
import urllib.request as request
from persistence.models import Subject
import re
import utils


class USCSubjectScrapper(SubjectScrapper):

    types = {
        "Obligatorio": "OB",
        "Formación básica": "BF",
        "Optativo": "OP",
        "Troncal": "TR"
    }
    period = {
        "A": 0,
        "1": 1,
        "2": 2,
        "T": 3,
        "P": 4
    }
    docencia = {
        '\xa0': "",
        "OFERTA.1": "OFERTA1",
        "OFERTA.REPT": "OFERTA.REPT"
    }

    def __init__(self, baseurl, careername):
        SubjectScrapper.__init__(self, baseurl)
        self.name = careername
        self.data = []

    def execute(self):
        response = request.urlopen(self.baseurl)
        if(response.status == 200):
            html_doc = response.read()
            # self.progressbar = utils.ScrapperProgressBar(
            #     self.calculateTotalSubjects(html_doc), self.name)
            soup = BeautifulSoup(html_doc, 'html.parser')
            subjects = {}
            # By course parser (code => name, credits, course)
            cursos = soup.select("#cursos #accordion-curso .panel .panel-body tbody")
            for idx, curso in enumerate(cursos, start=1):
                for row in curso.select("tr"):
                    code = row.td.getText()
                    subjects[code] = {'name': "", 'credits': "", 'course': -1, 'type': "", 'period': "", 'docencia': ""}
                    subjects[code]['name'] = row.td.next_sibling.getText()
                    subjects[code]['credits'] = row.td.next_sibling.next_sibling.getText()
                    subjects[code]['course'] = idx

            # By type (Basic formation, mandatory, optative)
            panel_caracter = soup.select("#modulos #accordion-caracter .panel")
            for caracter in panel_caracter:
                type = self.types[caracter.find("h4").getText()]
                for row in caracter.select("tbody tr"):
                    subjects[row.td.string]['type'] = type

            # Getting more data in other page (semester, docencia)
            link = soup.select("#ligazons .field-name-field-web-principal")[0].find("a")['href']
            response = request.urlopen(link)
            if(response.status == 200):
                soup = BeautifulSoup(response, 'html.parser')
                for key, value in subjects.items():
                    td = soup.find_all("td", string=key)[0]
                    subjects[td.string]['period'] = self.period[td.find_next_siblings("td")[3].string[0]]
                    subjects[td.string]['docencia'] = self.docencia[td.find_next_siblings("td")[4].string]

            for code, value in subjects.items():
                self.scheme['code'] = code
                self.scheme['name'] = value['name']
                self.scheme['credits'] = value['credits']
                self.scheme['course'] = value['course']
                self.scheme['period'] = value['period']
                self.scheme['type'] = value['type']
                self.scheme['docencia'] = value['docencia']
                self.data.append(Subject(self.scheme))

        else:
            pass

        # self.progressbar.finish()
        return self

    def getData(self):
        return self.data
