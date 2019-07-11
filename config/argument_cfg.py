
import argparse
import os

def parseArgs():
    parser = argparse.ArgumentParser()
    # '-t'                  : argument
    # '--test'              : argument2
    # dest='test_mode'      : argu variable name
    # action='store_true'   : argu variable is bool (ture/false)
    # help                  : explain in help
    parser.add_argument('-t', '--test', dest='test_mode', action='store_true', help='Question for customer could be ignored in test mode.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    parseArgs()
    os.system('pause')