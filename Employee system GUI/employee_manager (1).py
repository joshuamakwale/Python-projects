import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re
import sqlite3
import csv
from pathlib import Path

DB_FILE = "employees.db"

# -----------------------------
# Database Setup
# -----------------------------

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dob TEXT,
        email TEXT,
        phone TEXT,
        experience TEXT,
        address TEXT,
        photo TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Validation
# -----------------------------

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 7


# -----------------------------
# Login System
# -----------------------------

class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Employee System Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Username").pack(pady=5)
        self.user = tk.Entry(root)
        self.user.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=15)

    def login(self):
        if self.user.get() == "admin" and self.password.get() == "admin":
            self.root.destroy()
            main()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")


# -----------------------------
# Main Employee Application
# -----------------------------

class EmployeeApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Advanced Employee Management System")
        self.root.geometry("1100x600")

        self.photo_path = ""

        self.create_ui()
        self.refresh_table()

    # -----------------------------
    # UI
    # -----------------------------

    def create_ui(self):

        form = tk.Frame(self.root, padx=10, pady=10)
        form.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(form, text="Name").pack()
        self.name = tk.Entry(form)
        self.name.pack()

        tk.Label(form, text="DOB").pack()
        self.dob = tk.Entry(form)
        self.dob.pack()

        tk.Label(form, text="Email").pack()
        self.email = tk.Entry(form)
        self.email.pack()

        tk.Label(form, text="Phone").pack()
        self.phone = tk.Entry(form)
        self.phone.pack()

        tk.Label(form, text="Experience").pack()
        self.exp = tk.Entry(form)
        self.exp.pack()

        tk.Label(form, text="Address").pack()
        self.address = tk.Entry(form)
        self.address.pack()

        tk.Button(form, text="Upload Photo", command=self.upload_photo).pack(pady=5)

        tk.Button(form, text="Add Employee", command=self.add_employee).pack(pady=5)
        tk.Button(form, text="Update Employee", command=self.update_employee).pack(pady=5)
        tk.Button(form, text="Delete Employee", command=self.delete_employee).pack(pady=5)

        tk.Button(form, text="Export CSV", command=self.export_csv).pack(pady=5)

        tk.Button(form, text="Analytics Dashboard", command=self.show_analytics).pack(pady=5)

        # Table
        table_frame = tk.Frame(self.root)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("id", "name", "dob", "email", "phone", "experience", "address")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.upper())

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected)

        search_frame = tk.Frame(table_frame)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search").pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Find", command=self.search).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Show All", command=self.refresh_table).pack(side=tk.LEFT)

    # -----------------------------
    # CRUD Operations
    # -----------------------------

    def add_employee(self):

        data = self.get_form()

        if not data:
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO employees(name,dob,email,phone,experience,address,photo)
        VALUES(?,?,?,?,?,?,?)
        """, (*data, self.photo_path))

        conn.commit()
        conn.close()

        self.refresh_table()
        self.clear()

    def update_employee(self):

        selected = self.tree.selection()

        if not selected:
            return

        emp_id = self.tree.item(selected[0])["values"][0]

        data = self.get_form()

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("""
        UPDATE employees
        SET name=?,dob=?,email=?,phone=?,experience=?,address=?
        WHERE id=?
        """, (*data, emp_id))

        conn.commit()
        conn.close()

        self.refresh_table()

    def delete_employee(self):

        selected = self.tree.selection()

        if not selected:
            return

        emp_id = self.tree.item(selected[0])["values"][0]

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))

        conn.commit()
        conn.close()

        self.refresh_table()

    # -----------------------------
    # Helpers
    # -----------------------------

    def get_form(self):

        name = self.name.get()
        dob = self.dob.get()
        email = self.email.get()
        phone = self.phone.get()
        exp = self.exp.get()
        address = self.address.get()

        if not name:
            messagebox.showerror("Error", "Name required")
            return None

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid Email")
            return None

        if not validate_phone(phone):
            messagebox.showerror("Error", "Invalid Phone")
            return None

        return name, dob, email, phone, exp, address

    def clear(self):

        self.name.delete(0, tk.END)
        self.dob.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.exp.delete(0, tk.END)
        self.address.delete(0, tk.END)

    def upload_photo(self):

        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])

        if path:
            self.photo_path = path
            messagebox.showinfo("Photo", "Photo uploaded")

    def refresh_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        for row in cur.execute("SELECT id,name,dob,email,phone,experience,address FROM employees"):
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def load_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        self.clear()

        self.name.insert(0, values[1])
        self.dob.insert(0, values[2])
        self.email.insert(0, values[3])
        self.phone.insert(0, values[4])
        self.exp.insert(0, values[5])
        self.address.insert(0, values[6])

    def search(self):

        keyword = self.search_entry.get()

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        results = cur.execute("SELECT id,name,dob,email,phone,experience,address FROM employees WHERE name LIKE ?", (f"%{keyword}%",))

        for row in self.tree.get_children():
            self.tree.delete(row)

        for r in results:
            self.tree.insert("", tk.END, values=r)

        conn.close()

    # -----------------------------
    # Analytics Dashboard
    # -----------------------------

    def show_analytics(self):

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        total = cur.execute("SELECT COUNT(*) FROM employees").fetchone()[0]

        exp = cur.execute("SELECT experience FROM employees").fetchall()

        conn.close()

        total_exp = sum(int(e[0]) for e in exp if str(e[0]).isdigit())

        avg_exp = total_exp / len(exp) if exp else 0

        messagebox.showinfo("Analytics",
                            f"Total Employees: {total}\nAverage Experience: {avg_exp:.1f} years")

    # -----------------------------
    # Export CSV
    # -----------------------------

    def export_csv(self):

        file = filedialog.asksaveasfilename(defaultextension=".csv")

        if not file:
            return

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        rows = cur.execute("SELECT name,dob,email,phone,experience,address FROM employees").fetchall()

        conn.close()

        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "DOB", "Email", "Phone", "Experience", "Address"])
            writer.writerows(rows)

        messagebox.showinfo("Export", "CSV Export Successful")


# -----------------------------
# Run App
# -----------------------------


def main():

    init_db()

    root = tk.Tk()
    app = EmployeeApp(root)

    root.mainloop()


if __name__ == "__main__":

    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
