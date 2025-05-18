import tkinter as tk
from tkinter import ttk, messagebox


class RegisterUI:
    def __init__(self, window, auth_manager, login_window):
        self.window = window
        self.auth = auth_manager
        self.login_window = login_window

        # Window configuration
        self.window.title("Register")
        self.window.geometry("350x400")
        self.window.resizable(False, False)
        self.window.configure(bg='#f5f6fa')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color scheme
        self.primary_color = '#3498db'
        self.secondary_color = '#2c3e50'
        self.accent_color = '#e74c3c'
        self.bg_color = '#f5f6fa'

        # Main container
        main_frame = tk.Frame(self.window, bg=self.bg_color, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(main_frame,
                 text="Create Account",
                 font=('Helvetica', 18, 'bold'),
                 bg=self.bg_color,
                 fg=self.secondary_color).pack(pady=(0, 20))

        # Form fields
        field_config = {
            'bg': self.bg_color,
            'font': ('Helvetica', 10),
            'anchor': 'w'
        }

        entry_config = {
            'font': ('Helvetica', 11),
            'relief': 'flat',
            'highlightthickness': 1,
            'highlightbackground': '#ddd',
            'highlightcolor': self.primary_color
        }

        # Username field
        tk.Label(main_frame, text="Username:", **field_config).pack(fill=tk.X, pady=(5, 0))
        self.username_entry = tk.Entry(main_frame, **entry_config)
        self.username_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)

        # Password field
        tk.Label(main_frame, text="Password:", **field_config).pack(fill=tk.X, pady=(5, 0))
        self.password_entry = tk.Entry(main_frame, show="•", **entry_config)
        self.password_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)

        # Confirm Password field
        tk.Label(main_frame, text="Confirm Password:", **field_config).pack(fill=tk.X, pady=(5, 0))
        self.confirm_password_entry = tk.Entry(main_frame, show="•", **entry_config)
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 20), ipady=5)

        # Register Button
        tk.Button(main_frame,
                  text="Register",
                  command=self.register,
                  bg=self.primary_color,
                  fg='white',
                  font=('Helvetica', 12, 'bold'),
                  bd=0,
                  padx=20,
                  pady=8,
                  activebackground='#2980b9',
                  activeforeground='white',
                  cursor='hand2').pack(fill=tk.X, pady=(0, 15))

        # Back to Login Button
        tk.Button(main_frame,
                  text="Back to Login",
                  command=self.back_to_login,
                  bg='#ecf0f1',
                  fg='#7f8c8d',
                  font=('Helvetica', 10),
                  bd=0,
                  padx=20,
                  pady=5,
                  activebackground='#bdc3c7',
                  activeforeground='#34495e',
                  cursor='hand2').pack(fill=tk.X)

        self.window.protocol("WM_DELETE_WINDOW", self.back_to_login)

    # ALL ORIGINAL METHODS REMAIN EXACTLY THE SAME
    def register(self):
        """Handle user registration"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        # Validate all fields are filled
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Validate username length
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return

        # Validate password length
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Try to register the user
        try:
            result = self.auth.register_user(username, password)

            if result == "success":
                messagebox.showinfo("Success", "Registration successful!")
                self.back_to_login()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")

    def back_to_login(self):
        self.window.destroy()
        self.login_window.deiconify()