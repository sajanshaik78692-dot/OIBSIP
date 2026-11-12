import secrets
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip


class PasswordGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("450x450")

        self.history = []

        tk.Label(root, text="Password Length:").pack(pady=5)
        self.length_spin = tk.Spinbox(root, from_=8, to=64, width=5)
        self.length_spin.delete(0, "end")
        self.length_spin.insert(0, 16)
        self.length_spin.pack(pady=5)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=False)

        tk.Checkbutton(
            root, text="Include Uppercase Letters", variable=self.upper_var
        ).pack(anchor="w", padx=40)
        tk.Checkbutton(
            root, text="Include Lowercase Letters", variable=self.lower_var
        ).pack(anchor="w", padx=40)
        tk.Checkbutton(
            root, text="Include Digits", variable=self.digits_var
        ).pack(anchor="w", padx=40)
        tk.Checkbutton(
            root, text="Include Symbols", variable=self.symbols_var
        ).pack(anchor="w", padx=40)
        tk.Checkbutton(
            root,
            text="Exclude Ambiguous (0, O, 1, l, I)",
            variable=self.exclude_ambiguous_var,
        ).pack(anchor="w", padx=40)

        tk.Button(
            root,
            text="Generate Password",
            command=self.generate_password,
            bg="#008CBA",
            fg="white",
        ).pack(pady=10)

        self.password_entry = tk.Entry(
            root, font=("Courier", 12), width=30, justify="center"
        )
        self.password_entry.pack(pady=5)

        self.strength_label = tk.Label(
            root, text="Strength: -", font=("Helvetica", 10, "bold")
        )
        self.strength_label.pack(pady=5)

        tk.Button(
            root, text="Copy to Clipboard", command=self.copy_to_clipboard
        ).pack(pady=5)

        tk.Label(
            root, text="Session History (Last 5):", font=("Helvetica", 9, "bold")
        ).pack(pady=10)
        self.history_box = tk.Listbox(root, height=5, width=40)
        self.history_box.pack()

    def generate_password(self):
        length = int(self.length_spin.get())
        char_pools = []

        if self.upper_var.get():
            char_pools.append(string.ascii_uppercase)
        if self.lower_var.get():
            char_pools.append(string.ascii_lowercase)
        if self.digits_var.get():
            char_pools.append(string.digits)
        if self.symbols_var.get():
            char_pools.append(string.punctuation)

        if not char_pools:
            messagebox.showerror(
                "Error", "At least one character type must be selected."
            )
            return

        all_chars = "".join(char_pools)
        if self.exclude_ambiguous_var.get():
            for amb in "0O1lI":
                all_chars = all_chars.replace(amb, "")

        while True:
            password = "".join(
                secrets.choice(all_chars) for _ in range(length)
            )
            if all(
                any(c in pool for c in password)
                for pool in char_pools
                if any(c in all_chars for c in pool)
            ):
                break

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Strength calculation
        if length >= 14 and len(char_pools) >= 3:
            strength, color = "Strong", "green"
        elif length >= 10 and len(char_pools) >= 2:
            strength, color = "Medium", "orange"
        else:
            strength, color = "Weak", "red"

        self.strength_label.config(text=f"Strength: {strength}", fg=color)

        self.history.insert(0, password)
        self.history = self.history[:5]
        self.history_box.delete(0, tk.END)
        for p in self.history:
            self.history_box.insert(tk.END, p)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()