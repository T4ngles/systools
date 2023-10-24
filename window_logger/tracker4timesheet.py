from win32gui import GetWindowText, GetForegroundWindow
import datetime
import time
import csv
import asyncio
import threading

#async def track():

timestamp_old = datetime.datetime.now().strftime("%m-%d %H:%M")
activity = str(GetWindowText(GetForegroundWindow()))
timesheet_list = [("Activity","starttime","endtime")]

print("="*20)
print("Activity Tracking Started ", datetime.datetime.now().strftime("%m-%d %H:%M"))
print("="*20)

print(timestamp_old,activity)

while int(datetime.datetime.now().strftime("%H")) < 18:
    
    timestamp_new = datetime.datetime.now().strftime("%H:%M")
    
    if activity != str(GetWindowText(GetForegroundWindow())):
    	
    	print(timestamp_old,"-", activity)
    	timesheet_list.append((activity,timestamp_old,timestamp_new))
    	activity = str(GetWindowText(GetForegroundWindow()))
    	
    timestamp_old = datetime.datetime.now().strftime("%H:%M")
    
    #await asyncio.sleep(10)
    #threading.Event().wait(10)
    time.sleep(10)    

#asyncio.run(track())

with open('timesheet'+str(datetime.datetime.now().strftime("%m-%d"))+'.csv', 'w', newline='', encoding="utf-8") as f:
    
    write = csv.writer(f)
    write.writerows(timesheet_list)