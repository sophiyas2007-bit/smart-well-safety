import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    import winsound
except ImportError:
    winsound = None


class SmartWellDashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart Well Safety Dashboard")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 760)
        self.root.configure(bg="#101827")

        self.bg = "#101827"
        self.card = "#1e293b"
        self.blue = "#38bdf8"
        self.green = "#22c55e"
        self.red = "#ef4444"
        self.yellow = "#facc15"
        self.white = "#ffffff"
        self.muted = "#cbd5e1"

        self.person = 0
        self.animal = 0
        self.bird = 0

        self.distance_alarm = False
        self.buzzer_on = False
        self.buzzer_mode = None

        self.buzzer_after_id = None
        self.bathing_after_id = None

        self.seconds = 0

        self.setup_style()
        self.build_dashboard()

        self.add_history("Smart Well Dashboard Started")
        self.update_counts()
        self.draw_chart()

    # STYLE
    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=self.white,
            background=self.white,
            foreground="#111827",
            padding=5
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.white)],
            foreground=[("readonly", "#111827")]
        )

    # DASHBOARD
    def build_dashboard(self):

        header = tk.Frame(self.root, bg=self.bg)
        header.pack(fill="x", padx=18, pady=(15, 8))

        tk.Label(
            header,
            text="SMART WELL SAFETY DASHBOARD",
            bg=self.bg,
            fg=self.blue,
            font=("Arial", 24, "bold")
        ).pack()

        tk.Label(
            header,
            text="Real-Time Well Monitoring and Safety Alert System",
            bg=self.bg,
            fg=self.white,
            font=("Arial", 11)
        ).pack(pady=(3, 0))

        # WELL SELECTION
        well_panel = self.create_panel(
            self.root, "WELL SELECTION"
        )

        well_panel.pack(fill="x", padx=18, pady=7)

        tk.Label(
            well_panel,
            text="Select Well:",
            bg=self.card,
            fg=self.white,
            font=("Arial", 11)
        ).pack(side="left", padx=(12, 8), pady=9)

        self.well_choice = ttk.Combobox(
            well_panel,
            values=[
                "North Field Well",
                "Village Well",
                "Farm Well"
            ],
            state="readonly",
            width=25
        )

        self.well_choice.current(0)
        self.well_choice.pack(side="left", padx=5, pady=8)

        # COUNT CARDS
        counts = tk.Frame(self.root, bg=self.bg)
        counts.pack(fill="x", padx=18, pady=7)

        self.person_count = self.create_count_card(
            counts, "PERSON COUNT", 0, self.blue
        )

        self.animal_count = self.create_count_card(
            counts, "ANIMAL COUNT", 1, self.green
        )

        self.bird_count = self.create_count_card(
            counts, "BIRD COUNT", 2, self.yellow
        )

        self.total_count = self.create_count_card(
            counts, "TOTAL COUNT", 3, self.white
        )

        # MAIN PANELS
        panels = tk.Frame(self.root, bg=self.bg)
        panels.pack(fill="x", padx=18, pady=7)

        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)

        # SENSOR PANEL
        sensor_panel = self.create_panel(
            panels, "SENSOR MONITORING"
        )

        sensor_panel.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 7), pady=5
        )

        self.water_input = self.add_input_row(
            sensor_panel, "Water Level (cm):", "65"
        )

        self.distance_input = self.add_input_row(
            sensor_panel, "Distance (cm):", "150"
        )

        self.temp_input = self.add_input_row(
            sensor_panel, "Temperature (°C):", "28"
        )

        status_row = tk.Frame(
            sensor_panel, bg=self.card
        )

        status_row.pack(fill="x", padx=10, pady=5)

        tk.Label(
            status_row,
            text="Safety Status:",
            bg=self.card,
            fg=self.white,
            font=("Arial", 11)
        ).pack(side="left")

        self.safety_status = tk.Label(
            status_row,
            text="SAFE",
            bg=self.card,
            fg=self.green,
            font=("Arial", 13, "bold")
        )

        self.safety_status.pack(side="left", padx=10)

        self.make_button(
            sensor_panel,
            "UPDATE SENSOR",
            self.update_sensor
        ).pack(pady=(5, 10))

        # OBJECT DETECTION
        detection_panel = self.create_panel(
            panels, "OBJECT DETECTION"
        )

        detection_panel.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(7, 0), pady=5
        )

        tk.Label(
            detection_panel,
            text="Select Object:",
            bg=self.card,
            fg=self.white,
            font=("Arial", 11)
        ).pack(anchor="w", padx=12, pady=(15, 5))

        self.object_choice = ttk.Combobox(
            detection_panel,
            values=["Person", "Animal", "Bird"],
            state="readonly",
            width=22
        )

        self.object_choice.current(0)
        self.object_choice.pack(anchor="w", padx=12, pady=4)

        self.make_button(
            detection_panel,
            "DETECT OBJECT",
            self.detect_object
        ).pack(anchor="w", padx=12, pady=12)

        tk.Label(
            detection_panel,
            text="Bird detection is counted but ignored for buzzer alerts.",
            bg=self.card,
            fg=self.muted,
            font=("Arial", 9)
        ).pack(anchor="w", padx=12, pady=(0, 8))

        # BUZZER AND TIMER PANELS
        controls = tk.Frame(self.root, bg=self.bg)
        controls.pack(fill="x", padx=18, pady=7)

        controls.columnconfigure(0, weight=1)
        controls.columnconfigure(1, weight=1)

        # BUZZER PANEL
        buzzer_panel = self.create_panel(
            controls, "BUZZER CONTROL"
        )

        buzzer_panel.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 7), pady=5
        )

        buzzer_row = tk.Frame(
            buzzer_panel, bg=self.card
        )

        buzzer_row.pack(fill="x", padx=12, pady=12)

        tk.Label(
            buzzer_row,
            text="Buzzer Status:",
            bg=self.card,
            fg=self.white,
            font=("Arial", 11)
        ).pack(side="left")

        self.buzzer_status = tk.Label(
            buzzer_row,
            text="BUZZER OFF",
            bg=self.card,
            fg=self.green,
            font=("Arial", 13, "bold")
        )

        self.buzzer_status.pack(side="left", padx=10)

        self.make_button(
            buzzer_panel,
            "STOP BUZZER",
            self.stop_buzzer
        ).pack(anchor="w", padx=12, pady=(0, 12))

        # BATHING TIMER
        timer_panel = self.create_panel(
            controls, "BATHING TIME MONITOR"
        )

        timer_panel.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(7, 0), pady=5
        )

        timer_row = tk.Frame(
            timer_panel, bg=self.card
        )

        timer_row.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(
            timer_row,
            text="Bathing Time (Minutes):",
            bg=self.card,
            fg=self.white,
            font=("Arial", 10)
        ).pack(side="left")

        self.minutes_input = tk.Entry(
            timer_row,
            width=7,
            font=("Arial", 11)
        )

        self.minutes_input.insert(0, "5")
        self.minutes_input.pack(side="left", padx=8)

        timer_value_row = tk.Frame(
            timer_panel, bg=self.card
        )

        timer_value_row.pack(fill="x", padx=10, pady=4)

        tk.Label(
            timer_value_row,
            text="Remaining Time:",
            bg=self.card,
            fg=self.white,
            font=("Arial", 10)
        ).pack(side="left")

        self.timer_display = tk.Label(
            timer_value_row,
            text="05:00",
            bg=self.card,
            fg=self.yellow,
            font=("Arial", 18, "bold")
        )

        self.timer_display.pack(side="left", padx=8)

        timer_buttons = tk.Frame(
            timer_panel, bg=self.card
        )

        timer_buttons.pack(
            anchor="w", padx=8, pady=(5, 10)
        )

        self.make_button(
            timer_buttons, "START", self.start_timer
        ).pack(side="left", padx=4)

        self.make_button(
            timer_buttons, "STOP", self.stop_timer
        ).pack(side="left", padx=4)

        self.make_button(
            timer_buttons, "RESET", self.reset_timer
        ).pack(side="left", padx=4)

        # CHART AND HISTORY
        bottom = tk.Frame(self.root, bg=self.bg)

        bottom.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(7, 15)
        )

        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        # ONLY ONE CHART
        chart_panel = self.create_panel(
            bottom, "DETECTION COUNT CHART"
        )

        chart_panel.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(0, 7), pady=5
        )

        self.chart = tk.Canvas(
            chart_panel,
            height=220,
            bg=self.card,
            highlightthickness=0
        )

        self.chart.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.chart.bind(
            "<Configure>",
            lambda event: self.draw_chart()
        )

        # HISTORY
        history_panel = self.create_panel(
            bottom, "ACTIVITY HISTORY"
        )

        history_panel.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(7, 0), pady=5
        )

        history_frame = tk.Frame(
            history_panel, bg=self.card
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.history_list = tk.Listbox(
            history_frame,
            bg=self.card,
            fg=self.white,
            selectbackground=self.blue,
            font=("Arial", 9),
            height=11,
            borderwidth=0,
            highlightthickness=0
        )

        history_scroll = tk.Scrollbar(
            history_frame,
            command=self.history_list.yview
        )

        self.history_list.configure(
            yscrollcommand=history_scroll.set
        )

        self.history_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        history_scroll.pack(
            side="right",
            fill="y"
        )

        self.make_button(
            history_panel,
            "CLEAR HISTORY",
            self.clear_history
        ).pack(anchor="e", padx=10, pady=(0, 8))

    # CREATE PANEL
    def create_panel(self, parent, title):

        panel = tk.Frame(
            parent,
            bg=self.card,
            highlightbackground=self.blue,
            highlightthickness=1,
            padx=5,
            pady=5
        )

        tk.Label(
            panel,
            text=title,
            bg=self.card,
            fg=self.blue,
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=8, pady=(5, 3))

        return panel

    # COUNT CARD
    def create_count_card(
        self, parent, title, column, color
    ):

        card = tk.Frame(
            parent,
            bg=self.card,
            highlightbackground=self.blue,
            highlightthickness=1,
            padx=8,
            pady=8
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        parent.columnconfigure(column, weight=1)

        tk.Label(
            card,
            text=title,
            bg=self.card,
            fg=self.white,
            font=("Arial", 10, "bold")
        ).pack()

        value = tk.Label(
            card,
            text="0",
            bg=self.card,
            fg=color,
            font=("Arial", 23, "bold")
        )

        value.pack(pady=(3, 0))

        return value

    # INPUT FIELD
    def add_input_row(
        self, parent, label_text, initial_value
    ):

        row = tk.Frame(parent, bg=self.card)
        row.pack(fill="x", padx=10, pady=4)

        tk.Label(
            row,
            text=label_text,
            bg=self.card,
            fg=self.white,
            font=("Arial", 10),
            width=19,
            anchor="w"
        ).pack(side="left")

        entry = tk.Entry(
            row,
            width=9,
            font=("Arial", 10)
        )

        entry.insert(0, initial_value)
        entry.pack(side="left", padx=5)

        return entry

    # BUTTON
    def make_button(self, parent, text, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.blue,
            fg="#111827",
            activebackground="#7dd3fc",
            activeforeground="#111827",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2"
        )

    # UPDATE SENSOR
    def update_sensor(self):

        try:
            water = int(self.water_input.get())
            distance = int(self.distance_input.get())
            temperature = int(self.temp_input.get())

            if min(water, distance, temperature) < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid non-negative sensor values."
            )
            return

        if distance < 200:

            self.safety_status.config(
                text="UNSAFE",
                fg=self.red
            )

            if not self.distance_alarm:

                self.distance_alarm = True

                self.start_buzzer(continuous=True)

                self.add_history(
                    "UNSAFE: Object is near the well"
                )

        else:

            self.safety_status.config(
                text="SAFE",
                fg=self.green
            )

            if self.distance_alarm:

                self.distance_alarm = False

                self.stop_buzzer()

                self.add_history(
                    "SAFE: Distance is normal"
                )

        self.add_history(
            f"Water Level: {water} cm"
        )

        self.add_history(
            f"Distance: {distance} cm"
        )

        self.add_history(
            f"Temperature: {temperature} °C"
        )

    # OBJECT DETECTION
    def detect_object(self):

        selected = self.object_choice.get()

        if selected == "Person":

            self.person += 1

            self.add_history("Person Detected")

            self.update_counts()

            if not self.distance_alarm:
                self.start_buzzer(continuous=False)

        elif selected == "Animal":

            self.animal += 1

            self.add_history("Animal Detected")

            self.update_counts()

            if not self.distance_alarm:
                self.start_buzzer(continuous=False)

        elif selected == "Bird":

            self.bird += 1

            self.add_history(
                "Bird Detected - IGNORED"
            )

            self.update_counts()

            # Bird is counted.
            # It does not change safety status.
            # It does not start the buzzer.

    # UPDATE COUNTS
    def update_counts(self):

        self.person_count.config(
            text=str(self.person)
        )

        self.animal_count.config(
            text=str(self.animal)
        )

        self.bird_count.config(
            text=str(self.bird)
        )

        self.total_count.config(
            text=str(
                self.person + self.animal + self.bird
            )
        )

        self.draw_chart()

    # ONE BAR CHART
    def draw_chart(self):

        if not hasattr(self, "chart"):
            return

        canvas = self.chart
        canvas.delete("all")

        width = max(canvas.winfo_width(), 300)
        height = max(canvas.winfo_height(), 180)

        left = 48
        right = width - 20
        top = 18
        bottom = height - 42

        canvas.create_line(
            left, top, left, bottom,
            fill=self.muted
        )

        canvas.create_line(
            left, bottom, right, bottom,
            fill=self.muted
        )

        canvas.create_text(
            width / 2,
            9,
            text="Detected Objects",
            fill=self.white,
            font=("Arial", 10, "bold"),
            anchor="n"
        )

        values = [
            self.person,
            self.animal,
            self.bird
        ]

        labels = [
            "Person",
            "Animal",
            "Bird"
        ]

        colors = [
            self.blue,
            self.green,
            self.yellow
        ]

        maximum = max(max(values), 1)

        plot_height = bottom - top - 10

        slot_width = (right - left) / 3

        bar_width = min(55, slot_width * 0.48)

        for index, (value, label, color) in enumerate(
            zip(values, labels, colors)
        ):

            center_x = left + slot_width * (index + 0.5)

            bar_height = (
                value / maximum
            ) * plot_height

            x1 = center_x - bar_width / 2
            x2 = center_x + bar_width / 2

            y1 = bottom - bar_height

            canvas.create_rectangle(
                x1, y1, x2, bottom,
                fill=color,
                outline=""
            )

            canvas.create_text(
                center_x,
                max(y1 - 10, top + 3),
                text=str(value),
                fill=self.white,
                font=("Arial", 9, "bold")
            )

            canvas.create_text(
                center_x,
                bottom + 17,
                text=label,
                fill=self.white,
                font=("Arial", 9)
            )

    # BEEP SOUND
    def play_beep(self):

        try:
            if winsound is not None:

                winsound.MessageBeep(
                    winsound.MB_ICONEXCLAMATION
                )

            else:
                self.root.bell()

        except Exception:
            self.root.bell()

    # START BUZZER
    def start_buzzer(self, continuous=False):

        if (
            self.buzzer_on
            and self.buzzer_mode == "continuous"
        ):
            return

        if self.buzzer_on and not continuous:
            return

        self.cancel_buzzer_callback()

        self.buzzer_on = True

        if continuous:
            self.buzzer_mode = "continuous"
        else:
            self.buzzer_mode = "short"

        self.buzzer_status.config(
            text="BUZZER ON",
            fg=self.red
        )

        self.play_beep()

        if continuous:

            self.buzzer_after_id = self.root.after(
                1000,
                self.continuous_buzzer_tick
            )

        else:

            self.buzzer_after_id = self.root.after(
                3000,
                self.stop_buzzer
            )

    # CONTINUOUS BUZZER
    def continuous_buzzer_tick(self):

        if (
            self.buzzer_on
            and self.buzzer_mode == "continuous"
        ):

            self.play_beep()

            self.buzzer_after_id = self.root.after(
                1000,
                self.continuous_buzzer_tick
            )

    # CANCEL BUZZER
    def cancel_buzzer_callback(self):

        if self.buzzer_after_id is not None:

            try:
                self.root.after_cancel(
                    self.buzzer_after_id
                )

            except tk.TclError:
                pass

            self.buzzer_after_id = None

    # STOP BUZZER
    def stop_buzzer(self):

        self.cancel_buzzer_callback()

        self.buzzer_on = False
        self.buzzer_mode = None

        self.buzzer_status.config(
            text="BUZZER OFF",
            fg=self.green
        )

        self.add_history("Buzzer stopped")

    # START BATHING TIMER
    def start_timer(self):

        try:
            minutes = int(
                self.minutes_input.get()
            )

            if minutes < 1 or minutes > 180:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Time",
                "Enter a time between 1 and 180 minutes."
            )

            return

        self.cancel_bathing_callback()

        self.seconds = minutes * 60

        self.update_timer_display()

        self.add_history("Bathing Timer Started")

        self.bathing_after_id = self.root.after(
            1000,
            self.bathing_tick
        )

    # BATHING TIMER
    def bathing_tick(self):

        self.seconds -= 1

        if self.seconds <= 0:

            self.seconds = 0

            self.timer_display.config(
                text="COMPLETED",
                fg=self.green
            )

            self.add_history(
                "Bathing Time Completed"
            )

            if not self.distance_alarm:
                self.start_buzzer(continuous=False)

            self.bathing_after_id = None

            return

        self.update_timer_display()

        self.bathing_after_id = self.root.after(
            1000,
            self.bathing_tick
        )

    # UPDATE TIMER DISPLAY
    def update_timer_display(self):

        minutes, seconds = divmod(
            self.seconds, 60
        )

        self.timer_display.config(
            text=f"{minutes:02d}:{seconds:02d}",
            fg=self.yellow
        )

    # CANCEL TIMER
    def cancel_bathing_callback(self):

        if self.bathing_after_id is not None:

            try:
                self.root.after_cancel(
                    self.bathing_after_id
                )

            except tk.TclError:
                pass

            self.bathing_after_id = None

    # STOP TIMER
    def stop_timer(self):

        self.cancel_bathing_callback()

        self.add_history(
            "Bathing Timer Stopped"
        )

    # RESET TIMER
    def reset_timer(self):

        self.cancel_bathing_callback()

        self.seconds = 0

        self.timer_display.config(
            text="00:00",
            fg=self.yellow
        )

        self.add_history(
            "Bathing Timer Reset"
        )

    # ADD HISTORY
    def add_history(self, message):

        if hasattr(self, "history_list"):

            timestamp = datetime.now().strftime(
                "%H:%M:%S"
            )

            self.history_list.insert(
                tk.END,
                f"[{timestamp}] {message}"
            )

            self.history_list.yview_moveto(1)

    # CLEAR HISTORY
    def clear_history(self):

        self.history_list.delete(0, tk.END)


# MAIN
if __name__ == "__main__":

    root = tk.Tk()

    app = SmartWellDashboard(root)

    root.mainloop()