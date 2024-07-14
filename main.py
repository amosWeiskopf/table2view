import sys
import os
import pandas as pd
from tqdm import tqdm
import argparse
import logging
import chardet
import codecs
# כןכן
def detect_encoding(file):
    """
    Detects the encoding of a file.
    
    Parameters:
    file (str): The path to the file to be analyzed.
    
    Returns:
    str: The detected encoding.
    """
    with open(file, 'rb') as f:
        rawdata = f.read(100000)
    result = chardet.detect(rawdata)
    return result['encoding']

def remove_bom(file, encoding):
    """
    Removes BOM from the file if present.
    
    Parameters:
    file (str): The path to the file.
    encoding (str): The detected encoding of the file.
    
    Returns:
    str: The path to the cleaned file.
    """
    cleaned_file = file + '.cleaned'
    with open(file, 'rb') as f:
        content = f.read()
    if content[:3] == codecs.BOM_UTF8:
        content = content[3:]
    elif content[:2] in [codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE]:
        content = content[2:]
    with open(cleaned_file, 'wb') as f:
        f.write(content)
    return cleaned_file

def try_reading_file(file, encodings, delimiter='\t'):
    """
    Tries reading a file with different encodings until it succeeds.
    
    Parameters:
    file (str): The path to the file to be read.
    encodings (list): A list of encodings to try.
    delimiter (str): The delimiter to use.
    
    Returns:
    pd.DataFrame: The DataFrame.
    """
    for encoding in encodings:
        try:
            cleaned_file = remove_bom(file, encoding)
            with codecs.open(cleaned_file, 'r', encoding) as f:
                return pd.read_csv(f, delimiter=delimiter, header=None)
        except Exception as e:
            logging.warning(f"Failed to read with encoding {encoding}: {e}")
    raise ValueError(f"Failed to read the file with provided encodings: {encodings}")

def clean_data(df):
    """
    Cleans and preprocesses the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Drop any completely empty rows
    df.dropna(how='all', inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    # Handle malformed rows (e.g., rows with fewer columns)
    max_columns = df.apply(lambda row: len(row.dropna()), axis=1).max()
    df = df[df.apply(lambda row: len(row.dropna()), axis=1) == max_columns]

    # Set the first non-empty row as header if needed
    if df.iloc[0].isnull().sum() == 0:
        df.columns = df.iloc[0]
        df = df[1:]

    df.reset_index(drop=True, inplace=True)
    
    return df

def apply_regex(df, pattern):
    """
    Applies a regex pattern to the DataFrame and filters rows containing the pattern.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to be filtered.
    pattern (str): The regex pattern to apply.
    
    Returns:
    pd.DataFrame: The filtered DataFrame.
    """
    regex_matches = df.astype(str).apply(lambda row: row.str.contains(pattern, na=False))
    return df[regex_matches.any(axis=1)]

def print_status_bar(df):
    """
    Prints a status bar with information about the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to display status information for.
    """
    num_rows, num_cols = df.shape
    num_missing = df.isnull().sum().sum()
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # in MB

    status_info = (
        f"Rows: {num_rows}\n"
        f"Columns: {num_cols}\n"
        f"Missing Values: {num_missing}\n"
        f"Memory Usage: {memory_usage:.2f} MB\n"
    )

    print("\n--- Status Bar ---")
    print(status_info)
    print("------------------\n")

def parse_arguments():
    """
    Parses command-line arguments using argparse.
    
    Returns:
    argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Process and analyze a data file.")
    parser.add_argument('file', type=str, help='The path to the file to be processed.')
    parser.add_argument('--rows', type=int, default=10, help='Number of rows to read.')
    parser.add_argument('--sheet', type=int, default=0, help='Sheet number (for Excel files).')
    parser.add_argument('--regex', type=str, help='Regex pattern to filter rows.')
    parser.add_argument('--head', action='store_true', help='Display the first n rows.')
    parser.add_argument('--tail', action='store_true', help='Display the last n rows.')
    parser.add_argument('--random', action='store_true', help='Display a random sample of rows.')
    parser.add_argument('--toCsv', action='store_true', help='Save the output to a CSV file.')
    parser.add_argument('--toExcel', action='store_true', help='Save the output to an Excel file.')
    parser.add_argument('--toTsv', action='store_true', help='Save the output to a TSV file.')
    parser.add_argument('--desc', action='store_true', help='Display descriptive statistics.')
    parser.add_argument('--corr', action='store_true', help='Display the correlation matrix.')
    parser.add_argument('--count', action='store_true', help='Display the count of unique values.')
    parser.add_argument('--sort', type=str, help='Sort the DataFrame by a column (format: column,order).')
    
    return parser.parse_args()

def main():
    """
    Main function to process the file based on command-line arguments.
    """
    logging.basicConfig(level=logging.INFO)
    args = parse_arguments()

    try:
        file = args.file
        ext = file.split('.')[-1]
        nrows = args.rows
        sheet = args.sheet
        pattern = args.regex
        head = args.head
        tail = args.tail
        random_sample = args.random
        to_csv = args.toCsv
        to_excel = args.toExcel
        to_tsv = args.toTsv
        desc = args.desc
        corr = args.corr
        count = args.count
        sort_col, sort_order = None, None

        if args.sort:
            parts = args.sort.split(',')
            if len(parts) == 2:
                sort_col, sort_order = int(parts[0]), parts[1]

        encoding = detect_encoding(file)
        
        # Handle BOM (Byte Order Mark) if present
        if encoding.lower().startswith('utf-16') or encoding.lower().startswith('utf-32'):
            encoding = 'utf-8-sig'

        encodings_to_try = [encoding, 'utf-8-sig', 'utf-8', 'latin1', 'ISO-8859-1']

        if ext == 'csv' or ext == 'tsv':
            delimiter = '\t' if ext == 'tsv' else ','
            df = try_reading_file(file, encodings_to_try, delimiter=delimiter)
        elif ext in ['xlsx', 'xls']:
            df = pd.read_excel(file, sheet_name=sheet, nrows=nrows)
        else:
            raise ValueError("Unsupported file format.")

        df = clean_data(df)

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

        # Print status bar
        print_status_bar(df)

    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
