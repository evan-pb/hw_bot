import random as r
import sys
import time as t
import dotenv
import numpy as np
import pyautogui as pag
import pyperclip as pyc
from openai import OpenAI
from pynput import keyboard

dotenv.load_dotenv()
user_text = ""
client = OpenAI()


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
    if (pos and word[0].lower() in key_board) or (not pos and word[-1].lower() in key_board):
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
            print("id as link")
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
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": f"{mod1}, {prompt}. {mod2}"
            }
        ]
    )
    return completion.choices[0].message.content


def store_highlighted_text():
    t.sleep(0.5)
    pag.hotkey("ctrl", "c")
    t.sleep(0.5)                    # Wait for clipboard to update
    user_text = pyc.paste()         # Retrieve text from clipboard
    pag.press("end")
    pag.press("enter", interval=0.1, presses=2)
    pag.hotkey("ctrl", "b")
    auto_type(get_chat_response(user_text))
    pag.hotkey("ctrl", "b")
    user_text = ""


def on_press(key):
    try:
        if key == keyboard.Key.alt_l:
            store_highlighted_text()
            return False
        if key == keyboard.Key.alt_r:
            sys.exit()
    except AttributeError:
        pass

mod1 = input("Beginning prompt modifier: ")
mod2 = input("End prompt modifier: ")
