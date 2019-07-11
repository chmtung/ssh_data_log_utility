import sys
import time
import paramiko
import os
import datetime
import xlwt
import msvcrt
import subprocess
import socket
from ui import cconsole
from ui import DisplayBoard
from config import argument_cfg
from windows import environ

#------------CONFIG-----------------------
utility_version  = 'v1.1'
product_version  = 'ESOM012-ECU01'
HOST_IP          = '192.168.10.3'
N310_CHECK_CMD   = 'uhd_usrp_probe --version'
N310_READ_CMD    = 'uhd_usrp_probe --sensor /mboards/0/sensors/temp'
SEARCH_IP_RETRY  = 5                # times
CHECK_N310_RETRY = 5                # times
LOGGING_INTERVAL = 300              # sec
READ_PERIOD      = 10               # sec
#-----------------------------------------

welcome_msg =(
"""
***************************************************************************************************
#                                     Delta Electronics, Inc.                                     #
#                                          ICTBG/CISBG                                            #
#                             SSH Temp Log Utility product_version utility_version                #
#                                                                                                 #
#                             Applicable system: Microsoft Windows 10                             # 
#                                                Microsoft Windows 7                              #
#                                                                                                 #    
#                             Applicable sku:                                                     #
#                                        ECU01                                                    #
#                                                                                                 #
***************************************************************************************************
""")
note_msg = (
"""
Before the upgrade process, please read following note massage carefully.
Note to test:
1. Only use applicable sku which are listed in the welcome massage.
2. DC  power (48 V) should be supplied to the unit.
3. Config local IP address to 192.168.10.XX  (Except for 192.168.10.1 or 192.168.10.3) 
""")


