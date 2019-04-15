from sympy.functions.elementary.complexes import im
__author__name__ = 'Vaisakh Viswanathan'
__author__ = 'U51855'
"""
A Command Line Interface program for fetching the start time for all jobs required in the shift update as of 27th March 2018

**python version 3.5 and above**

dependencies:
paramiko - for establishing SSH connection
getpass - for securely handling the password
cryptography - for encrypted communication with the server
gc - for memory optimization
sys - for handling few exceptions

___________________________If inside UST Proxy____________________________
Terminal settings for UST proxy:
SET HTTPS_PROXY=gateway.zscaler.net:9400
 
Pip command - for installing the dependencies 
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org  <package_name>
__________________________________________________________________________


path = C:\Anaconda3\python.exe
Bat File Content - for executing the script (*Optional*)
create a new .bat file and copy paste the below command and edit the content within "<>"
eg: cmd /k C:\Anaconda3\python.exe D:\Vaisakh\vaisakh\Python\shiftUpdate.py
Now just double click the bat file for executng the script

cmd /k <python_path> <path_to_dir>\shiftUpdate.py
"""
import paramiko
import getpass
import sys, os, gc, webbrowser
import datetime

def getConnection(param):
    '''
    Establishes an SSH connection to the specified server through the specified port using the given credentials
    :param
    hostname
    port
    username
    password
    :return
    client
    '''
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("**Connecting**")
    hostname = param["hostname"]
    port = param["port"]
    username = param["username"]
    password = getpass.getpass('Enter password for '+param["username"]+'@'+param["hostname"]+' : ')#will not echo the input
    try:
        client.connect(hostname,port,username,password)
        print("**Connected to "+username+"@"+hostname+"**")
        return client
    except Exception as e:
        print("Connection failed")
        print(str(e))
        sys.exit("205")


def getAixInfo(client, cmd, jobDispName):
    '''
    gets the start time of all the jobs needed for the shift update as of on 23rd March 2019
    :param
    client
    cmd
    :return
    startTime
    '''

    start = "cd /opt/unikix/prd_failover/pulse/history; " # hist directory
    final = start+cmd #for executing the command passed to the function in the hist directory
    stdin, stdout, stderr = client.exec_command(final)
    try:
        job = stdout.readlines()
        for x in job:
            date = str(x).split(".")[-2]
            startTime = str(x).split(".")[-1]
        #cmd = str(cmd).replace("\n",'')
        return ["Last successful run started at "+jobDispName+"    "+startTime.replace("\n",''), date]
    except:
        print(stderr)

def main():
    param = {
        "hostname" : "ukprodapp01.int.hlg.de",
        "port" : 22,
        "username" : "HISG234"
    }

    client = getConnection(param)
    cmds = ["\nMIS Check","ls -lrt PMIPDT03*",
            "\nWeb Tracking (Amazon) Check","ls -lrt PPTPPP02*", "ls -lrt PPTPPW02*",
            "\nDepot & Hub Jobs","ls -lrt PPSPAD03*", "ls -lrt PPSPAH03*",
            "\nPre Advice Load Check","ls -lrt PMDPCL03*", "ls -lrt PMDPN803*","ls -lrt PMDPN903*", "ls -lrt PMDPNT03*",
            "\nScan Processing Check","ls -lrt PPSPIN06*", "ls -lrt PPSPSP06*","ls -lrt PPSPLU03*",
            "\nManifest load & Printing Check","ls -lrt PCMPMA03*",
            "\nNEXT Sacks Monitoring check","ls -lrt PPSPNX03*", "ls -lrt PPSPNF*"]

    jobLongNames = {
                    "PMIPDT03" :"PMIPDT",
                    "PPTPPP02" : "(to extract data)  PPTPPP",
                    "PPTPPW02" : "(to load data)      PPTPPW",
                    "PPSPAD03" : "PPSPAD03",
                    "PPSPAH03" : "PPSPAH03",
                    "PMDPCL03" : "PMDPCLN_COLSLOAD",
                    "PMDPN803" : "PMDPN8N_PREADVLD",
                    "PMDPN903" : "PMDPN9N_NEXTCOLS",
                    "PMDPNT03" : "PMDPNTN_NEXTPAD",
                    "PPSPIN06" : "PPSPINE_SCANACCM",
                    "PPSPSP06" : "PPSPSPE_SCANLOAD",
                    "PPSPLU03" : "PPSPLUE_UNDLVPCL",
                    "PCMPMA03" : "PCMPMAE_MFSTPRNT",
                    "PPSPNX03" : "PPSPNXE_NEXTTRNK",
                    "PPSPNF" : "PPSPNFE_NEXTSCAN"
                }
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    for c in cmds:
        if str(c).startswith("ls -lrt "):
            out = getAixInfo(client, c, jobLongNames[c[8:-1]])
            date = out[-1]
            line = out[0]
            if date == today:
                print(line)
            else:
                print(line.replace("\n",'')+" ("+date+")")
            gc.collect()
        else:
            print(c)
    client.close()

if __name__ == '__main__':
    main()
