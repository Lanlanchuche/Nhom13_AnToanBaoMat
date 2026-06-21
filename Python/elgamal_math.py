import random
import math


class ElGamalMath:
    """
    Lớp cung cấp các hàm toán học số luận và logic cốt lõi cho hệ mật ElGamal.
    Tất cả các phương thức đều là tĩnh (staticmethod), độc lập hoàn toàn với giao diện.
    Phiên bản đã được tinh chỉnh hiệu suất (C-optimized) để chạy mượt mà với khóa 256-bit.
    """

    @staticmethod
    def is_prime(n: int) -> bool:
        """Kiểm tra số nguyên tố cho các số nhỏ."""
        if n <= 1: return False
        if n == 2: return True
        if n % 2 == 0: return False
        square_root = int(math.sqrt(n))
        for i in range(3, square_root + 1, 2):
            if n % i == 0: return False
        return True

    @staticmethod
    def is_prime_miller_rabin(n: int, k: int = 5) -> bool:
        """
        Kiểm tra tính nguyên tố cực nhanh cho số nguyên cực lớn (256-bit trở lên)
        bằng thuật toán xác suất Miller-Rabin.
        """
        if n <= 1: return False
        if n in (2, 3): return True
        if n % 2 == 0: return False

        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2

        for _ in range(k):
            a = random.randint(2, n - 2)
            # Dùng hàm pow mặc định của Python được tối ưu bằng C, cực nhanh cho số lớn
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def power(a: int, b: int, n: int) -> int:
        """Tính lũy thừa mô-đun (Sử dụng cho số nhỏ / mục đích học tập)."""
        result = 1
        a = a % n
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % n
            a = (a * a) % n
            b //= 2
        return result

    @staticmethod
    def gcd(a: int, b: int):
        """Tìm ƯCLN và hệ số Bézout bằng thuật toán Euclid mở rộng (Cho số nhỏ)."""
        if a == 0:
            return b, 0, 1
        ucln, x1, y1 = ElGamalMath.gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return ucln, x, y

    @staticmethod
    def mod_reverse(a: int, m: int):
        """Tính nghịch đảo mô-đun cho số nhỏ."""
        ucln, x, y = ElGamalMath.gcd(a, m)
        if ucln != 1:
            return None
        else:
            return (x % m + m) % m

    @staticmethod
    def generate_safe_prime(bits: int = 256) -> tuple:
        """Sinh ngẫu nhiên Số nguyên tố an toàn (Safe Prime) p = 2q + 1."""
        while True:
            q = random.getrandbits(bits - 1)
            q |= (1 << (bits - 2)) | 1  # Đảm bảo bit đầu và bit cuối là 1

            if ElGamalMath.is_prime_miller_rabin(q):
                p = 2 * q + 1
                if ElGamalMath.is_prime_miller_rabin(p):
                    return p, q

    @staticmethod
    def generate_keys(bits: int = 256) -> tuple:
        """
        Sinh cặp khóa (Công khai, Bí mật) cho hệ mật ElGamal với độ dài số nguyên tố lớn.
        """
        # 1. Sinh số nguyên tố p an toàn và số q (p = 2q + 1)
        p, q = ElGamalMath.generate_safe_prime(bits)

        # 2. Tìm phần tử nguyên thủy g
        g = 2
        while True:
            if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
                break
            g += 1

        # 3. Chọn ngẫu nhiên khóa bí mật x thỏa mãn (1 < x < p-1)
        x = random.randint(2, p - 2)

        # 4. Tính thành phần khóa công khai y = g^x mod p
        y = pow(g, x, p)

        public_key = (p, g, y)
        private_key = x

        return public_key, private_key

    @staticmethod
    def find_primitive_root(p: int):
        """Tìm phần tử nguyên thủy (Dùng cho các số nguyên tố nhỏ)."""
        if p == 2: return 1
        phi = p - 1
        prime_factors = []
        n = phi
        if n % 2 == 0:
            prime_factors.append(2)
            while n % 2 == 0: n //= 2
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                prime_factors.append(i)
                while n % i == 0: n //= 2
        if n > 2: prime_factors.append(n)

        for g in range(2, p):
            flag = True
            for factor in prime_factors:
                if ElGamalMath.power(g, phi // factor, p) == 1:
                    flag = False
                    break
            if flag: return g
        return None

    @staticmethod
    def encrypt(plaintext: str, p: int, g: int, y: int) -> list:
        """Mã hóa một chuỗi văn bản rõ thành danh sách các cặp số bản mã."""
        cipher_pairs = []
        for char in plaintext:
            m = ord(char)
            if m >= p:
                raise ValueError(f"Ký tự '{char}' ({m}) >= p ({p}). Hãy chọn số p lớn hơn!")

            while True:
                k = random.randint(2, p - 2)
                if math.gcd(k, p - 1) == 1: break

            # Dùng pow() thay thế tự viết để tăng tốc độ với số lớn
            c1 = pow(g, k, p)
            c2 = (m * pow(y, k, p)) % p
            cipher_pairs.append((c1, c2))
        return cipher_pairs

    @staticmethod
    def decrypt(cipher_pairs: list, p: int, x: int) -> str:
        """Giải mã danh sách các cặp số bản mã trở lại thành chuỗi văn bản rõ."""
        plaintext_chars = []
        for c1, c2 in cipher_pairs:
            c1_x = pow(c1, x, p)

            # Sử dụng pow() tích hợp của Python để tính nghịch đảo mô-đun siêu tốc
            try:
                c1_x_inv = pow(c1_x, -1, p)
            except ValueError:
                raise ValueError("Không tìm thấy nghịch đảo mô-đun.")

            m = (c2 * c1_x_inv) % p
            plaintext_chars.append(chr(m))
        return "".join(plaintext_chars)

    @staticmethod
    def encrypt_bytes(data: bytes, p: int, g: int, y: int) -> list:
        """Mã hóa chuỗi bytes thô từ tệp tin thành bản mã."""
        cipher_pairs = []
        for b in data:
            if b >= p:
                raise ValueError(f"Giá trị byte ({b}) >= p ({p}). Hãy chọn số p lớn hơn 256!")

            while True:
                k = random.randint(2, p - 2)
                if math.gcd(k, p - 1) == 1: break

            c1 = pow(g, k, p)
            c2 = (b * pow(y, k, p)) % p
            cipher_pairs.append((c1, c2))
        return cipher_pairs

    @staticmethod
    def decrypt_bytes(cipher_pairs: list, p: int, x: int) -> bytes:
        """Giải mã bản mã thành chuỗi dữ liệu bytes thô ban đầu để ghi ra file."""
        plaintext_bytes = bytearray()
        for c1, c2 in cipher_pairs:
            c1_x = pow(c1, x, p)

            # Tính nghịch đảo mô-đun cực nhanh và tránh lỗi vượt quá giới hạn đệ quy
            try:
                c1_x_inv = pow(c1_x, -1, p)
            except ValueError:
                raise ValueError("Không tìm thấy nghịch đảo mô-đun khi giải mã byte.")

            b = (c2 * c1_x_inv) % p
            plaintext_bytes.append(b)
        return bytes(plaintext_bytes)