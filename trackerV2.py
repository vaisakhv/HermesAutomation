__author__name__ = "Vaisakh Viswanathan"
__author__ = 'U51855'


import csv, os, gc, datetime
import shiftUpdate

def findStatus(startTime ,found, scheduleTime):
    # x = line
    end =''
    startTime = datetime.datetime.strptime(startTime, "%H:%M")
    minusEarly = datetime.datetime.strptime(scheduleTime, "%H:%M") -\
                    datetime.timedelta(minutes=15)
    plusLate = datetime.datetime.strptime(scheduleTime, "%H:%M") +\
                    datetime.timedelta(minutes=15)
    earlyMax = datetime.datetime.strptime(scheduleTime, "%H:%M") -\
                    datetime.timedelta(minutes=30)
    lateMax = datetime.datetime.strptime(scheduleTime, "%H:%M") +\
                    datetime.timedelta(minutes=30)
    startTime = str(startTime).split(" ")[-1][:-3]
    minusEarly = str(minusEarly).split(" ")[-1][:-3]
    plusLate = str(plusLate).split(" ")[-1][:-3]
    earlyMax = str(earlyMax).split(" ")[-1][:-3]
    lateMax = str(lateMax).split(" ")[-1][:-3]
    if found == False:
        if startTime == scheduleTime :
            end = "started ontime at "+startTime.replace("\n",'')+" OK"
            found = True
        elif startTime > scheduleTime :#found == False and
            if startTime > plusLate:
                end = "started Late   at "+startTime.replace("\n",'')+" --Verify"
                found = True
            else:
                end = "started Late   at "+startTime.replace("\n",'')+" OK"
                found = True
            # elif startTime > lateMax and end.endswith("OK"):
            #     end = "No run for +/- 35mins (last run at "+startTime.replace("\n",'')+")"

        if startTime < scheduleTime :
            if startTime < minusEarly:
                end = "started Early  at "+startTime.replace("\n",'')+" --Verify"
            else:
                end = "started Early  at "+startTime.replace("\n",'')+" OK"
            # if startTime < earlyMax:
            #     end = "No run for last 35mins (last run at "+startTime.replace("\n",'')+")"
    return end,found
def getCriticalJobStatus():
    jobFile = os.path.realpath("tracker_24x7.csv")
    criticalJobFile = csv.DictReader(open(jobFile, 'r'), delimiter=',')

    param = {
        "hostname" : "ukprodapp01.int.hlg.de",
        "port" : 22,
        "username" : "HISG234"
    }

    client = shiftUpdate.getConnection(param)

    exclusion = {
        "PMDPEN" : "PMDPEN*",
        "PPSPNF" : "PPSPNF*",
        "PCMPCD" : "PCMPCD*",
        "PPOPEP" : "PPOPEP*",
        "PPOPSP" : "PPOPSP*"
    }
    startJobs = {
        "PMDPN9" : "PMDPN903*", "PCMPMA": "PCMPMA03",
        "PCMPDS" : "PCMPDS03","PPSPH7": "PPSPH703", "PCMPML" : "PCMPML03",
        "PRCPSC" : "PRCPSC03", "PPSPLU" : "PPSPLU03", "PPSPHA" : "PPSPHA03",
        "PPOPSW" : "PPOPSW03","PPSPNX" : "PPSPNX03", "PPSPIN" : "PPSPIN06",
        "PMDPAZ" : "PMDPAZ02", "PPSPSP" : "PPSPSP06", "PCMPMB" : "PCMPMB03",
        "PMIPDT" : "PMIPDT03", "PPRPAL" : "PPRPAL02", "PPCPCL" : "PPCPCL03",
        "PMDPNT" : "PMDPNT03", "PMDPCL" : "PMDPCL03", "PCMPIV" : "PCMPIV02",
        "PMDPN8" : "PMDPN803", "PPTPAZ" : "PPTPAZ02", "PPSPHC" : "PPSPHC03",
        "PCMPH1" : "PCMPH103", "PCOPE8" : "PCOPE803", "PPSPGP" : "PPSPGP02",
        "PMDPEN" : "PMDPEN", "PPSPNF" : "PPSPNF", "PCMPCD" : "PCMPCD",
        "PPOPEP" : "PPOPEP", "PPOPSP" : "PPOPSP"
    }

    partialCmd = "cd /opt/unikix/prd_failover/pulse/history; "
    ls = " ls -lrt "
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    past = datetime.datetime.now() - datetime.timedelta(hours=2, minutes=00)
    past = past.strftime('%H:%M')

    # print(datetime.datetime.now().strftime('%H:%M'), past)
    lateThreshold = ''
    earlyThreshold = ''
    startTime = ''
    scheduleTime = ''
    start = ''
    end  = ''
    secondaryEnd = ''
    for row in criticalJobFile:
        found = False
        end = ""
        try:
            currentJob = str(row["command"])[8:-1]
            if currentJob in startJobs.keys():
                scheduleTime = str(row["Time_of_activity_UK Time"]).replace("\n",'')
                currentTime = datetime.datetime.now().strftime('%H:%M')
                yesterday = datetime.datetime.today()-datetime.timedelta(1)
                yesterday = yesterday.strftime('%m%d%y')
                if len(str(scheduleTime).split(":")[0]) == 1:
                    scheduleTime = "0"+str(scheduleTime)
                if scheduleTime <= currentTime and  scheduleTime >= past :
                    start = "Status of "+currentJob+" scheduled at "+scheduleTime+": "
                    stdin, stdout, stderr = client.exec_command(partialCmd+ls+str(startJobs[currentJob])+"*")
                    try:
                        aixOut = stdout.readlines()
                        for x in aixOut:
                            date = str(x).split(".")[-2]
                            startTime = str(x).split(".")[-1].replace("\n","")
                            if date == today and found != True:
                                if end.endswith(" OK"):
                                    secondaryEnd = end
                                end, found = findStatus(startTime,found, scheduleTime)
                                # end = out[-1]
                                # found = out[0]
                                gc.collect()
                            # elif date == yesterday:
                            #     end =findStatus(x, found, scheduleTime)
                            #     gc.collect()
                    except Exception as e:
                        print("--error--")
                        print(str(e))
                        print(str(stderr))

            if secondaryEnd.endswith(" OK") and end.endswith("--Verify"):
                if currentJob in exclusion.keys():
                    print(start+secondaryEnd+" Crosscheck")
                else:
                    print(start+secondaryEnd)
                end = ''
                secondaryEnd = ''
                found = False
            elif end!='':
                if currentJob in exclusion.keys():
                    print(start+end+" Crosscheck")
                else:
                    print(start+end)
                end = ''
                found = False

        except Exception as e:
            print("--error---")
            print(str(e))
            pass


if __name__ == '__main__':
    getCriticalJobStatus()
