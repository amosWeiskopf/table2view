#!/bin/bash

install_table2view() {
    mkdir -p ~/.scripts
    curl -o ~/.scripts/table2view.py https://raw.githubusercontent.com/amosWeiskopf/table2view/main/main.py
    chmod +x ~/.scripts/table2view.py
    if ! grep -q 'alias table2view=' ~/.bashrc; then
        echo 'alias table2view="python3 ~/.scripts/table2view.py"' >> ~/.bashrc
    fi
    source ~/.bashrc
}

uninstall_table2view() {
    rm -f ~/.scripts/table2view.py
    sed -i '/alias table2view/d' ~/.bashrc
    echo "table2view has been successfully uninstalled."
}

if [ "$1" = "uninstall" ]; then
    uninstall_table2view
else
    install_table2view
    echo "table2view has been successfully installed."
fi
