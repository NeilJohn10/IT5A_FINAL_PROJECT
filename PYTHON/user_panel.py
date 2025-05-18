import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, VERTICAL, RIGHT, LEFT, Y, BOTH
from tkcalendar import DateEntry


class UserPanel:
    def __init__(self, window, auth_manager, login_window):
        self.window = window
        self.auth = auth_manager
        self.login_window = login_window

        # Configure main window
        self.window.title("Dental Clinic - Patient Portal")
        self.window.state('zoomed')
        self.window.configure(bg='#ffffff')

        # Create main container
        main_frame = tk.Frame(self.window, bg='#ffffff', padx=40, pady=40)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with clinic branding
        header_frame = tk.Frame(main_frame, bg='#ffffff')
        header_frame.pack(fill=tk.X, pady=(0, 30))

        # Clinic name and logo
        clinic_name = tk.Label(header_frame,
                               text="AMPƎW DENTAL CLINIC",
                               font=('Helvetica', 24, 'bold'),
                               fg='#005b96',
                               bg='#ffffff')
        clinic_name.pack(side=tk.LEFT)

        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg='#ffffff')
        welcome_frame.pack(fill=tk.X, pady=(0, 40))

        tk.Label(welcome_frame,
                 text=f"Welcome, {self.auth.current_user}",
                 font=('Helvetica', 18),
                 fg='#333333',
                 bg='#ffffff').pack(side=tk.LEFT)

        # Main action buttons
        button_frame = tk.Frame(main_frame, bg='#ffffff')
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Button styling
        btn_style = {
            'font': ('Helvetica', 12),
            'width': 25,
            'bd': 0,
            'highlightthickness': 0,
            'activebackground': '#003d66',
            'activeforeground': 'white',
            'cursor': 'hand2'
        }

        # Book Appointment Button
        book_btn = tk.Button(button_frame,
                             text="Book New Appointment",
                             command=self.show_booking_form,
                             bg='#005b96',
                             fg='white',
                             **btn_style)
        book_btn.pack(pady=15, ipady=12)

        # View History Button
        history_btn = tk.Button(button_frame,
                                text="View Appointment History",
                                command=self.view_history,
                                bg='#005b96',
                                fg='white',
                                **btn_style)
        history_btn.pack(pady=15, ipady=12)

        # View Receipts Button
        receipt_btn = tk.Button(button_frame,
                                text="View Receipts",
                                command=self.show_receipt,
                                bg='#005b96',
                                fg='white',
                                **btn_style)
        receipt_btn.pack(pady=15, ipady=12)

        # Footer with logout
        footer_frame = tk.Frame(main_frame, bg='#ffffff')
        footer_frame.pack(fill=tk.X, pady=(40, 0))

        logout_btn = tk.Button(footer_frame,
                               text="Logout",
                               command=self.logout,
                               font=('Helvetica', 10),
                               bg='#d9534f',
                               fg='white',
                               bd=0,
                               padx=20,
                               pady=8,
                               activebackground='#c9302c',
                               cursor='hand2')
        logout_btn.pack(side=tk.RIGHT)

        self.window.protocol("WM_DELETE_WINDOW", self.logout)

    import tkinter as tk
    from tkinter import ttk
    from tkcalendar import DateEntry  # Make sure to install tkcalendar (pip install tkcalendar)

    def show_booking_form(self):
        booking_window = tk.Toplevel(self.window)
        booking_window.title("Dental Clinic - New Appointment")
        booking_window.state('zoomed')
        booking_window.configure(bg='#f5f9ff')

        # Main container
        main_frame = tk.Frame(booking_window, bg='#f5f9ff', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Form container
        form_frame = tk.Frame(main_frame, bg='white', bd=1, relief=tk.RIDGE, padx=40, pady=40)
        form_frame.pack(fill=tk.BOTH, expand=True, ipadx=20, ipady=20)

        # Title
        tk.Label(form_frame, text="New Appointment Booking",
                 font=('Helvetica', 20, 'bold'), bg='white', fg='#005b96') \
            .grid(row=0, column=0, columnspan=4, pady=(0, 30), sticky='w')

        # Form fields
        fields = [
            ("First Name:", 1, 0),
            ("Last Name:", 1, 2),
            ("Date of Birth:", 2, 0),
            ("Gender:", 2, 2),
            ("Contact Number:", 3, 0),
            ("Email Address:", 3, 2),
            ("Appointment Date:", 4, 0),
            ("Preferred Time:", 4, 2),
            ("Address:", 5, 0)
        ]

        self.entries = {}
        for label, row, col in fields:
            tk.Label(form_frame, text=label, font=('Helvetica', 11), bg='white', fg='#333') \
                .grid(row=row, column=col, padx=(10, 5), pady=10, sticky='e')

            if label == "Appointment Date:":
                entry = DateEntry(form_frame, width=20, font=('Helvetica', 11),
                                  background='#005b96', foreground='white',
                                  borderwidth=1, date_pattern='yyyy-mm-dd')
            elif label == "Gender:":
                entry = ttk.Combobox(form_frame, width=20, font=('Helvetica', 11),
                                     values=["Male", "Female", "Other", "Prefer not to say"])
            elif label == "Preferred Time:":
                entry = ttk.Combobox(form_frame, width=20, font=('Helvetica', 11),
                                     values=["Morning (9AM-12PM)", "Afternoon (1PM-5PM)", "Evening (6PM-8PM)"])
            elif label == "Address:":
                entry = tk.Text(form_frame, width=60, height=4, font=('Helvetica', 11),
                                wrap=tk.WORD, padx=5, pady=5)
                entry.grid(row=row, column=1, columnspan=3, padx=10, pady=10, sticky='w')
                self.entries[label] = entry
                continue
            else:
                entry = tk.Entry(form_frame, width=25, font=('Helvetica', 11),
                                 relief=tk.FLAT, highlightthickness=1,
                                 highlightbackground='#cccccc', highlightcolor='#4a90e2')

            entry.grid(row=row, column=col + 1, padx=(5, 20), pady=10, sticky='w')
            self.entries[label] = entry

        # Submit button function
        def submit():
            # Get the date from DateEntry and convert it to the correct format
            appointment_date = self.entries["Appointment Date:"].get_date()
            formatted_date = appointment_date.strftime('%Y-%m-%d')

            # Collect all form data
            data = {
                "first_name": self.entries["First Name:"].get().strip(),
                "last_name": self.entries["Last Name:"].get().strip(),
                "dob": self.entries["Date of Birth:"].get().strip() or None,
                "gender": self.entries["Gender:"].get().strip() or None,
                "contact": self.entries["Contact Number:"].get().strip() or None,
                "email": self.entries["Email Address:"].get().strip() or None,
                "appointment_date": formatted_date,
                "preferred_time": self.entries["Preferred Time:"].get().strip(),
                "preferred_doctor": self.preferred_doctor_cb.get().strip() or None,
                "address": self.entries["Address:"].get("1.0", tk.END).strip() or None,
                "services": [service for service, var in self.service_vars if var.get()]
            }

            # Validate required fields
            required_fields = {
                "first_name": "First Name",
                "last_name": "Last Name",
                "appointment_date": "Appointment Date",
                "preferred_time": "Preferred Time"
            }

            for field, name in required_fields.items():
                if not data[field]:
                    messagebox.showerror("Missing Information", f"{name} is required")
                    return

            if not data["services"]:
                messagebox.showerror("Missing Information", "Please select at least one service")
                return

            # Save appointment
            username = self.auth.current_user
            if username:
                success = self.auth.add_user_appointment(username, data)
                if success:
                    services_list = "\n".join(f"• {service}" for service in data["services"])
                    confirmation_msg = f"""
    Appointment Confirmed!

    Patient: {data['first_name']} {data['last_name']}
    Date: {data['appointment_date']} ({data['preferred_time']})
    Doctor: {data['preferred_doctor'] or 'Any Available Doctor'}
    Contact: {data['contact'] or 'Not provided'}

    Services booked:
    {services_list}

    We'll send a confirmation to {data['email'] or 'your contact number'}.
    """
                    messagebox.showinfo("Appointment Confirmed", confirmation_msg)

                    # Optional: Clear form fields (if keeping window open)
                    for label, widget in self.entries.items():
                        if isinstance(widget, tk.Text):
                            widget.delete("1.0", tk.END)
                        else:
                            widget.delete(0, tk.END)

                    for _, var in self.service_vars:
                        var.set(False)

                    self.preferred_doctor_cb.set("Dr Ondangan")
                    booking_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to book appointment. Please try again.")
            else:
                messagebox.showerror("Authentication Error", "You are not logged in.")

        # Dental services section with scrollable checkbox frame
        services_frame = tk.Frame(form_frame, bg='white')
        services_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0), sticky='nw')  # span 2 columns on left

        tk.Label(services_frame,
                 text="Dental Services Required:",
                 font=('Helvetica', 12, 'bold'),
                 bg='white',
                 fg='#005b96').pack(anchor='w', pady=(0, 15))

        # Scrollable frame setup for services
        scroll_canvas = Canvas(services_frame, height=140, bg='white', highlightthickness=0)
        scrollbar = Scrollbar(services_frame, orient=VERTICAL, command=scroll_canvas.yview)
        scrollable_frame = Frame(scroll_canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )

        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        services = [
            "Dental Checkup",
            "Teeth Cleaning",
            "Tooth Filling",
            "Root Canal Treatment",
            "Tooth Extraction",
            "Dental Crown",
            "Teeth Whitening",
            "Dental Implant",
            "Braces/Orthodontics",
            "Dentures"
        ]

        self.service_vars = []

        # Create checkboxes in scrollable frame (two columns)
        for i, service in enumerate(services):
            var = tk.BooleanVar()
            self.service_vars.append((service, var))

            cb = tk.Checkbutton(scrollable_frame,
                                text=service,
                                variable=var,
                                font=('Helvetica', 11),
                                bg='white',
                                activebackground='white',
                                selectcolor='#e1f0ff',
                                anchor='w')
            cb.grid(row=i // 2, column=i % 2, sticky='w', padx=10, pady=5)

        # Preferred Doctor Label and Combobox
        tk.Label(form_frame,
                 text="Preferred Doctor:",
                 font=('Helvetica', 11),
                 bg='white',
                 fg='#555555').grid(row=7, column=0, padx=(10, 5), pady=10, sticky='e')

        self.preferred_doctor_cb = ttk.Combobox(form_frame,
                                                width=22,
                                                font=('Helvetica', 11),
                                                values=["Dr Ondangan", "Dr Adlawan"])
        self.preferred_doctor_cb.grid(row=7, column=1, padx=(5, 10), pady=10, sticky='w')
        self.preferred_doctor_cb.set("Dr Ondangan")  # default value

        # Move Form buttons to the right side of services
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.grid(row=6, column=2, rowspan=3, sticky='ne', padx=(30, 10),
                          pady=(20, 0))  # row spans services + preferred doctor + some margin

        submit_btn = tk.Button(
            button_frame,
            text="Submit Appointment",
            command=submit,  # Changed to use the local submit function
            bg='#2ecc71',
            fg='white',
            font=('Helvetica', 12, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            activebackground='#27ae60',
            cursor='hand2'
        )
        submit_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(button_frame,
                               text="Cancel",
                               command=lambda: booking_window.destroy(),
                               bg='#d9534f',
                               fg='white',
                               font=('Helvetica', 12),
                               bd=0,
                               padx=30,
                               pady=10,
                               activebackground='#c9302c',
                               cursor='hand2')
        cancel_btn.pack(side=tk.TOP)

        # Clear form
        for entry in self.entries.values():
            if isinstance(entry, (ttk.Combobox, tk.Entry)):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)

        self.preferred_doctor_cb.set("Dr Ondangan")

        for _, var in self.service_vars:
            var.set(False)

    def view_history(self):
        username = self.auth.current_user
        if not username:
            messagebox.showerror("Error", "Please login to view history")
            return

        appointments = self.auth.get_user_appointments(username)
        if not appointments:
            messagebox.showinfo("No Appointments", "You don't have any appointments yet")
            return

        history_window = tk.Toplevel(self.window)
        history_window.title("Ampew Dental Clinic - Appointment History")
        history_window.state('zoomed')  # Make window fullscreen
        history_window.configure(bg='#f8f9fa')

        # Main container with padding
        main_container = tk.Frame(history_window, bg='#f8f9fa', padx=40, pady=30)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header with clinic name and title
        header_frame = tk.Frame(main_container, bg='#f8f9fa')
        header_frame.pack(fill=tk.X, pady=(0, 30))

        tk.Label(header_frame,
                 text="AMPƎW DENTAL CLINIC",
                 font=('Helvetica', 24, 'bold'),
                 bg='#f8f9fa',
                 fg='#005b96').pack(side=tk.LEFT)

        tk.Label(header_frame,
                 text="Appointment History",
                 font=('Helvetica', 18),
                 bg='#f8f9fa',
                 fg='#333333').pack(side=tk.RIGHT)

        # Create scrollable container
        canvas = tk.Canvas(main_container, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Display appointments in a modern card layout
        for i, appointment in enumerate(appointments, 1):
            # Card container
            card = tk.Frame(scrollable_frame, bg='white', bd=0, relief=tk.RIDGE)
            card.pack(fill=tk.X, pady=10, padx=20)

            # Add subtle shadow effect
            card.configure(highlightbackground="#dddddd", highlightthickness=1)

            # Card content container with padding
            content = tk.Frame(card, bg='white', padx=25, pady=20)
            content.pack(fill=tk.X)

            # Header row with appointment number and date
            header = tk.Frame(content, bg='white')
            header.pack(fill=tk.X, pady=(0, 15))

            tk.Label(header,
                     text=f"Appointment #{i}",
                     font=('Helvetica', 16, 'bold'),
                     fg='#005b96',
                     bg='white').pack(side=tk.LEFT)

            tk.Label(header,
                     text=f"Date: {appointment.get('appointment_date', 'N/A')}",
                     font=('Helvetica', 14),
                     fg='#666666',
                     bg='white').pack(side=tk.RIGHT)

            # Two-column layout for details
            details_frame = tk.Frame(content, bg='white')
            details_frame.pack(fill=tk.X, pady=10)

            # Left column - Patient details
            left_col = tk.Frame(details_frame, bg='white')
            left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            details = [
                ("Patient Name", f"{appointment.get('first_name', '')} {appointment.get('last_name', '')}"),
                ("Contact", appointment.get('contact', 'N/A')),
                ("Email", appointment.get('email', 'N/A')),
                ("Time Slot", appointment.get('preferred_time', 'N/A')),
                ("Doctor", appointment.get('preferred_doctor', 'N/A'))
            ]

            for label, value in details:
                row = tk.Frame(left_col, bg='white')
                row.pack(fill=tk.X, pady=3)

                tk.Label(row,
                         text=f"{label}:",
                         font=('Helvetica', 11, 'bold'),
                         fg='#444444',
                         bg='white',
                         width=15,
                         anchor='w').pack(side=tk.LEFT)

                tk.Label(row,
                         text=value,
                         font=('Helvetica', 11),
                         fg='#666666',
                         bg='white').pack(side=tk.LEFT, padx=(10, 0))

            # Right column - Services
            right_col = tk.Frame(details_frame, bg='white')
            right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 0))

            tk.Label(right_col,
                     text="Services:",
                     font=('Helvetica', 11, 'bold'),
                     fg='#444444',
                     bg='white').pack(anchor='w', pady=(0, 5))

            services_frame = tk.Frame(right_col, bg='white')
            services_frame.pack(fill=tk.X)

            for service in appointment.get('services', []):
                tk.Label(services_frame,
                         text=f"• {service}",  # Fixed the double equals to single equals
                         font=('Helvetica', 11),
                         fg='#666666',
                         bg='white').pack(anchor='w', pady=2)

        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add a close button at the bottom
        button_frame = tk.Frame(main_container, bg='#f8f9fa', pady=20)
        button_frame.pack(fill=tk.X)

        close_btn = tk.Button(button_frame,
                              text="Close",
                              command=history_window.destroy,
                              font=('Helvetica', 12),
                              bg='#005b96',
                              fg='white',
                              padx=30,
                              pady=10,
                              bd=0,
                              cursor='hand2')
        close_btn.pack(side=tk.RIGHT)

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