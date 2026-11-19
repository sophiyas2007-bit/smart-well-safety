import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import winsound

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Smart Well Safety Dashboard")
root.geometry("1400x900")
root.configure(bg="#101827")


# ================= COLORS =================

BG = "#101827"
CARD = "#1E293B"
WHITE = "#FFFFFF"
BLUE = "#38BDF8"
GREEN = "#22C55E"
RED = "#EF4444"
YELLOW = "#FACC15"


# ================= DATA =================

person_count = 0
animal_count = 0
bird_count = 0

temperature_values = []
distance_values = []
water_values = []
sensor_times = []

object_distances = []
object_times = []

animation_job = None


# ================= MAIN TITLE =================

title = tk.Label(
    root,
    text="SMART WELL SAFETY DASHBOARD",
    font=("Arial", 24, "bold"),
    bg=BG,
    fg=BLUE
)
title.pack(pady=15)


# ================= MAIN FRAME =================

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)

left_frame = tk.Frame(main_frame, bg=CARD, width=330)
left_frame.pack(side="left", fill="y", padx=10)
left_frame.pack_propagate(False)

right_frame = tk.Frame(main_frame, bg=BG)
right_frame.pack(side="right", fill="both", expand=True)


# ================= OBJECT DETECTION =================

tk.Label(
    left_frame,
    text="OBJECT DETECTION",
    font=("Arial", 17, "bold"),
    bg=CARD,
    fg=BLUE
).pack(pady=15)

object_choice = tk.StringVar(value="Person")

tk.Label(
    left_frame,
    text="Select Object",
    font=("Arial", 12),
    bg=CARD,
    fg=WHITE
).pack(pady=5)

object_dropdown = ttk.Combobox(
    left_frame,
    textvariable=object_choice,
    values=["Person", "Animal", "Bird"],
    state="readonly",
    font=("Arial", 12)
)
object_dropdown.pack(pady=5)


# ================= DISTANCE INPUT =================

tk.Label(
    left_frame,
    text="Distance (cm)",
    font=("Arial", 12),
    bg=CARD,
    fg=WHITE
).pack(pady=5)

distance_entry = tk.Entry(
    left_frame,
    font=("Arial", 12),
    justify="center"
)
distance_entry.insert(0, "250")
distance_entry.pack(pady=5)


# ================= DETECTION STATUS =================

status_label = tk.Label(
    left_frame,
    text="Waiting for Detection",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=GREEN,
    wraplength=280
)
status_label.pack(pady=10)


# ================= SAFETY STATUS =================

safety_label = tk.Label(
    left_frame,
    text="SAFE - NO DANGER DETECTED",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=GREEN,
    wraplength=280
)
safety_label.pack(pady=10)


# ================= ANIMATION =================

def detection_animation(message, color):

    global animation_job

    if animation_job is not None:
        root.after_cancel(animation_job)
        animation_job = None

    status_label.config(
        text=message,
        bg=CARD,
        fg=color
    )

    flash_colors = [color, WHITE] * 5

    def flash(index=0):

        global animation_job

        if index < len(flash_colors):

            status_label.config(
                fg=flash_colors[index]
            )

            animation_job = root.after(
                200,
                lambda: flash(index + 1)
            )

        else:

            status_label.config(fg=color)
            animation_job = None

    flash()


# ================= SOUND =================

def play_detection_sound():

    def ring_sound():

        try:
            winsound.Beep(1000, 5000)

        except RuntimeError:
            winsound.MessageBeep(
                winsound.MB_ICONEXCLAMATION
            )

    threading.Thread(
        target=ring_sound,
        daemon=True
    ).start()


# ================= DETECTION COUNTS =================

tk.Label(
    left_frame,
    text="DETECTION COUNTS",
    font=("Arial", 15, "bold"),
    bg=CARD,
    fg=BLUE
).pack(pady=10)

person_label = tk.Label(
    left_frame,
    text="Person : 0",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE
)
person_label.pack(pady=5)

animal_label = tk.Label(
    left_frame,
    text="Animal : 0",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE
)
animal_label.pack(pady=5)

bird_label = tk.Label(
    left_frame,
    text="Bird : 0",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=WHITE
)
bird_label.pack(pady=5)


# ================= NOTEBOOK =================

notebook = ttk.Notebook(right_frame)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

object_tab = tk.Frame(notebook, bg=BG)
sensor_tab = tk.Frame(notebook, bg=BG)

