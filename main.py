import argparse

import requests
from bs4 import BeautifulSoup


class Getchu:
    getchu_url = 'http://www.getchu.com'

    def __init__(self):
        self.session = requests.session()
        self.session.get(self.getchu_url + '/top.html', params={'gc': 'gc'})

    def search(self, **kwargs):
        links = []
        r = self.session.get(self.getchu_url + '/php/search.phtml', params=kwargs)
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a', {'class': 'blueb'}):
            href = self.getchu_url + link.get('href').strip('.')
            links.append(href)
        return links

    def parse_item(self, url):
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
            item['image'] = self.getchu_url + image.get('src').strip('.')

        return item

    def crawl(self, genre, max_pages=10):
        items = []
        for page in range(1, max_pages + 1):
            links = self.search(genre=genre, sort='create_date', pageID=page)
            for link in links:
                item = self.parse_item(link)
                items.append(item)
        return items


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--genre', type=str, default='pc_soft')
    parser.add_argument('--max-pages', type=int, default=1)
    args = parser.parse_args()
    print(args)

    g = Getchu()
    print(g.crawl(args.genre, args.max_pages))
