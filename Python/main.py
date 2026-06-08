# main.py
import tkinter as tk
from elgamal_ui import ElGamalUI

def main():
    root = tk.Tk()
    # Khởi tạo luồng giao diện xử lý File
    app = ElGamalUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()