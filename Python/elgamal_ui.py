# elgamal_ui.py
import tkinter as tk
from tkinter import messagebox, ttk
from elgamal_math import ElGamalMath
import random


class ElGamalUI:
    """
    Lớp quản lý giao diện đồ họa (UI) phiên bản cải tiến thẩm mỹ và điều khiển luồng sự kiện.
    Áp dụng màu sắc hiện đại, tăng khoảng cách padding và phân cấp nút bấm rõ ràng.
    """

    def __init__(self, root: tk.Tk):
        """
        Khởi tạo đối tượng giao diện ứng dụng ElGamal với thiết kế mới.

        Args:
            root (tk.Tk): Cửa sổ gốc của ứng dụng Tkinter.
        """
        self.root = root
        self.root.title("HỆ THỐNG MÃ HÓA & GIẢI MÃ ELGAMAL")
        self.root.geometry("820x720")
        self.root.configure(bg="#F5F7FA")  # Màu nền tổng thể sáng sủa, hiện đại

        # Các thuộc tính lưu trữ trạng thái dữ liệu
        self.p = self.g = self.x = self.y = None
        self.current_cipher = []

        # Thiết lập cấu trúc giao diện
        self._init_styles()
        self._build_widgets()

    def _init_styles(self):
        """Thiết lập cấu hình giao diện nâng cao (Ttk Styles) với màu sắc chủ đề."""
        style = ttk.Style()
        style.theme_use('clam')

        # Cấu hình phong cách cho các Group Box (LabelFrame)
        style.configure("TLabelframe", background="#F5F7FA", bordercolor="#E4E7EB")
        style.configure("TLabelframe.Label", background="#F5F7FA", font=("Helvetica", 11, "bold"), foreground="#1E3D59")

        # Cấu hình phong cách cho các nút bấm
        style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#17B890",
                        borderwidth=0)
        style.map("Primary.TButton", background=[('active', '#139675'), ('pressed', '#0F785D')])

        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#1E3D59",
                        borderwidth=0)
        style.map("Accent.TButton", background=[('active', '#173046'), ('pressed', '#102232')])

        style.configure("Danger.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#FF6B6B",
                        borderwidth=0)
        style.map("Danger.TButton", background=[('active', '#E85A5A'), ('pressed', '#CF4F4F')])

    def _build_widgets(self):
        """Xây dựng kết cấu, bố cục Layout và định vị các thành phần đồ họa theo lưới cân đối."""

        # --- TIÊU ĐỀ CHÍNH ---
        title_container = tk.Frame(self.root, bg="#1E3D59", height=70)
        title_container.pack(fill="x", side="top")
        title_container.pack_propagate(False)

        title_lbl = tk.Label(
            title_container,
            text="PHẦN MỀM MÔ PHỎNG HỆ MẬT KHÓA CÔNG KHAI ELGAMAL",
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg="#1E3D59"
        )
        title_lbl.pack(expand=True)

        # Toàn bộ nội dung nằm trong một khung đệm (Main Padding Frame)
        main_frame = tk.Frame(self.root, bg="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # ----------------- KHUNG 1: KHỞI TẠO KHÓA -----------------
        key_frame = ttk.LabelFrame(main_frame, text=" 1. THIẾT LẬP CẶP KHÓA HỆ THỐNG ")
        key_frame.pack(fill="x", pady=8, ipady=5)

        # Grid layout bên trong khung sinh khóa
        tk.Label(key_frame, text="Nhập số nguyên tố (p):", font=("Helvetica", 10), bg="#F5F7FA").grid(row=0, column=0,
                                                                                                      padx=15, pady=10,
                                                                                                      sticky="w")
        self.ent_p = ttk.Entry(key_frame, width=15, font=("Helvetica", 10))
        self.ent_p.insert(0, "65537")
        self.ent_p.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        btn_gen = ttk.Button(key_frame, text="Tự Động Sinh Khóa", style="Primary.TButton",
                             command=self._on_generate_keys)
        btn_gen.grid(row=0, column=2, padx=20, pady=10, ipadx=10)

        # Khu vực hiển thị thông số sau khi sinh khóa
        info_frame = tk.Frame(key_frame, bg="#E4E7EB", height=1, bd=0)
        info_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=15, pady=5)
        tk.Label(key_frame, text="Toán tử gốc (g):", font=("Helvetica", 10), fg="#4A5568", bg="#F5F7FA").grid(row=2,
                                                                                                              column=0,
                                                                                                              padx=15,
                                                                                                              pady=5,
                                                                                                              sticky="w")
        self.lbl_g = tk.Label(key_frame, text="Chưa khởi tạo", font=("Helvetica", 10, "bold"), fg="#2B6CB0",
                              bg="#F5F7FA")
        self.lbl_g.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(key_frame, text="Khóa Bí Mật (x):", font=("Helvetica", 10), fg="#4A5568", bg="#F5F7FA").grid(row=2,
                                                                                                              column=2,
                                                                                                              padx=15,
                                                                                                              pady=5,
                                                                                                              sticky="w")
        self.lbl_x = tk.Label(key_frame, text="Chưa khởi tạo", font=("Helvetica", 10, "bold"), fg="#C53030",
                              bg="#F5F7FA")
        self.lbl_x.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        tk.Label(key_frame, text="Khóa Công Khai (y):", font=("Helvetica", 10), fg="#4A5568", bg="#F5F7FA").grid(row=3,
                                                                                                                 column=0,
                                                                                                                 padx=15,
                                                                                                                 pady=5,
                                                                                                                 sticky="w")
        self.lbl_y = tk.Label(key_frame, text="Chưa khởi tạo", font=("Helvetica", 9, "bold"), fg="#2F855A",
                              bg="#F5F7FA", wraplength=500, justify="left")
        self.lbl_y.grid(row=3, column=1, padx=5, pady=5, columnspan=3, sticky="w")

        # ----------------- KHUNG 2: QUÁ TRÌNH MÃ HÓA -----------------
        enc_frame = ttk.LabelFrame(main_frame, text=" 2. PHÂN HỆ MÃ HÓA VĂN BẢN (SENDER) ")
        enc_frame.pack(fill="x", pady=8, ipady=5)

        tk.Label(enc_frame, text="Văn bản rõ (Plaintext):", font=("Helvetica", 10), bg="#F5F7FA").grid(row=0, column=0,
                                                                                                       padx=15, pady=8,
                                                                                                       sticky="nw")

        self.txt_plain = tk.Text(enc_frame, height=3, width=54, font=("Courier New", 10), bd=1, relief="solid")
        self.txt_plain.insert("1.0", "Hello ElGamal 2026!")
        self.txt_plain.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        btn_enc = ttk.Button(enc_frame, text="Thực Hiện Mã Hóa", style="Accent.TButton", command=self._on_encrypt)
        btn_enc.grid(row=1, column=1, pady=5, sticky="e", ipadx=10)

        tk.Label(enc_frame, text="Bản mã nhận được (C):\nFormat: (c1, c2)", font=("Helvetica", 10), bg="#F5F7FA").grid(
            row=2, column=0, padx=15, pady=8, sticky="nw")

        self.txt_cipher = tk.Text(enc_frame, height=3, width=54, font=("Courier New", 10), bg="#EDF2F7", fg="#2D3748",
                                  bd=1, relief="solid", state="disabled")
        self.txt_cipher.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        # ----------------- KHUNG 3: QUÁ TRÌNH GIẢI MÃ -----------------
        dec_frame = ttk.LabelFrame(main_frame, text=" 3. PHÂN HỆ GIẢI MÃ BẢN MÃ (RECEIVER) ")
        dec_frame.pack(fill="x", pady=8, ipady=5)

        # Căn giữa nút bấm Giải mã
        btn_container = tk.Frame(dec_frame, bg="#F5F7FA")
        btn_container.pack(fill="x", pady=5)
        btn_dec = ttk.Button(btn_container, text="Thực Hiện Giải Mã", style="Danger.TButton", command=self._on_decrypt)
        btn_dec.pack(ipadx=15, ipady=2)

        output_container = tk.Frame(dec_frame, bg="#F5F7FA")
        output_container.pack(fill="x", padx=15, pady=5)

        tk.Label(output_container, text="Văn bản gốc khôi phục (Decrypted Text):", font=("Helvetica", 10),
                 bg="#F5F7FA").pack(anchor="w", pady=2)
        self.txt_decrypted = tk.Text(output_container, height=3, width=73, font=("Courier New", 10, "bold"),
                                     bg="#EDF2F7", fg="#1A202C", bd=1, relief="solid", state="disabled")
        self.txt_decrypted.pack(fill="x", pady=5)

    # --- Các hàm xử lý sự kiện (Event Handlers) ---
    def _on_generate_keys(self):
        """Đọc số p, kiểm tra tính hợp lệ toán học, gọi hàm sinh khóa và hiển thị cặp khóa."""
        try:
            p = int(self.ent_p.get())
            if not ElGamalMath.is_prime(p):
                messagebox.showerror("Lỗi Số Học", "Số hệ thống (p) bạn nhập không phải là số nguyên tố!")
                return
            if p < 256:
                messagebox.showwarning("Cảnh báo",
                                       "Hệ thống khuyến nghị chọn số p > 256 để chứa vừa bảng ký tự Unicode!")
                return

            g = ElGamalMath.find_primitive_root(p)
            x = random.randint(2, p - 2)
            y = ElGamalMath.power(g, x, p)

            # Cập nhật bộ nhớ chương trình
            self.p, self.g, self.x, self.y = p, g, x, y

            # Đẩy dữ liệu hiển thị lên View
            self.lbl_g.config(text=str(g))
            self.lbl_x.config(text=str(x))
            self.lbl_y.config(text=f"Bộ khóa: (p={p}, g={g}, y={y})")
            messagebox.showinfo("Thành công", "Hệ thống đã khởi tạo xong cặp khóa an toàn!")
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Vui lòng nhập định dạng số nguyên hợp lệ!")

    def _on_encrypt(self):
        """Mã hóa văn bản rõ từ giao diện và hiển thị chuỗi cặp số bản mã."""
        if self.p is None:
            messagebox.showerror("Lỗi An Toàn", "Vui lòng khởi tạo cặp khóa hệ thống trước khi mã hóa!")
            return

        plaintext = self.txt_plain.get("1.0", tk.END).strip()
        if not plaintext:
            messagebox.showwarning("Thông báo", "Vui lòng nhập nội dung văn bản rõ cần truyền tải.")
            return

        try:
            self.current_cipher = ElGamalMath.encrypt(plaintext, self.p, self.g, self.y)

            # Cập nhật ô văn bản mã hóa (Mở khóa -> Ghi dữ liệu -> Khóa lại)
            self.txt_cipher.config(state="normal")
            self.txt_cipher.delete("1.0", tk.END)
            cipher_str = " ".join([f"({c1},{c2})" for c1, c2 in self.current_cipher])
            self.txt_cipher.insert("1.0", cipher_str)
            self.txt_cipher.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Lỗi Mã hóa", str(e))

    def _on_decrypt(self):
        """Giải mã mảng bản mã lưu trong bộ nhớ và in kết quả văn bản rõ."""
        if self.p is None or not self.current_cipher:
            messagebox.showerror("Lỗi Dữ Liệu", "Không tìm thấy thông số khóa hoặc gói bản mã phù hợp để giải mã!")
            return

        try:
            decrypted_text = ElGamalMath.decrypt(self.current_cipher, self.p, self.x)

            # Cập nhật ô văn bản giải mã (Mở khóa -> Ghi dữ liệu -> Khóa lại)
            self.txt_decrypted.config(state="normal")
            self.txt_decrypted.delete("1.0", tk.END)
            self.txt_decrypted.insert("1.0", decrypted_text)
            self.txt_decrypted.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Lỗi Giải mã", str(e))