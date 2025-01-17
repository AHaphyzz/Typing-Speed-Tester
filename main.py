import keyboard
from _datetime import datetime
import requests


# -----------------Set up Screen-------------------
print("Welcome to Speedster, a Python-based typing speed test program that measures your typing speed,"
      "detects mistakes and calculates your Words Per Minute (WPM)\n")

# -----Accepts input from user and sets difficulty
difficulty = int(input("Select the number of paragraph you will like to type\n"
                       "EASY, 25 words max: --> 1\n"
                       "MEDIUM, 40 words max: --> 2\n"
                       "HARD, 60 words --> 3\n"
                       "Choose difficulty: \n"
                       "You can set a custom word count: Enter a number between 1 - 500 words max): "))
print("Instructions: The timer starts when you click 'Enter', click 'Esc' to stop")

num_words = difficulty
if difficulty < 1:
    num_words = 25
elif difficulty == 2:
    num_words = 40
elif difficulty == 3:
    num_words = 60
elif difficulty == 1:
    num_words = num_words
elif difficulty > 500:
    num_words = 200

random_words_url = f"https://random-word-api.herokuapp.com/word?number={num_words}"
response = requests.get(random_words_url)
web_texts = response.json()

# joined all each letter and space together a single statement: display for user
display_text = " ".join(web_texts)
print(f"Type what see on your screen:\n{display_text}")
word_length = len(web_texts)


# global variable
typed_keys = []


def record_key(keystroke):
    global typed_keys, web_texts

    # Skip function keys (e.g., F1-F12, Ctrl, Shift, Alt, etc.)
    if len(keystroke.name) > 1 and keystroke.name not in ("space", "backspace"):
        return
    if keystroke.name == "space":
        typed_keys.append(" ")
    elif keystroke.name == "backspace":
        typed_keys.pop()    # Simulate backspace
    else:
        typed_keys.append(keystroke.name)


keyboard.wait("enter")
start_time = datetime.now()

keyboard.on_press(record_key)

keyboard.wait("esc")
stop_time = datetime.now()


keyboard.unhook_all() # Cleanup listener

# --------------------------Time--------------------------
type_time = stop_time - start_time
total_secs = int(type_time.total_seconds())
total_min = total_secs // 60
word_per_min = word_length / total_min


# ----------------- format user's typed words
"""
 user's typed_keys is currently saved as list with each letter and space as a single string item e.g 'l', 'o', 'r', 'e', 'm'
 letters are joined together to form a word string, e.g 'lorem' and separated by space
 words and space are then joined together to form sentences, display the same format as words from web"""
joined_words = " ".join("".join(typed_keys).split())

#  separate the words individual str, needed for error checking
users_words = joined_words.split(" ")

# ------------------------- check for wrong words ---------------------
wrong_words = [typed_word for typed_word in users_words if typed_word not in web_texts]
if wrong_words:
    print(f"\nErrors: {len(wrong_words)}")
    print(wrong_words)
else:
    print("You did not make any mistake")

print(f'Duration: {str(type_time).split(".")[0]}')

if len(users_words) == word_length:
    print(f"You did completed the test.")
else:
    print(f"The Speed test was not completed, you typed {len(users_words)} out of {word_length}")

print(f"Your typing speed is approximately {round(word_per_min, 0)}WPM")
