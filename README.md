# table2view

table2view is a command-line tool that brings the power of pandas data manipulation to the terminal. It allows users to perform various data operations on CSV, XLSX, and TSV files directly from the command line.
Features

 - Read large files in chunks
 - Filter data by regex
 - Perform basic data operations like head, tail, describe, correlation, and count
 - Random data sampling
 - Sort data by specified columns
 - Convert files between CSV, TSV, and Excel formats

## Why table2view?

- **Effortless Installation**
- **User-Friendly**: Designed with simplicity in mind.
- **Versatile**: Crafted to work with CSV, TSV and Excel files
- **Powerful**: Converts, filters, sorts, slices, and dices your data with ease.
- **Lightweight**: No heavy dependencies, just pure efficiency.

## Installation

To install table2view, run the following command in your linux terminal:

```curl -sSL https://raw.githubusercontent.com/amosWeiskopf/table2view/main/install.sh | bash```

### This script will:

 - Create a directory at ~/.scripts
 - Download table2view.py to this directory
 - Set the necessary permissions
 - Create an alias in your .bashrc file

## Usage

After installation, you can use table2view as follows:

```table2view [file] [options]```

Options

 - --rows [number]: Specify the number of rows to read.
 - --sheet [number]: For Excel files, specify the sheet number.
 - --regex [pattern]: Apply a regex pattern to filter rows.
 - --head: Display the first few rows of the file.
 - --tail: Display the last few rows of the file.
 - --random: Randomly sample data from the file. **Currently buggy**.
 - --toCsv: Convert the file to CSV format.
 - --toExcel: Convert the file to Excel format.
 - --toTsv: Convert the file to TSV format.
 - --desc: Display statistical summaries. **Currently buggy**.
 - --corr: Display correlation matrix. **Currently buggy**.
 - --count: Display count of unique values. **Currently buggy**.
 - --sort [column_index][a/d]: Sort by the specified column. 'a' for ascending, 'd' for descending. **Currently buggy**.

Examples

```
# Display the first 10 rows of a CSV file
table2view data.csv --head --rows 10
```

```
# Sort an Excel file by the first column in descending order and convert it to CSV
table2view data.xlsx --sort 0d --toCsv
```

## Uninstallation

To uninstall table2view, run:

```curl -sSL https://raw.githubusercontent.com/amosWeiskopf/table2view/main/install.sh | bash -s -- uninstall```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on the GitHub repository.
License


## Roadmap for `table2view`

### Immediate enhancements
- **Test & optimize data loading** for large files.
- **Refine CLI** for more intuitive user commands.

### Near-term goals
- **Implement data plotting** via the terminal
- **Support Additional Formats** like JSON, XML, Parquet files.
- **Advanced Data Operations** like group-by, join, and pivot functionalities.

### Mid-term objectives
- **Develop Interactive Mode** to allow users to manipulate and view data in an interactive shell.
- **Plugin Framework** system for users to add custom commands or functionalities.

### Long-term vision
- **Graphical User Interface**
- **Machine Learning integration** for simple ML tasks (e.g., linear regression, clustering).
- **Cloud functionality** for cloud-based data processing and storage.

### Continuous improvement
- **User feedback loop**: I want to regularly update the tool based on user reviews and suggestions. Please send me your ideas, or feel free to contribute to the codebase.
- **Regular Security Audits**

## Aspirational goal
- **Standardization**: Position `table2view` as a go-to tool in data analysis and manipulation communities.

_Note: This roadmap is adaptive and will evolve based on technological advancements and community feedback._


## Author
Amos Weiskopf (amosWeiskopf on GitHub)

This project is licensed under MIT.

## MIT License

Copyright (c) 2024 Amos Weiskopf.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