class EcuN310SshLogger(object):
    _sraech_ip_retry  = SEARCH_IP_RETRY
    _check_n310_retry = CHECK_N310_RETRY
    _serial_umber = 0
    _timeInterval_list = []
    _temperature_lsit = []
    _realTime_list = []
    _total_slope = 0

    def __init__(self, ip, ui, args):
        self.ip = ip
        self.ui = ui
        self.args = args

    def welcomeMassage(self):
        ask_serial_number_msg = 'Please enter the S/N "Last 4 numbers" in 1040009-XXXX (from 0000 to 9999) : '
        welcome_msg_tmp =  welcome_msg.replace("product_version", product_version)
        welcome_msg_tmp =  welcome_msg_tmp.replace("utility_version", utility_version + (" " * 13))
        self.ui.printI(welcome_msg_tmp)
        time.sleep(1.5)
        self.ui.printI(note_msg)
        if self.args.test_mode:
            # Skip question
            self._serial_umber = '1040009-0000'
        else:
            while True:
                sn = input(self.ui.returnI(ask_serial_number_msg))
                # Check input is a int number
                if sn.isdigit() and (len(sn) is 4):
                    sn = int(sn)
                    if (sn >= 0000) and (sn <= 9999):
                        self._serial_umber = '1040009-' + str(sn)
                        break
        return True

    def checkOperatingSystem(self):
        """Check is Windows 7, 8, 10"""
        result = False
        self.ui.registerDisplayBoard("Checking PC operating system")
        if environ.isApplicableOs():
            self.ui.logPassMsg(environ.getOsInformation())
            result = True
        else:
            self.ui.logTroubleshooting("PC OS is not applicable")
            self.ui.logFailMsg(environ.getOsInformation())
            result = False
        return self.ui.printDisplayBoard(result)

    def isIpValid(self):
        myip = socket.gethostbyname(socket.gethostname())
        myip = myip.split('.')
        target_ip = HOST_IP.split('.')
        for i in range(4):
            if i < 3:
                if myip[i] != target_ip[i]:
                    return False
            elif i == 3:
                if (myip[i] == target_ip[i]) or (myip[i] == '1'):
                    return False
        return True

    def checkTargetIp(self):
        """Check IP is correct"""
        result = False
        self.ui.registerDisplayBoard("Checking target IP")

        while self._sraech_ip_retry > 0:
            self.ui.setIndent("Lv3")
            self.ui.printIAnyway('Ping target IP...\n')
            status, result = subprocess.getstatusoutput('ping ' + self.ip)
            if status is 0:
                result = True
                self.ui.logPassMsg('Target IP:' + self.ip)
                break

            self._sraech_ip_retry -= 1
            time.sleep(1)
        if self._sraech_ip_retry is 0:
            result = False
            self.ui.logFailMsg('Checking IP is timeout, please check the ethernet connection')
            self.ui.logFailMsg('Invalid host IP : ' + socket.gethostbyname(socket.gethostname()))
            self.ui.logFailMsg('Address should be 192.168.10.XX  (Except for 192.168.10.1 or 192.168.10.3)')
        return self.ui.printDisplayBoard(result)

    def checkN310Feedback(self):
        """Check N310 can send temperature"""
        temperature = ''
        result = False
        self.ui.registerDisplayBoard("Checking feedback from N310")
        while self._check_n310_retry > 0:
            self.ui.setIndent("Lv3")
            self.ui.printIAnyway('Wait N310 initialization...\n')
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(HOST_IP, username='root', password='')
                stdin, stdout, stderr = ssh.exec_command(N310_CHECK_CMD, timeout=10)
                version = str(stdout.read())
                version = version[2:10]
                ssh.close()
                result = True
                self.ui.logPassMsg("N310 fw version : " + version)
                break
            except:
                ssh.close()

            self._check_n310_retry -= 1
            if self._check_n310_retry is 0:
                result = False
                self.ui.logFailMsg('Checking feedback is timeout.')
                break
        time.sleep(30)
        return self.ui.printDisplayBoard(result)

    def readTemperature(self):
        result = False
        global exe_stamp
        global exe_stamp_prev
        global exe_interval

        self.ui.printI('\nYou can keep pressing [e] or [E] to escape\n')

        # Open an SSH handler
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST_IP, username='root', password='')
        #shell = ssh.invoke_shell()

        while True:
            # Execute command and get results.
            # e.g. stdin, stdout, stderr = ssh.exec_command('ifconfig eth0')
            stdin, stdout, stderr = ssh.exec_command(N310_READ_CMD, timeout=10)
            temperature = str(stdout.read())

            # Replace temperature string format from [b'42.0\n] to [42]
            if temperature is not '' and temperature[2:4].isdigit():
                temperature = int(temperature[2:4])
                while (exe_stamp - exe_stamp_prev) < READ_PERIOD:
                    exe_stamp = time.time()
                exe_stamp_prev = exe_stamp
                exe_interval += READ_PERIOD

                present_time = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')

                if exe_interval < 100:
                    output_string = present_time + '   ' + str(exe_interval) + ' sec' + '    ' + str(temperature) + ' degree'
                else:
                    output_string = present_time + '   ' + str(exe_interval) + ' sec' + '   ' + str(temperature) + ' degree'
                # Data collection
                self.ui.printI(output_string)
                self._realTime_list.append(present_time)
                self._timeInterval_list.append(exe_interval)
                self._temperature_lsit.append(temperature)

            time.sleep(1)
            # Leave break
            if msvcrt.kbhit():
                answer = ord(msvcrt.getch())
                if (answer is ord("e")) or (answer is ord("E")):
                    result = True
                    break
            if exe_interval >= LOGGING_INTERVAL:
                result = True
                break
        # Close connection.
        ssh.close()

        return result

    def verifyData(self):
        n = len(self._timeInterval_list)
        if n is 0:
            return False

        x = int(self._temperature_lsit[n-1])
        y = int(self._temperature_lsit[0])
        self._total_slope = (x - y)/(n * READ_PERIOD)
        self.ui.printI('Total slope is '+ str(self._total_slope) + ' (degree/sec)')
        return True

    def logData(self):
        COL_REAL_TIME    = 0
        COL_PASSING_TIME = 1
        COL_TEMPERATURE  = 2
        directory = os.getcwd()

        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('mysheet', cell_overwrite_ok=True)

        sheet.write(0, COL_TEMPERATURE, self._serial_umber)
        for i in range(len(self._timeInterval_list)):
            row = i+1
            sheet.write(row, COL_REAL_TIME, self._realTime_list[i])
            sheet.write(row, COL_PASSING_TIME, self._timeInterval_list[i])
            sheet.write(row, COL_TEMPERATURE, self._temperature_lsit[i])

        sheet.write(row+1, COL_PASSING_TIME, 'Total slope')
        sheet.write(row+1, COL_TEMPERATURE, self._total_slope)
        time_stamp = datetime.datetime.now()
        file_name = self._serial_umber + '-ESOM012-ECU01_log' + time_stamp.strftime('_%Y.%m.%d_%Hh%Mm') + '.xls'
        excel_dic = os.path.join(directory, file_name)
        book.save(excel_dic)

        self.ui.printI('Data log is saved in ' + file_name)
        return True


    def execute(self):
        # 0.1.
        if not self.welcomeMassage():
            return False
        # ------------------------- CHECK SECTION ------------------------------
        self.ui.setIndent("Lv1")
        self.ui.printI("\n\nTemperature logging task 1 of 3: Check status\n")
        self.ui.setIndent("Lv2")
        # 1.1.
        if not self.checkOperatingSystem():
            return False
        # 1.2.
        if not self.checkTargetIp():
            return False
        time.sleep(5)
        # 1.3.
        if not self.checkN310Feedback():
            return False

        # ---------------------- VERIFICATION SECTION ---------------------------
        self.ui.setIndent("Lv1")
        self.ui.printI("\n\nTemperature logging task 2 of 3: Start to log temperature")
        self.ui.setIndent("Lv2")
        # 2.1.
        if not self.readTemperature():
            return False
        # 2.2.
        if not self.verifyData():
            return False

        # ------------------------- LOGGING SECTION -----------------------------
        self.ui.setIndent("Lv1")
        self.ui.printI("\n\nTemperature logging task 3 of 3: Record data into an excel\n")
        self.ui.setIndent("Lv2")
        # 3.1
        if not self.logData():
            return False
        # Done
        return True

