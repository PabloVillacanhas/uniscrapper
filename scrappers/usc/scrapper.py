from bs4 import BeautifulSoup
import urllib.request as request
import models
import re

url = """http://www.usc.es/es/centros/medodo/programas.html?plan=14002"""
data = {
    "name": "",
    "credits": "",
    "course": "",
    "period": "",
    "type": ""
}

types = {
    "Obligatorio": "OB",
    "Formación básica": "FB",
    "Optativo": "OP"
}

subjects = []


def scrapper():
    response = request.urlopen(url)
    if(response.status == 200):
        print(response.status)
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        for table in soup.findAll("tbody"):
            trs = table.findAll("tr")
            for tr in trs:
                code = tr.td.string
                data["code"] = code
                name = tr.td.next_sibling.a.string
                getCredits(tr.td.next_sibling.a['href'])
                data["name"] = name
                type = tr.td.next_sibling.next_sibling.string
                period = tr.td.next_sibling.next_sibling.next_sibling.string
                parser(type, period, code)
                create()
    return subjects


def parser(type, period, code):
    data["type"] = types[type]
    data["period"] = period[0]
    data["course"] = code[5]


def create():
    subjects.append(models.Subject(data))


def getCredits(url):
    url = "http://www.usc.es/es/centros/medodo/" + url
    response = request.urlopen(url)
    if(response.status == 200):
        pattern = re.compile("Créditos ECTS: ([0-9.]*)")
        html_doc = response.read().decode('utf-8')
        match = re.search(pattern, html_doc)
        data["credits"] = match.group(1)
