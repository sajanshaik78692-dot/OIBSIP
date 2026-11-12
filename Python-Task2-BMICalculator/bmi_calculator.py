import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt


def init_db():
    conn = sqlite3.connect("bmi_history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


class BMICalculatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("400x500")

        init_db()

        tk.Label(root, text="User Name:").pack(pady=5)
        self.user_entry = tk.Entry(root)
        self.user_entry.pack(pady=5)

        tk.Label(root, text="Weight (kg):").pack(pady=5)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.pack(pady=5)

        tk.Label(root, text="Height (m):").pack(pady=5)
        self.height_entry = tk.Entry(root)
        self.height_entry.pack(pady=5)

        tk.Button(
            root,
            text="Calculate & Save",
            command=self.calculate_bmi,
            bg="#4CAF50",
            fg="white",
        ).pack(pady=10)
        tk.Button(
            root,
            text="View Historical Trend",
            command=self.plot_trend,
            bg="#2196F3",
            fg="white",
        ).pack(pady=5)

        self.result_label = tk.Label(
            root, text="", font=("Helvetica", 12, "bold")
        )
        self.result_label.pack(pady=20)

    def calculate_bmi(self):
        username = self.user_entry.get().strip()
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter positive numerical values."
            )
            return

        bmi = round(weight / (height**2), 2)
        if bmi < 18.5:
            category = "Underweight"
            color = "#FFC107"
        elif 18.5 <= bmi < 25.0:
            category = "Normal"
            color = "#4CAF50"
        elif 25.0 <= bmi < 30.0:
            category = "Overweight"
            color = "#FF9800"
        else:
            category = "Obese"
            color = "#F44336"

        self.result_label.config(
            text=f"BMI: {bmi}\nCategory: {category}", fg=color
        )

        conn = sqlite3.connect("bmi_history.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bmi_records (username, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
            (username or "Default User", weight, height, bmi, category),
        )
        conn.commit()
        conn.close()

    def plot_trend(self):
        username = self.user_entry.get().strip() or "Default User"
        conn = sqlite3.connect("bmi_history.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, bmi FROM bmi_records WHERE username = ? ORDER BY timestamp ASC",
            (username,),
        )
        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo(
                "Info", f"No historical data found for {username}."
            )
            return

        dates = [r[0] for r in records]
        bmis = [r[1] for r in records]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, bmis, marker="o", linestyle="-", color="b")
        plt.title(f"BMI History Trend for {username}")
        plt.xlabel("Timestamp")
        plt.ylabel("BMI Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()