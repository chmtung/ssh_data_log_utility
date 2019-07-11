#!/usr/bin/env python
import os
import sys
import shutil
import ecu_ssh_logger_main

def makePythonToExe():
    os.system('pyinstaller -F .\\ecu_ssh_logger_main.py')

def batch_rename():
    # Get path
    directory = os.getcwd()

    # New name
    product = ecu_ssh_logger_main.product_version
    version = ecu_ssh_logger_main.utility_version.replace('.', '_')
    new_name = product + '_temp_logger_' + version + '.exe'

    # Rename command
    src = os.path.join(directory, 'dist' , 'ecu_ssh_logger_main.exe')
    dst = os.path.join(directory, 'dist' , new_name)
    print('\n Rename ecu_ssh_logger_main.exe to ' + new_name)
    os.rename( src, dst )

if __name__ == '__main__':
    makePythonToExe()
    batch_rename()
    sys.exit(1)