def displayEndMessage(update_result = False):
    ui = DisplayBoard()
    ui.setIndent("Lv1")
    time.sleep(0.5)
    if update_result:
        ui.printI("\nDone!\n\n")
        time.sleep(1)
        os.system('pause')
    else:
        ui.printI("\nTest has been aborted!\n\n")
        time.sleep(1)
        ui.printI("Please input [e] or [E] to escape utility.")
        while(1):
            if msvcrt.kbhit():
                answer = ord(msvcrt.getch())
                if (answer is ord("e")) or (answer is ord("E")):
                    break

def mainFunction():
    global exe_stamp
    global exe_stamp_prev
    global exe_interval

    exe_stamp = 0
    exe_stamp_prev = 0
    exe_interval = 0

    # I.  Config console window size
    cconsole.windowConfig(109, 40, 200)  # width, height, line buffer
    cconsole.quick_edit_mode(False)
    #os.system('quickEdit.bat 2')

    # II. Execute  main procedure
    ui = DisplayBoard()
    args = argument_cfg.parseArgs()
    if args.test_mode:
        logger = EcuN310SshLogger(HOST_IP, ui, args)
        update_result = logger.execute()
    else:
        try:
            logger = EcuN310SshLogger(HOST_IP, ui, args)
            update_result = logger.execute()
        except:
            ui.printI("\nAn unexpected except error occurred.")
            update_result = False

    # III.   Show result
    displayEndMessage(update_result)

if __name__ == '__main__':
    sys.exit(mainFunction())

