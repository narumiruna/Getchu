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
        item.setdefault('genre', []).append(genre.string)

        brand = soup.find('td', text='ブランド：')
        brand = brand.find_next('td', {'align': 'top'})
        item['brand'] = brand.text.split('\n')[0].strip()

        price = soup.find('td', text='定価：')
        price = price.find_next('td', {'align': 'top'})
        item['price'] = price.string

        date = soup.find('td', text='発売日：')
        if date:
            date = date.find_next('td', {'align': 'top'})
            item['date'] = date.text.split('\n')[1].strip()

        media = soup.find('td', text='メディア：')
        if media:
            item['media'] = media.find_next('td', {'align': 'top'}).string

        genre = soup.find('td', text='ジャンル：')
        if genre:
            item['genre'].append(genre.find_next('td', {'align': 'top'}).string)

        painting = soup.find('td', text='原画：')
        if painting:
            item['painting'] = painting.find_next('td', {'align': 'top'}).text.split('、')

        scenario = soup.find('td', text='シナリオ：')
        if scenario:
            item['scenario'] = scenario.find_next('td', {'align': 'top'}).text.split('、')

        category = soup.find('td', text='カテゴリ：')
        if category:
            item['category'] = category.find_next('td', {'align': 'top'}).text.strip('[一覧]').strip().split('、')

        image = soup.find('img', {'width': '280', 'height': '400'})
        if image:
            item['image'] = URL + image.get('src').strip('.')

        return item

    def pc_soft(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.item, self.search(genre='pc_soft', sort='create_date', pageID=page)):
                print(item)

    def goods(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.item, self.search(genre='goods', sort='create_date', pageID=page)):
                print(item)

    def anime_dvd(self, max_pages):
        for page in range(1, max_pages + 1):
            for item in map(self.item,
                            self.search(genre='anime_dvd', age='18:lady', sort='create_date', pageID=page)):
                print(item)


if __name__ == '__main__':
    g = Getchu()
    g.pc_soft(1)
    g.goods(1)
    g.anime_dvd(1)
