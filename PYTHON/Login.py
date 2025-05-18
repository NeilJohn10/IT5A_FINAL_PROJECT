import tkinter as tk
from tkinter import ttk, messagebox
from register_ui import RegisterUI
from admin_panel import AdminPanel
from user_panel import UserPanel


class LoginUI:
    def __init__(self, root, auth_manager):
        self.root = root
        self.auth = auth_manager

        # Window configuration
        self.root.title('Login System')
        self.root.geometry('350x350')
        self.root.resizable(False, False)
        self.root.configure(bg='#f5f5f5')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Colors
        self.primary_color = '#4a6baf'
        self.secondary_color = '#f5f5f5'
        self.accent_color = '#e74c3c'

        # Main container
        self.main_frame = tk.Frame(root, bg=self.secondary_color, padx=30, pady=30)
        self.main_frame.pack(expand=True, fill='both')

        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="DENTAL CLINIC",
            font=('Helvetica', 18, 'bold'),
            bg=self.secondary_color,
            fg=self.primary_color
        )
        self.title_label.pack(pady=(0, 30))

        # Username field
        self.username_frame = tk.Frame(self.main_frame, bg=self.secondary_color)
        self.username_frame.pack(fill='x', pady=(0, 15))

        self.label_username = tk.Label(
            self.username_frame,
            text='Username:',
            font=('Helvetica', 10),
            bg=self.secondary_color,
            fg='#555'
        )
        self.label_username.pack(anchor='w')

        self.entry_username = ttk.Entry(
            self.username_frame,
            font=('Helvetica', 11)
        )
        self.entry_username.pack(fill='x', pady=(5, 0), ipady=5)

        # Password field
        self.password_frame = tk.Frame(self.main_frame, bg=self.secondary_color)
        self.password_frame.pack(fill='x', pady=(0, 25))

        self.label_password = tk.Label(
            self.password_frame,
            text='Password:',
            font=('Helvetica', 10),
            bg=self.secondary_color,
            fg='#555'
        )
        self.label_password.pack(anchor='w')

        self.entry_password = ttk.Entry(
            self.password_frame,
            show='•',
            font=('Helvetica', 11)
        )
        self.entry_password.pack(fill='x', pady=(5, 0), ipady=5)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_frame, bg=self.secondary_color)
        self.buttons_frame.pack(fill='x', pady=(10, 0))

        # Login button
        self.login_button = tk.Button(
            self.buttons_frame,
            text='Login',
            command=self.validate_login,
            bg=self.primary_color,
            fg='white',
            font=('Helvetica', 10, 'bold'),
            bd=0,
            padx=20,
            pady=8,
            activebackground='#3a5a9f',
            activeforeground='white',
            cursor='hand2'
        )
        self.login_button.pack(side=tk.LEFT, padx=(0, 10))

        # Register button
        self.register_button = tk.Button(
            self.buttons_frame,
            text='Register',
            command=self.show_register_window,
            bg='#e0e0e0',
            fg='#555',
            font=('Helvetica', 10),
            bd=0,
            padx=20,
            pady=8,
            activebackground='#d0d0d0',
            activeforeground='#333',
            cursor='hand2'
        )
        self.register_button.pack(side=tk.LEFT)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.validate_login())

    # ALL ORIGINAL METHODS REMAIN EXACTLY THE SAME
    def validate_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user_type = self.auth.validate_login(username, password)

        if user_type == "admin":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.root.withdraw()
            AdminPanel(tk.Toplevel(), self.auth, self.root)
        elif user_type == "user":
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.root.withdraw()
            UserPanel(tk.Toplevel(), self.auth, self.root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_register_window(self):
        self.root.withdraw()
        RegisterUI(tk.Toplevel(), self.auth, self.root)

    def admin_panel(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username != self.auth.admin_email or password != self.auth.admin_password:
            messagebox.showerror("Access Denied", "Please login with admin credentials first")
            return

        self.root.withdraw()
        AdminPanel(tk.Toplevel(), self.auth, self.root)