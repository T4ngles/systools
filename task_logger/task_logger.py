"""
    Task Logger
    to add:
        CLI task adder
        export csv of tasks
        add voice recognition
        Kivy android app compile
"""

import os
import csv
import datetime

def task_log(task_list,task_name):
    start_time = str(datetime.datetime.now().strftime("%H:%M"))
    print(task_name, ": ", start_time)
    task_list.append([start_time,task_name])

def main():
    
    task_list = []
    task_name = ""

    start_time = str(datetime.datetime.now().strftime("%H:%M"))
    print("#"*60)
    print("Log started at", str(start_time))

    while task_name != "end":
        task_name = input("Task:")
        task_log(task_list, task_name)

    print(os.path.split(os.path.abspath(__file__))[0])
    logs_path = str(os.path.split(os.path.abspath(__file__))[0]) + "\\logs\\"
    
    #compare new hashlist to old and write out new hash summary log
    log_name = logs_path + str(datetime.datetime.now().strftime("%d-%m-%Y"))+' - task_log.csv'     
    
    with open(log_name, 'a', encoding='utf-8', newline='') as csvfile:
        
        writer = csv.writer(csvfile)
        writer.writerows(task_list)

    end_time = str(datetime.datetime.now().strftime("%H:%M"))
    
    print("Log ended at", str(end_time))
    print("#"*60)
    
    print("log file saved at " + log_name)

            
if __name__ == '__main__':
    main()
