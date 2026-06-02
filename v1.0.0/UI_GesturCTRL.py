import tkinter as tk
import csv
import os

def run_ui(shared_data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ver = 0
    combined = 0
    Window = tk.Tk()
    Window.title("GesturCTRL")
    img_path = os.path.join(BASE_DIR, "GesturCTRL-1-7-2026.png")
    img = tk.PhotoImage(file=img_path)
    canvas_width = img.width() + 180
    canvas_height = img.height() + 100
    canvas = tk.Canvas(Window, width=canvas_width, height=canvas_height, highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, image=img, anchor="nw")

    pill_x = 0
    pill_y = img.height() + 10
    canvas.create_oval(pill_x, pill_y, pill_x + 40, pill_y + 40, fill="#333", outline="", tags="toggle")
    canvas.create_rectangle(pill_x + 20, pill_y, pill_x + 120, pill_y + 40, fill="#333", outline="", tags="toggle")
    canvas.create_oval(pill_x + 100, pill_y, pill_x + 140, pill_y + 40, fill="#333", outline="", tags="toggle")

    label = canvas.create_text(
        pill_x + 70, pill_y + 20,
        text="OFF",
        fill="white",
        font=("Segoe UI", 11, "bold"),
        tags="toggle_label"
    )

    state = 0

    def toggle(event=None):
        nonlocal state, combined
        state = 1 - state
        combined = state + ver

        if combined == 2:
            combined = 0
        shared_data['mode'] = combined
        color = "#000000" if state else "#333"
        text = "ON" if state else "OFF"
        canvas.itemconfig("toggle", fill=color)
        canvas.itemconfig("toggle_label", text=text)

    canvas.tag_bind("toggle", "<Button-1>", toggle)
    canvas.tag_bind("toggle_label", "<Button-1>", toggle)

    dropdown_x = pill_x + 160
    dropdown_y = pill_y
    versions = ["Main Version", "Lite Version"]
    selected_index = [0]

    canvas.create_oval(dropdown_x, dropdown_y, dropdown_x + 40, dropdown_y + 40, fill="#555", outline="", tags="dropdown")
    canvas.create_rectangle(dropdown_x + 20, dropdown_y, dropdown_x + 120, dropdown_y + 40, fill="#555", outline="", tags="dropdown")
    canvas.create_oval(dropdown_x + 100, dropdown_y, dropdown_x + 140, dropdown_y + 40, fill="#555", outline="", tags="dropdown")

    dd_text = canvas.create_text(
        dropdown_x + 70, dropdown_y + 20,
        text=versions[selected_index[0]],
        fill="white",
        font=("Segoe UI", 11, "bold"),
        tags="dropdown_text"
    )

    def call_version(index):
        nonlocal ver
        ver = 2 if versions[index] == "Main Version" else 0
        combined = state + ver
        shared_data['mode'] = combined
    def cycle_version(event=None):
        selected_index[0] = (selected_index[0] + 1) % len(versions)
        canvas.itemconfig(dd_text, text=versions[selected_index[0]])
        call_version(selected_index[0])

    canvas.tag_bind("dropdown", "<Button-1>", cycle_version)
    canvas.tag_bind("dropdown_text", "<Button-1>", cycle_version)

    def check_shutdown():
        if shared_data.get('shutdown') == True:
            Window.destroy()
        else:
            Window.after(1000, check_shutdown)

    Window.after(1000, check_shutdown)
    Window.mainloop()
