import tkinter as tk
from tkinter import ttk, messagebox


class AdminPanel:
    def __init__(self, window, auth_manager, login_window):
        self.window = window
        self.auth = auth_manager
        self.login_window = login_window
        self.window.title("Admin Panel")
        self.window.geometry("900x650")
        self.window.configure(bg='#f5f6fa')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color scheme
        self.primary_color = '#3498db'
        self.secondary_color = '#2c3e50'
        self.accent_color = '#e74c3c'
        self.bg_color = '#f5f6fa'
        self.text_bg = '#ffffff'

        # Reload users at start
        self.auth.load_users()

        # Main container
        main_frame = tk.Frame(self.window, bg=self.bg_color, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Users list
        left_frame = tk.Frame(main_frame, bg=self.bg_color, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right panel - User details
        right_frame = tk.Frame(main_frame, bg=self.bg_color, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left panel widgets
        tk.Label(left_frame,
                 text="Admin Dashboard",
                 font=('Helvetica', 16, 'bold'),
                 bg=self.bg_color,
                 fg=self.secondary_color).pack(pady=(0, 20))

        # Search bar
        tk.Label(left_frame, text="Search Users:", font=('Helvetica', 10), bg=self.bg_color).pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(left_frame, textvariable=self.search_var, font=('Helvetica', 10))
        self.search_entry.pack(fill=tk.X, pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search)

        tk.Label(left_frame,
                 text="Registered Users:",
                 font=('Helvetica', 10),
                 bg=self.bg_color).pack(anchor='w')

        # Users listbox with scrollbar
        list_frame = tk.Frame(left_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.users_listbox = tk.Listbox(
            list_frame,
            height=15,
            width=30,
            font=('Helvetica', 10),
            bg=self.text_bg,
            relief='flat',
            yscrollcommand=scrollbar.set
        )
        self.users_listbox.pack(fill=tk.BOTH, expand=True)
        self.users_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        scrollbar.config(command=self.users_listbox.yview)

        # Button frame
        btn_frame = tk.Frame(left_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="Refresh Users",
            command=self.reload_users,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            btn_frame,
            text="Generate Receipt",
            command=self.generate_receipt,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Add the Delete User button
        ttk.Button(
            btn_frame,
            text="Delete User",
            command=self.delete_user,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        ttk.Button(
            left_frame,
            text="Logout",
            command=self.logout,
            style='Secondary.TButton'
        ).pack(fill=tk.X, pady=(10, 0))

        # Right panel widgets
        tk.Label(right_frame,
                 text="User Services",
                 font=('Helvetica', 14, 'bold'),
                 bg=self.bg_color,
                 fg=self.secondary_color).pack(pady=(0, 15))

        # Services text area with scrollbar
        services_frame = tk.Frame(right_frame, bg=self.bg_color)
        services_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        scrollbar_services = ttk.Scrollbar(services_frame)
        scrollbar_services.pack(side=tk.RIGHT, fill=tk.Y)

        self.services_text = tk.Text(
            services_frame,
            height=10,
            width=40,
            font=('Helvetica', 10),
            bg=self.text_bg,
            relief='flat',
            wrap=tk.WORD,
            yscrollcommand=scrollbar_services.set
        )
        self.services_text.pack(fill=tk.BOTH, expand=True)
        self.services_text.config(state='disabled')
        scrollbar_services.config(command=self.services_text.yview)

        # Anesthesia dosage
        tk.Label(right_frame,
                 text="Anesthesia Dosage:",
                 font=('Helvetica', 10),
                 bg=self.bg_color).pack(anchor='w', pady=(5, 0))

        self.anesthesia_entry = ttk.Entry(
            right_frame,
            font=('Helvetica', 10)
        )
        self.anesthesia_entry.pack(fill=tk.X, pady=(0, 5))

        # Prescription field
        tk.Label(right_frame,
                 text="Prescription:",
                 font=('Helvetica', 10),
                 bg=self.bg_color).pack(anchor='w', pady=(5, 0))

        self.prescription_entry = tk.Text(
            right_frame,
            height=3,
            font=('Helvetica', 10),
            wrap=tk.WORD
        )
        self.prescription_entry.pack(fill=tk.X, pady=(0, 5))

        # Doctor's recommendation
        tk.Label(right_frame,
                 text="Doctor's Recommendation:",
                 font=('Helvetica', 10),
                 bg=self.bg_color).pack(anchor='w', pady=(5, 0))

        self.recommendation_entry = tk.Text(
            right_frame,
            height=3,
            font=('Helvetica', 10),
            wrap=tk.WORD
        )
        self.recommendation_entry.pack(fill=tk.X, pady=(0, 10))

        # Overall pay
        tk.Label(right_frame,
                 text="Overall Pay:",
                 font=('Helvetica', 10),
                 bg=self.bg_color).pack(anchor='w', pady=(5, 0))

        self.pay_entry = ttk.Entry(
            right_frame,
            font=('Helvetica', 10)
        )
        self.pay_entry.pack(fill=tk.X, pady=(0, 10))

        # Configure styles
        self.style.configure('Primary.TButton',
                             foreground='white',
                             background=self.primary_color,
                             font=('Helvetica', 10, 'bold'),
                             padding=8)

        self.style.configure('Secondary.TButton',
                             foreground='white',
                             background=self.accent_color,
                             font=('Helvetica', 10, 'bold'),
                             padding=8)

        self.style.map('Primary.TButton',
                       background=[('active', '#2980b9')])

        self.style.map('Secondary.TButton',
                       background=[('active', '#c0392b')])

        self.window.protocol("WM_DELETE_WINDOW", self.logout)
        self.display_users()

    def on_search(self, event):
        search_text = self.search_var.get().lower()
        self.users_listbox.delete(0, tk.END)
        for username in self.auth.users:
            if username == self.auth.admin_email:
                continue
            if search_text in username.lower():
                self.users_listbox.insert(tk.END, username)

    def reload_users(self):
        self.auth.load_users()
        self.display_users()
        messagebox.showinfo("Info", "User list refreshed.")

    def display_users(self):
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ''
        self.users_listbox.delete(0, tk.END)
        for username in self.auth.users:
            if username == self.auth.admin_email:
                continue
            if search_text in username.lower():
                self.users_listbox.insert(tk.END, username)

    def on_user_select(self, event):
        if not self.users_listbox.curselection():
            return

        selected_user = self.users_listbox.get(self.users_listbox.curselection())
        self.display_user_services(selected_user)

    def display_user_services(self, username):
        self.services_text.config(state='normal')
        self.services_text.delete(1.0, tk.END)

        services = self.auth.get_user_services(username)

        self.services_text.insert(tk.END, f"Services for {username}:\n\n")
        if services:
            for service in services:
                self.services_text.insert(tk.END, f"- {service}\n")
        else:
            self.services_text.insert(tk.END, "No services selected yet")

        self.services_text.config(state='disabled')

    def delete_user(self):
        if not self.users_listbox.curselection():
            messagebox.showerror("Error", "Please select a user first.")
            return

        # Get selected user index and username
        selected_index = self.users_listbox.curselection()[0]
        username = self.users_listbox.get(selected_index)

        # Prevent deletion of admin account
        if username == self.auth.admin_email:
            messagebox.showerror("Error", "Cannot delete admin account!")
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete user '{username}'?\nThis action cannot be undone!",
            icon='warning'
        )

        if confirm:
            try:
                # Delete the user
                success = False
                if hasattr(self.auth, 'delete_user'):
                    success = self.auth.delete_user(username)
                else:
                    # Fallback if delete_user method doesn't exist
                    if isinstance(self.auth.users, list):
                        # Handle list-based user storage
                        for i, user in enumerate(self.auth.users):
                            if user == username or (isinstance(user, dict) and user.get('username') == username):
                                self.auth.users.pop(i)
                                success = True
                                break
                    elif isinstance(self.auth.users, dict):
                        # Handle dictionary-based user storage
                        if username in self.auth.users:
                            del self.auth.users[username]
                            success = True

                    # Save changes if we made any
                    if success and hasattr(self.auth, 'save_users'):
                        self.auth.save_users()

                if success:
                    # Clear the user's information from display
                    self.services_text.config(state='normal')
                    self.services_text.delete(1.0, tk.END)
                    self.services_text.config(state='disabled')
                    self.anesthesia_entry.delete(0, tk.END)
                    self.prescription_entry.delete(1.0, tk.END)
                    self.recommendation_entry.delete(1.0, tk.END)
                    self.pay_entry.delete(0, tk.END)

                    # Refresh the user list
                    self.reload_users()
                    messagebox.showinfo("Success", f"User '{username}' has been deleted.")
                else:
                    messagebox.showerror("Error", f"Failed to delete user '{username}'.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_receipt(self):
        if not self.users_listbox.curselection():
            messagebox.showerror("Error", "Please select a user first.")
            return

        username = self.users_listbox.get(self.users_listbox.curselection())
        first_name = username
        last_name = ""

        services = self.auth.get_user_services(username)
        anesthesia_dosage = self.anesthesia_entry.get().strip()
        prescription = self.prescription_entry.get("1.0", tk.END).strip()
        recommendation = self.recommendation_entry.get("1.0", tk.END).strip()
        overall_pay = self.pay_entry.get().strip()

        if not anesthesia_dosage or not overall_pay:
            messagebox.showerror("Error", "Please enter anesthesia dosage and overall pay.")
            return

        receipt_text = (
            f"Receipt for {first_name} {last_name}\n"
            f"---------------------------------\n"
            f"Services:\n"
        )
        if services:
            for serv in services:
                receipt_text += f"- {serv}\n"
        else:
            receipt_text += "No services selected\n"

        receipt_text += (
            f"\nAnesthesia Dosage: {anesthesia_dosage}\n"
            f"\nPrescription:\n{prescription}\n"
            f"\nDoctor's Recommendation:\n{recommendation}\n"
            f"\nOverall Pay: {overall_pay}\n"
            "---------------------------------\n"
            "Thank you for your visit!"
        )

        # Save receipt to user data
        success = self.auth.set_user_receipt(username, receipt_text)
        if success:
            messagebox.showinfo("Success", f"Receipt saved and sent to {username}.")
        else:
            messagebox.showerror("Error", "Could not save receipt.")

        # Show receipt preview
        receipt_window = tk.Toplevel(self.window)
        receipt_window.title("Receipt Preview")
        text_widget = tk.Text(receipt_window, width=60, height=25, font=('Courier', 10))
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, receipt_text)
        text_widget.config(state='disabled')

    def logout(self):
        self.auth.current_user = None
        self.window.destroy()
        self.login_window.deiconify()