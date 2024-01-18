import sys, os, random
import pandas as pd
import re
from colorama import Fore, Style


def read_file_in_chunks(file, chunksize=10000):
    # function to read large files in chunks
    chunks = []
    for chunk in pd.read_csv(file, chunksize=chunksize):
        chunks.append(chunk)
        if len(chunks) * chunksize >= 100000:  # limit to 100,000 rows
            break
    return pd.concat(chunks)

def apply_regex(df, pattern):
    # function to filter rows based on regex pattern and colorize matches
    regex_matches = df.astype(str).apply(lambda row: row.str.contains(pattern))
    return df[regex_matches.any(axis=1)]

df = None
# init df to None
df = None

# main logic
file = sys.argv[1]
ext = file.split('.')[-1]
nrows, sheet, pattern = 10, 0, None
head, tail, desc, corr, count, sort_col, sort_order, to_csv, to_tsv, to_excel, random_sample = False, False, False, False, False, None, None, False, False, False, False

# parsing command line arguments
for i in range(2, len(sys.argv), 2):
    arg, val = sys.argv[i], sys.argv[i+1] if i+1 < len(sys.argv) else ''
    if arg == '--rows': nrows = int(val)
    elif arg == '--sheet': sheet = int(val)
    elif arg == '--regex': pattern = val
    elif arg == '--head': head = True
    elif arg == '--tail': tail = True
    elif arg == '--random': random_sample = True
    elif arg == '--toCsv': to_csv = True
    elif arg == '--toExcel': to_excel = True
    elif arg == '--toTsv': to_tsv = True
    elif arg == '--desc': desc = True
    elif arg == '--corr': corr = True
    elif arg == '--count': count = True
    elif arg.startswith('--sort'):
        sort_col = int(arg[6])  # get column index
        sort_order = arg[7]     # get sort order ('a' or 'd')
    # ... other arguments ...

# apply sorting if needed
if sort_col is not None:
    ascending = True if sort_order == 'a' else False
    df = df.sort_values(df.columns[sort_col], ascending=ascending)

# display statistical summaries if requested
if desc: print(df.describe())
elif corr: print(df.corr())
elif count: print(df.nunique())


file_size = os.path.getsize(file) / (1024 * 1024)  # file size in mb

# reading file based on extension and size
if file_size > 10:  # large file
    df = read_file_in_chunks(file)
else:
    if ext == 'csv':
        df = pd.read_csv(file, nrows=nrows)
    elif ext in ['xlsx', 'xls']:
        df = pd.read_excel(file, sheet_name=sheet, nrows=nrows)
    elif ext == 'tsv':
        df = pd.read_csv(file, sep='\t', nrows=nrows)

if df is not None:
    # Now all operations on df are within this block
    # apply sorting if needed
    if sort_col is not None:
        ascending = True if sort_order == 'a' else False
        df = df.sort_values(df.columns[sort_col], ascending=ascending)

    # apply regex if needed
    if pattern:
        df = apply_regex(df, pattern)

    # random sampling
    if random_sample:
        df = df.sample(n=nrows) if len(df) > nrows else df

    # adjust display settings
    pd.set_option('display.max_columns', None)  # display all columns
    pd.set_option('display.max_rows', nrows)    # display specified number of rows
    pd.set_option('display.width', None)        # automatically adjust display width

    # display head, tail, or stats
    if head: print(df.head(nrows))
    elif tail: print(df.tail(nrows))
    elif desc: print(df.describe())
    elif corr: print(df.corr())
    elif count: print(df.nunique())
    else: print(df)

    # file conversion using the processed dataframe
    output_filename = file.split('.')[0]
    if to_csv: df.to_csv(output_filename + '.csv', index=False)
    elif to_tsv: df.to_csv(output_filename + '.tsv', sep='\t', index=False)
    elif to_excel: df.to_excel(output_filename + '.xlsx', index=False)
else:
    print("Error: Data could not be loaded. Please check the file format and path.")

# adjust display settings if needed
pd.set_option('display.max_columns', None)  # display all columns
pd.set_option('display.max_rows', nrows)    # display specified number of rows

# display head, tail, or stats
if head: print(df.head(nrows))
elif tail: print(df.tail(nrows))
else: print(df)

# file conversion using the processed dataframe
output_filename = file.split('.')[0]
if to_csv: df.to_csv(output_filename + '.csv', index=False)
elif to_tsv: df.to_csv(output_filename + '.tsv', sep='\t', index=False)
elif to_excel: df.to_excel(output_filename + '.xlsx', index=False)
