import tkinter as tk
from tkinter import ttk, messagebox
import requests
import geocoder
from PIL import Image, ImageTk
import io

#Replace with your WeatherAPI.com API key
API_KEY = '7c5fa8ea847946a98fc131909240107' 

#Fetch weather data using WeatherAPI.com
def fetch_weather(location, units='metric'):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=no"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        messagebox.showerror("Error", f"HTTP Error: {err}")
    except requests.exceptions.RequestException as err:
        messagebox.showerror("Error", f"Error: {err}")

#Use IP-based location detection if no manual input is given
def fetch_ip_location():
    g = geocoder.ip('me')
    return g.city

#Update the weather information in the GUI
def update_weather():
    location = location_entry.get() or fetch_ip_location()
    units = unit_var.get()
    weather_data = fetch_weather(location)
    if weather_data:
        city_label.config(text=f"City: {weather_data['location']['name']}")
        temperature_c = weather_data['current']['temp_c']
        temperature_f = weather_data['current']['temp_f']
        if units == 'metric':
            temperature_label.config(text=f"Temperature: {temperature_c}°C")
        else:
            temperature_label.config(text=f"Temperature: {temperature_f}°F")
        
        conditions_label.config(text=f"Conditions: {weather_data['current']['condition']['text']}")
        wind_kph = weather_data['current']['wind_kph']
        wind_mph = weather_data['current']['wind_mph']
        if units == 'metric':
            wind_label.config(text=f"Wind Speed: {wind_kph} kph")
        else:
            wind_label.config(text=f"Wind Speed: {wind_mph} mph")
        
        #Fetch and display the weather icon
        icon_url = f"http:{weather_data['current']['condition']['icon']}"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

#Set up the Tkinter GUI
root = tk.Tk()
root.title("Weather Application made by Himanshu")
root.geometry("400x450")

#Location input and submit button
location_label = tk.Label(root, text="Enter location:")
location_label.pack(pady=10)
location_entry = tk.Entry(root)
location_entry.pack(pady=10)

#Unit selection
unit_var = tk.StringVar(value='metric')
unit_label = tk.Label(root, text="Select Unit:")
unit_label.pack(pady=5)
unit_menu = ttk.Combobox(root, textvariable=unit_var, values=['metric', 'imperial'])
unit_menu.pack(pady=5)
unit_menu.current(0)

submit_button = tk.Button(root, text="Get Weather", command=update_weather)
submit_button.pack(pady=10)

#Weather information display
city_label = tk.Label(root, text="City: ")
city_label.pack(pady=5)
temperature_label = tk.Label(root, text="Temperature: ")
temperature_label.pack(pady=5)
conditions_label = tk.Label(root, text="Conditions: ")
conditions_label.pack(pady=5)
wind_label = tk.Label(root, text="Wind Speed: ")
wind_label.pack(pady=5)
icon_label = tk.Label(root)
icon_label.pack(pady=10)

root.mainloop()
