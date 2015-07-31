import requests
from bs4 import BeautifulSoup

URL = 'http://www.getchu.com'


class Getchu:
    def __init__(self):
        self.session = requests.session()
        self.session.get(URL + '/top.html', params={'gc': 'gc'})

    def search(self, **kwargs):
        links = []
        r = self.session.get(
            URL + '/php/search.phtml', params=kwargs)
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a', {'class': 'blueb'}):
            href = URL + link.get('href').strip('.')
            links.append(href)
        return links

    def item(self, url):
        item = {'url': url}
        soup = BeautifulSoup(self.session.get(url).text, 'html.parser')

        title = soup.find('h1', {'id': 'soft-title'})
        item['title'] = title.text.split('\n')[1].strip()

        genre = soup.find('li', {'class': 'genretab current'})
        genre = genre.find('a')
        item['genre'] = genre.string

        date = soup.find('td', text='発売日：')
        date = date.find_next('td', {'align': 'top'})
        item['date'] = date.text.split('\n')[1].strip()

        brand = soup.find('td', text='ブランド：')
        brand = brand.find_next('td', {'align': 'top'})
        item['brand'] = brand.text.split('\n')[0].strip()

        price = soup.find('td', text='定価：')
        price = price.find_next('td', {'align': 'top'})
        price = price.string
        item.setdefault('price', price.string)

        image = soup.find('img', {'width': '280', 'height': '400'})
        if image:
            item['image'] = URL + image.get('src').strip('.')

        return item


class Test:
    def __init__(self):
        self.g = Getchu()

    def pc_soft(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.g.item, self.g.search(genre='pc_soft', sort='create_date', pageID=page)):
                print(item)

    def goods(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.g.item, self.g.search(genre='goods', sort='create_date', pageID=page)):
                print(item)

    def anime_dvd(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.g.item,
                            self.g.search(genre='anime_dvd', age='18:lady', sort='create_date', pageID=page)):
                print(item)


if __name__ == '__main__':
    Test().pc_soft(1)
    Test().goods(1)
    Test().anime_dvd(1)
