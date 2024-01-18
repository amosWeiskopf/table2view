#!/bin/bash
curl -o ~/scripts/table2view.py https://raw.githubusercontent.com/amosWeiskopf/table2view/main/table2view.py
chmod +x ~/scripts/table2view.py
echo 'alias table2view="python3 ~/scripts/table2view.py"' >> ~/.bashrc
source ~/.bashrc
