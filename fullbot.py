import random as r
import time as t
import dotenv
import numpy as np
import pyautogui as pag
import pyperclip as pyc
from openai import OpenAI
from pynput import keyboard

dotenv.load_dotenv()
client = OpenAI()

context = "answer the environmental science question in the simplest and shortest (most concise) way possible, using simple vocab. Do not provide any examples unless asked to. Avoid any kind of list formatting and return plain text ONLY."
# context = "Using the web, answer the history term / definition / person in the shortest way possible, preferably one sentence. Use simple vocab. Attach the link where you found your definition at the end of your response with no transition phrase, just the link by itself."
keys_pressed = set()


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
    # Ensure that leading or trailing character exists in keyboard array
    if (pos and word[0].lower() in key_board) or (
        not pos and word[-1].lower() in key_board
    ):
        if pos:
            idx = np.where(key_board == word[0].lower())
        else:
            idx = np.where(key_board == word[-1].lower())
        # ord_pair = np.hstack([idx[0][0], idx[1][0]])
        ord_pair = (idx[0][0], idx[1][0])
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
                    pag.write(f"{key_board[bad_letter_idx[0], bad_letter_idx[1]]}")
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
            pag.hotkey("command", "v", interval=0.1)
        else:
            pag.keyUp("fn")
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
    # messages = [msg for msg in messages if msg]

    completion = client.chat.completions.create(model="gpt-4o", messages=messages)
    print(f"Response:\n{completion.choices[0].message.content}\n")
    return completion.choices[0].message.content


def store_highlighted_text():
    t.sleep(0.5)
    pag.hotkey("command", "c", interval=0.1)
    t.sleep(0.5)  # Wait for clipboard to update
    user_text = pyc.paste()
    print(f"Client:\n{user_text}\n")
    pag.press("right")
    # pag.press("enter", presses=2, interval=.3)
    pag.press("enter")
    pag.hotkey("command", "b", interval=0.3)
    auto_type(get_chat_response(user_text))
    pag.hotkey("command", "b", interval=0.3)


def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            keys_pressed.add("ctrl")
        if key.char == "`":
            keys_pressed.add("`")

        if "ctrl" in keys_pressed and "`" in keys_pressed:
            store_highlighted_text()
    except AttributeError:
        pass


def on_release(key):
    try:
        if key == keyboard.Key.ctrl_l:
            keys_pressed.discard("ctrl")
        if key.char == "`":
            keys_pressed.discard("`")
    except AttributeError:
        pass


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
