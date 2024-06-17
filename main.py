import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
from datetime import datetime
import pandas as pd

def get_atomic_time():
    response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
    time_data = response.json()
    utc_datetime = datetime.strptime(time_data['utc_datetime'], '%Y-%m-%dT%H:%M:%S.%f%z')
    return utc_datetime.strftime('%Y-%m-%d %H:%M:%S')

def get_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 42.8333,
        "longitude": 12.8333,
        "hourly": "temperature_2m"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract the hourly temperature data
    hourly_data = data['hourly']['temperature_2m']

    # Extract the time data
    time_data = data['hourly']['time']

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame({
        'time': time_data,
        'temperature_2m': hourly_data
    })

    return df

def plot_weather_data(df):
    fig = Figure(figsize=(10, 5))
    a = fig.add_subplot(111)
    a.plot(df['time'], df['temperature_2m'], label='Temperature (2m)')
    a.set_xlabel('Time')
    a.set_ylabel('Temperature (2m)')
    a.set_title('Hourly Temperature (2m)')
    a.legend()

    return fig

def update_time():
    current_time = get_atomic_time()
    time_label.config(text=current_time)
    root.after(1000, update_time)  # update time every second

def update_weather():
    df = get_weather_data()
    fig = plot_weather_data(df)
    canvas.figure = fig
    canvas.draw()

root = tk.Tk()
root.title("Atomic Time Clock")

time_label = tk.Label(root, font=('Arial', 30), fg='black')
time_label.pack(expand=True)

# Create a canvas for the plot and add it to the Tkinter window
fig = Figure(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

update_time()
update_weather()

root.mainloop()