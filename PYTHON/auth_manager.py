import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json


class AuthManager:
    def __init__(self):
        self.current_user = None
        self.admin_email = "admin"
        self.admin_password = "123123"
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'auth_plugin': 'mysql_native_password'
        }

        # Initialize users list
        self.users = []

        # Initialize database and tables
        self._initialize_system()

        # Load users at startup
        self.load_users()

    def delete_user(self, username):
        """
        Delete a user from the system

        Args:
            username (str): The username to delete

        Returns:
            bool: True if user was deleted, False otherwise
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Delete the user from the database
            cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()

            # Check if any rows were affected
            if cursor.rowcount > 0:
                # Update the users list
                if username in self.users:
                    self.users.remove(username)
                return True
            return False

        except Error as e:
            print(f"Error deleting user: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def archive_user(self, username):
        """Archive a user instead of deleting"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Move user to archived status
            cursor.execute("""
                UPDATE users 
                SET status = 'archived' 
                WHERE username = %s
            """, (username,))
            
            conn.commit()
            success = cursor.rowcount > 0

            if success:
                self.load_users()  # Reload active users list
            return success

        except Error as e:
            print(f"Error archiving user: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def _initialize_system(self):
        """Initialize the complete database system"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS dental_clinic_system")
            cursor.execute("USE dental_clinic_system")

            # Update users table to include status
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    status VARCHAR(20) DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)

            # Update existing users to have status if not set
            try:
                cursor.execute("UPDATE users SET status = 'active' WHERE status IS NULL")
            except Error:
                pass

            conn.commit()
            self.db_config['database'] = 'dental_clinic_system'

        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def get_archived_users(self):
        """Get list of archived users"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT username FROM users WHERE status = 'archived'")
            users = cursor.fetchall()
            return [user[0] for user in users]

        except Error as e:
            print(f"Error getting archived users: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def load_users(self):
        """Load only active users"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT username FROM users WHERE status = 'active'")
            users = cursor.fetchall()
            self.users = [user[0] for user in users]
            return True

        except Error as e:
            print(f"Error loading users: {e}")
            self.users = []
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def register_user(self, username, password):
        """Register a new user"""
        if not username or not password:
            return "Please fill all fields"

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
            if cursor.fetchone()[0] > 0:
                return "Username already exists"

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            conn.commit()

            # Update users list
            self.load_users()

            print(f"User {username} registered successfully")
            return "success"

        except Error as e:
            print(f"Registration error: {e}")
            if 'conn' in locals():
                conn.rollback()
            return "Could not save user data"
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def validate_login(self, username, password):
        """Validate user login credentials"""
        if username == self.admin_email and password == self.admin_password:
            self.current_user = username
            return "admin"

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()

            if user:
                self.current_user = username
                return "user"
            return None

        except Error as e:
            print(f"Login error: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def add_user_appointment(self, username, appointment_data):
        """Add new appointment for user"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Get user ID
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return False

            user_id = result[0]

            # Format the appointment date
            if isinstance(appointment_data['appointment_date'], str):
                appointment_date = datetime.strptime(appointment_data['appointment_date'], '%Y-%m-%d').date()
            else:
                appointment_date = appointment_data['appointment_date']

            # Insert appointment
            insert_query = """
                           INSERT INTO appointments (user_id, first_name, last_name, dob, gender, \
                                                     contact, email, appointment_date, preferred_time, \
                                                     preferred_doctor, address, status) \
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                           """
            cursor.execute(insert_query, (
                user_id,
                appointment_data['first_name'],
                appointment_data['last_name'],
                appointment_data.get('dob', None),
                appointment_data.get('gender', None),
                appointment_data['contact'],
                appointment_data.get('email', None),
                appointment_date,
                appointment_data['preferred_time'],
                appointment_data['preferred_doctor'],
                appointment_data.get('address', None),
                'pending'
            ))

            appointment_id = cursor.lastrowid

            # Add services
            if appointment_data['services']:
                service_query = "INSERT INTO services (appointment_id, service_name) VALUES (%s, %s)"
                service_values = [(appointment_id, service) for service in appointment_data['services']]
                cursor.executemany(service_query, service_values)

            # Generate and store receipt
            receipt_text = self._generate_receipt(appointment_data, appointment_id)
            cursor.execute(
                "INSERT INTO receipts (user_id, receipt_text, amount) VALUES (%s, %s, %s)",
                (user_id, receipt_text, 0.00)
            )

            conn.commit()
            return True

        except Error as e:
            print(f"Error adding appointment: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def _generate_receipt(self, appointment_data, appointment_id):
        """Generate receipt text"""
        services_text = "\n".join(f"• {service}" for service in appointment_data['services'])

        # Format the appointment date
        try:
            if isinstance(appointment_data['appointment_date'], str):
                appointment_date = datetime.strptime(appointment_data['appointment_date'], '%Y-%m-%d').strftime(
                    '%Y-%m-%d')
            else:
                appointment_date = appointment_data['appointment_date'].strftime('%Y-%m-%d')
        except (ValueError, AttributeError):
            appointment_date = str(appointment_data['appointment_date'])

        receipt = f"""
AMPƎW DENTAL CLINIC
Receipt #{appointment_id}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Patient Information:
------------------
Name: {appointment_data['first_name']} {appointment_data['last_name']}
Contact: {appointment_data['contact']}
Email: {appointment_data.get('email', 'N/A')}

Appointment Details:
------------------
Date: {appointment_date}
Time: {appointment_data['preferred_time']}
Doctor: {appointment_data['preferred_doctor']}

Services:
---------
{services_text}

Thank you for choosing AMPƎW DENTAL CLINIC!
"""
        return receipt

    def get_user_appointments(self, username):
        """Get appointments for specific user from database"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            # Get user's appointments with complete details
            query = """
                SELECT 
                    a.*,
                    GROUP_CONCAT(s.service_name) as services,
                    u.username,
                    CONCAT(a.first_name, ' ', a.last_name) as patient_name,
                    a.email,
                    a.contact,
                    a.gender,
                    a.dob as date_of_birth,
                    a.address,
                    a.appointment_date,
                    a.preferred_time,
                    a.preferred_doctor,
                    a.status,
                    a.created_at
                FROM appointments a
                LEFT JOIN services s ON a.id = s.appointment_id
                JOIN users u ON a.user_id = u.id
                WHERE u.username = %s
                GROUP BY a.id
                ORDER BY a.appointment_date DESC, a.created_at DESC
            """
            cursor.execute(query, (username,))
            appointments = cursor.fetchall()

            # Process results
            for appt in appointments:
                if appt['services']:
                    appt['services'] = appt['services'].split(',')
                else:
                    appt['services'] = []
                    
                # Convert date objects to string format
                for date_field in ['appointment_date', 'date_of_birth', 'created_at']:
                    if appt.get(date_field):
                        appt[date_field] = appt[date_field].strftime('%Y-%m-%d')

            return appointments

        except Error as e:
            print(f"Error getting appointments: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def get_user_receipt(self, username):
        """Get latest receipt for a user"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            query = """
                    SELECT r.receipt_text
                    FROM receipts r
                             JOIN users u ON r.user_id = u.id
                    WHERE u.username = %s
                    ORDER BY r.created_at DESC LIMIT 1 \
                    """
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result['receipt_text'] if result else None

        except Error as e:
            print(f"Error getting receipt: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def get_user_services(self, username):
        """Get all services for a specific user"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            query = """
                    SELECT DISTINCT s.service_name
                    FROM services s
                             JOIN appointments a ON s.appointment_id = a.id
                             JOIN users u ON a.user_id = u.id
                    WHERE u.username = %s \
                    """
            cursor.execute(query, (username,))
            services = cursor.fetchall()
            return [service['service_name'] for service in services]

        except Error as e:
            print(f"Error getting user services: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def set_user_receipt(self, username, receipt_text):
        """Save a new receipt for a user"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # Get user ID
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return False

            user_id = result[0]

            # Insert receipt
            cursor.execute(
                "INSERT INTO receipts (user_id, receipt_text, amount) VALUES (%s, %s, %s)",
                (user_id, receipt_text, 0.00)
            )
            conn.commit()
            return True

        except Error as e:
            print(f"Error saving receipt: {e}")
            if 'conn' in locals():
                conn.rollback()
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def save_appointment(self, appointment_data):
        """Save appointment data to database"""
        try:
            return self.add_user_appointment(self.current_user, appointment_data)
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return False