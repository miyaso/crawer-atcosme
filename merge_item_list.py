import pandas as pd
import os
import csv

OUTPUT_DIR = 'output'
included_extensions = ['newcols']

files = [fn for fn in os.listdir(OUTPUT_DIR)
              if any(fn.endswith(ext) for ext in included_extensions)]

df = pd.concat([pd.read_csv(os.path.join(OUTPUT_DIR, file)) for file in files])
df.description = df.description.str.replace('\r', '')

df.to_csv(os.path.join(OUTPUT_DIR, 'merge_item_list.csv'), index=False, quoting=csv.QUOTE_ALL )
