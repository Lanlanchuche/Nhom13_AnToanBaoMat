
import random
import math


class ElGamalMath:
    """
    Lớp cung cấp các hàm toán học số luận và logic cốt lõi cho hệ mật ElGamal.
    Tất cả các phương thức đều là tĩnh (staticmethod), độc lập hoàn toàn với giao diện.
    """

    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Kiểm tra một số nguyên bất kỳ có phải là số nguyên tố hay không.

        Args:
            n (int): Số nguyên cần kiểm tra.

        Returns:
            bool: True nếu n là số nguyên tố, ngược lại trả về False.
        """
        if n <= 1: return False
        if n == 2: return True
        if n % 2 == 0: return False
        square_root = int(math.sqrt(n))
        for i in range(3, square_root + 1, 2):
            if n % i == 0: return False
        return True

    @staticmethod
    def power(a: int, b: int, n: int) -> int:
        """
        Tính lũy thừa mô-đun nhanh bằng thuật toán bình phương và nhân liên tiếp.
        Tính giá trị của biểu thức: (a^b) mod n.

        Args:
            a (int): Cơ số.
            b (int): Số mũ.
            n (int): Hệ số mô-đun.

        Returns:
            int: Kết quả của phép toán (a^b) mod n.
        """
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
        """
        Tìm ước số chung lớn nhất (ƯCLN) và các hệ số Bézout bằng thuật toán Euclid mở rộng.
        Tìm x, y thỏa mãn phương trình: a*x + b*y = gcd(a, b).

        Args:
            a (int): Số nguyên thứ nhất.
            b (int): Số nguyên thứ hai.

        Returns:
            tuple: Bộ 3 số nguyên (ucln, x, y) trong đó ucln là gdc(a,b), x và y là hệ số Bézout.
        """
        if a == 0:
            return b, 0, 1
        ucln, x1, y1 = ElGamalMath.gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return ucln, x, y

    @staticmethod
    def mod_reverse(a: int, m: int):
        """
        Tính nghịch đảo mô-đun của một số nguyên theo một mô-đun cho trước.
        Tìm x sao cho: (a * x) mod m = 1. (Ký hiệu x = a^-1 mod m).

        Args:
            a (int): Số cần tính nghịch đảo.
            m (int): Hệ số mô-đun.

        Returns:
            int hoặc None: Trả về số nguyên x thuộc khoảng [0, m-1] nếu tồn tại,
                           trả về None nếu gcd(a, m) != 1 (không tồn tại nghịch đảo).
        """
        ucln, x, y = ElGamalMath.gcd(a, m)
        if ucln != 1:
            return None
        else:
            return (x % m + m) % m

    @staticmethod
    def find_primitive_root(p: int):
        """
        Tìm một phần tử nguyên thủy (primitive root/generator) g của số nguyên tố p.
        Phần tử g thỏa mãn bậc lũy thừa nhỏ nhất sinh ra toàn bộ nhóm nhân là p-1.

        Args:
            p (int): Số nguyên tố đầu vào.

        Returns:
            int hoặc None: Số nguyên g đầu tiên tìm được, hoặc None nếu không tìm thấy.
        """
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
        """
        Mã hóa một chuỗi văn bản rõ thành danh sách các cặp số bản mã theo hệ mật ElGamal.
        Mỗi ký tự được chuyển sang mã Unicode nguyên, sau đó chọn số ngẫu nhiên k ngẫu nhiên
        để tính cặp (c1, c2) = (g^k mod p, m * y^k mod p).

        Args:
            plaintext (str): Chuỗi văn bản rõ cần mã hóa.
            p (int): Số nguyên tố lớn (thành phần khóa công khai).
            g (int): Phần tử nguyên thủy (thành phần khóa công khai).
            y (int): Khóa công khai thành phần (y = g^x mod p).

        Raises:
            ValueError: Nếu mã số của ký tự lớn hơn hoặc bằng giá trị của p.

        Returns:
            list: Danh sách các bộ tuple dạng [(c1_1, c2_1), (c1_2, c2_2), ...] đại diện cho bản mã.
        """
        cipher_pairs = []
        for char in plaintext:
            m = ord(char)
            if m >= p:
                raise ValueError(f"Ký tự '{char}' ({m}) >= p ({p}). Hãy chọn số p lớn hơn!")

            while True:
                k = random.randint(2, p - 2)
                if math.gcd(k, p - 1) == 1: break

            c1 = ElGamalMath.power(g, k, p)
            c2 = (m * ElGamalMath.power(y, k, p)) % p
            cipher_pairs.append((c1, c2))
        return cipher_pairs

    @staticmethod
    def decrypt(cipher_pairs: list, p: int, x: int) -> str:
        """
        Giải mã danh sách các cặp số bản mã ElGamal trở lại thành chuỗi văn bản rõ ban đầu.
        Công thức giải mã: m = c2 * (c1^x)^-1 mod p.

        Args:
            cipher_pairs (list): Danh sách các cặp số bản mã [(c1, c2), ...].
            p (int): Số nguyên tố hệ thống.
            x (int): Khóa bí mật của người nhận.

        Raises:
            ValueError: Nếu trong quá trình tính toán không thể tìm thấy nghịch đảo mô-đun.

        Returns:
            str: Chuỗi văn bản rõ đã được khôi phục nguyên vẹn.
        """
        plaintext_chars = []
        for c1, c2 in cipher_pairs:
            c1_x = ElGamalMath.power(c1, x, p)
            c1_x_inv = ElGamalMath.mod_reverse(c1_x, p)
            if c1_x_inv is None:
                raise ValueError("Không tìm thấy nghịch đảo mô-đun.")
            m = (c2 * c1_x_inv) % p
            plaintext_chars.append(chr(m))
        return "".join(plaintext_chars)