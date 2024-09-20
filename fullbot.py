import random as r
import sys
import time as t
import dotenv
import numpy as np
import pyautogui as pag
import pyperclip as pyc
from openai import OpenAI
from pynput import keyboard
import tkinter as tk
import threading

dotenv.load_dotenv()
client = OpenAI()

context = ""


def typo(word: str, pos: bool):
    # pos True = typo at beginning of word, pos False = typo at end of word
    key_board = np.array(
        [
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
        ]
    )
    # length of typo
    typo_length = r.choice([1, 3])
    if (pos and word[0].lower() in key_board) or (
        not pos and word[-1].lower() in key_board
    ):
        if pos:
            idx = np.where(key_board == word[0].lower())
        else:
            idx = np.where(key_board == word[-1].lower())
        ord_pair = np.hstack([idx[0][0], idx[1][0]])
        # construct all possible location for typo letters
        locations = np.array(
            [
                [ord_pair[0] + 1, ord_pair[1]],
                [ord_pair[0] - 1, ord_pair[1]],
                [ord_pair[0], ord_pair[1] + 1],
                [ord_pair[0], ord_pair[1] - 1],
            ]
        )
        for _ in range(typo_length):
            while True:
                try:
                    bad_letter_idx = r.choice(locations)
                    pag.write(f"{key_board[*bad_letter_idx]}")
                except IndexError:
                    continue
                break
        t.sleep(0.2)
        for _ in range(typo_length):
            pag.press("backspace")


def auto_type(string: str):
    times = np.linspace(0.02, 0.07, 4)
    for word in string.split(" "):
        if "http" in word:
            t.sleep(1)
            pyc.copy(word)
            t.sleep(1.5)
            pag.hotkey("ctrl", "v")
        else:
            typo(word, True) if r.random() < 0.035 else None
            pag.write(word, interval=r.choice(times))
            typo(word, False) if r.random() < 0.035 else None
            pag.write(" ")


def get_chat_response(prompt: str) -> str:
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": prompt},
    ]
    # Remove None values
    messages = [msg for msg in messages if msg]

    completion = client.chat.completions.create(model="gpt-4o", messages=messages)
    return completion.choices[0].message.content


def store_highlighted_text():
    t.sleep(0.5)
    pag.hotkey("ctrl", "c")
    t.sleep(0.5)  # Wait for clipboard to update
    user_text = pyc.paste()  # Retrieve text from clipboard
    pag.press("end")
    if line.get():
        pag.press("space")
    else:
        pag.press("enter", interval=0.1, presses=2)
    pag.hotkey("ctrl", "b")
    auto_type(get_chat_response(user_text))
    pag.hotkey("ctrl", "b")


def on_press(key):
    try:
        if key == keyboard.Key.alt_l:
            keys_pressed.add("alt")
        elif key.char == "c":
            keys_pressed.add("c")

        if "alt" in keys_pressed and "c" in keys_pressed:
            store_highlighted_text()
    except AttributeError:
        pass


def on_release(key):
    try:
        if key == keyboard.Key.alt_l:
            keys_pressed.discard("alt")
        elif key.char == "c":
            keys_pressed.discard("c")
    except AttributeError:
        pass


def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def run_tkinter():
    global instruction_text, text_box, line

    def take_input(box: str) -> str:
        text = eval(box).get("1.0", "end-1c")
        eval(box).delete("1.0", "end-1c")
        return text

    def instructions_button():
        global context
        context = take_input("instruction_text").strip()

    def type_out():
        t.sleep(5)
        auto_type(take_input("text_box"))

    root = tk.Tk()
    root.title("Homework Assistant")
    W = 500
    H = 500
    root.minsize(W, H)
    line = tk.BooleanVar(root, False)

    welcome = tk.Label(root, text="Welcome to Homework Assistant\n")
    welcome.pack()

    instruction_label = tk.Label(
        root, text="Instructions on how you would like your questions to be answered"
    )
    instruction_label.pack()

    instruction_text = tk.Text(root, height=7, width=50)
    instruction_text.pack()

    send_instructions = tk.Button(root, text="Submit", command=instructions_button)
    send_instructions.pack()

    newline_radio = tk.Radiobutton(root, text="New line", variable=line, value=False)
    newline_radio.pack()

    sameline_radio = tk.Radiobutton(root, text="Same line", variable=line, value=True)
    sameline_radio.pack()

    text_label = tk.Label(root, text="Text to automatically type out (After 5 seconds)")
    text_label.pack()

    text_box = tk.Text(root, height=7, width=50)
    text_box.pack()

    text_button = tk.Button(root, text="Submit", command=type_out)
    text_button.pack()

    close = tk.Button(root, text="Quit", width=10, command=root.destroy)
    close.pack()

    root.mainloop()


keys_pressed = set()

listener_thread = threading.Thread(target=start_listener)
listener_thread.daemon = True
listener_thread.start()
