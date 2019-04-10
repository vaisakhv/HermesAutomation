__author__name__ = "Vaisakh Viswanathan"
__author__ = 'U51855'


from path import Path

import os, sys, subprocess

# def selection(sel):
#     if sel == 1:
#         os.system(shiftUpdate.main())
#     elif sel == 2:
#         os.system(trackerV2.getCriticalJobStatus())
#
# def disp():
#     print("Enter the Appropriate number")
#     print("1.   Shift Update")
#     print("2.   Monitoring Tracker")
#     selection(int(input("Your selection: ")))


def installDeps():

    commands = {
        "proxy" : "SET HTTPS_PROXY=gateway.zscaler.net:9400",
        "paramiko" : "pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org paramiko" ,
        "getpass" : "pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org getpass2"
    }

    subprocess.call(commands["proxy"], shell=True)
    try:
        import paramiko
        print("Paramiko : Already installed")
    except ImportError:
        subprocess.call(commands["paramiko"], shell=True)
    try:
        import getpass
        print("getpass : Already installed")
    except ImportError:
        subprocess.call(commands["getpass"], shell=True)

    createBats()

def createBats():
    out = subprocess.Popen("where python", stdout=subprocess.PIPE,shell=True)
    path = out.communicate()[0].strip().decode('ascii')
    programs = {
    "trackerV2" : "cmd /k "+path+" "+os.path.realpath("trackerV2.py"),
    "shiftUpdate" : "cmd /k "+path+" "+os.path.realpath("shiftUpdate.py")
    }
    print("Creating shortcut bat files")
    for one in programs.keys():
        print(os.path.join(sys.path[0])+"//"+one)
        bat = open(os.path.join(sys.path[0])+"//"+one+".bat", "w")
        bat.write(programs[one])

if __name__ == '__main__':
    installDeps()
