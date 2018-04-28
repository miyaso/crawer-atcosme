# -*- coding: utf-8 -*-
import urllib.request
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

BASE_URL_DATA = pd.read_csv('url.txt', sep=' ')
SKIP_COUNT = 22
for row, base_url_dict in BASE_URL_DATA.iterrows():
    print(base_url_dict)
    if SKIP_COUNT > row:
        continue
    large_category = base_url_dict['大カテゴリ']
    middle_category = base_url_dict['中カテゴリ']
    base_url = base_url_dict['口コミ件数順URL']
    print('##### START: %s #####'%(base_url))

    headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                        }

    url_list = [base_url+'/srt/1'] + [base_url+'/page/{0}/srt/1'.format(i) for i in range(1, 100)]

    output_list = []
    for url in url_list:
        print('crawl target >> {}'.format(url))
        request = urllib.request.Request(url=url, headers=headers)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e)
            continue
        html = response.read()
        #html = urllib2.urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        # itemリスト抽出
        crawl_items = soup.find_all("div", class_="keyword-product-section")
        for item in crawl_items:
            item_dict = {} 
            # 基本情報
            try:
                item_dict['brand'] = item.find(class_="brand").find("a", attrs={"itemprop": "name"}).text
                item_dict['name'] = item.find(class_="item").text
                item_dict['url'] = item.find(class_="item").a.attrs['href']
                # スペック系
                item_dict['reviewer-average'] = item.find(class_="spec").find(class_="reviewer-average").text
                item_dict['point'] = item.find(class_="point").text.strip('pt')
                item_dict['kuchikomi'] = item.find(class_="spec").find(class_="count").span.text
                item_dict['price'] = item.find_all(class_="spec")[1].find(class_='price').text.strip(u'\u672c\u4f53\u4fa1\u683c\uff1a')
                item_dict['sell'] = item.find_all(class_="spec")[1].find(class_='sell').text.strip(u'\u767a\u58f2\u65e5\uff1a')
                # カテゴリー
                item_dict['categories'] =  '|'.join([ c.text for c in item.find(class_="category").select('a')])
                item_dict['large_category'] = large_category
                item_dict['middle_category'] = middle_category
                # リストに追加
            except Exception as e:
                print(e)
                print(item)
                continue
            output_list.append(item_dict)
        print('>> catched item count is {}'.format(len(output_list)))
        time.sleep(0.5)

    pd.DataFrame(output_list).to_csv('output/item_list_{}_{}.csv'.format(large_category, middle_category), index=False, quoting=csv.QUOTE_ALL )




