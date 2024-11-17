import psutil
import os
import threading #Лаба для интервалов и корутин
import subprocess
import datetime #Для работы с датой

app_path = r"C:/Users/Максим Б/AppData/Local/Programs/Python/Launcher/py.exe"

def is_script_running(script_name):
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any(script_name in arg for arg in proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def ChecScripts():

    if is_script_running('ChecDublicates_Script.py'):
        print("Скрипт DelDublicat запущен.")
    else:
        print("Скрипт DelDublicat не запущен.")
        subprocess.Popen(["start", app_path, "../DelDublicat/ChecDublicates_Script.py"], shell=True)

    #if is_script_running('Check_NoWork_Agents.py'):
    #    print("Скрипт NoWorkAgents запущен.")
    #else:
    #    print("Скрипт NoWorkAgents не запущен.")
    #    subprocess.Popen(["start", app_path, "../NoWorkAgents/Check_NoWork_Agents.py"], shell=True)

    #if is_script_running('SendDailyCode.py'):
    #    print("Скрипт SendCode запущен.")
    #else:
    #    print("Скрипт SendCode не запущен.")
    #    subprocess.Popen(["start", app_path, "../SendCode/SendDailyCode.py"], shell=True)

    if is_script_running('CheckDeals_InWork_Sctipt.py'):
        print("Скрипт CheckDeals_InWork запущен.")
    else:
        print("Скрипт CheckDeals_InWork не запущен.")
        subprocess.Popen(["start", app_path, "../CheckDeals_InWork/CheckDeals_InWork_Sctipt.py"], shell=True)

    if is_script_running('CheckTests_Script.py'):
        print("Скрипт CheckTests запущен.")
    else:
        print("Скрипт CheckTests не запущен.")
        subprocess.Popen(["start", app_path, "../CheckTests/CheckTests_Script.py"], shell=True)

    if is_script_running('ReservBery_Script.py'):
        print("Скрипт ReservBery запущен.")
    else:
        print("Скрипт ReservBery не запущен.")
        subprocess.Popen(["start", app_path, "../ReservBery/ReservBery_Script.py"], shell=True)

    if is_script_running('CheckUnix.py'):
        print("Скрипт CheckUnix запущен.")
    else:
        print("Скрипт CheckUnix не запущен.")
        subprocess.Popen(["start", app_path, "../CheckUnix/CheckUnix.py"], shell=True)

    if is_script_running('StopPause_WorkTime.py'):
        print("Скрипт StopPause_WorkTime запущен.")
    else:
        print("Скрипт StopPause_WorkTime не запущен.")
        subprocess.Popen(["start", app_path, "../StopPause_WorkTime/StopPause_WorkTime.py"], shell=True)

    if is_script_running('ReplyWorkTimeBot.py'):
        print("Скрипт ReplyWorkTimeBot запущен.")
    else:
        print("Скрипт ReplyWorkTimeBot не запущен.")
        subprocess.Popen(["start", app_path, "../StopPause_WorkTime/ReplyWorkTimeBot.py"], shell=True)

    print("")
    current_datetime = datetime.datetime.now()
    print("Закончил: ", current_datetime)

    print("")
    print("--------------------------------------------")
    print("")
  
    

#Вызываю основные функции в интерале 15мин (900сек)
def printit():
  print("")
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)
  print("")

  ChecScripts()
  threading.Timer(900, printit).start()

printit()
