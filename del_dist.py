#!/usr/bin/env python
import os
import shutil

def clearDistFolder():
    if os.path.exists('dist'):
        shutil.rmtree('dist')

if __name__ == '__main__':
    clearDistFolder()