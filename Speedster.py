from tkinter import *
from tkinter import messagebox
import requests
from _datetime import datetime

speedster = Tk()
speedster.title("Speedster Typing Test")
speedster.geometry("650x600")  # Set size of window
speedster.config(bg="#1E1E2E")  # #ecebeb


# display answer
def get_words():
    global start_time, word_length, web_texts

    start_button.config(state=DISABLED)  # to prevent simultaneous operation
    display_web_text.delete("1.0", END)  # delete previous text
    display_typed_text.config(state=NORMAL)
    display_typed_text.delete("1.0", END)
    display_typed_text.config(state=DISABLED)

    difficulty = difficulty_var.get()

    if difficulty == "easy":
        num_words = 25
    elif difficulty == "medium":
        num_words = 40
    elif difficulty == "hard":
        num_words = 60
    elif difficulty == "custom":
        try:
            num_words = int(entry_field.get())
            if num_words < 1 or num_words > 60:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid number", "Please enter values between 1 and 60")

            start_button.config(state="normal")
            # Re-enable difficulty selection
            easy_button.config(state=NORMAL)
            medium_button.config(state=NORMAL)
            hard_button.config(state=NORMAL)
            custom_button.config(state=NORMAL)
            entry_field.config(state=NORMAL)

    # fetch words from web
    random_words_url = f"https://random-word-api.herokuapp.com/word?number={num_words}"
    try:
        response = requests.get(random_words_url)
        response.raise_for_status()  # Raise error for bad responses
        web_texts = response.json()
    except (requests.RequestException, ValueError):
        messagebox.showerror("Network Error", f"Failed to fetch words, check your connection")
        speedster.quit()
        return

    # format words and display for user
    display_text = " ".join(web_texts)
    display_web_text.config(state=NORMAL)
    display_web_text.insert("1.0", display_text)
    display_web_text.config(state=DISABLED)  # ensure the web texts can't be altered

    display_typed_text.config(state=NORMAL)

    start_time = datetime.now()
    word_length = len(web_texts)

    display_typed_text.bind("<Return>", check_typing)
    display_typed_text.bind("<Escape>", handle_escape)


def restart():
    # Reset UI elements for a new game
    start_button.config(state=NORMAL)
    display_typed_text.config(state=NORMAL)
    display_typed_text.delete("1.0", END)
    display_typed_text.config(state=DISABLED)
    display_web_text.config(state=NORMAL)
    display_web_text.delete("1.0", END)
    display_web_text.config(state=DISABLED)

    # Re-enable difficulty selection
    easy_button.config(state=NORMAL)
    medium_button.config(state=NORMAL)
    hard_button.config(state=NORMAL)
    custom_button.config(state=NORMAL)
    entry_field.config(state=NORMAL)


def show_results():
    typed_texts = display_typed_text.get("1.0", END).strip()
    users_words = typed_texts.split()  # turn to word rather than character
    stop_time = datetime.now()

    if len(users_words) == word_length:  # show results if the type test isn't empty
        # --------------------------Time--------------------------
        type_time = stop_time - start_time
        total_secs = int(type_time.total_seconds())
        total_min = total_secs // 60

        # avoid zero division error
        if total_min == 0:
            word_per_min = word_length / (total_secs / 60)
        else:
            word_per_min = word_length / total_min

        # check for error
        wrong_words = [typed_word for typed_word in users_words if typed_word not in web_texts]
        reply = messagebox.askyesno("Speedster Results",
                                    f"Your typing speed is {round(word_per_min, 0)}WPM\n"
                                    f"{len(wrong_words)} errors: {', '.join(wrong_words) if wrong_words else None}\n"
                                    f"Do you want to try again?")

        if not reply:
            speedster.destroy()
        else:
            restart()

    # Show result with uncompleted user words
    elif len(users_words) < word_length:
        type_time = stop_time - start_time
        total_secs = int(type_time.total_seconds())
        total_min = total_secs // 60

        # avoid zero division error
        if total_min == 0:
            word_per_min = word_length / (total_secs / 60)
        else:
            word_per_min = word_length / total_min
        reply = messagebox.askyesno("Speedster Results",
                                    "You did not complete the test\n"
                                    f"Your typing speed is approximately {round(word_per_min, 0)}WPM\n"
                                    f"Do you want to try again?")
        if not reply:
            speedster.destroy()
        else:
            restart()

    # Show feedback when there are no words typed
    else:
        reply = messagebox.askyesno("Speedster Results",
                                    "Empty text: You did not type anything\n"
                                    f"Do you want to try again?")
        if not reply:
            speedster.destroy()
        else:
            # Reset UI elements for a new game
            restart()


