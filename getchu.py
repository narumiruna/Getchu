import requests
from bs4 import BeautifulSoup

URL = 'http://www.getchu.com/'


class Getchu:
    def __init__(self):
        self.session = requests.session()
        self.session.get(URL + 'top.html', params={'gc': 'gc'})

    def search(self, **kwargs):
        links = []
        r = self.session.get(
            URL + 'php/search.phtml', params=kwargs)
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a', {'class': 'blueb'}):
            href = URL + link.get('href').strip('.')
            links.append(href)
            print(href)
        return links

    def item(self, url):
        item = {'url': url}
        soup = BeautifulSoup(self.session.get(url).text, 'html.parser')

        title = soup.find('h1', {'id': 'soft-title'})
        item['title'] = title.text.split('\n')[1].strip(' ')

        date = soup.find('a', {'id': 'tooltip-day'})
        if date:
            item['date'] = date.string

        brand = soup.find('a', {'class': 'glance'})
        if brand:
            item['brand'] = brand.string
        else:
            brand = soup.find('td', text='ブランド：')
            brand = brand.find_next('td', {'align': 'top'})
            item['brand'] = brand.text.split('\n')[0].strip(' ')

        image = soup.find('img', {'width': '280', 'height': '400'})
        if image:
            item['image'] = URL + image.get('src').strip('.')

        return item


if __name__ == '__main__':
    g = Getchu()
    for page in range(1, 2):
        links = g.search(genre='pc_soft', sort='create_date', pageID=page)
        for link in links:
            print(g.item(link))
