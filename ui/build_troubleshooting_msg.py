#!/usr/bin/env python

import os
import sys
import xlrd
try:
    from ui import troubleshooting_msg_template
except:
    import troubleshooting_msg_template

FIRST_ROW = 1     # rowItemStart  1
FIRST_COL = 0     # colItemStart 'A"

def generate_output_files(list_msg, output_dir):
    #///////////////////////////////////////////////////////////////////////////
    # 1. generate *.py file
    # 1.1) generate the content of *.py
    c_def = ''
    for msg in list_msg:
        c_def += troubleshooting_msg_template.TROUBLESHOOT_DICTIONARY_DEF % msg

    # 1.2) write the .c file
    fname = os.path.join(output_dir, troubleshooting_msg_template.FILENAME_TROUBLESHOOT_MSG)
    fcontent = troubleshooting_msg_template.TROUBLESHOOT_MSG_TEMPLATE % c_def

    with open(fname, 'w') as ofile:
        ofile.write(fcontent)
    # return OS_SUCCESS


def xls_to_truobleshoot_definitions(xls_filename):
    '''
    # Read the trouble shooting definitions in the Excel file and represent them by
    # a list of following dictionary:
        { 'number:
          'level':
          'ErrorCode':
          'Message':
        }
    '''
    # open the xls file.
    workbook = xlrd.open_workbook(xls_filename)
    sheet = workbook.sheet_by_name("trouble_shooting_msg")

    # read the msgs
    row = FIRST_ROW
    col = FIRST_COL
    list_msg = []
    while row < sheet.nrows:
        name = sheet.cell_value(row, col)
        cell_type = sheet.cell_type(row, col)
        if (name == "") or (cell_type == xlrd.XL_CELL_EMPTY) or (cell_type == xlrd.XL_CELL_BLANK):
            break
        else:
            dic = {}
            dic['number'] = str(int(sheet.cell_value(row, col)))
            dic['level'] = '"'+sheet.cell_value(row, col + 1).strip()+'"'
            dic['errorCode'] = '"'+sheet.cell_value(row, col + 2).strip()+'"'
            dic['message'] = '"""'+sheet.cell_value(row, col + 3).strip()+'"""'
            list_msg.append(dic)
            row += 1

        while row < sheet.nrows:
            name = sheet.cell_value(row, col)
            cell_type = sheet.cell_type(row, col)
            if (name == "") or (cell_type == xlrd.XL_CELL_EMPTY) or (cell_type == xlrd.XL_CELL_BLANK):
                break
            else:
                dic = {}
                dic['number'] = str(int(sheet.cell_value(row, col)))
                dic['level'] = '"' + sheet.cell_value(row, col + 1).strip() + '"'
                dic['errorCode'] = '"' + sheet.cell_value(row, col + 2).strip() + '"'
                dic['message'] = '"""' + sheet.cell_value(row, col + 3).strip() + '"""'
                list_msg.append(dic)
                row += 1


    # generate output file (.py)
    return generate_output_files(list_msg, os.getcwd())

if __name__ == '__main__':
    sys.exit(xls_to_truobleshoot_definitions("troubleshooting_msg.xlsx"))