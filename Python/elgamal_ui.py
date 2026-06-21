import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from elgamal_math import ElGamalMath
import random
import os
import re
import threading


class ElGamalUI:
    """
    Lớp quản lý giao diện đồ họa (UI) hoàn chỉnh cho hệ mật ElGamal.
    Sử dụng cấu trúc Tab (Notebook) chia rõ 3 phân hệ: Quản lý Khóa, Mã hóa, Giải mã.
    Hỗ trợ luồng khóa chia sẻ toàn cục: nạp khóa từ bất kỳ tab nào cũng tự động đồng bộ.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HỆ THỐNG MÃ HÓA & GIẢI MÃ TỆP TIN ELGAMAL")
        self.root.geometry("1100x850")
        self.root.configure(bg="#F5F7FA")

        # Lưu trữ trạng thái bộ nhớ dữ liệu hệ thống
        self.p = self.g = self.x = self.y = None
        self.selected_input_path = ""
        self.selected_cipher_path = ""

        # Bộ nhớ đệm lưu kết quả để chờ người dùng bấm nút lưu file
        self.last_encrypted_pairs = None
        self.last_decrypted_bytes = None

        self._init_styles()
        self._build_widgets()

    def _init_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabelframe", background="#F5F7FA", bordercolor="#E4E7EB")
        style.configure("TLabelframe.Label", background="#F5F7FA", font=("Helvetica", 11, "bold"), foreground="#1E3D59")

        # Buttons
        style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#17B890",
                        borderwidth=0)
        style.map("Primary.TButton", background=[('active', '#139675')])

        style.configure("Accent.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#1E3D59",
                        borderwidth=0)
        style.map("Accent.TButton", background=[('active', '#173046')])

        style.configure("Danger.TButton", font=("Helvetica", 10, "bold"), foreground="white", background="#FF6B6B",
                        borderwidth=0)
        style.map("Danger.TButton", background=[('active', '#E85A5A')])

        # Tabs
        style.configure("TNotebook", background="#F5F7FA", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"), padding=[15, 5], background="#E4E7EB",
                        foreground="#1E3D59")
        style.map("TNotebook.Tab", background=[("selected", "#1E3D59")], foreground=[("selected", "white")])

    def _build_widgets(self):
        title_container = tk.Frame(self.root, bg="#1E3D59", height=55)
        title_container.pack(fill="x", side="top")
        title_container.pack_propagate(False)

        tk.Label(
            title_container, text="HỆ THỐNG MÃ HÓA & GIẢI MÃ FILE ĐA LUỒNG AN TOÀN ELGAMAL",
            font=("Helvetica", 14, "bold"), fg="white", bg="#1E3D59"
        ).pack(expand=True)

        main_frame = tk.Frame(self.root, bg="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Cấu trúc Tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)

        tab_keys = tk.Frame(self.notebook, bg="#F5F7FA")
        tab_enc = tk.Frame(self.notebook, bg="#F5F7FA")
        tab_dec = tk.Frame(self.notebook, bg="#F5F7FA")

        self.notebook.add(tab_keys, text="🔑 1. QUẢN LÝ KHÓA")
        self.notebook.add(tab_enc, text="🔒 2. PHÂN HỆ MÃ HÓA")
        self.notebook.add(tab_dec, text="🔓 3. PHÂN HỆ GIẢI MÃ")

        self._build_key_tab(tab_keys)
        self._build_enc_tab(tab_enc)
        self._build_dec_tab(tab_dec)

        # Thanh trạng thái
        self.lbl_status = tk.Label(self.root, text="Trạng thái: Hệ thống sẵn sàng.", font=("Helvetica", 10),
                                   bg="#E2E8F0", fg="#4A5568", anchor="w", padx=20, pady=5)
        self.lbl_status.pack(fill="x", side="bottom")

    # ================== THIẾT KẾ TAB 1: QUẢN LÝ KHÓA ==================
    def _build_key_tab(self, parent):
        key_frame = ttk.LabelFrame(parent, text=" THIẾT LẬP VÀ QUẢN LÝ BỘ KHÓA (TỰ GÕ HOẶC TỰ ĐỘNG) ")
        key_frame.pack(fill="both", expand=True, padx=20, pady=20)

        inputs_key_frame = tk.Frame(key_frame, bg="#F5F7FA")
        inputs_key_frame.pack(pady=30)

        # Nhập p, g
        tk.Label(inputs_key_frame, text="Số nguyên tố p:", font=("Helvetica", 11), bg="#F5F7FA").grid(row=0, column=0,
                                                                                                      padx=10, pady=15,
                                                                                                      sticky="w")
        self.ent_p = ttk.Entry(inputs_key_frame, width=35, font=("Helvetica", 11))
        self.ent_p.insert(0, "65537")
        self.ent_p.grid(row=0, column=1, padx=10, pady=15, sticky="w")

        tk.Label(inputs_key_frame, text="Toán tử gốc g:", font=("Helvetica", 11), bg="#F5F7FA").grid(row=0, column=2,
                                                                                                     padx=20, pady=15,
                                                                                                     sticky="w")
        self.ent_g = ttk.Entry(inputs_key_frame, width=35, font=("Helvetica", 11))
        self.ent_g.grid(row=0, column=3, padx=10, pady=15, sticky="w")

        # Nhập x, y
        tk.Label(inputs_key_frame, text="Khóa bí mật x:", font=("Helvetica", 11), bg="#F5F7FA").grid(row=1, column=0,
                                                                                                     padx=10, pady=15,
                                                                                                     sticky="w")
        self.ent_x = ttk.Entry(inputs_key_frame, width=35, font=("Helvetica", 11))
        self.ent_x.grid(row=1, column=1, padx=10, pady=15, sticky="w")

        tk.Label(inputs_key_frame, text="Khóa công khai y:", font=("Helvetica", 11), bg="#F5F7FA").grid(row=1, column=2,
                                                                                                        padx=20,
                                                                                                        pady=15,
                                                                                                        sticky="w")
        self.ent_y = ttk.Entry(inputs_key_frame, width=35, font=("Helvetica", 11))
        self.ent_y.grid(row=1, column=3, padx=10, pady=15, sticky="w")

        btn_key_frame = tk.Frame(key_frame, bg="#F5F7FA")
        btn_key_frame.pack(pady=20)
        ttk.Button(btn_key_frame, text="Áp Dụng Khóa Gõ Tay", style="Accent.TButton",
                   command=self._on_apply_manual_keys).pack(side="left", padx=10, ipady=3)
        ttk.Button(btn_key_frame, text="Sinh Khóa Tự Động (Ngẫu Nhiên)", style="Primary.TButton",
                   command=self._on_generate_keys).pack(side="left", padx=10, ipady=3)
        ttk.Button(btn_key_frame, text="Tải Khóa Từ File", style="Accent.TButton",
                   command=self._on_load_keys_from_file).pack(side="left", padx=10, ipady=3)
        ttk.Button(btn_key_frame, text="Lưu Cặp Khóa Ra File", style="Accent.TButton",
                   command=self._on_save_keys_to_file).pack(side="left", padx=10, ipady=3)

    # ================== THIẾT KẾ TAB 2: MÃ HÓA ==================
    def _build_enc_tab(self, parent):
        # Trạng thái khóa nội bộ của Tab Mã hóa
        key_status_frame = tk.Frame(parent, bg="#E2E8F0")
        key_status_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.lbl_enc_key_status = tk.Label(key_status_frame,
                                           text="Khóa công khai chưa được nạp. Vui lòng sinh khóa ở Tab 1 hoặc tải file.",
                                           font=("Helvetica", 10, "bold"), fg="#C53030", bg="#E2E8F0")
        self.lbl_enc_key_status.pack(side="left", padx=10, pady=8)
        ttk.Button(key_status_frame, text="Tải File Khóa", command=self._on_load_keys_from_file).pack(side="right",
                                                                                                      padx=10, pady=5)

        # Khu vực nhập liệu
        input_frame = ttk.LabelFrame(parent, text=" 1. NGUỒN VĂN BẢN (GÕ TAY HOẶC TẢI FILE) ")
        input_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        tools_input = tk.Frame(input_frame, bg="#F5F7FA")
        tools_input.pack(fill="x", padx=10, pady=5)
        ttk.Button(tools_input, text="📁 Chọn File Text/Nhị Phân...", style="Accent.TButton",
                   command=self._on_browse_input_file).pack(side="left", padx=(0, 5))
        self.lbl_input_path = tk.Label(tools_input, text="Chưa chọn file...", font=("Helvetica", 9, "italic"),
                                       fg="gray", bg="#F5F7FA")
        self.lbl_input_path.pack(side="left", padx=5)

        ttk.Button(tools_input, text="Xóa File Chọn", command=self._clear_input_file_selection).pack(side="right")
        ttk.Button(tools_input, text="💾 Lưu Chữ Đang Gõ Ra File", command=self._on_save_manual_plain_to_file).pack(
            side="right", padx=5)

        scroll_in = ttk.Scrollbar(input_frame)
        scroll_in.pack(side="right", fill="y")
        self.txt_manual_plain = tk.Text(input_frame, font=("Courier New", 11), bd=1, relief="solid",
                                        yscrollcommand=scroll_in.set, height=12)
        self.txt_manual_plain.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scroll_in.config(command=self.txt_manual_plain.yview)

        action_bar = tk.Frame(parent, bg="#F5F7FA")
        action_bar.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_bar, text="⬇️ THỰC HIỆN MÃ HÓA ELGAMAL ⬇️", style="Primary.TButton",
                   command=self._on_encrypt_action).pack(fill="x", ipady=5)

        # Khu vực xuất liệu
        output_frame = ttk.LabelFrame(parent, text=" 2. BẢN MÃ THU ĐƯỢC (CIPHERTEXT) ")
        output_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        tools_output = tk.Frame(output_frame, bg="#F5F7FA")
        tools_output.pack(fill="x", padx=10, pady=5)
        self.btn_save_cipher = ttk.Button(tools_output, text="💾 Xuất Bản Mã Ra File (.enc)...", style="Accent.TButton",
                                          command=self._on_save_cipher_to_file, state="disabled")
        self.btn_save_cipher.pack(side="left")

        scroll_out = ttk.Scrollbar(output_frame)
        scroll_out.pack(side="right", fill="y")
        self.txt_display_cipher = tk.Text(output_frame, font=("Courier New", 10), bg="#EDF2F7", fg="#2D3748", bd=1,
                                          relief="solid", yscrollcommand=scroll_out.set, wrap="word", height=12)
        self.txt_display_cipher.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scroll_out.config(command=self.txt_display_cipher.yview)

    # ================== THIẾT KẾ TAB 3: GIẢI MÃ ==================
    def _build_dec_tab(self, parent):
        # Trạng thái khóa nội bộ của Tab Giải mã
        key_status_frame = tk.Frame(parent, bg="#E2E8F0")
        key_status_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.lbl_dec_key_status = tk.Label(key_status_frame,
                                           text="Khóa bí mật chưa được nạp. Vui lòng sinh khóa ở Tab 1 hoặc tải file.",
                                           font=("Helvetica", 10, "bold"), fg="#C53030", bg="#E2E8F0")
        self.lbl_dec_key_status.pack(side="left", padx=10, pady=8)
        ttk.Button(key_status_frame, text="Tải File Khóa", command=self._on_load_keys_from_file).pack(side="right",
                                                                                                      padx=10, pady=5)

        input_frame = ttk.LabelFrame(parent, text=" 1. DÁN CHUỖI MẬT HOẶC TẢI FILE BẢN MÃ (.enc) ")
        input_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        tools_input = tk.Frame(input_frame, bg="#F5F7FA")
        tools_input.pack(fill="x", padx=10, pady=5)
        ttk.Button(tools_input, text="📁 Chọn File Mật (.enc)...", style="Accent.TButton",
                   command=self._on_browse_cipher_file).pack(side="left", padx=(0, 5))
        self.lbl_cipher_path = tk.Label(tools_input, text="Chưa chọn file...", font=("Helvetica", 9, "italic"),
                                        fg="gray", bg="#F5F7FA")
        self.lbl_cipher_path.pack(side="left", padx=5)

        ttk.Button(tools_input, text="Xóa Trắng / Bỏ File", command=self._clear_cipher_file_selection).pack(
            side="right")

        scroll_in = ttk.Scrollbar(input_frame)
        scroll_in.pack(side="right", fill="y")
        self.txt_manual_cipher = tk.Text(input_frame, font=("Courier New", 10), bd=1, relief="solid",
                                         yscrollcommand=scroll_in.set, wrap="word", height=12)
        self.txt_manual_cipher.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scroll_in.config(command=self.txt_manual_cipher.yview)

        action_bar = tk.Frame(parent, bg="#F5F7FA")
        action_bar.pack(fill="x", padx=10, pady=5)
        ttk.Button(action_bar, text="⬇️ THỰC HIỆN GIẢI MÃ ELGAMAL ⬇️", style="Danger.TButton",
                   command=self._on_decrypt_action).pack(fill="x", ipady=5)

        output_frame = ttk.LabelFrame(parent, text=" 2. VĂN BẢN GỐC ĐƯỢC KHÔI PHỤC (PLAINTEXT) ")
        output_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        tools_output = tk.Frame(output_frame, bg="#F5F7FA")
        tools_output.pack(fill="x", padx=10, pady=5)
        self.btn_save_plain = ttk.Button(tools_output, text="💾 Xuất Văn Bản Gốc Ra File...", style="Primary.TButton",
                                         command=self._on_save_plain_to_file, state="disabled")
        self.btn_save_plain.pack(side="left")

        scroll_out = ttk.Scrollbar(output_frame)
        scroll_out.pack(side="right", fill="y")
        self.txt_display_plain = tk.Text(output_frame, font=("Courier New", 11), bg="white", fg="#1A202C", bd=1,
                                         relief="solid", yscrollcommand=scroll_out.set, height=12)
        self.txt_display_plain.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        scroll_out.config(command=self.txt_display_plain.yview)

    # ================== HÀM TIỆN ÍCH VÀ QUẢN LÝ KHÓA ==================
    def _log(self, message: str):
        self.lbl_status.config(text=f"Trạng thái: {message}")

    def _sync_key_entries(self):
        """Đồng bộ dữ liệu RAM lên UI của cả 3 Tab."""
        self.ent_p.delete(0, tk.END);
        self.ent_p.insert(0, str(self.p) if self.p else "")
        self.ent_g.delete(0, tk.END);
        self.ent_g.insert(0, str(self.g) if self.g else "")
        self.ent_x.delete(0, tk.END);
        self.ent_x.insert(0, str(self.x) if self.x else "")
        self.ent_y.delete(0, tk.END);
        self.ent_y.insert(0, str(self.y) if self.y else "")

        if self.p and self.y:
            self.lbl_enc_key_status.config(
                text=f"Khóa công khai đang dùng: p={self.p[:10] if isinstance(self.p, str) else str(self.p)[:10]}..., y={str(self.y)[:10]}...",
                fg="#2F855A")
        else:
            self.lbl_enc_key_status.config(text="Chưa nạp khóa mã hóa (p, y)!", fg="#C53030")

        if self.p and self.x:
            self.lbl_dec_key_status.config(
                text=f"Khóa bí mật đang dùng: p={str(self.p)[:10]}..., x={str(self.x)[:10]}...", fg="#2F855A")
        else:
            self.lbl_dec_key_status.config(text="Chưa nạp khóa giải mã (p, x)!", fg="#C53030")

    def _read_keys_from_ui(self) -> bool:
        def parse(entry):
            s = entry.get().strip()
            return int(s) if s else None

        try:
            self.p = parse(self.ent_p)
            self.g = parse(self.ent_g)
            self.x = parse(self.ent_x)
            self.y = parse(self.ent_y)
            self._sync_key_entries()
            return True
        except ValueError:
            messagebox.showerror("Lỗi", "Khóa phải là số nguyên!")
            return False

    def _on_apply_manual_keys(self):
        if self._read_keys_from_ui():
            if self.p and self.g and self.x and self.y:
                if ElGamalMath.power(self.g, self.x, self.p) != self.y:
                    messagebox.showerror("Lỗi", "Khoá đã bị chỉnh sửa!")
                    return
            messagebox.showinfo("Thành công", "Đã nạp bộ khóa thành công cho toàn hệ thống!")
            self._log("Áp dụng khóa gõ tay thành công.")

    def _on_generate_keys(self):
        try:
            self._log("Đang dò tìm bộ khóa nguyên tố lớn an toàn... Vui lòng đợi...")
            self.root.update()

            public_key, private_key = ElGamalMath.generate_keys(bits=256)
            self.p, self.g, self.y = public_key
            self.x = private_key

            self._sync_key_entries()
            self._log("Sinh khóa an toàn thành công.")
            messagebox.showinfo("Thành công", "Đã sinh bộ khóa mật mã an toàn! Có thể chuyển sang Tab Mã hóa ngay.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def _on_save_keys_to_file(self):
        if not self.p: return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"p={self.p}\ng={self.g}\nx={self.x if self.x else ''}\ny={self.y}\n")
            self._log("Đã lưu thông số khóa.")

    def _on_load_keys_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text File", "*.txt")])
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

                if self.x and self.g and self.y and ElGamalMath.power(self.g, self.x, self.p) != self.y:
                    messagebox.showwarning("Cảnh báo", "Khoá đã bị chỉnh sửa!")
                else:
                    messagebox.showinfo("Thành công", "Tải bộ khóa từ file hoàn tất!")
                self._log("Tải dữ liệu file khóa hoàn tất.")
            except Exception:
                messagebox.showerror("Lỗi", "Cấu trúc file khóa không hợp lệ.")

    # ================== LOGIC PHÂN HỆ MÃ HÓA ==================
    def _on_save_manual_plain_to_file(self):
        content = self.txt_manual_plain.get("1.0", tk.END).rstrip("\n")
        if not content.strip() or content.startswith("[File nhị phân"):
            messagebox.showwarning("Thiếu dữ liệu", "Không có nội dung văn bản hợp lệ để lưu!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self._log("Đã lưu nội dung gõ tay thành file.")

    def _on_browse_input_file(self):
        path = filedialog.askopenfilename(title="Chọn file cần mã hóa")
        if path:
            self.selected_input_path = path
            self.lbl_input_path.config(text=os.path.basename(path), fg="black")
            self._preview_file_content(path, self.txt_manual_plain)

    def _clear_input_file_selection(self):
        self.selected_input_path = ""
        self.lbl_input_path.config(text="Chưa chọn file...", fg="gray")
        self.txt_manual_plain.config(state="normal")
        self.txt_manual_plain.delete("1.0", tk.END)

    def _preview_file_content(self, path: str, widget: tk.Text, max_bytes: int = 4000):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        try:
            size = os.path.getsize(path)
            with open(path, "rb") as f:
                raw = f.read(max_bytes)
            try:
                text = raw.decode("utf-8")
                preview = text + (
                    f"\n\n... [Chỉ xem trước {max_bytes} byte / tổng {size} byte]" if size > max_bytes else "")
            except UnicodeDecodeError:
                preview = f"[File nhị phân không hiển thị chữ]\nKích thước: {size} byte\nHex: {raw[:16].hex(' ')}"
            widget.insert("1.0", preview)
        except Exception as e:
            widget.insert("1.0", f"[Lỗi: {e}]")
        finally:
            widget.config(state="disabled")

    def _on_encrypt_action(self):
        self._read_keys_from_ui()
        if not self.p or not self.y:
            messagebox.showerror("Lỗi Khóa", "Yêu cầu có Khóa công khai (p, y) trước khi mã hóa!")
            self.notebook.select(0)
            return

        is_file = bool(self.selected_input_path)
        if not is_file:
            plain_text = self.txt_manual_plain.get("1.0", tk.END).strip()
            if not plain_text:
                messagebox.showwarning("Trống", "Vui lòng nhập chữ hoặc chọn file!")
                return
            file_data = plain_text.encode("utf-8")
        else:
            self._log("Đang đọc file nhị phân...")
            with open(self.selected_input_path, "rb") as f:
                file_data = f.read()

        def worker():
            try:
                self._log("Đang tính toán mã hóa...")
                self.last_encrypted_pairs = ElGamalMath.encrypt_bytes(file_data, self.p, self.g, self.y)

                preview = "\n".join([f"[Khối {i}]  C1 = {c1}   |   C2 = {c2}" for i, (c1, c2) in
                                     enumerate(self.last_encrypted_pairs[:500], 1)])
                if len(self.last_encrypted_pairs) > 500:
                    preview += f"\n\n... [Hiển thị 500/{len(self.last_encrypted_pairs)} khối]"

                self.root.after(0, lambda: update_ui(preview))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", str(e)))

        def update_ui(text):
            self.txt_display_cipher.delete("1.0", tk.END)
            self.txt_display_cipher.insert("1.0", text)
            self.btn_save_cipher.config(state="normal")
            self._log("Mã hóa hoàn tất.")

        threading.Thread(target=worker, daemon=True).start()

    def _parse_labeled_cipher_text(self, text: str):
        pattern = re.compile(r"C1\s*=\s*(-?\d+).*?C2\s*=\s*(-?\d+)")
        return [(int(c1), int(c2)) for c1, c2 in pattern.findall(text)]

    def _on_save_cipher_to_file(self):
        if not self.last_encrypted_pairs: return
        pairs_to_save = self.last_encrypted_pairs
        path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Cipher", "*.enc"), ("All", "*.*")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                for c1, c2 in pairs_to_save:
                    f.write(f"{c1},{c2}\n")
            self._log("Đã lưu file mật mã.")

    # ================== LOGIC PHÂN HỆ GIẢI MÃ ==================
    def _on_browse_cipher_file(self):
        path = filedialog.askopenfilename(title="Chọn file mật")
        if path:
            self.selected_cipher_path = path
            self.lbl_cipher_path.config(text=os.path.basename(path), fg="black")
            self._preview_cipher_file(path)

    def _clear_cipher_file_selection(self):
        self.selected_cipher_path = ""
        self.lbl_cipher_path.config(text="Chưa chọn file...", fg="gray")
        self.txt_manual_cipher.config(state="normal")
        self.txt_manual_cipher.delete("1.0", tk.END)

    def _preview_cipher_file(self, path: str, max_lines: int = 50):
        self.txt_manual_cipher.config(state="normal")
        self.txt_manual_cipher.delete("1.0", tk.END)
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            preview = "\n".join(
                [f"[Khối {i}]  C1 = {l.split(',')[0]}   |   C2 = {l.split(',')[1]}" if ',' in l else f"Lỗi: {l}" for
                 i, l in enumerate(lines[:max_lines], 1)])
            if len(lines) > max_lines: preview += f"\n\n... [Xem trước {max_lines}/{len(lines)} khối]"
            self.txt_manual_cipher.insert("1.0", preview)
        except Exception as e:
            self.txt_manual_cipher.insert("1.0", f"[Lỗi đọc file: {e}]")
        finally:
            self.txt_manual_cipher.config(state="disabled")

    def _parse_cipher_text_robust(self, raw_text: str):
        labeled = self._parse_labeled_cipher_text(raw_text)
        if labeled: return labeled, None
        tokens = [t for t in raw_text.replace("(", "").replace(")", " ").split() if t.strip()]
        pairs = []
        for idx, token in enumerate(tokens, 1):
            try:
                c1, c2 = map(int, token.split(","))
                pairs.append((c1, c2))
            except ValueError:
                return pairs, idx
        return pairs, None

    def _on_decrypt_action(self):
        self._read_keys_from_ui()
        if not self.p or not self.x:
            messagebox.showerror("Lỗi Khóa", "Yêu cầu có Khóa bí mật (x, p) để giải mã!")
            self.notebook.select(0)
            return

        is_file = bool(self.selected_cipher_path)
        if not is_file:
            text = self.txt_manual_cipher.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Trống", "Vui lòng dán bản mã hoặc chọn file .enc!")
                return
            raw_text = text
        else:
            with open(self.selected_cipher_path, "r", encoding="utf-8") as f:
                raw_text = f.read()

        def worker():
            try:
                is_cipher_modified = False
                is_key_modified = False

                # 1. Kiểm tra định dạng bản mã
                pairs, err = self._parse_cipher_text_robust(raw_text)
                if err is not None or not pairs:
                    is_cipher_modified = True

                # 2. Kiểm tra tính hợp lệ của khóa
                if self.g and self.y and ElGamalMath.power(self.g, self.x, self.p) != self.y:
                    is_key_modified = True

                # 3. Thử giải mã nếu khóa đúng và cấu trúc bản mã đúng để check sâu bên trong
                if not is_cipher_modified and not is_key_modified:
                    try:
                        self.last_decrypted_bytes = ElGamalMath.decrypt_bytes(pairs, self.p, self.x)
                        if any(b > 255 for b in self.last_decrypted_bytes):
                            is_cipher_modified = True
                    except ValueError:
                        is_cipher_modified = True

                # 4. Hiển thị thông báo cực kỳ đơn giản theo yêu cầu
                if is_key_modified and is_cipher_modified:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Cả bản mã và khoá đã bị chỉnh sửa!"))
                    return
                elif is_key_modified:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Khoá đã bị chỉnh sửa!"))
                    return
                elif is_cipher_modified:
                    self.root.after(0, lambda: messagebox.showerror("Lỗi", "Bản mã đã bị sửa!"))
                    return

                # Nếu tất cả hợp lệ, tiến hành xuất kết quả
                try:
                    content = self.last_decrypted_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    content = f"[File Nhị phân]\nHex: {self.last_decrypted_bytes.hex()[:500]}..."

                self.root.after(0, lambda: update_ui(content))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", str(e)))

        def update_ui(text):
            self.txt_display_plain.delete("1.0", tk.END)
            self.txt_display_plain.insert("1.0", text)
            self.btn_save_plain.config(state="normal")
            self._log("Giải mã thành công.")

        threading.Thread(target=worker, daemon=True).start()

    def _on_save_plain_to_file(self):
        if not self.last_decrypted_bytes: return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All", "*.*")])
        if path:
            with open(path, "wb") as f:
                f.write(self.last_decrypted_bytes)
            self._log("Lưu văn bản khôi phục thành công.")