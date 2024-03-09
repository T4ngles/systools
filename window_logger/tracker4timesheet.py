"""
	Window Logger

		To log activity during work hours and summarise time spent on tasks for
		billing time to projects.
	
	to add:
		[ ]Inactivity check based on mouse cursor position
		[ ]Grouping of tasks using regex matching and stored application name list       
		[ ]Summary of tasks logged
		[ ]visualisation of tasks logged for day
		[ ]alerts based on time logged for task with long time
		   
"""

from win32gui import GetWindowText, GetForegroundWindow
import datetime
import time
import csv
import asyncio
import threading
import os
import sys

#async def track():

#TODO: add in activity class and activity dictionary
class Window_Task:
	_tasks_dict = {}

	def __init__(self, name, time_Spent=0):
		self.name = name
		time_Spent = time_Spent

	def calc_Time_Spent(self):
		pass

	@classmethod
	def time_Summary(cls):
		for key, value in _tasks_dict.values():
			print(key, value)

logs_path = os.path.dirname(sys.argv[0]) + "\\window_logs\\"

def writeLogEntry(path,activity,timestamp_old,timestamp_new):
	try: 
		test = os.listdir(path)
	except FileNotFoundError:
		os.mkdir(path)
	with open(path + 'timesheet'+str(datetime.datetime.now().strftime("%y-%m-%d"))+'.csv', 'a', newline='', encoding="utf-8") as f:	
		write = csv.writer(f)
		write.writerow((activity,timestamp_old,timestamp_new))

timestamp_old = datetime.datetime.now().strftime("%m-%d %H:%M")
activity = str(GetWindowText(GetForegroundWindow()))

print("="*20)
print("Activity Tracking Started ", datetime.datetime.now().strftime("%m-%d %H:%M"))
print("="*20)

print(timestamp_old,activity)

while int(datetime.datetime.now().strftime("%H")) < 17:
	
	timestamp_new = datetime.datetime.now().strftime("%H:%M:%S")
	
	if activity != str(GetWindowText(GetForegroundWindow())):
		
		print(timestamp_old,"-", timestamp_new, ":", activity)
		writeLogEntry(logs_path,activity,timestamp_old,timestamp_new)
		activity = str(GetWindowText(GetForegroundWindow()))
		timestamp_old = datetime.datetime.now().strftime("%H:%M:%S")
	
	#await asyncio.sleep(10)
	#threading.Event().wait(10)
	time.sleep(1)    

#asyncio.run(track())

# with open('timesheet'+str(datetime.datetime.now().strftime("%m-%d"))+'.csv', 'w', newline='', encoding="utf-8") as f:
	
#     write = csv.writer(f)
#     write.writerows(timesheet_list)

