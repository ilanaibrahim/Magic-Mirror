import tkinter as tk
from time_module import get_time, get_date
from words_module import random_line 
from weather_module import get_weather


class Mirror:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Mirror")
        self.master.configure(bg="black")
        self.master.attributes("-fullscreen", True)

        self.widgets()
        self.update_time()
        self.update_date()
        self.update_quote()
        self.update_weather()
        

    def widgets(self):
        uk_frame = tk.Frame(self.master,bg="black")
        uk_frame.grid(row = 0, column = 0, sticky = "W", padx= 20)
        uktime_label = tk.Label(uk_frame, text= "UK: ", font= ("Helvetica",50), fg="white", bg="black")
        uktime_label.grid(row = 0, column = 0, sticky = "W")
        self.uktime_display = tk.Label(uk_frame, font=("Helvetica",50), fg="white", bg="black")
        self.uktime_display.grid(row = 0, column = 1, sticky = "W")

        mv_frame = tk.Frame(self.master,bg="black")
        mv_frame.grid(row = 1, column = 0, sticky = "W", padx= 20)
        mvtime_label = tk.Label(mv_frame, text= "MV: ", font= ("Helvetica",50), fg="white", bg="black")
        mvtime_label.grid(row = 1, column = 0, sticky = "W")
        self.mvtime_display = tk.Label(mv_frame, font=("Helvetica",50), fg="white", bg="black")
        self.mvtime_display.grid(row = 1, column = 1,sticky = "W")

        self.date_display = tk.Label(self.master, font= ("Arial",30), fg="white", bg="black")
        self.date_display.grid(row = 2, column = 0, sticky = "W", padx= 20, pady= 10)

        self.line_display = tk.Label(self.master, font= ("Arial",30), fg="white", bg="black", wraplength=1000)
        self.line_display.place(relx=0.5, rely=0.98, anchor = 's')

        weather_frame = tk.Frame(self.master,bg="black")
        weather_frame.pack(padx=20, pady=20, anchor = "e")
        self.daily_weather_display = tk.Label(weather_frame, font=("Helvetica",16), fg="white", bg="black")
        self.daily_weather_display.pack(anchor = 'e')
        self.hourly_weather_display = tk.Label(weather_frame, font=("Helvetica",10), fg="white", bg="black")
        self.hourly_weather_display.pack(anchor = 'e')

    def update_time(self):
        times = get_time()
        self.uktime_display.config(text=times["UK"].strftime("%I:%M %p"))
        self.mvtime_display.config(text=times["MV"].strftime("%I:%M %p"))
        self.master.after(1000, self.update_time)

    def update_date(self):
        date = get_date()
        self.date_display.config(text=date)
        self.master.after(3600000, self.update_date)

    def update_quote(self):
        line = random_line()
        self.line_display.config(text = line)
        self.master.after(86400, self.update_quote)

    def update_weather(self):
        lat = 50.904
        lon = -1.4043
        forecast_data = get_weather(lat,lon)
        self.daily_weather_display.config(text=forecast_data["daily"])
        hourly_text = "\n".join(forecast_data["hourly"])
        self.hourly_weather.display.config(text=hourly_text)
        self.master.after(1800000,self.update_weather) 
        

if __name__ == "__main__" :
    root = tk.Tk()
    app = Mirror(root)
    root.mainloop()