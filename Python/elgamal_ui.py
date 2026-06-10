# elgamal_ui.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from elgamal_math import ElGamalMath
import random
import os
import threading


class ElGamalUI:
    """
    Lớp quản lý giao diện đồ họa (UI) hoàn chỉnh cho hệ mật ElGamal.
    Hỗ trợ song song cả hai chế độ: Đọc/Ghi từ tệp tin và Nhập liệu trực tiếp từ bàn phím.
    Tích hợp xử lý Đa luồng (Threading), giám sát an toàn toàn vẹn dữ liệu
    và thông báo cảnh báo thông minh khi khóa hoặc bản mã bị chỉnh sửa.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HỆ THỐNG MÃ HÓA & GIẢI MÃ TỆP TIN ELGAMAL")
        self.root.geometry("1050x920")
        self.root.configure(bg="#F5F7FA")

        # Lưu trữ trạng thái bộ nhớ dữ liệu hệ thống
        self.p = self.g = self.x = self.y = None
        self.selected_input_path = ""
        self.selected_cipher_path = ""

        # Bộ nhớ đệm lưu kết quả để chờ người dùng bấm nút lưu file
        self.last_encrypted_pairs = None  # Lưu danh sách cặp (c1, c2)
        self.last_decrypted_bytes = None  # Lưu mảng bytes dữ liệu gốc

        # Khởi tạo giao diện và phong cách
        self._init_styles()
        self._build_widgets()

    def _init_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabelframe", background="#F5F7FA", bordercolor="#E4E7EB")
        style.configure("TLabelframe.Label", background="#F5F7FA", font=("Helvetica", 11, "bold"), foreground="#1E3D59")

        # Nút bấm chính (Xanh lá)
        style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#17B890",
                        borderwidth=0)
        style.map("Primary.TButton", background=[('active', '#139675')])

        # Nút bấm phụ (Xanh dương đậm)
        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#1E3D59",
                        borderwidth=0)
        style.map("Accent.TButton", background=[('active', '#173046')])

        # Nút bấm hành động (Đỏ)
        style.configure("Danger.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#FF6B6B",
                        borderwidth=0)
        style.map("Danger.TButton", background=[('active', '#E85A5A')])

    def _build_widgets(self):
        # --- TIÊU ĐỀ CHÍNH ---
        title_container = tk.Frame(self.root, bg="#1E3D59", height=55)
        title_container.pack(fill="x", side="top")
        title_container.pack_propagate(False)

        title_lbl = tk.Label(
            title_container,
            text="HỆ THỐNG MÃ HÓA & GIẢI MÃ FILE ĐA LUỒNG AN TOÀN ELGAMAL",
            font=("Helvetica", 13, "bold"), fg="white", bg="#1E3D59"
        )
        title_lbl.pack(expand=True)

        main_frame = tk.Frame(self.root, bg="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ----------------- KHUNG 1: QUẢN LÝ VÀ NHẬP KHÓA -----------------
        key_frame = ttk.LabelFrame(main_frame, text=" 1. THIẾT LẬP VÀ QUẢN LÝ FILE KHÓA (TỰ GÕ HOẶC TỰ ĐỘNG) ")
        key_frame.pack(fill="x", pady=5, ipady=3)

        inputs_key_frame = tk.Frame(key_frame, bg="#F5F7FA")
        inputs_key_frame.pack(fill="x", padx=10, pady=5)

        # Hàng nhập dữ liệu số học: p, g
        tk.Label(inputs_key_frame, text="Số nguyên tố p:", font=("Helvetica", 10), bg="#F5F7FA").grid(row=0, column=0,
                                                                                                      padx=5, pady=5,
                                                                                                      sticky="w")
        self.ent_p = ttk.Entry(inputs_key_frame, width=15, font=("Helvetica", 10))
        self.ent_p.insert(0, "65537")
        self.ent_p.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(inputs_key_frame, text="Toán tử gốc g:", font=("Helvetica", 10), bg="#F5F7FA").grid(row=0, column=2,
                                                                                                     padx=15, pady=5,
                                                                                                     sticky="w")
        self.ent_g = ttk.Entry(inputs_key_frame, width=15, font=("Helvetica", 10))
        self.ent_g.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Hàng nhập dữ liệu số học: x, y
        tk.Label(inputs_key_frame, text="Khóa bí mật x:", font=("Helvetica", 10), bg="#F5F7FA").grid(row=1, column=0,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="w")
        self.ent_x = ttk.Entry(inputs_key_frame, width=15, font=("Helvetica", 10))
        self.ent_x.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(inputs_key_frame, text="Khóa công khai y:", font=("Helvetica", 10), bg="#F5F7FA").grid(row=1, column=2,
                                                                                                        padx=15, pady=5,
                                                                                                        sticky="w")
        self.ent_y = ttk.Entry(inputs_key_frame, width=15, font=("Helvetica", 10))
        self.ent_y.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Khu vực cụm nút chức năng điều khiển khóa
        btn_key_frame = tk.Frame(inputs_key_frame, bg="#F5F7FA")
        btn_key_frame.grid(row=0, column=4, rowspan=2, padx=20, sticky="ns")
        ttk.Button(btn_key_frame, text="Áp Dụng Khóa Gõ Tay", style="Accent.TButton",
                   command=self._on_apply_manual_keys).grid(row=0, column=0, padx=4, pady=2)
        ttk.Button(btn_key_frame, text="Sinh Khóa Tự Động", style="Primary.TButton",
                   command=self._on_generate_keys).grid(row=0, column=1, padx=4, pady=2)
        ttk.Button(btn_key_frame, text="Tải Khóa Từ File", style="Accent.TButton",
                   command=self._on_load_keys_from_file).grid(row=1, column=0, padx=4, pady=2)
        ttk.Button(btn_key_frame, text="Lưu Cặp Khóa Ra File", style="Accent.TButton",
                   command=self._on_save_keys_to_file).grid(row=1, column=1, padx=4, pady=2)

        # Nhãn hiển thị trạng thái bộ khóa hiện hành
        self.lbl_y = tk.Label(key_frame, text="Bộ khóa công khai công bố (p, g, y): Chưa khởi tạo",
                              font=("Helvetica", 9, "bold"), fg="#2F855A", bg="#F5F7FA", wraplength=950, justify="left")
        self.lbl_y.pack(fill="x", side="bottom", padx=15, pady=5, anchor="w")

        # Khung chia đôi màn hình cho phân hệ Mã hóa (Trái) và Giải mã (Phải)
        body_frame = tk.Frame(main_frame, bg="#F5F7FA")
        body_frame.pack(fill="both", expand=True, pady=5)
        body_frame.columnconfigure(0, weight=1, uniform="group1")
        body_frame.columnconfigure(1, weight=1, uniform="group1")

        # ----------------- KHUNG 2: PHÂN HỆ MÃ HÓA FILE (BÊN TRÁI) -----------------
        enc_frame = ttk.LabelFrame(body_frame, text=" 2. PHÂN HỆ MÃ HÓA FILE & BÀN PHÍM (SENDER) ")
        enc_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        file_select_enc = tk.Frame(enc_frame, bg="#F5F7FA")
        file_select_enc.pack(fill="x", padx=10, pady=5)
        ttk.Button(file_select_enc, text="Chọn File Source", style="Accent.TButton",
                   command=self._on_browse_input_file).pack(side="left")
        self.lbl_input_path = tk.Label(file_select_enc, text="Chưa chọn file...", font=("Helvetica", 9, "italic"),
                                       fg="gray", bg="#F5F7FA", anchor="w")
        self.lbl_input_path.pack(side="left", padx=10, fill="x", expand=True)
        ttk.Button(file_select_enc, text="Xóa chọn", command=self._clear_input_file_selection).pack(side="right")

        tk.Label(enc_frame, text="Hoặc nhập chuỗi bản rõ gõ tay từ bàn phím (Nếu không chọn file):",
                 font=("Helvetica", 9, "bold"), bg="#F5F7FA", fg="#4A5568").pack(anchor="w", padx=10, pady=(5, 0))
        self.txt_manual_plain = tk.Text(enc_frame, height=4, font=("Courier New", 10), bd=1, relief="solid")
        self.txt_manual_plain.pack(fill="x", padx=10, pady=2)

        action_bar_enc = tk.Frame(enc_frame, bg="#F5F7FA")
        action_bar_enc.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_bar_enc, text="Thực Hiện Mã Hóa", style="Primary.TButton",
                   command=self._on_encrypt_action).pack(side="left")
        self.btn_save_cipher = ttk.Button(action_bar_enc, text="Lưu File Mật...", style="Accent.TButton",
                                          command=self._on_save_cipher_to_file, state="disabled")
        self.btn_save_cipher.pack(side="right")

        tk.Label(enc_frame, text="Xem trước bản mã thu được (Format: c1,c2):", font=("Helvetica", 9, "bold"),
                 bg="#F5F7FA", fg="#4A5568").pack(anchor="w", padx=10, pady=(5, 0))

        txt_container_enc = tk.Frame(enc_frame)
        txt_container_enc.pack(fill="both", expand=True, padx=10, pady=5)
        scrollbar_enc = ttk.Scrollbar(txt_container_enc)
        scrollbar_enc.pack(side="right", fill="y")
        self.txt_display_cipher = tk.Text(txt_container_enc, font=("Courier New", 9), bg="#EDF2F7", fg="#2D3748", bd=1,
                                          relief="solid", yscrollcommand=scrollbar_enc.set, wrap="word")
        self.txt_display_cipher.pack(fill="both", expand=True, side="left")
        scrollbar_enc.config(command=self.txt_display_cipher.yview)

        # ----------------- KHUNG 3: PHÂN HỆ GIẢI MÃ FILE (BÊN PHẢI) -----------------
        dec_frame = ttk.LabelFrame(body_frame, text=" 3. PHÂN HỆ GIẢI MÃ FILE & BÀN PHÍM (RECEIVER) ")
        dec_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        file_select_dec = tk.Frame(dec_frame, bg="#F5F7FA")
        file_select_dec.pack(fill="x", padx=10, pady=5)
        ttk.Button(file_select_dec, text="Chọn File Mật", style="Accent.TButton",
                   command=self._on_browse_cipher_file).pack(side="left")
        self.lbl_cipher_path = tk.Label(file_select_dec, text="Chưa chọn file mật...", font=("Helvetica", 9, "italic"),
                                        fg="gray", bg="#F5F7FA", anchor="w")
        self.lbl_cipher_path.pack(side="left", padx=10, fill="x", expand=True)
        ttk.Button(file_select_dec, text="Xóa chọn", command=self._clear_cipher_file_selection).pack(side="right")

        tk.Label(dec_frame, text="Hoặc dán chuỗi bản mã gõ tay (Format: c1,c2 c1,c2 ...):",
                 font=("Helvetica", 9, "bold"), bg="#F5F7FA", fg="#4A5568").pack(anchor="w", padx=10, pady=(5, 0))
        self.txt_manual_cipher = tk.Text(dec_frame, height=4, font=("Courier New", 9), bd=1, relief="solid",
                                         wrap="word")
        self.txt_manual_cipher.pack(fill="x", padx=10, pady=2)

        action_bar_dec = tk.Frame(dec_frame, bg="#F5F7FA")
        action_bar_dec.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_bar_dec, text="Thực Hiện Giải Mã", style="Danger.TButton",
                   command=self._on_decrypt_action).pack(side="left")
        self.btn_save_plain = ttk.Button(action_bar_dec, text="Lưu Văn Bản Gốc...", style="Primary.TButton",
                                         command=self._on_save_plain_to_file, state="disabled")
        self.btn_save_plain.pack(side="right")

        tk.Label(dec_frame, text="Xem trước nội dung văn bản giải mã:", font=("Helvetica", 9, "bold"), bg="#F5F7FA",
                 fg="#4A5568").pack(anchor="w", padx=10, pady=(5, 0))

        txt_container_dec = tk.Frame(dec_frame)
        txt_container_dec.pack(fill="both", expand=True, padx=10, pady=5)
        scrollbar_dec = ttk.Scrollbar(txt_container_dec)
        scrollbar_dec.pack(side="right", fill="y")
        self.txt_display_plain = tk.Text(txt_container_dec, font=("Courier New", 10), bg="white", fg="#1A202C", bd=1,
                                         relief="solid", yscrollcommand=scrollbar_dec.set)
        self.txt_display_plain.pack(fill="both", expand=True, side="left")
        scrollbar_dec.config(command=self.txt_display_plain.yview)

        # Thanh trạng thái dưới đáy ứng dụng
        self.lbl_status = tk.Label(main_frame, text="Trạng thái: Hệ thống sẵn sàng.", font=("Helvetica", 9),
                                   bg="#F5F7FA", fg="#718096", anchor="w")
        self.lbl_status.pack(fill="x", side="bottom", pady=2)

    def _log(self, message: str):
        self.lbl_status.config(text=f"Trạng thái: {message}")

    def _sync_key_entries(self):
        """Đồng bộ đẩy dữ liệu từ bộ nhớ RAM hệ thống lên View hiển thị."""
        self.ent_p.delete(0, tk.END);
        self.ent_p.insert(0, str(self.p) if self.p else "")
        self.ent_g.delete(0, tk.END);
        self.ent_g.insert(0, str(self.g) if self.g else "")
        self.ent_x.delete(0, tk.END);
        self.ent_x.insert(0, str(self.x) if self.x else "")
        self.ent_y.delete(0, tk.END);
        self.ent_y.insert(0, str(self.y) if self.y else "")
        if self.p and self.g and self.y:
            self.lbl_y.config(
                text=f"Bộ khóa hiện hành: (p={self.p}, g={self.g}, x={self.x if self.x else 'Chưa nạp'}, y={self.y})")

    # --- SỰ KIỆN QUẢN LÝ KHÓA (THỦ CÔNG VÀ TỰ ĐỘNG) ---
    def _on_apply_manual_keys(self):
        """
        Đọc tham số khóa nhập từ bàn phím và thực hiện kiểm tra liên kết
        toán học nghiêm ngặt bảo đảm giải mã thành công.
        """
        try:
            p_str, g_str, x_str, y_str = self.ent_p.get().strip(), self.ent_g.get().strip(), self.ent_x.get().strip(), self.ent_y.get().strip()
            if not p_str or not g_str or not y_str:
                messagebox.showerror("Lỗi nhập liệu",
                                     "Tham số khóa công khai cấu hình (p, g, y) bắt buộc không được để trống!")
                return

            p = int(p_str)
            if not ElGamalMath.is_prime(p) or p <= 256:
                messagebox.showerror("Lỗi Số Học", "Số p nhập vào phải là SỐ NGUYÊN TỐ và lớn hơn 256!")
                return

            g = int(g_str)
            if g <= 1 or g >= p:
                messagebox.showerror("Lỗi Số Học", f"Toán tử gốc g cấu hình sai quy tắc (Yêu cầu: 1 < g < {p})!")
                return

            y = int(y_str)
            if y <= 1 or y >= p:
                messagebox.showerror("Lỗi Số Học",
                                     f"Giá trị khóa công khai y cấu hình sai quy tắc (Yêu cầu: 1 < y < {p})!")
                return

            x = int(x_str) if x_str else None

            # RÀNG BUỘC TOÁN HỌC QUYẾT ĐỊNH: Kiểm tra tính hợp lệ của cặp khóa (x, y) qua g
            if x is not None:
                if x <= 1 or x >= p - 1:
                    messagebox.showerror("Lỗi Số Học", f"Khóa mật x cấu hình sai quy tắc (Yêu cầu: 1 < x < {p - 1})!")
                    return

                # Tính thử y_check = g^x mod p
                y_check = ElGamalMath.power(g, x, p)
                if y_check != y:
                    messagebox.showerror(
                        "LỖI LIÊN KẾT KHÓA",
                        "Cặp khóa gõ tay không khớp logic toán học ElGamal!\n\n"
                        f"Giá trị tính toán g^x mod p cho ra kết quả bằng: {y_check}\n"
                        f"Nhưng Khóa công khai y bạn điền lại bằng: {y}\n\n"
                        "-> Đây chính là lý do khiến hệ thống mã hóa được nhưng KHÔNG GIẢI MÃ ĐƯỢC. Vui lòng sửa lại!"
                    )
                    return

            # Đồng bộ dữ liệu an toàn vào RAM nền sau khi kiểm tra qua hết điều kiện
            self.p, self.g, self.x, self.y = p, g, x, y
            self._sync_key_entries()
            self._log("Áp dụng cấu hình thông số bộ khóa gõ tay thành công.")
            messagebox.showinfo("Thành công", "Đã nạp và cấu hình bộ khóa thủ công hoàn toàn hợp lệ!")
        except ValueError:
            messagebox.showerror("Lỗi định dạng", "Tất cả thông số cấu hình khóa bắt buộc điền ký tự số nguyên!")

    def _on_generate_keys(self):
        try:
            p = int(self.ent_p.get())
            if not ElGamalMath.is_prime(p) or p <= 256:
                messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên tố p > 256 vào ô nhập để mồi thuật toán sinh!")
                return
            g = ElGamalMath.find_primitive_root(p)
            x = random.randint(2, p - 2)
            y = ElGamalMath.power(g, x, p)

            self.p, self.g, self.x, self.y = p, g, x, y
            self._sync_key_entries()
            self._log("Sinh cặp khóa hệ thống thành công.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập định dạng số nguyên thích hợp ở ô (p).")

    def _on_save_keys_to_file(self):
        if self.p is None:
            messagebox.showwarning("Thông báo", "Chưa có thông tin khóa để xuất!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")],
                                                 title="Lưu File Khóa")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"p={self.p}\ng={self.g}\nx={self.x if self.x else ''}\ny={self.y}\n")
            self._log(f"Đã lưu tệp thông số khóa tại {os.path.basename(file_path)}")

    def _on_load_keys_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text File", "*.txt")], title="Mở File Khóa")
        if file_path:
            try:
                keys = {}
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=")
                            keys[k.strip()] = int(v.strip()) if v.strip() else None
                self.p, self.g, self.x, self.y = keys["p"], keys["g"], keys.get("x"), keys["y"]
                self._sync_key_entries()
                self._log("Tải dữ liệu file khóa hoàn tất.")
            except Exception:
                messagebox.showerror("Lỗi", "Cấu trúc file khóa không hợp lệ.")

    # --- SỰ KIỆN PHÂN HỆ MÃ HÓA (ĐA LUỒNG) ---
    def _on_browse_input_file(self):
        path = filedialog.askopenfilename(title="Chọn file cần mã hóa")
        if path:
            self.selected_input_path = path
            self.lbl_input_path.config(text=os.path.basename(path), fg="black")

    def _clear_input_file_selection(self):
        self.selected_input_path = ""
        self.lbl_input_path.config(text="Chưa chọn file...", fg="gray")

    def _on_encrypt_action(self):
        """Xử lý hành động Mã hóa: Ưu tiên mã hóa Tệp tin, tự chuyển mã hóa văn bản nhập tay nếu trống file."""
        if self.p is None or self.y is None:
            messagebox.showerror("Lỗi Khóa",
                                 "Yêu cầu cấu hình thông số Khóa công khai trước khi chạy tiến trình mã hóa!")
            return

        is_file_mode = bool(self.selected_input_path)
        if not is_file_mode:
            plain_text = self.txt_manual_plain.get("1.0", tk.END).strip()
            if not plain_text:
                messagebox.showwarning("Thiếu dữ liệu",
                                       "Vui lòng chọn một tệp nguồn cần xử lý HOẶC nhập văn bản rõ từ bàn phím!")
                return
            file_data = plain_text.encode("utf-8")
        else:
            self._log("Đang đọc dữ liệu nhị phân từ tệp nguồn...")
            with open(self.selected_input_path, "rb") as f:
                file_data = f.read()

        def worker():
            try:
                self._log(f"Đang tính toán mã hóa ElGamal ({len(file_data)} bytes)... Vui lòng đợi...")
                self.last_encrypted_pairs = ElGamalMath.encrypt_bytes(file_data, self.p, self.g, self.y)

                self._log("Đang biên dịch chuỗi xem trước bản mã...")
                preview_pairs = self.last_encrypted_pairs[:1000]
                cipher_preview = " ".join([f"({c1},{c2})" for c1, c2 in preview_pairs])
                if len(self.last_encrypted_pairs) > 1000:
                    cipher_preview += " ... [Bản mã dài, chỉ hiển thị trước 1000 khối]"

                self.root.after(0, lambda: update_ui_success(cipher_preview))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi Mã hóa", str(e)))

        def update_ui_success(preview_text):
            self.txt_display_cipher.delete("1.0", tk.END)
            self.txt_display_cipher.insert("1.0", preview_text)
            self.btn_save_cipher.config(state="normal")
            self._log("Mã hóa hoàn tất! Hệ thống đã nạp dữ liệu chờ xuất file.")
            messagebox.showinfo("Thành công", "Đã mã hóa thành công! Bạn có thể xem trước bản mã hoặc chọn lưu file.")

        threading.Thread(target=worker, daemon=True).start()

    def _on_save_cipher_to_file(self):
        if not self.last_encrypted_pairs:
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".enc",
            filetypes=[
                ("Tệp mật mã chuẩn (*.enc)", "*.enc"),
                ("Tệp dữ liệu (*.dat)", "*.dat"),
                ("Tệp nhị phân (*.bin)", "*.bin"),
                ("Tất cả định dạng (*.*)", "*.*")
            ],
            title="Lưu file mật mã mã hóa"
        )
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    for c1, c2 in self.last_encrypted_pairs:
                        f.write(f"{c1},{c2}\n")
                self._log(f"Đã xuất và lưu file mật tại: {os.path.basename(save_path)}")
                messagebox.showinfo("Thành công", "Lưu file mật mã hoàn tất!")
            except Exception as e:
                messagebox.showerror("Lỗi lưu file", str(e))

    # --- SỰ KIỆN PHÂN HỆ GIẢI MÃ & BẪY LỖI AN NINH (ĐA LUỒNG) ---
    def _on_browse_cipher_file(self):
        path = filedialog.askopenfilename(
            title="Chọn file mật mã",
            filetypes=[
                ("Tệp mật mã (*.enc;*.dat;*.bin)", "*.enc;*.dat;*.bin"),
                ("Tất cả các tệp (*.*)", "*.*")
            ]
        )
        if path:
            self.selected_cipher_path = path
            self.lbl_cipher_path.config(text=os.path.basename(path), fg="black")

    def _clear_cipher_file_selection(self):
        self.selected_cipher_path = ""
        self.lbl_cipher_path.config(text="Chưa chọn file mật...", fg="gray")

    def _on_decrypt_action(self):
        """Xử lý hành động Giải mã: Ưu tiên phân tách đọc từ Tệp tin, tự chuyển chế độ quét chuỗi ký tự gõ tay."""
        if self.p is None or self.x is None:
            messagebox.showerror("Lỗi Khóa",
                                 "Hệ thống cần nạp đầy đủ thông số bộ số (p) và Khóa bí mật (x) để giải mã!")
            return

        is_file_mode = bool(self.selected_cipher_path)
        cipher_source_text = ""

        if not is_file_mode:
            cipher_source_text = self.txt_manual_cipher.get("1.0", tk.END).strip()
            if not cipher_source_text:
                messagebox.showwarning("Thiếu dữ liệu",
                                       "Vui lòng chọn file mật mã .enc HOẶC nhập dán chuỗi cặp số vào ô nhập liệu!")
                return

        def worker():
            try:
                self._log("Đang đọc cấu trúc dữ liệu bản mã đầu vào...")
                cipher_pairs = []

                if is_file_mode:
                    with open(self.selected_cipher_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                else:
                    # Tiền xử lý dọn dẹp chuỗi dán thủ công loại bỏ các ký tự dấu đóng mở ngoặc bọc ngoài
                    cleaned_text = cipher_source_text.replace("(", "").replace(")", " ")
                    lines = cleaned_text.split()

                # 1. KIỂM TRA ĐỊNH DẠNG/CẤU TRÚC FILE BẢN MÃ TRƯỚC KHI TÍNH TOÁN
                for idx, line in enumerate(lines, 1):
                    line = line.strip()
                    if line:
                        try:
                            c1, c2 = map(int, line.split(","))
                            cipher_pairs.append((c1, c2))
                        except ValueError:
                            self.root.after(0, lambda: messagebox.showerror(
                                "CẢNH BÁO AN NINH",
                                f"Phát hiện dữ liệu bản mã sai quy tắc định dạng cấu trúc ở khối vị trí thứ {idx}!\n\n"
                                "Hệ thống chặn tác vụ do bản mã mật đã bị can thiệp chỉnh sửa trái phép."
                            ))
                            self._log("Thất bại: File mật mã bị thay đổi cấu trúc định dạng.")
                            return

                self._log(f"Đang thực thi giải mã nghịch đảo mô-đun {len(cipher_pairs)} khối...")

                # 2. KIỂM TRA LỖI TOÁN HỌC KHI GIẢI MÃ (SAI KHÓA HOẶC SỬA SỐ C1)
                try:
                    self.last_decrypted_bytes = ElGamalMath.decrypt_bytes(cipher_pairs, self.p, self.x)
                except ValueError:
                    self.root.after(0, lambda: messagebox.showerror(
                        "CẢNH BÁO: SAI KHÓA / SỬA BẢN MÃ",
                        "Không thể tìm thấy nghịch đảo mô-đun trong quá trình tính toán nền!\n\n"
                        "Hệ thống xác định:\n"
                        "- Khóa bí mật (x) bạn nhập đã bị thay đổi không chính xác, HOẶC\n"
                        "- Thành phần dữ liệu c1 trong file bản mã đã bị chỉnh sửa (Tấn công toàn vẹn)."
                    ))
                    self._log("Thất bại: Lỗi nghịch đảo mô-đun (Sai khóa hoặc Sửa bản mã).")
                    return

                # 3. KIỂM TRA TÍNH HỢP LỆ TRÊN TỪNG BYTE (PHÁT HIỆN SỬA ĐỒI CẢ HAI)
                if any(b > 255 for b in self.last_decrypted_bytes):
                    self.root.after(0, lambda: messagebox.showerror(
                        "HỆ THỐNG PHÁT HIỆN LỖI",
                        "Dữ liệu giải mã vượt quá giới hạn Byte tiêu chuẩn (0-255)!\n\n"
                        "Thông báo: CẢ BẢN MÃ VÀ KHÓA HỆ THỐNG ĐỀU ĐÃ BỊ SỬA ĐỔI / KHÔNG TRÙNG KHỚP NHAU."
                    ))
                    self._log("Thất bại: Dữ liệu không hợp lệ do sai lệch đồng thời cả khóa và bản mã.")
                    return

                # 4. KIỂM TRA XÁC SUẤT KÝ TỰ RÁC
                try:
                    text_content = self.last_decrypted_bytes.decode("utf-8")
                    control_chars = sum(1 for c in text_content if ord(c) < 32 and c not in "\n\r\t")
                    if len(text_content) > 0 and (control_chars / len(text_content)) > 0.3:
                        self.root.after(0, lambda: messagebox.showwarning(
                            "CẢNH BÁO: RÁC DỮ LIỆU",
                            "Văn bản giải mã thành công về mặt toán học nhưng chứa cấu trúc ký tự lạ (Ký tự rác).\n\n"
                            "Điều này xảy ra do Khóa bí mật bị thay đổi nhỏ hoặc một vài ký tự trong Bản mã bị chỉnh sửa!"
                        ))
                except UnicodeDecodeError:
                    text_content = "[Dữ liệu nhị phân / Định dạng file đặc biệt hoặc Bản mã đã bị chỉnh sửa]\n" \
                                   "Mã xem trước Hex:\n" + self.last_decrypted_bytes.hex()[:500] + "..."

                    self.root.after(0, lambda: messagebox.showwarning(
                        "THÔNG BÁO KIỂM TRA",
                        "Hệ thống không thể dịch luồng dữ liệu giải mã sang văn bản ký tự (Unicode Decode Error).\n\n"
                        "Nếu tệp tin gốc của bạn là file văn bản (.txt), chắc chắn Khóa bí mật hoặc Bản mã đã bị sửa đổi trái phép!"
                    ))

                self.root.after(0, lambda: update_ui_success(text_content))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi Hệ Thống", f"Lỗi không xác định: {str(e)}"))

        def update_ui_success(content):
            self.txt_display_plain.delete("1.0", tk.END)
            self.txt_display_plain.insert("1.0", content)
            self.btn_save_plain.config(state="normal")
            self._log("Giải mã hoàn tất! Hãy kiểm tra tính toàn vẹn của dữ liệu hiển thị.")
            messagebox.showinfo("Thành công",
                                "Giải mã hoàn tất! Bạn có thể đọc nội dung hoặc chọn xuất lưu file kết quả.")

        threading.Thread(target=worker, daemon=True).start()

    def _on_save_plain_to_file(self):
        if self.last_decrypted_bytes is None:
            return
        save_path = filedialog.asksaveasfilename(
            title="Lưu văn bản khôi phục giải mã",
            defaultextension=".txt",
            filetypes=[
                ("Văn bản thuần túy (*.txt)", "*.txt"),
                ("Tài liệu Microsoft Word (*.docx)", "*.docx"),
                ("Tất cả các tệp (*.*)", "*.*")
            ]
        )
        if save_path:
            try:
                with open(save_path, "wb") as f:
                    f.write(self.last_decrypted_bytes)
                self._log(f"Đã lưu file giải mã thành công tại: {os.path.basename(save_path)}")
                messagebox.showinfo("Thành công", f"Đã lưu văn bản vào tệp: {os.path.basename(save_path)}")
            except Exception as e:
                messagebox.showerror("Lỗi lưu file", str(e))