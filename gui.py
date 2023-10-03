import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("Dashboard")
root.protocol("WM_DELETE_WINDOW",on_closing)
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 1000
window_height = 400 

# Calculate the position to place the window at screen center
x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height)

root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))


# Create a frame for the graph
frame_line = ttk.Frame(root)
frame_line.pack(padx=10, pady=10, side=tk.LEFT)

# Create a frame for the pie chart
frame_bar = ttk.Frame(root)
frame_bar.pack(padx=10, pady=10, side=tk.RIGHT)

# Set up the figure and axis for the line graph
fig_line, ax_line = plt.subplots(figsize=(5, 5))
canvas_line = FigureCanvasTkAgg(fig_line, master=frame_line)
canvas_line.draw()
canvas_line.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# Set up the figure and axis for the bar chart
fig_bar, ax_bar = plt.subplots(figsize=(5, 3))
canvas_bar = FigureCanvasTkAgg(fig_bar, master=frame_bar)
canvas_bar.draw()
canvas_bar.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Initialize lists to store time and score data
times = []
scores = []

def get_drowsiness_counts():
    low_count = sum(1 for s in scores if 0 < s < 5)
    medium_count = sum(1 for s in scores if 5 <= s < 15)
    high_count = sum(1 for s in scores if s >= 15)
    return [low_count, medium_count, high_count]

def update_series_graph():
    global times, scores

    # Update the graph
    ax_line.clear()
    
    colors = {
        'none': 'green',
        'low': 'yellow',
        'medium': 'orange',
        'high': 'red'
    }
    
    start_idx = 0
    for i in range(1, len(scores)):
        if 0 < scores[i] < 5:
            color = colors['low']
        elif 5 <= scores[i] < 15:
            color = colors['medium']
        elif scores[i] >= 15:
            color = colors['high']
        else:
            color = colors['none']
            
        if i == len(scores) - 1 or (scores[i] != scores[i+1]):
            ax_line.plot(times[start_idx:i+1], scores[start_idx:i+1], color=color)
            start_idx = i
    
    ax_line.set_title("Drowsiness Level Over Time")
    ax_line.set_xlabel("Time (Second)")
    ax_line.set_ylabel("Drowsiness Level")
    ax_line.set_ylim(-1, 35)
    canvas_line.draw()
    
def update_bar_graph():
    counts = get_drowsiness_counts()
    labels = ["Low", "Medium", "High"]
    ax_bar.clear()
    ax_bar.bar(labels, counts, color=['yellow', 'orange', 'red',])
    ax_bar.set_title("Drowsiness Level Distribution")
    ax_bar.set_ylabel("Count")
    canvas_bar.draw()


def start_gui():
    root.mainloop()
    