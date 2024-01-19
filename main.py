import sys
import os
import pandas as pd

def read_file_in_chunks(file, chunksize=10000):
    chunks = []
    for chunk in pd.read_csv(file, chunksize=chunksize):
        chunks.append(chunk)
        if len(chunks) * chunksize >= 100000:
            break
    return pd.concat(chunks)

def apply_regex(df, pattern):
    regex_matches = df.astype(str).apply(lambda row: row.str.contains(pattern, na=False))
    return df[regex_matches.any(axis=1)]

def main():
    if len(sys.argv) < 2:
        print("Error: No file specified.")
        return

    file = sys.argv[1]
    ext = file.split('.')[-1]
    nrows, sheet, pattern = 10, 0, None
    head, tail, desc, corr, count, sort_col, sort_order, to_csv, to_tsv, to_excel, random_sample = False, False, False, False, False, None, None, False, False, False, False

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        i += 1
        if i < len(sys.argv):
            val = sys.argv[i]
        else:
            val = None

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
            if val:
                parts = val.split(',')
                if len(parts) == 2:
                    sort_col, sort_order = int(parts[0]), parts[1]
        i += 1

    try:
        file_size = os.path.getsize(file) / (1024 * 1024)  # File size in MB
        if file_size > 10:
            df = read_file_in_chunks(file)
        else:
            if ext == 'csv':
                df = pd.read_csv(file, nrows=nrows)
            elif ext in ['xlsx', 'xls']:
                df = pd.read_excel(file, sheet_name=sheet, nrows=nrows)
            elif ext == 'tsv':
                df = pd.read_csv(file, sep='\t', nrows=nrows)
            else:
                raise ValueError("Unsupported file format.")

        if df is not None:
            if sort_col is not None and sort_order in ['a', 'd']:
                ascending = sort_order == 'a'
                df = df.sort_values(df.columns[sort_col], ascending=ascending)

            if pattern:
                df = apply_regex(df, pattern)

            if random_sample:
                df = df.sample(n=min(nrows, len(df)))

            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', nrows)
            pd.set_option('display.width', None)

            if head: print(df.head(nrows))
            elif tail: print(df.tail(nrows))
            elif desc: print(df.describe())
            elif corr: print(df.corr())
            elif count: print(df.nunique())
            else: print(df)

            output_filename = file.split('.')[0]
            if to_csv: df.to_csv(output_filename + '.csv', index=False)
            elif to_tsv: df.to_csv(output_filename + '.tsv', sep='\t', index=False)
            elif to_excel: df.to_excel(output_filename + '.xlsx', index=False)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
