import requests
from bs4 import BeautifulSoup as BS
import codecs
import time

session = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
base_url = 'https://djinni.co/jobs/?primary_keyword=Python&location=Киев'

domain = 'https://djinni.co'
jobs = []   # список для хранения вакансий
urls = []   # список для хранения ссылок в поле пагинации
urls.append(base_url)
urls.append(base_url + '&page=2')

# req = session.get(base_url, headers = headers)

# if req.status_code == 200:
#     bsObj = BS(req.content, "html.parser")
#     pagination = bsObj.find('ul', attrs = {'class': 'pagination'})
#     if pagination:
#         pages = pagination.find_all('li', attrs = {'class': False})
#         for page in pages:
#             urls.append(domain + page.a['href'])

for url in urls:
    time.sleep(2)
    req = session.get(url, headers = headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        li_list = bsObj.find_all('li', attrs = {'class' : 'list-jobs__item'})
        for li in li_list:
            div_title = li.find('div', attrs = {'class': 'list-jobs__title'})
            title = div_title.a.text
            href = div_title.a['href']
            short = 'No description'
            # company = 'No name'
            descr = li.find('div', attrs = {'class': 'list-jobs__description'})            
            if descr:
                short = descr.p.text
            jobs.append({'href': domain + href, 'title': title, 'descript': short, 'company': 'No company name'})
    #print ('https://www.work.ua' + href)
    #print (div.find('p', attrs = {'class': 'overflow'}).text)
# data = bsObj.prettify()#.encode('utf-8')
template = '<!doctytpe html><html lang="en"><head><meta charset= "utf-8"></head><body>'
end = '</body></html>'

content = '<h2> djinni.co</h2>'
for job in jobs:
    content += '<a href = "{href}" target = "_blank">{title}</a><br/><p>{descript}</p><p>{company}</p><br/>'.format(**job)
    content += '<hr/><br><br/>'
data = template + content + end
handle = codecs.open('djinni.html', "w", 'utf-8')
handle.write(str(data))
handle.close()
