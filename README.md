# HermesAutomation

This project's main intention is to reduce the man hours by semi-automating the mundane and repetitive tasks.

The two major programs in this project are:

1. ShiftUpdate
  Automatically grabs all the time of the jobs that ahev to filled in the shift update mail.
  The ouput is excactly the same as that of the content of the shift update mail upto the the brackets and spaces.
  [ETL timings has to entered manually]

2. TrackerV2
  This is a program to replace the repetitive task of 24x7 monitoring tracker.
  Instead of copying the commands from the tracker and running it in Putty and finding whether the job ran at the specified time, the user   can just run rhis script and enter the password for the server. The program will display the jobs for the last 2 hours and the satus       based on the run time vs the scheduled time (ontime/Late/Early). If the job ran within a window of 15mins (ie., scheduled time +/-         15mins) along with the statu it will show "OK" else "--Verify"
  In the case of jobs without a specific start job it show the status and along with that it will display "Crosscheck", which is a info     for the user to check whether the data shown is correct.
  This script uses the csv file Tracker24x7 to get the time and job names. this only has 2 columns "time of activity" and "commands"
  
The third script main.py is kind of an installer file. This will install the necesseray packages and create ".bat" file in the same directory where all the file is present. This can be used to run the programs at a click.
 
More scripts will be added to this as the work progresses.
Like Trigger checking programs for triggered jobs like PCMPMA
