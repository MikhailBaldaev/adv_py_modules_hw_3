import requests
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HEADERS = {
    'Cookies': 'yandexuid=7872100861644332491; yuidss=7872100861644332491; my=YwA=; ymex=1972109901.yrts.1656749901;'
               ' yandex_gid=117428; gdpr=0; _ym_uid=1645464466702207110; amcuid=4972560311656757599;'
               ' is_gdpr=1; is_gdpr_b=CNzDcxCdfBgBKAI=; _ym_d=1657306071;',
    'Acceept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}


def scrap(url: str):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    articles = soup.find_all("article")
    article_id = [i["id"] for i in articles]
    titles = []
    dates = []
    for i in articles:
        title = str(i.find("h2").find("span"))
        title = title.replace("<span>", "").replace("</span>", "")
        titles.append(title)
        date = i.find("time")
        dates.append(date["title"][:10])
    links = [f'https://habr.com/ru/post/{i}/' for i in article_id]
    previews = dict()
    k = 0
    for i in articles:
        preview = i.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
        if preview:
            previews.setdefault(k, preview.text)
        else:
            preview = i.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
            previews.setdefault(k, preview.text)
        k += 1
    hubs = []
    for i in articles:
        hub_items = [i.span.text for i in i.find_all(class_="tm-article-snippet__hubs-item")]
        hubs.append(str(hub_items))
    total = {key: [value0, value1, value2, value3, value4] for (key, value0, value1, value2, value3, value4) in zip(article_id, titles, dates, links, previews.values(), hubs)}
    for key, value in total.items():
        for i in KEYWORDS:
            if i in value[3] or i in value[4]:
                print(f'<{value[1]}> - <{value[0]}> - <{value[2]}>')
                break


if __name__ == '__main__':
    scrap('https://habr.com/ru/all/')