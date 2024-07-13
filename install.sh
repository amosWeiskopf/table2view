#!/bin/bash

# Function to check Python and Pandas installation
check_dependencies() {
    # Check Python installation
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 is not installed. Installing..."
        sudo apt-get install python3
    fi

    # Check Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo "Python version $PYTHON_VERSION found."

    # Check for pandas installation
    if ! python3 -c "import pandas" &> /dev/null; then
        echo "Pandas is not installed. Installing..."
        pip3 install pandas || sudo apt-get install python3-pandas
        pip3 install chardet || sudo apt-get install python3-chardet

    fi
}

# Function to install table2view
install_table2view() {
    check_dependencies

    echo "Creating directory ~/.scripts"
    mkdir -p ~/.scripts && echo "Directory created."

    echo "Downloading table2view.py..."
    if curl -o ~/.scripts/table2view.py https://raw.githubusercontent.com/amosWeiskopf/table2view/main/main.py; then
        echo "Download successful."
    else
        echo "Error in downloading file."
        exit 1
    fi

    chmod +x ~/.scripts/table2view.py
    echo "Permissions set for table2view.py."

    # Remove existing alias from .bashrc if it exists
    if grep -q "alias table2view=" ~/.bashrc; then
        sed -i '/alias table2view=/d' ~/.bashrc
        echo "Existing alias removed from .bashrc."
    fi

    # Add new alias to .bashrc
    echo 'alias table2view="python3 ~/.scripts/table2view.py"' >> ~/.bashrc
    echo "New alias added to .bashrc."

    # Reload .bashrc
    . ~/.bashrc
    echo "Installation complete. You can now use table2view."
}

# Function to simulate installation (dry run)
dry_run() {
    echo "Performing a dry run of the installation..."
    check_dependencies
    echo "Would create directory ~/.scripts"
    echo "Would download table2view.py to ~/.scripts"
    echo "Would set permissions for table2view.py"
    echo "Would update .bashrc with the new alias"
    echo "Dry run complete."
}

# Function to uninstall table2view
uninstall_table2view() {
    if [ -f ~/.scripts/table2view.py ]; then
        rm -f ~/.scripts/table2view.py
        echo "table2view.py removed from ~/.scripts."
    else
        echo "table2view.py not found in ~/.scripts."
    fi

    if grep -q "alias table2view=" ~/.bashrc; then
        sed -i '/alias table2view=/d' ~/.bashrc
        echo "Alias removed from .bashrc."
    else
        echo "Alias not found in .bashrc."
    fi

    echo "table2view has been successfully uninstalled."
}

# Check for arguments
if [ "$1" = "uninstall" ]; then
    uninstall_table2view
elif [ "$1" = "dryrun" ]; then
    dry_run
else
    install_table2view
    echo "Post-Installation Instructions: To start using table2view, simply type 'table2view' in your terminal."
fi
