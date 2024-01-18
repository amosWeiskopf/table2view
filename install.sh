#!/bin/bash
curl -o table2view.py https://raw.githubusercontent.com/amosWeiskopf/table2view/main/table2view.py
chmod +x table2view.py
echo 'alias table2view="python3 table2view.py"' >> ~/.bashrc
. ~/.bashrc
rm table2view.py
