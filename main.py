from pip._vendor import requests 
import tkinter as tk
from datetime import datetime

def get_atomic_time():
    response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
    time_data = response.json()
    utc_datetime = datetime.strptime(time_data['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f%z')
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

root = tk.Tk()
root.title("Atomic Time Clock")

time_label = tk.Label(root, font=('Arial', 30), fg='black')
time_label.pack(expand=True)

def update_time():
    current_time = get_atomic_time()
    time_label.config(text=current_time)
    root.after(1000, update_time)
    
update_time()

root.mainloop()

