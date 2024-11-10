import tkinter as tk
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}

#---------------------------CHANGE THE SIDE OF THE CARD--------------------------------#
def change_card_side():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(front_canvas, image=image_back_card)

#---------------------------RANDOM WORD FOR THE CARD--------------------------------#

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(front_canvas, image=image_front_card)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, change_card_side)
#--------------------------------REMOVE AND WRITE THE KNOWN WORDS----------------------------------#
def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
#--------------------------------------------------------------------------------------------------#

window = tk.Tk()
window.title("Flash Card App")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, change_card_side)

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image_front_card = tk.PhotoImage(file="images/card_front.png")
image_back_card = tk.PhotoImage(file="images/card_back.png")
front_canvas = canvas.create_image(400, 263, image=image_front_card)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


#Buttons
cross_image = tk.PhotoImage(file="images/wrong.png")
cross_button = tk.Button(image=cross_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
cross_button.grid(row=1, column=0)

tick_image = tk.PhotoImage(file="images/right.png")
tick_button = tk.Button(image=tick_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
tick_button.grid(row=1, column=1)


next_card()

window.mainloop()