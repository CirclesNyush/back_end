import bs4
import requests
import json


def getData():
    res = requests.get('https://shanghai.nyu.edu/', "lxml")

    content = bs4.BeautifulSoup(res.text)

    img = []
    data = {}
    for i in content.select("div .home-carousel-item"):
        img.append(i.find('div').attrs['style'].split('//')[-1].rstrip(');'))

    con = content.select("div .item-content-box")
    data['length'] = len(con)
    item = []
    for i in range(len(con)):
        d = dict()
        d['title'] = con[i].find('h3').getText()
        for n in con[i].findAll('p'):
            if n is not None:
                d['detail'] = n.getText()
        d['link'] = con[i].find('a').attrs['href']
        d['img'] = img[i]
        item.append( d )
    data['item'] = item

    return data
