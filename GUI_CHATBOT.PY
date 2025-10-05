import os
import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- ChatGPT API Call ---
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.3
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# --- Tkinter GUI Setup ---
root = tk.Tk()
root.title("AI Q&A Bot 🤖")
root.geometry("700x550")
root.configure(bg="#F5F5F5")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=25, font=("Segoe UI", 10))
chat_box.pack(padx=10, pady=10)
chat_box.config(state=tk.DISABLED)

entry_frame = tk.Frame(root, bg="#F5F5F5")
entry_frame.pack(pady=5)

user_input = tk.Entry(entry_frame, width=65, font=("Segoe UI", 11))
user_input.pack(side=tk.LEFT, padx=10, pady=10)

def send_message(event=None):
    prompt = user_input.get().strip()
    if not prompt:
        messagebox.showinfo("Input Required", "Please type a question.")
        return

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {prompt}\n", "user")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)
    user_input.delete(0, tk.END)

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "Bot: Thinking...\n", "bot")
    chat_box.update()
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

    answer = ask_openai(prompt)
    chat_box.config(state=tk.NORMAL)
    chat_box.delete("end-2l", "end-1l")
    chat_box.insert(tk.END, f"Bot: {answer}\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

send_button = tk.Button(entry_frame, text="Ask", command=send_message, bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"))
send_button.pack(side=tk.RIGHT, padx=5)

user_input.bind("<Return>", send_message)

chat_box.tag_config("user", foreground="#1E90FF", font=("Segoe UI", 10, "bold"))
chat_box.tag_config("bot", foreground="#2F4F4F", font=("Segoe UI", 10))

root.mainloop()
