import tkinter as tk
from auth_manager import AuthManager
from Login import LoginUI

def main():
    root = tk.Tk()
    auth_manager = AuthManager()
    LoginUI(root, auth_manager)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Application error: {e}")
