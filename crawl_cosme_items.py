import os
import pandas as pd
import time
import urllib.request
import csv
from bs4 import BeautifulSoup 

OUTPUT_DIR = 'output'
included_extensions = ['csv']
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }

files = [fn for fn in os.listdir(OUTPUT_DIR)
              if any(fn.endswith(ext) for ext in included_extensions)]
 
for file in files:
    print('【START】Read file of '+os.path.join(OUTPUT_DIR, file))
    file_path = os.path.join(OUTPUT_DIR, file)

    df = pd.read_csv(file_path)
    out_df = df.copy()
    out_df['maker'] = ''
    out_df['discription'] = ''
    out_df['categorys'] = ''
    for row, record in df.iterrows():
        url = record['url']
        print('>>'+url)
        try:
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(html, 'lxml')
            spec = soup.find('div', id='product-spec')
            out_df.loc[row, 'maker'] = spec.select('.maker')[0].dd.text
            out_df.loc[row, 'categorys'] = '|'.join([ ci.text.replace('\n', ' ') for ci in spec.select('.item-category')[0].dd.select('span')])
            out_df.loc[row, 'description'] = spec.select('dd[itemprop=description]')[0].text.replace('\n', '')
            time.sleep(0.5)
        except Exception as e:
            print('【ERROR】Load URL of '+url)
            print(e)
    print('【END】Read file of '+os.path.join(OUTPUT_DIR, file))
    out_df.to_csv(os.path.join(OUTPUT_DIR, file+'.newcols'), index=False, quoting=csv.QUOTE_ALL )

