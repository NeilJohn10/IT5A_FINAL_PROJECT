import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, VERTICAL, RIGHT, LEFT, Y, BOTH
from tkcalendar import DateEntry


class UserPanel:
    def __init__(self, window, auth_manager, login_window):
        self.window = window
        self.auth = auth_manager
        self.login_window = login_window

        # Configure main window with a modern look
        self.window.title("Dental Clinic - Patient Portal")
        self.window.state('zoomed')
        self.window.configure(bg='#f0f2f5')  # Light gray background

        # Create main container with shadow effect
        main_frame = tk.Frame(self.window, bg='white', padx=50, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        self.add_shadow(main_frame)

        # Modern header with gradient effect
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 40))

        # Left side - Clinic logo and name
        logo_frame = tk.Frame(header_frame, bg='white')
        logo_frame.pack(side=tk.LEFT)

        clinic_name = tk.Label(logo_frame,
                             text="AMPƎW",
                             font=('Montserrat', 32, 'bold'),
                             fg='#1a73e8',
                             bg='white')
        clinic_name.pack(side=tk.LEFT)

        tk.Label(logo_frame,
                text="DENTAL CLINIC",
                font=('Montserrat', 32),
                fg='#333333',
                bg='white').pack(side=tk.LEFT, padx=(5, 0))

        # Right side - Logout button in header
        logout_btn = tk.Button(header_frame,
                             text="Logout",
                             command=self.logout,
                             font=('Helvetica', 12, 'bold'),
                             bg='#dc3545',
                             fg='white',
                             bd=0,
                             padx=30,
                             pady=12,
                             cursor='hand2')
        logout_btn.pack(side=tk.RIGHT, padx=20)
        
        # Add hover effect to logout button
        self.add_hover_effect(logout_btn, '#c82333', '#dc3545')

        # Welcome message with user info card
        welcome_frame = tk.Frame(main_frame, bg='#f8f9fa', pady=20, padx=30)
        welcome_frame.pack(fill=tk.X, pady=(0, 40))
        self.add_shadow(welcome_frame)

        tk.Label(welcome_frame,
                text=f"Welcome back, {self.auth.current_user}",
                font=('Helvetica', 20),
                fg='#333333',
                bg='#f8f9fa').pack(side=tk.LEFT)

        # Card container for main actions
        card_container = tk.Frame(main_frame, bg='white')
        card_container.pack(fill=tk.BOTH, expand=True)

        # Create action cards with hover effect
        actions = [
            ("Book New Appointment", "calendar.png", self.show_booking_form, "#4CAF50"),
            ("View Appointment History", "history.png", self.view_history, "#2196F3"),
            ("View Receipts", "receipt.png", self.show_receipt, "#FF9800")
        ]

        for i, (text, icon, command, color) in enumerate(actions):
            card = self.create_action_card(card_container, text, icon, command, color)
            card.grid(row=0, column=i, padx=20, sticky='nsew')

        card_container.grid_columnconfigure((0,1,2), weight=1)

        # Remove the old footer frame and logout button
        # Modern footer with gradient
        footer_frame = tk.Frame(main_frame, bg='#f8f9fa', pady=20)
        footer_frame.pack(fill=tk.X, pady=(40, 0))

        # logout_btn = tk.Button(footer_frame,
        #                      text="Logout",
        #                      command=self.logout,
        #                      font=('Helvetica', 12),
        #                      bg='#dc3545',
        #                      fg='white',
        #                      bd=0,
        #                      padx=30,
        #                      pady=12,
        #                      cursor='hand2')
        # logout_btn.pack(side=tk.RIGHT)
        
        # # Add hover effect to logout button
        # self.add_hover_effect(logout_btn, '#c82333', '#dc3545')

    def add_shadow(self, widget):
        """Add shadow effect to widgets"""
        widget.configure(relief=tk.RAISED,
                       highlightbackground='#dddddd',
                       highlightthickness=1)

    def create_action_card(self, parent, text, icon, command, color):
        """Create a modern card-style button with hover effect"""
        card = tk.Frame(parent, bg='white', padx=20, pady=30)
        self.add_shadow(card)

        # Icon placeholder (you can add actual icons later)
        tk.Label(card,
                text="🔷",  # Replace with actual icon
                font=('Segoe UI Emoji', 48),
                fg=color,
                bg='white').pack(pady=(0,15))

        tk.Label(card,
                text=text,
                font=('Helvetica', 14, 'bold'),
                fg='#333333',
                bg='white').pack(pady=(0,20))

        btn = tk.Button(card,
                       text="Open",
                       command=command,
                       font=('Helvetica', 12),
                       bg=color,
                       fg='white',
                       bd=0,
                       padx=30,
                       pady=10,
                       cursor='hand2')
        btn.pack()

        # Add hover effect
        self.add_hover_effect(card, '#f8f9fa', 'white')
        self.add_hover_effect(btn, self.adjust_color(color, -20), color)
        
        return card

    def add_hover_effect(self, widget, hover_color, normal_color):
        """Add hover effect to widgets"""
        widget.bind('<Enter>', lambda e: widget.configure(bg=hover_color))
        widget.bind('<Leave>', lambda e: widget.configure(bg=normal_color))

    def adjust_color(self, color, amount):
        """Adjust color brightness for hover effect"""
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        new_rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def show_booking_form(self):
        booking_window = tk.Toplevel(self.window)
        booking_window.title("Dental Clinic - New Appointment")
        booking_window.state('zoomed')
        booking_window.configure(bg='#f5f9ff')

        # Main container with scrolling
        outer_frame = tk.Frame(booking_window, bg='#f5f9ff')
        outer_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas with scrollbar
        canvas = tk.Canvas(outer_frame, bg='#f5f9ff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        
        # Main content frame
        main_frame = tk.Frame(canvas, bg='#f5f9ff', padx=40, pady=30)
        
        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create window in canvas and bind scroll region
        canvas.create_window((0, 0), window=main_frame, anchor='nw', width=canvas.winfo_screenwidth()-60)
        
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
        main_frame.bind('<Configure>', on_configure)
        
        # Add mousewheel scrolling with safe binding
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
                
        def bind_mousewheel():
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def unbind_mousewheel():
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass

        # Bind mousewheel when window gets focus
        booking_window.bind("<FocusIn>", lambda e: bind_mousewheel())
        booking_window.bind("<FocusOut>", lambda e: unbind_mousewheel())
        
        # When the window is closed, unbind the mousewheel
        def on_closing():
            unbind_mousewheel()
            booking_window.destroy()
        
        booking_window.protocol("WM_DELETE_WINDOW", on_closing)
        booking_window.focus_force()

        # Header with logo and title
        header_frame = tk.Frame(main_frame, bg='white', pady=20)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        self.add_shadow(header_frame)

        # Logo and title container
        logo_container = tk.Frame(header_frame, bg='white', padx=30)
        logo_container.pack(fill=tk.X)

        tk.Label(logo_container,
                text="AMPƎW",
                font=('Montserrat', 24, 'bold'),
                fg='#1a73e8',
                bg='white').pack(side=tk.LEFT)

        tk.Label(logo_container,
                text="DENTAL CLINIC",
                font=('Montserrat', 24),
                fg='#333333',
                bg='white').pack(side=tk.LEFT, padx=(5, 0))

        # Form container with shadow
        form_container = tk.Frame(main_frame, bg='white', padx=40, pady=30)
        form_container.pack(fill=tk.BOTH, expand=True)
        self.add_shadow(form_container)

        # Title and description
        tk.Label(form_container,
                text="New Appointment Booking",
                font=('Helvetica', 20, 'bold'),
                fg='#1a73e8',
                bg='white').pack(anchor='w', pady=(0, 10))

        tk.Label(form_container,
                text="Please fill in the details below to schedule your appointment",
                font=('Helvetica', 12),
                fg='#666666',
                bg='white').pack(anchor='w', pady=(0, 30))

        # Create two columns for better organization
        columns_frame = tk.Frame(form_container, bg='white')
        columns_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Personal Information
        left_col = tk.Frame(columns_frame, bg='white')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        tk.Label(left_col,
                text="Personal Information",
                font=('Helvetica', 14, 'bold'),
                fg='#333333',
                bg='white').pack(anchor='w', pady=(0, 15))

        # Personal Information Fields
        fields = [
            ("First Name:", "Entry"),
            ("Last Name:", "Entry"),
            ("Date of Birth:", "Date"),
            ("Gender:", "Combo", ["Male", "Female", "Other", "Prefer not to say"]),
            ("Contact Number:", "Entry"),
            ("Email Address:", "Entry"),
            ("Address:", "Text")
        ]

        self.entries = {}
        for label, field_type, *args in fields:
            field_frame = tk.Frame(left_col, bg='white')
            field_frame.pack(fill=tk.X, pady=8)

            tk.Label(field_frame,
                    text=label,
                    font=('Helvetica', 11),
                    fg='#555555',
                    bg='white',
                    width=15,
                    anchor='e').pack(side=tk.LEFT, padx=(0, 10))

            if field_type == "Entry":
                entry = tk.Entry(field_frame,
                               font=('Helvetica', 11),
                               bg='#f8f9fa',
                               relief=tk.FLAT,
                               highlightthickness=1,
                               highlightbackground='#dddddd',
                               highlightcolor='#1a73e8',
                               width=30)
            elif field_type == "Date":
                entry = DateEntry(field_frame,
                                width=28,
                                font=('Helvetica', 11),
                                background='#1a73e8',
                                foreground='white',
                                borderwidth=0,
                                date_pattern='yyyy-mm-dd')
            elif field_type == "Combo":
                entry = ttk.Combobox(field_frame,
                                   values=args[0],
                                   font=('Helvetica', 11),
                                   width=28,
                                   state='readonly')
            elif field_type == "Text":
                entry = tk.Text(field_frame,
                              height=4,
                              font=('Helvetica', 11),
                              bg='#f8f9fa',
                              relief=tk.FLAT,
                              highlightthickness=1,
                              highlightbackground='#dddddd',
                              highlightcolor='#1a73e8',
                              width=30)

            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[label] = entry

        # Right column - Appointment Details
        right_col = tk.Frame(columns_frame, bg='white')
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

        tk.Label(right_col,
                text="Appointment Details",
                font=('Helvetica', 14, 'bold'),
                fg='#333333',
                bg='white').pack(anchor='w', pady=(0, 15))

        # Appointment Details Fields
        appt_frame = tk.Frame(right_col, bg='white')
        appt_frame.pack(fill=tk.X)

        # Date and Time Selection
        tk.Label(appt_frame,
                text="Appointment Date:",
                font=('Helvetica', 11),
                fg='#555555',
                bg='white').pack(anchor='w', pady=(0, 5))

        self.entries["Appointment Date:"] = DateEntry(appt_frame,
                                                    width=30,
                                                    font=('Helvetica', 11),
                                                    background='#1a73e8',
                                                    foreground='white',
                                                    borderwidth=0,
                                                    date_pattern='yyyy-mm-dd')
        self.entries["Appointment Date:"].pack(anchor='w', pady=(0, 15))

        tk.Label(appt_frame,
                text="Preferred Time:",
                font=('Helvetica', 11),
                fg='#555555',
                bg='white').pack(anchor='w', pady=(0, 5))

        self.entries["Preferred Time:"] = ttk.Combobox(appt_frame,
                                                      values=["Morning (9AM-12PM)", 
                                                             "Afternoon (1PM-5PM)", 
                                                             "Evening (6PM-8PM)"],
                                                      font=('Helvetica', 11),
                                                      width=28,
                                                      state='readonly')
        self.entries["Preferred Time:"].pack(anchor='w', pady=(0, 15))

        # Doctor Selection
        tk.Label(appt_frame,
                text="Preferred Doctor:",
                font=('Helvetica', 11),
                fg='#555555',
                bg='white').pack(anchor='w', pady=(0, 5))

        self.preferred_doctor_cb = ttk.Combobox(appt_frame,
                                              values=["Dr Ondangan", "Dr Adlawan"],
                                              font=('Helvetica', 11),
                                              width=28,
                                              state='readonly')
        self.preferred_doctor_cb.pack(anchor='w', pady=(0, 20))
        self.preferred_doctor_cb.set("Dr Ondangan")

        # Services Section with modern styling
        services_label = tk.Label(right_col,
                text="Select Services",
                font=('Helvetica', 16, 'bold'),
                fg='#1a73e8',
                bg='white')
        services_label.pack(anchor='w', pady=(20, 15))

        # Services container with border
        services_container = tk.Frame(right_col, bg='white', relief=tk.GROOVE, bd=1)
        services_container.pack(fill=tk.X, pady=(0, 20))

        # Services frame with padding
        services_frame = tk.Frame(services_container, bg='white', padx=20, pady=15)
        services_frame.pack(fill=tk.X)

        # Services list with prices
        services = [
            "Dental Checkup - ₱500",
            "Teeth Cleaning - ₱1,500",
            "Tooth Filling - ₱800-1,500",
            "Root Canal - ₱8,000-15,000",
            "Tooth Extraction - ₱800-1,500",
            "Dental Crown - ₱8,000-15,000",
            "Teeth Whitening - ₱5,000-8,000",
            "Dental Implant - ₱50,000-80,000",
            "Braces - ₱80,000-150,000",
            "Dentures - ₱15,000-30,000"
        ]

        # Create checkboxes in a grid layout - 2 columns
        self.service_vars = []
        for i, service in enumerate(services):
            var = tk.BooleanVar()
            self.service_vars.append((service, var))
            
            # Create checkbutton
            cb = tk.Checkbutton(services_frame,
                              text=service,
                              variable=var,
                              font=('Helvetica', 11),
                              bg='white',
                              activebackground='white',
                              cursor='hand2',
                              wraplength=250)
            
            # Calculate row and column positions
            row = i // 2
            col = i % 2
            cb.grid(row=row, column=col, sticky='w', padx=10, pady=5)

        # Configure grid columns
        services_frame.grid_columnconfigure(0, weight=1, minsize=250)
        services_frame.grid_columnconfigure(1, weight=1, minsize=250)

        # Bottom button frame 
        button_frame = tk.Frame(form_container, bg='white', pady=20)
        button_frame.pack(fill=tk.X)

        # Left side - Clear form button
        clear_btn = tk.Button(button_frame,
                            text="Clear Form",
                            command=self.clear_booking_form,
                            font=('Helvetica', 12),
                            bg='#6c757d',
                            fg='white',
                            padx=30,
                            pady=12,
                            bd=0,
                            cursor='hand2')
        clear_btn.pack(side=tk.LEFT)

        # Right side buttons container
        right_buttons = tk.Frame(button_frame, bg='white')
        right_buttons.pack(side=tk.RIGHT)

        cancel_btn = tk.Button(right_buttons,
                             text="Cancel",
                             command=booking_window.destroy,
                             font=('Helvetica', 12),
                             bg='#dc3545',
                             fg='white',
                             padx=30,
                             pady=12,
                             bd=0,
                             cursor='hand2')
        cancel_btn.pack(side=tk.RIGHT, padx=10)

        submit_btn = tk.Button(right_buttons,
                             text="Book Appointment",
                             command=lambda: self.submit_booking(booking_window),
                             font=('Helvetica', 12, 'bold'),
                             bg='#28a745',
                             fg='white',
                             padx=30,
                             pady=12,
                             bd=0,
                             cursor='hand2')
        submit_btn.pack(side=tk.RIGHT)

        # Add hover effects
        for btn in [clear_btn, cancel_btn, submit_btn]:
            self.add_hover_effect(btn, 
                                self.adjust_color(btn.cget('bg'), -20),
                                btn.cget('bg'))

        # When the window is closed, unbind the mousewheel
        def on_closing():
            unbind_mousewheel()
            booking_window.destroy()
        
        booking_window.protocol("WM_DELETE_WINDOW", on_closing)
        booking_window.focus_force()

    def clear_booking_form(self):
        """Clear all form fields"""
        for entry in self.entries.values():
            if isinstance(entry, (tk.Entry, ttk.Combobox)):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
        
        for _, var in self.service_vars:
            var.set(False)

    def submit_booking(self, booking_window):
        """Handle appointment booking submission"""
        try:
            # Validate required fields
            required_fields = ["First Name:", "Last Name:", "Contact Number:", "Email Address:", 
                             "Appointment Date:", "Preferred Time:"]
            
            for field in required_fields:
                if not self.entries[field].get():
                    messagebox.showerror("Error", f"{field[:-1]} is required")
                    return

            # Get selected services
            selected_services = []
            for service, var in self.service_vars:
                if var.get():
                    selected_services.append(service)

            if not selected_services:
                messagebox.showerror("Error", "Please select at least one service")
                return

            # Get appointment details
            appointment_data = {
                'username': self.auth.current_user,
                'first_name': self.entries["First Name:"].get().strip(),
                'last_name': self.entries["Last Name:"].get().strip(),
                'date_of_birth': self.entries["Date of Birth:"].get(),
                'gender': self.entries["Gender:"].get() if "Gender:" in self.entries else "",
                'contact': self.entries["Contact Number:"].get().strip(),
                'email': self.entries["Email Address:"].get().strip(),
                'address': self.entries["Address:"].get("1.0", tk.END).strip(),
                'appointment_date': self.entries["Appointment Date:"].get(),
                'preferred_time': self.entries["Preferred Time:"].get(),
                'preferred_doctor': self.preferred_doctor_cb.get(),
                'services': selected_services
            }

            if messagebox.askyesno("Confirm Booking", "Are you sure you want to book this appointment?"):
                if self.auth.save_appointment(appointment_data):
                    messagebox.showinfo("Success", "Appointment booked successfully!")
                    booking_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save appointment")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def view_history(self):
        """Display appointment history in a scrollable window"""
        username = self.auth.current_user
        if not username:
            messagebox.showerror("Error", "Please login to view history")
            return

        try:
            # Get appointments from database 
            appointments = self.auth.get_user_appointments(username)
            if not appointments:
                messagebox.showinfo("No Appointments", "You don't have any appointments yet")
                return

            # Create history window
            history_window = tk.Toplevel(self.window)
            history_window.title("Ampew Dental Clinic - Appointment History")
            history_window.state('zoomed')
            history_window.configure(bg='#f8f9fa')

            # Main container with scrolling
            outer_frame = tk.Frame(history_window, bg='#f8f9fa', padx=40, pady=30)
            outer_frame.pack(fill=tk.BOTH, expand=True)

            # Create canvas with scrollbar
            canvas = tk.Canvas(outer_frame, bg='#f8f9fa', highlightthickness=0)
            scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
            
            # Main content frame
            scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
            
            # Configure scrolling
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_screenwidth()-100)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Safe mousewheel scrolling
            def _on_mousewheel(event):
                try:
                    if canvas.winfo_exists():
                        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                except:
                    pass

            def bind_mousewheel():
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
            def unbind_mousewheel():
                try:
                    canvas.unbind_all("<MouseWheel>")
                except:
                    pass
            
            # Bind mousewheel when window gets focus    
            history_window.bind("<FocusIn>", lambda e: bind_mousewheel())
            history_window.bind("<FocusOut>", lambda e: unbind_mousewheel())

            # Setup header
            header_frame = tk.Frame(scrollable_frame, bg='white', pady=20)
            header_frame.pack(fill=tk.X, pady=(0,20))
            self.add_shadow(header_frame)

            tk.Label(header_frame,
                    text="Appointment History",
                    font=('Helvetica', 24, 'bold'),
                    fg='#1a73e8',
                    bg='white').pack(pady=10)

            # Display appointments
            for appointment in appointments:
                # Create appointment card
                card = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20)
                card.pack(fill=tk.X, pady=10)
                self.add_shadow(card)

                # Appointment header
                tk.Label(card,
                        text=f"Appointment Date: {appointment['appointment_date']}",
                        font=('Helvetica', 14, 'bold'),
                        fg='#333',
                        bg='white').pack(anchor='w')

                tk.Label(card,
                        text=f"Time: {appointment['preferred_time']}",
                        font=('Helvetica', 12),
                        fg='#666',
                        bg='white').pack(anchor='w')

                ttk.Separator(card, orient='horizontal').pack(fill=tk.X, pady=10)

                # Services
                services_text = "\n".join(f"• {service}" for service in appointment['services'])
                tk.Label(card,
                        text=f"Services:\n{services_text}",
                        font=('Helvetica', 11),
                        fg='#666',
                        justify=tk.LEFT,
                        bg='white').pack(anchor='w', pady=5)

            # Pack canvas and scrollbar
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Handle window close
            def on_closing():
                unbind_mousewheel()
                history_window.destroy()

            history_window.protocol("WM_DELETE_WINDOW", on_closing)
            history_window.focus_force()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading appointments: {str(e)}")

    def show_receipt(self):
        username = self.auth.current_user
        if not username:
            messagebox.showerror("Error", "Please login to view receipts")
            return

        receipt_text = self.auth.get_user_receipt(username)
        if not receipt_text or receipt_text == "No receipt generated yet.":
            messagebox.showinfo("No Receipts", "You don't have any receipts yet")
            return

        receipt_window = tk.Toplevel(self.window)
        receipt_window.title("Ampew Dental Clinic - Receipt")
        receipt_window.geometry("700x800")
        receipt_window.configure(bg='#f8f9fa')

        header_frame = tk.Frame(receipt_window, bg='#f8f9fa', padx=30, pady=20)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame,
                 text="Your Receipt",
                 font=('Helvetica', 18, 'bold'),
                 bg='#f8f9fa',
                 fg='#005b96').pack()

        receipt_frame = tk.Frame(receipt_window, bg='white', bd=1, relief=tk.RIDGE)
        receipt_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

        text_widget = tk.Text(receipt_frame,
                              wrap=tk.WORD,
                              font=('Courier', 12),
                              padx=20,
                              pady=20)
        text_widget.pack(fill=tk.BOTH, expand=True)

        text_widget.insert(tk.END, receipt_text)
        text_widget.config(state='disabled')

    def logout(self):
        self.auth.current_user = None
        self.window.destroy()
        self.login_window.deiconify()