notebook.add(object_tab, text="Object Visualization")
notebook.add(sensor_tab, text="Sensor Visualization")


# ==================================================
# OBJECT VISUALIZATION
# ==================================================

object_figure = Figure(figsize=(10, 7), dpi=100)

bar_chart = object_figure.add_subplot(221)
line_chart = object_figure.add_subplot(222)
pie_chart = object_figure.add_subplot(223)
hist_chart = object_figure.add_subplot(224)

object_canvas = FigureCanvasTkAgg(
    object_figure,
    master=object_tab
)

object_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


def update_object_visualization():

    labels = ["Person", "Animal", "Bird"]

    counts = [
        person_count,
        animal_count,
        bird_count
    ]

    # BAR CHART

    bar_chart.clear()

    bar_chart.bar(labels, counts)

    bar_chart.set_title("Object Detection Count")
    bar_chart.set_ylabel("Number of Detections")


    # LINE CHART

    line_chart.clear()

    if object_distances:

        line_chart.plot(
            object_distances,
            object_times,
            marker="o",
            linewidth=2
        )

        line_chart.set_xlabel("Distance (cm)")
        line_chart.set_ylabel("Detection Time")

        line_chart.yaxis.set_major_formatter(
            mdates.DateFormatter("%H:%M:%S")
        )

        line_chart.tick_params(axis="x", rotation=20)

    else:

        line_chart.text(
            0.5, 0.5,
            "No Detection Yet",
            ha="center",
            va="center",
            transform=line_chart.transAxes
        )

    line_chart.set_title("Distance vs Detection Time")


    # PIE CHART

    pie_chart.clear()

    if sum(counts) > 0:

        pie_chart.pie(
            counts,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

    else:

        pie_chart.text(
            0.5, 0.5,
            "No Detection Yet",
            ha="center",
            va="center"
        )

    pie_chart.set_title("Detection Percentage")


    # HISTOGRAM

    hist_chart.clear()

    detection_types = (
        [0] * person_count +
        [1] * animal_count +
        [2] * bird_count
    )

    if detection_types:

        hist_chart.hist(
            detection_types,
            bins=[-0.5, 0.5, 1.5, 2.5],
            rwidth=0.7
        )

        hist_chart.set_xticks([0, 1, 2])
        hist_chart.set_xticklabels(
            ["Person", "Animal", "Bird"]
        )

    hist_chart.set_title("Detection Histogram")
    hist_chart.set_ylabel("Number of Detections")

    object_figure.tight_layout(pad=3)
    object_canvas.draw_idle()


# ==================================================
# DETECTION FUNCTION
# ==================================================

def update_counts():

    person_label.config(text=f"Person : {person_count}")
    animal_label.config(text=f"Animal : {animal_count}")
    bird_label.config(text=f"Bird : {bird_count}")


def detect_object():

    global person_count
    global animal_count
    global bird_count

    selected = object_choice.get()

    try:

        distance = float(distance_entry.get())

        if distance < 0 or distance > 500:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Distance",
            "Enter a distance between 0 and 500 cm."
        )
        return


    # PERSON

    if selected == "Person":

        person_count += 1

        if distance <= 200:

            detection_animation(
                "PERSON DETECTED!",
                RED
            )

            safety_label.config(
                text="UNSAFE ZONE - PERSON DETECTED",
                fg=RED
            )

            play_detection_sound()

        else:

            detection_animation(
                "PERSON DETECTED!",
                GREEN
            )

            safety_label.config(
                text="SAFE ZONE - DISTANCE NORMAL",
                fg=GREEN
            )


    # ANIMAL

    elif selected == "Animal":

        animal_count += 1

        if distance <= 200:

            detection_animation(
                "ANIMAL DETECTED!",
                RED
            )

            safety_label.config(
                text="UNSAFE ZONE - ANIMAL DETECTED",
                fg=RED
            )

            play_detection_sound()

        else:

            detection_animation(
                "ANIMAL DETECTED!",
                GREEN
            )

            safety_label.config(
                text="SAFE ZONE - DISTANCE NORMAL",
                fg=GREEN
            )


    # BIRD

    elif selected == "Bird":

        bird_count += 1

        detection_animation(
            "BIRD DETECTED - IGNORED",
            YELLOW
        )

        safety_label.config(
            text="BIRD DETECTED - IGNORED",
            fg=YELLOW
        )


    # SAVE DETECTION DATA

    object_distances.append(distance)
    object_times.append(datetime.now())

    update_counts()
    update_object_visualization()


