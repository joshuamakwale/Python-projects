import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "students.db"


# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_id TEXT UNIQUE,
        marks INTEGER
    )
    """)

    conn.commit()
    conn.close()


# ---------------- MAIN CLASS ----------------

class StudentSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("450x300")
        self.root.config(bg="#2C3E50")
        self.root.resizable(False, False)

        self.main_ui()

    # ---------------- MAIN WINDOW ----------------

    def main_ui(self):

        frame = tk.Frame(self.root, bg="#34495E", padx=20, pady=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(
            frame,
            text="Student Management System",
            font=("Arial", 16, "bold"),
            bg="#34495E",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            frame,
            text="Add Student",
            width=20,
            height=2,
            bg="#3498DB",
            fg="white",
            command=self.add_student_window
        ).pack(pady=10)

        tk.Button(
            frame,
            text="View Students",
            width=20,
            height=2,
            bg="#1ABC9C",
            fg="white",
            command=self.view_students_window
        ).pack(pady=10)

    # ---------------- ADD STUDENT ----------------

    def add_student_window(self):

        window = tk.Toplevel(self.root)
        window.title("Add Student")
        window.geometry("400x320")
        window.config(bg="#2C3E50")

        frame = tk.Frame(window, bg="#34495E", padx=20, pady=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame, text="Add Student",
                 font=("Arial", 15),
                 bg="#34495E",
                 fg="white").pack(pady=10)

        tk.Label(frame, text="Name", bg="#34495E", fg="white").pack()
        name = tk.Entry(frame, width=30)
        name.pack()

        tk.Label(frame, text="Student ID", bg="#34495E", fg="white").pack()
        sid = tk.Entry(frame, width=30)
        sid.pack()

        tk.Label(frame, text="Marks", bg="#34495E", fg="white").pack()
        marks = tk.Entry(frame, width=30)
        marks.pack()

        def save_student():

            n = name.get().strip()
            s = sid.get().strip()
            m = marks.get().strip()

            if not n or not s or not m:
                messagebox.showerror("Error", "All fields required")
                return

            if not m.isdigit():
                messagebox.showerror("Error", "Marks must be a number")
                return

            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO students(name,student_id,marks) VALUES(?,?,?)",
                    (n, s, m)
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Student added")

                name.delete(0, tk.END)
                sid.delete(0, tk.END)
                marks.delete(0, tk.END)

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Student ID already exists")

        tk.Button(
            frame,
            text="Save Student",
            width=20,
            height=2,
            bg="#1ABC9C",
            fg="white",
            command=save_student
        ).pack(pady=10)

    # ---------------- VIEW STUDENTS ----------------

    def view_students_window(self):

        window = tk.Toplevel(self.root)
        window.title("Student Records")
        window.geometry("520x400")
        window.config(bg="#2C3E50")

        columns = ("ID", "Name", "Student ID", "Marks")

        tree = ttk.Treeview(window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)

        tree.pack(fill="both", expand=True, pady=10)

        self.load_students(tree)

        tk.Button(
            window,
            text="Refresh",
            bg="#3498DB",
            fg="white",
            command=lambda: self.load_students(tree)
        ).pack(pady=5)

    # ---------------- LOAD DATA ----------------

    def load_students(self, tree):

        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.close()


# ---------------- RUN PROGRAM ----------------

create_database()

root = tk.Tk()
app = StudentSystem(root)

messagebox.showinfo(
    "Student Management System",
    "Demo Application\nBuilt by Joshua Makwale"
)

root.mainloop()