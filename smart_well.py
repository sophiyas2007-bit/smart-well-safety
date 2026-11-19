    refresh_sensor_cards(False)

tk.Button(object_box, text="CLEAR OBJECT STATUS",
          command=clear_detection_status, bg="#40536d", fg=WHITE,
          font=("Segoe UI", 9, "bold"), relief="flat",
          padx=12, pady=7).pack(anchor="w")

# Bathing reminder timer
timer_box = make_section(root, "BATHING TIME REMINDER")
timer_box.pack(fill="x", padx=22, pady=(0, 16))
tk.Label(timer_box, text="Set duration (minutes):", bg=PANEL, fg=WHITE,
         font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 8))
timer_entry = tk.Entry(timer_box, textvariable=timer_minutes_var, width=7,
                       font=("Segoe UI", 13, "bold"), justify="center",
                       bg=CARD, fg=CYAN, insertbackground=WHITE, relief="flat")
timer_entry.pack(side="left", ipady=5, padx=5)

timer_display = tk.Label(timer_box, text="60:00", bg=PANEL, fg=WHITE,
                         font=("Segoe UI", 22, "bold"))
timer_display.pack(side="left", padx=22)
timer_message = tk.Label(timer_box, text="Timer ready", bg=PANEL, fg=MUTED,
                         font=("Segoe UI", 9))
timer_message.pack(side="left", padx=8)

def show_timer():
    mins, secs = divmod(timer_remaining, 60)
    timer_display.config(text=f"{mins:02d}:{secs:02d}")

def timer_tick():
    global timer_remaining, timer_after_id, timer_running
    if not timer_running:
        return
    if timer_remaining > 0:
        timer_remaining -= 1
        show_timer()
        timer_after_id = root.after(1000, timer_tick)
    else:
        timer_running = False
        timer_after_id = None
        timer_display.config(text="TIME UP!", fg=RED)
        timer_message.config(text="Time completed — buzzer activated!", fg=RED)
        play_buzzer()
        messagebox.showinfo("Bathing time completed", "Your set time is over.")

def start_timer():
    global timer_remaining, timer_running
    if timer_running:
        return
    try:
        mins = int(timer_minutes_var.get())
        if not 1 <= mins <= 180:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid time", "Enter a whole number from 1 to 180 minutes.")
        return
    timer_remaining = mins * 60
    timer_running = True
    timer_display.config(fg=CYAN)
    timer_message.config(text="Timer running...", fg=GREEN)
    show_timer()
    timer_tick()

def stop_timer():
    global timer_running, timer_after_id
    timer_running = False
    if timer_after_id is not None:
        root.after_cancel(timer_after_id)
        timer_after_id = None
    timer_message.config(text="Timer stopped", fg=ORANGE)

def reset_timer():
    global timer_remaining, timer_running, timer_after_id
    timer_running = False
    if timer_after_id is not None:
        root.after_cancel(timer_after_id)
        timer_after_id = None
    try:
        mins = int(timer_minutes_var.get())
        if not 1 <= mins <= 180:
            raise ValueError
    except ValueError:
        mins = 60
        timer_minutes_var.set("60")
    timer_remaining = mins * 60
    show_timer()
    timer_display.config(fg=WHITE)
    timer_message.config(text="Timer ready", fg=MUTED)

tk.Button(timer_box, text="START", command=start_timer,
          bg=GREEN, fg=WHITE, font=("Segoe UI", 9, "bold"),
          relief="flat", padx=13, pady=7).pack(side="left", padx=5)
tk.Button(timer_box, text="STOP", command=stop_timer,
          bg=RED, fg=WHITE, font=("Segoe UI", 9, "bold"),
          relief="flat", padx=13, pady=7).pack(side="left", padx=5)
tk.Button(timer_box, text="RESET", command=reset_timer,
          bg="#40536d", fg=WHITE, font=("Segoe UI", 9, "bold"),
          relief="flat", padx=13, pady=7).pack(side="left", padx=5)

# Footer
tk.Label(root,
         text="Demo only: values and object detections are entered manually. Keep this window open for the timer.",
         bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(pady=(0, 8))

refresh_sensor_cards(False)
update_charts()
root.mainloop()

