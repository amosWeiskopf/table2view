import sys
import os
import pandas as pd

def read_csv_in_chunks(filepath, chunksize=10000, max_rows=100000):
    """Reads a large CSV file in chunks to avoid memory issues."""
    chunk_container = pd.read_csv(filepath, chunksize=chunksize)
    chunks = []
    for number, chunk in enumerate(chunk_container):
        if number * chunksize < max_rows:
            chunks.append(chunk)
        else:
            break
    return pd.concat(chunks, ignore_index=True)

def read_file(filepath, file_ext, nrows=10, sheet=0):
    """Reads file based on file extension."""
    if file_ext == 'csv':
        return pd.read_csv(filepath, nrows=nrows)
    elif file_ext in ['xlsx', 'xls']:
        return pd.read_excel(filepath, sheet_name=sheet, nrows=nrows)
    elif file_ext == 'tsv':
        return pd.read_csv(filepath, sep='\t', nrows=nrows)
    return None

def apply_filters(df, args):
    """Applies various filters and operations to the dataframe."""
    if 'sort_col' in args:
        df.sort_values(df.columns[args['sort_col']], ascending=args.get('sort_order', 'a') == 'a', inplace=True)
    if 'pattern' in args and args['pattern']:
        pattern = args['pattern']
        df = df[df.astype(str).apply(lambda row: row.str.contains(pattern)).any(axis=1)]
    if 'random_sample' in args and args['random_sample']:
        df = df.sample(n=args.get('nrows', 10))
    return df

def output_data(df, filepath, args):
    """Outputs data to various formats based on arguments."""
    base_filename = os.path.splitext(filepath)[0]
    if args.get('to_csv'):
        df.to_csv(f'{base_filename}.csv', index=False)
    if args.get('to_tsv'):
        df.to_csv(f'{base_filename}.tsv', sep='\t', index=False)
    if args.get('to_excel'):
        df.to_excel(f'{base_filename}.xlsx', index=False)

def main():
    args = { '--rows': int, '--sheet': int, '--regex': str, '--sort_col': int, '--sort_order': str, 
             '--toCsv': bool, '--toTsv': bool, '--toExcel': bool, '--random': bool }
    parsed_args = {}

    for i in range(2, len(sys.argv), 2):
        arg, val = sys.argv[i], sys.argv[i+1] if i+1 < len(sys.argv) else None
        if arg in args:
            parsed_args[arg[2:]] = args[arg](val) if val is not None else True

    filepath = sys.argv[1]
    file_ext = filepath.split('.')[-1]
    file_size = os.path.getsize(filepath) / (1024 * 1024)  # File size in MB

    df = read_csv_in_chunks(filepath) if file_size > 10 else read_file(filepath, file_ext, **parsed_args)
    
    if df is not None:
        df = apply_filters(df, parsed_args)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', parsed_args.get('nrows', 10))
        pd.set_option('display.width', None)

        if 'head' in parsed_args: print(df.head(parsed_args['nrows']))
        elif 'tail' in parsed_args: print(df.tail(parsed_args['nrows']))
        elif 'desc' in parsed_args: print(df.describe())
        elif 'corr' in parsed_args: print(df.corr())
        elif 'count' in parsed_args: print(df.nunique())
        else: print(df)

        output_data(df, filepath, parsed_args)
    else:
        print("Error: Data could not be loaded. Please check the file format and path.")

if __name__ == "__main__":
    main()
