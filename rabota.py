import requests
from bs4 import BeautifulSoup as BS
import codecs
import time
import datetime

session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
base_url = 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2?period=2&lastdate='
# 'https://rabota.ua/zapros/python/Киев' 

domain = 'https://rabota.ua'
jobs = []   # список для хранения вакансий
urls = []   # список для хранения ссылок в поле пагинации
yesterday = datetime.date.today() - datetime.timedelta(1)
one_day_ago = yesterday.strftime('%d.%m.%Y')
base_url = base_url + one_day_ago
urls.append(base_url)

req = session.get(base_url, headers = headers)
if req.status_code == 200:
    bsObj = BS(req.content, "html.parser")
    pagination = bsObj.find('dl', attrs = {'id': 'ctl00_content_vacancyList_gridList_ctl23_pagerInnerTable'})
    if pagination:
        pages = pagination.find_all('a', attrs = {'class': 'f-always-blue'})
        for page in pages:
            urls.append(domain + page['href'])

for url in urls:
    time.sleep(2)
    req = session.get(url, headers = headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        table = bsObj.find('table', attrs = {'id' : 'ctl00_content_vacancyList_gridList'})
        if table:
            tr_list = bsObj.find_all('tr', attrs = {'id': True})
            for tr in tr_list:
                h3 = tr.find('h3', attrs = {'class': 'f-vacancylist-vacancytitle'})
                title = h3.a['title']
                href = h3.a['href']
                short = 'No description'
                company = 'No name'

                companyname = tr.find('p', attrs = {'class': 'f-vacancylist-companyname fd-merchant f-text-dark-bluegray'})
                if companyname:
                    company = companyname.a['title']
                descr = tr.find('p', attrs = {'class': 'f-vacancylist-shortdescr f-text-gray fd-craftsmen'})
                if descr:
                    short = descr.text
                jobs.append({'href': domain + href, 'title': title, 'descript': short, 'company': company})
                


template = '<!doctytpe html><html lang="en"><head><meta charset= "utf-8"></head><body>'
end = '</body></html>'

content = '<h2> rabota.ua</h2>'
for job in jobs:
    content += '<a href = "{href}" target = "_blank">{title}</a><br/><p>{descript}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br><br/>'
data = template + content + end
handle = codecs.open('rabota.html', "w", 'utf-8')
handle.write(str(data))
handle.close()
