# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:36:19 2019

@author: U51855
"""
import pandas as pd
import numpy as np
import trackerV2

def color(val):
    if val == "OK":
        color = 'green'
    elif val == "--Verify":
        color = 'red'
    else:
        color = 'amber'
    return 'background-color: %s' % color
    
def test():
    startJobs = {
        "PMDPN9" : "PMDPN903*", "PCMPMA": "PCMPMA03","PCMPDS" : "PCMPDS03",
        "PPSPH7": "PPSPH703", "PCMPML" : "PCMPML03", "PRCPSC" : "PRCPSC03",
        "PPSPLU" : "PPSPLU03", "PPSPHA" : "PPSPHA03", "PPOPSW" : "PPOPSW03",
        "PPSPNX" : "PPSPNX03", "PPSPIN" : "PPSPIN06", "PMDPAZ" : "PMDPAZ02",
        "PPSPSP" : "PPSPSP06", "PCMPMB" : "PCMPMB03", "PMIPDT" : "PMIPDT03",
        "PPRPAL" : "PPRPAL02", "PPCPCL" : "PPCPCL03", "PMDPNT" : "PMDPNT03",
        "PMDPCL" : "PMDPCL03", "PCMPIV" : "PCMPIV02", "PMDPN8" : "PMDPN803",
        "PPTPAZ" : "PPTPAZ02", "PPSPHC" : "PPSPHC03", "PCMPH1" : "PCMPH103",
        "PCOPE8" : "PCOPE803", "PPSPGP" : "PPSPGP02", "PMDPEN" : "PMDPEN",
        "PPSPNF" : "PPSPNF", "PCMPCD" : "PCMPCD", "PPOPEP" : "PPOPEP",
        "PPOPSP" : "PPOPSP", "PCMPST" : "PCMPST03"
    }
    
    out = trackerV2.getCriticalJobStatus()
    for job in startJobs.keys():
      if job in out.keys():
          pass
      else:
          out[job] = 'No run '
    nestedVal = [o for o in out.values()]
    nestedName = [n for n in out.keys()]
    #status = np.array(nested)
    df = pd.DataFrame({"Job Name":nestedName,"Job Status":nestedVal})
    #df.style.applymap(color, subset=['Job Status']).render()
    #df.style.set_properties(**{'font-size': '9pt', 'font-family': 'Calibri'}).render()
    #html = df.to_html(index=False)
    html = (
        df.style
        .applymap(color, subset=['Job Status'])
        .set_properties(**{'font-size': '9pt', 'font-family': 'Calibri'})

        .render()
        )
    f = open("out.html", 'w')
    f.write(html)
    f.close
    
    
test()
