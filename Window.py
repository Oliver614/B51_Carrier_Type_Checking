"""
Contains functions for making the GUI window attaching buttons, events etc...
"""

import tkinter as tk
from PIL import ImageTk, Image
from io import BytesIO
from UtilityFunctions import resize_image, save_image
import HistoryLog

# Global variables for storing GUI information

# The window object
window = tk.Tk()

# Buttons
save_to_button: tk.Button
load_from_button: tk.Button
classify_current_carrier_button: tk.Button
reclassify_old_image_button: tk.Button
test_button: tk.Button
classification_history: tk.Listbox

# Labels
image_output: tk.Label

last_captured_image: BytesIO
image_list = []
image_to_convert: BytesIO
image_to_display = None

# Display Variables
image_buffer_count = tk.StringVar()


def reclassify_old_image():
    pass


def classify_current_carrier():
    pass


def get_history():
    return HistoryLog.get_history_list()


def format_history(hist):
    formatted_data = []
    for i in range(0, 10):
        date = "{},     ".format(hist[i][0])
        data = "Carrier Type: {},     ".format(hist[i][1].get("carrier_type"))
        data += "Probability: {}".format(hist[i][1].get("probability"))
        formatted_data.append(date + data)
    return formatted_data


def update_history():
    h = get_history()
    h = format_history(h)
    classification_history.delete(0, tk.END)
    for i in range(len(h)):
        classification_history.insert(i, h[-i-1])


def update_photo(event):
    global image_output
    global image_to_display
    hist = get_history()
    selected_indices = (classification_history.curselection())
    image_location = hist[-selected_indices[0]-1][1].get("image_location")  # bruh this makes me sick
    image = Image.open(image_location)
    image = resize_image(image)
    image_to_display = ImageTk.PhotoImage(image)
    image_output.configure(image=image_to_display)


def make_window():
    global window
    global save_to_button
    global load_from_button
    global classify_current_carrier_button
    global reclassify_old_image_button
    global image_to_display
    global image_output
    global image_buffer_count
    global test_button
    global classification_history

    window.title("Visu")
    window.rowconfigure(0, minsize=300, weight=1)
    window.columnconfigure(1, minsize=400, weight=1)

    # Create the frame for the buttons to fit in
    frame_for_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    frame_for_information = tk.Frame(window, relief=tk.RAISED, bd=2)

    # make the buttons and GUI
    save_to_button = tk.Button(frame_for_buttons, text="Save Image", font=('Ariel', 10),
                               command=lambda: save_image(image_to_display, manual_save=True))
    load_from_button = tk.Button(frame_for_buttons, text="Load From",
                                 font=('Ariel', 10), command=lambda: update_history())
    classify_current_carrier_button = tk.Button(frame_for_buttons, text="Classify Carrier", font=('Ariel', 10))
    reclassify_old_image_button = tk.Button(frame_for_buttons, text="Reclassify Carrier", font=('Ariel', 10))
    image_buffer_length_label = tk.Label(frame_for_buttons, textvariable=image_buffer_count, font=('Ariel', 10))
    history_label = tk.Label(window, text="History")
    image_output = tk.Label(window)

    # history box
    classification_history = tk.Listbox(window)
    classification_history.bind("<<ListboxSelect>>", update_photo)
    scrollbar = tk.Scrollbar(window, orient='vertical', command=classification_history.yview)
    classification_history['yscrollcommand'] = scrollbar.set

    # bind the buttons and image to the window
    image_output.grid(row=0, column=1, sticky="nw")
    save_to_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    load_from_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    classify_current_carrier_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    reclassify_old_image_button.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    image_buffer_length_label.grid(row=4, column=0, sticky="s", padx=5, pady=5)
    history_label.grid(row=2, column=0, columnspan=2, sticky="ew")
    classification_history.grid(row=3, column=0, columnspan=2, sticky="ew")
    frame_for_buttons.grid(row=0, column=0, rowspan=2, sticky="ns")
    frame_for_information.grid(row=1, column=1, sticky="ew")
    scrollbar.grid(column=2, row=3, sticky='ns')

    return window
