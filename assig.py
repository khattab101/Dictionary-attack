import tkinter as tk
from tkinter import ttk, messagebox
import itertools
import string
import threading

CORRECT_PASSWORD = "cookie"

# Function to load passwords from an external file
def load_password_dictionary(file_path):
    encodings = ["utf-8", "ISO-8859-1", "Windows-1252"]  # List of encodings to try
    for encoding in encodings:
        try:
            with open("./password.txt", "r", encoding=encoding) as file:
                return [line.strip() for line in file]
        except UnicodeDecodeError:
            continue  # Try the next encoding
        except FileNotFoundError:
            messagebox.showerror("Error", "Password file not found!")
            return []
    messagebox.showerror("Error", "Failed to read the file. Unsupported encoding.")
    return []

def check_password():
    entered_password = password_entry.get()
    if entered_password == CORRECT_PASSWORD:
        open_welcome_page()  # Open the welcome page on successful login
    else:
        messagebox.showerror("Login Failed", "Incorrect password!")

def dictionary_attack():
    password_dictionary = load_password_dictionary("rockyou.txt")  # Load passwords from file
    if not password_dictionary:
        return

    for guess in password_dictionary:
        if guess == CORRECT_PASSWORD:
            # Updated message to include "Hello"
            messagebox.showinfo("Dictionary Attack", f"Hello, password was found in the dictionary: {guess}")
            open_welcome_page()  # Open the welcome page on successful dictionary attack
            return
    messagebox.showinfo("Dictionary Attack", "Password not found in dictionary.")

# Function to perform a brute-force attack
def brute_force_attack():
    charset = string.ascii_letters + string.digits  # Character set: a-z, A-Z, 0-9
    max_length = 8  # Maximum password length to try

    for length in range(1, max_length + 1):  # Try passwords of length 1 to max_length
        for guess in itertools.product(charset, repeat=length):
            guess = ''.join(guess)  # Convert tuple to string
            if guess == CORRECT_PASSWORD:
                messagebox.showinfo("Brute-Force Attack", f"Password found: {guess}")
                open_welcome_page()  # Open the welcome page on successful brute-force attack
                return
    messagebox.showinfo("Brute-Force Attack", "Password not found. Brute-force attack failed.")

def start_brute_force_attack():
    # Disable the brute-force button to prevent multiple clicks
    brute_force_button.config(state=tk.DISABLED)

    # Run the brute-force attack in a separate thread
    brute_force_thread = threading.Thread(target=brute_force_attack)
    brute_force_thread.start()

    # Re-enable the button after the thread finishes
    brute_force_thread.join()
    brute_force_button.config(state=tk.NORMAL)

def open_welcome_page():
    welcome_window = tk.Toplevel(root)
    welcome_window.title("Welcome")
    welcome_window.geometry("300x200") 
    welcome_window.resizable(False, False)  
    welcome_window.configure(bg="#FFD700")  # Bright gold background

    welcome_label = ttk.Label(welcome_window, text="Welcome!", font=("Helvetica", 20, "bold"), background="#FFD700")
    welcome_label.pack(pady=50)

    close_button = ttk.Button(welcome_window, text="Close", command=welcome_window.destroy, style="Accent.TButton")
    close_button.pack(pady=10)

root = tk.Tk()
root.title("Login GUI")
root.geometry("450x350") 
root.resizable(False, False)  
root.configure(bg="#87CEEB")  # Bright sky blue background

style = ttk.Style()
style.theme_use("clam") 

# Configure bright colors for buttons and labels
style.configure("TFrame", background="#87CEEB")  # Match frame background to root
style.configure("TLabel", background="#87CEEB", foreground="#000080", font=("Helvetica", 12))  # Bright blue text
style.configure("TButton", background="#FF6347", foreground="white", font=("Helvetica", 12, "bold"))  # Bright coral buttons
style.map("TButton", background=[("active", "#FF4500")])  # Brighter coral on hover
style.configure("Accent.TButton", background="#32CD32", foreground="white", font=("Helvetica", 12, "bold"))  # Bright green for login button
style.map("Accent.TButton", background=[("active", "#228B22")])  # Darker green on hover

login_frame = ttk.Frame(root, padding="20")
login_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(login_frame, text="Login System", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

password_label = ttk.Label(login_frame, text="Enter Password:", font=("Helvetica", 12))
password_label.pack(pady=5)

password_entry = ttk.Entry(login_frame, show="*", font=("Helvetica", 12))
password_entry.pack(pady=5, ipady=5)  

login_button = ttk.Button(login_frame, text="Login", command=check_password, style="Accent.TButton")
login_button.pack(pady=10, ipady=5, ipadx=20)  

dictionary_attack_button = ttk.Button(login_frame, text="Dictionary Attack", command=dictionary_attack)
dictionary_attack_button.pack(pady=10, ipady=5, ipadx=20)

brute_force_button = ttk.Button(login_frame, text="Brute-Force Attack", command=start_brute_force_attack)
brute_force_button.pack(pady=10, ipady=5, ipadx=20)

root.mainloop()