# ================= DETECT BUTTON =================

detect_button = tk.Button(
    left_frame,
    text="DETECT OBJECT",
    font=("Arial", 13, "bold"),
    bg=BLUE,
    fg="black",
    width=20,
    command=detect_object
)
detect_button.pack(pady=15)


# ==================================================
# SENSOR SECTION
# ==================================================

tk.Label(
    left_frame,
    text="SENSOR INPUT",
    font=("Arial", 15, "bold"),
    bg=CARD,
    fg=BLUE
).pack(pady=10)


# TEMPERATURE

tk.Label(
    left_frame,
    text="Temperature (°C)",
    font=("Arial", 11),
    bg=CARD,
    fg=WHITE
).pack()

temperature_entry = tk.Entry(
    left_frame,
    font=("Arial", 11),
    justify="center"
)
temperature_entry.insert(0, "30")
temperature_entry.pack(pady=5)


# WATER LEVEL

tk.Label(
    left_frame,
    text="Water Level (%)",
    font=("Arial", 11),
    bg=CARD,
    fg=WHITE
).pack()

water_entry = tk.Entry(
    left_frame,
    font=("Arial", 11),
    justify="center"
)
water_entry.insert(0, "50")
water_entry.pack(pady=5)


# SENSOR STATUS

sensor_status = tk.Label(
    left_frame,
    text="Sensor Waiting",
    font=("Arial", 11, "bold"),
    bg=CARD,
    fg=GREEN
)
sensor_status.pack(pady=10)


# ==================================================
# SENSOR VISUALIZATION
# ==================================================

sensor_figure = Figure(figsize=(10, 7), dpi=100)

temp_chart = sensor_figure.add_subplot(311)
distance_chart = sensor_figure.add_subplot(312)
water_chart = sensor_figure.add_subplot(313)

sensor_canvas = FigureCanvasTkAgg(
    sensor_figure,
    master=sensor_tab
)

sensor_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


def update_sensor_charts():

    temp_chart.clear()
    distance_chart.clear()
    water_chart.clear()

    if sensor_times:

        temp_chart.plot(
            sensor_times,
            temperature_values,
            marker="o"
        )

        temp_chart.set_title("Temperature Monitoring")
        temp_chart.set_ylabel("Temperature °C")


        distance_chart.plot(
            sensor_times,
            distance_values,
            marker="o"
        )

        distance_chart.set_title("Distance Monitoring")
        distance_chart.set_ylabel("Distance cm")


        water_chart.plot(
            sensor_times,
            water_values,
            marker="o"
        )

        water_chart.set_title("Water Level Monitoring")
        water_chart.set_ylabel("Water Level %")


        for chart in [
            temp_chart,
            distance_chart,
            water_chart
        ]:

            chart.xaxis.set_major_formatter(
                mdates.DateFormatter("%H:%M:%S")
            )

            chart.tick_params(axis="x", rotation=20)

    sensor_figure.tight_layout(pad=3)
    sensor_canvas.draw_idle()


# ================= SENSOR UPDATE =================

def update_sensor():

    try:

        temperature = float(temperature_entry.get())
        distance = float(distance_entry.get())
        water = float(water_entry.get())

        if distance < 0 or distance > 500 or water < 0 or water > 100:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Distance must be 0-500 cm. Water level must be 0-100."
        )
        return


    current_time = datetime.now()

    temperature_values.append(temperature)
    distance_values.append(distance)
    water_values.append(water)
    sensor_times.append(current_time)


    # KEEP LATEST 20 READINGS

    if len(sensor_times) > 20:

        temperature_values.pop(0)
        distance_values.pop(0)
        water_values.pop(0)
        sensor_times.pop(0)


    sensor_status.config(
        text="SENSOR DATA UPDATED",
        fg=GREEN
    )

    update_sensor_charts()


# ================= SENSOR BUTTON =================

sensor_button = tk.Button(
    left_frame,
    text="UPDATE SENSOR",
    font=("Arial", 12, "bold"),
    bg=GREEN,
    fg="black",
    width=20,
    command=update_sensor
)
sensor_button.pack(pady=15)


# ================= INITIAL CHARTS =================

update_object_visualization()
update_sensor_charts()


# ================= START DASHBOARD =================

root.mainloop()