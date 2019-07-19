import time
import numpy as np
import bs4
import re,os,sys
from selenium import webdriver
import traceback
import unidecode
import io
import csv
import xlsxwriter

def get_driver(driver_width=600, driver_height=300, limit=300):
    connections_attempted = 0
    while connections_attempted < limit:
        try:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.set_window_size(driver_width, driver_height)
            #driver.minimize_window()
            return driver
        except:
            connections_attempted += 1
            print('Getting driver again...')
            print('  connections attempted: {}'.format(connections_attempted))
            print('  exception message: {}')
            traceback.print_exc()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def extract_news_links():
    base = 'https://www.eranico.com/fa/service/news/'
    path = 'eranico//'
    #os.mkdir(path)
    for i in range(395,492):
        os.mkdir(path + str(i + 1) + '//')
        driver = get_driver()
        driver.get(base + str(i + 1))
        soup = bs4.BeautifulSoup(driver.page_source)
        news_in_page = []
        for j in range(20):
            if(j<10):
                link = soup.findAll('a',{'id':'MainContentPlaceHolder_ContentsListUserControl_ctl0'+str(j)+'_ContentListHyperLink'})
                news_in_page.append('https://www.eranico.com' + str(link).split(' ')[1].split('=')[1][1:-1])
            if(j>=10):
                link = soup.findAll('a', {'id': 'MainContentPlaceHolder_ContentsListUserControl_ctl' + str(j) + '_ContentListHyperLink'})
                news_in_page.append('https://www.eranico.com' + str(link).split(' ')[1].split('=')[1][1:-1])
        f = open(path + str(i + 1) + '//' + "links.txt", "w")
        for k in range(len(news_in_page)):
            try:
                f.write(news_in_page[k] + '\n')
            except:
                print('shit')
        f.close()

def scrape_eranico_news(url):
    #url = 'https://www.eranico.com/fa/content/102106'
    driver = get_driver()
    driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source)

    time = soup.find('div',{'class':'pageDetail'})
    time = (cleanhtml(str(time.findAll('span')[-1]))).strip()
    #time = time.decode().encode('utf-8')

    title = soup.find('header', {'class': 'contentPageHeader'})
    title = (cleanhtml(str(title))).strip()
    #title = unicode.join(u'\n', map(unicode, title))

    abstract = soup.find('p',{'class':'abstract'})
    abstract = (cleanhtml(str(abstract)).strip())
    #abstract = unicode.join(u'\n', map(unicode, abstract))

    body = soup.find('div',{'id':'MainContentPlaceHolder_ContentUserControl_ContentDetailsBodyDivision'})
    body = (cleanhtml(str(body)).strip())
    #body = unicode.join(u'\n', map(unicode, body))
    return [time, title, abstract+body]

def write_news(n):
    reload(sys)
    sys.setdefaultencoding("utf-8")
    path = 'eranico//'
    f1 = open(path + str(n) + '//links.txt', 'r')
    doc = f1.read()
    lines = doc.split('\n')
    for j in range(len(lines)):
        x = (scrape_eranico_news(lines[j]))
        workbook = xlsxwriter.Workbook(path + str(n) +'//item'+str(j+1)+ '.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A2', x[0])
        worksheet.write('B2', x[1])
        worksheet.write('C2', x[2])
        workbook.close()
    f1.close()

for i in range(6,10):
    write_news(i)