def check_typing(event):
    typed_text = display_typed_text.get("1.0", END).strip()
    users_word = typed_text.split()  # turn to word rather than character
    if not users_word or len(users_word) < len(web_texts):
        return
    if len(users_word) >= word_length:
        show_results()


def handle_escape(event):
    show_results()


# ------------------------Title and subtitle------------------
welcome_label = Label(speedster, text="Welcome to Speedster",
                      font=("Courier New", 24, "bold"), fg="#f2cec0", bg="#1E1E2E")
welcome_label.pack(pady=(10, 0))
subtitle_label = Label(speedster, text="Test Your Typing Speed",
                       font=("Courier New", 20, "normal"), fg="#f2cec0", bg="#1E1E2E")
subtitle_label.pack()

# --------------------Difficulty frame-----------------------
difficulty_label = Label(speedster, text="Select difficulty",
                         font=("Courier New", 14), fg="#F8F8F2", bg="#1E1E2E")
difficulty_label.pack(pady=(10, 0))

difficulty_var = StringVar(value="easy")  # Value assigned to radiobuttons

difficulty_frame = Frame(speedster, bg="#F8F8F2")
difficulty_frame.pack()
easy_button = Radiobutton(difficulty_frame, text="Easy (25 words)", bg="#F8F8F2",
                          fg="#1E1E2E", variable=difficulty_var, value="easy")
medium_button = Radiobutton(difficulty_frame, text="Medium (40 words)", bg="#F8F8F2",
                            fg="#1E1E2E", variable=difficulty_var, value="medium")
hard_button = Radiobutton(difficulty_frame, text="Hard (60 words)", bg="#F8F8F2",
                          fg="#1E1E2E", variable=difficulty_var, value="hard")
easy_button.grid(row=0, column=0, padx=10)
medium_button.grid(row=0, column=1, padx=10)
hard_button.grid(row=0, column=2, padx=10)

# --------------------Custom difficulty frame---------------------
custom_diff_frame = Frame(speedster, bg="#F8F8F2")
custom_diff_frame.pack()
entry_field = Entry(custom_diff_frame, width=16, font=("Courier New", 8), bg="#d9cbc5")
custom_button = Radiobutton(custom_diff_frame, text="Set Manually", bg="#F8F8F2",
                            command=lambda: entry_field.focus(), fg="#1E1E2E", variable=difficulty_var, value="custom")

custom_button.grid(row=1, column=0, padx=(10, 0))
entry_field.grid(row=1, column=1, padx=(0, 10))

# --------------------Start button--------------------------
start_button = Button(speedster, text="Start Test", font=("Courier New", 14), bg="#FFA500",
                      highlightthickness=0, fg="white", command=get_words)
start_button.pack(pady=20)

# --------------------Text Display Fields--------------------------
display_web_text = Text(speedster, height=7, width=60, wrap=WORD, font=("Courier New", 12, "bold"),
                        bg="#d9cbc5", padx=10, pady=10)
display_web_text.pack(padx=20)
display_web_text.config(state=DISABLED)

display_typed_text = Text(speedster, height=7, width=60, wrap=WORD, font=("Courier New", 12, "bold"),
                          bg="#d9cbc5", padx=10, pady=10)
display_typed_text.pack(pady=20, padx=20)
display_typed_text.insert(1.0, "Press 'Enter' to submit and 'Esc' to force ending")
display_typed_text.config(state=DISABLED)

speedster.mainloop()
