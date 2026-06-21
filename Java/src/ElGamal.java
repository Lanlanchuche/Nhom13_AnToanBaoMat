import java.math.BigInteger;
import java.security.SecureRandom;

public class ElGamal {

    private static final SecureRandom RANDOM = new SecureRandom();
    private static final BigInteger TWO = BigInteger.valueOf(2);

    // ĐỘ DÀI KHÓA MẶC ĐỊNH (BIT) — MỨC AN TOÀN HIỆN TẠI
    public static final int KEY_BITS = 512;

    // ĐỘ CHẮC CHẮN KHI KIỂM TRA SỐ NGUYÊN TỐ (MILLER-RABIN)
    // Xác suất sai (nhận nhầm hợp số là số nguyên tố) nhỏ hơn 2^-CERTAINTY
    private static final int CERTAINTY = 80;

    // KIỂM TRA SỐ NGUYÊN TỐ
    public static boolean isPrime(BigInteger n) {
        if (n == null || n.compareTo(TWO) < 0) return false;
        return n.isProbablePrime(CERTAINTY);
    }

    // KIỂM TRA: (p - 1) CÓ CHIA HẾT CHO q HAY KHÔNG
    public static boolean isFactor(BigInteger p, BigInteger q) {
        return p.subtract(BigInteger.ONE).mod(q).signum() == 0;
    }

    // NGUYÊN TỐ CÙNG NHAU
    public static boolean gcdEqualsOne(BigInteger a, BigInteger b) {
        return a.gcd(b).equals(BigInteger.ONE);
    }

    // A^B MOD N
    public static BigInteger modPow(BigInteger a, BigInteger b, BigInteger n) {
        return a.modPow(b, n);
    }

    // NGHỊCH ĐẢO MODULO (TRẢ VỀ -1 NẾU KHÔNG TỒN TẠI)
    public static BigInteger modInverse(BigInteger a, BigInteger n) {
        try {
            return a.modInverse(n);
        } catch (ArithmeticException e) {
            return BigInteger.valueOf(-1);
        }
    }

    /**
     * KIỂM TRA p CÓ PHẢI LÀ "SỐ NGUYÊN TỐ AN TOÀN" HAY KHÔNG, TỨC p = 2q + 1
     * VỚI q CŨNG LÀ SỐ NGUYÊN TỐ.
     *
     * Với số nguyên tố thường (không an toàn), muốn kiểm tra một phần tử có
     * phải là phần tử sinh hay không thì cần phân tích (p-1) ra thừa số
     * nguyên tố — điều này KHÔNG khả thi về mặt tính toán khi p có 256 bit
     * (phân tích số 256-bit có thể mất hàng tỷ năm với máy tính thông thường).
     *
     * Với số nguyên tố an toàn, nhóm Zp* chỉ có đúng 2 nhóm con thực sự
     * (ứng với 2 ước nguyên tố của p-1 là 2 và q), nên việc kiểm tra phần tử
     * sinh chỉ cần 2 phép lũy thừa modulo — vẫn nhanh ngay cả với số 256-bit.
     * Đây là cách tiếp cận chuẩn được dùng trong thực tế (OpenSSL, RFC 3526...).
     */
    public static boolean isSafePrime(BigInteger p) {
        if (!isPrime(p)) return false;
        BigInteger q = p.subtract(BigInteger.ONE).divide(TWO);
        return isPrime(q);
    }

    // KIỂM TRA PHẦN TỬ SINH — CHỈ ÁP DỤNG KHI p LÀ SỐ NGUYÊN TỐ AN TOÀN (p = 2q+1)
    public static boolean isGenerator(BigInteger g, BigInteger p) {
        if (!isSafePrime(p)) return false;
        BigInteger q = p.subtract(BigInteger.ONE).divide(TWO);
        return isGenerator(g, p, q);
    }

    // PHIÊN BẢN NHANH KHI ĐÃ BIẾT SẴN q = (p-1)/2 (TRÁNH KIỂM TRA isSafePrime LẠI NHIỀU LẦN)
    public static boolean isGenerator(BigInteger g, BigInteger p, BigInteger q) {
        if (g.compareTo(TWO) < 0 || g.compareTo(p.subtract(BigInteger.ONE)) >= 0) return false;
        if (g.modPow(TWO, p).equals(BigInteger.ONE)) return false;
        return !g.modPow(q, p).equals(BigInteger.ONE);
    }

    // SINH MỘT SỐ NGUYÊN TỐ AN TOÀN p = 2q + 1 NGẪU NHIÊN, p CÓ ĐỘ DÀI bitLength BIT
    // TRẢ VỀ {p, q}
    public static BigInteger[] generateSafePrime(int bitLength) {
        BigInteger q, p;
        do {
            q = BigInteger.probablePrime(bitLength - 1, RANDOM);
            p = q.shiftLeft(1).add(BigInteger.ONE); // p = 2q + 1
        } while (!p.isProbablePrime(CERTAINTY));
        return new BigInteger[]{p, q};
    }

    // SINH PHẦN TỬ SINH g CỦA Zp* (p LÀ SỐ NGUYÊN TỐ AN TOÀN, q = (p-1)/2)
    public static BigInteger generateGenerator(BigInteger p, BigInteger q) {
        BigInteger g;
        do {
            g = randomBigInteger(TWO, p.subtract(TWO));
        } while (!isGenerator(g, p, q));
        return g;
    }

    // SINH SỐ NGẪU NHIÊN PHÂN BỐ ĐỀU TRONG ĐOẠN [min, max]
    public static BigInteger randomBigInteger(BigInteger min, BigInteger max) {
        BigInteger range = max.subtract(min);
        if (range.signum() < 0) throw new IllegalArgumentException("Khoảng giá trị không hợp lệ");
        int bits = range.bitLength() + 1; // +1 để tránh lệch phân bố do làm tròn
        BigInteger result;
        do {
            result = new BigInteger(bits, RANDOM);
        } while (result.compareTo(range) > 0);
        return min.add(result);
    }

    // SINH SỐ NGẪU NHIÊN k THỎA 1 < k < p-1 VÀ gcd(k, p-1) = 1 (DÙNG ĐỂ MÃ HÓA)
    public static BigInteger generateK(BigInteger p) {
        BigInteger pMinus1 = p.subtract(BigInteger.ONE);
        BigInteger k;
        do {
            k = randomBigInteger(TWO, pMinus1.subtract(BigInteger.ONE));
        } while (!gcdEqualsOne(k, pMinus1));
        return k;
    }

    // SINH KHÓA — MẶC ĐỊNH 512-BIT (p LÀ SỐ NGUYÊN TỐ AN TOÀN)
    // TRẢ VỀ {p, g, x, y}
    public static BigInteger[] generateKey() {
        return generateKey(KEY_BITS);
    }

    public static BigInteger[] generateKey(int bitLength) {
        BigInteger[] safe = generateSafePrime(bitLength);
        BigInteger p = safe[0], q = safe[1];

        BigInteger g = generateGenerator(p, q);
        BigInteger x = randomBigInteger(TWO, p.subtract(TWO));
        BigInteger y = g.modPow(x, p);

        return new BigInteger[]{p, g, x, y};
    }

    // MÃ HÓA 1 KÝ TỰ / KHỐI: m PHẢI THỎA 0 <= m < p
public static BigInteger[] encryptChar(BigInteger m, BigInteger p, BigInteger g, BigInteger y, BigInteger k) {
    // kiểm tra dữ liệu đầu vào
    if (m == null || p == null || g == null || y == null || k == null) {
        throw new IllegalArgumentException("Tham số mã hóa không được để trống.");
    }

    if (m.compareTo(BigInteger.ZERO) < 0 || m.compareTo(p) >= 0) {
        throw new IllegalArgumentException("Bản rõ m phải thỏa 0 <= m < p.");
    }

    BigInteger pMinus1 = p.subtract(BigInteger.ONE);
    if (k.compareTo(BigInteger.ONE) <= 0 || k.compareTo(pMinus1) >= 0) {
        throw new IllegalArgumentException("k phải thỏa 1 < k < p-1.");
    }

    if (!gcdEqualsOne(k, pMinus1)) {
        throw new IllegalArgumentException("k phải nguyên tố cùng nhau với p-1.");
    }

    // ElGamal:
    // c1 = g^k mod p
    // c2 = m * y^k mod p
    BigInteger c1 = g.modPow(k, p);
    BigInteger c2 = m.multiply(y.modPow(k, p)).mod(p);

    return new BigInteger[]{c1, c2};
}

// GIẢI MÃ 1 KÝ TỰ / KHỐI
public static BigInteger decryptChar(BigInteger c1, BigInteger c2, BigInteger p, BigInteger x) {
    // kiểm tra dữ liệu đầu vào
    if (c1 == null || c2 == null || p == null || x == null) {
        throw new IllegalArgumentException("Tham số giải mã không được để trống.");
    }

    if (c1.compareTo(BigInteger.ZERO) < 0 || c1.compareTo(p) >= 0) {
        throw new IllegalArgumentException("c1 không hợp lệ.");
    }

    if (c2.compareTo(BigInteger.ZERO) < 0 || c2.compareTo(p) >= 0) {
        throw new IllegalArgumentException("c2 không hợp lệ.");
    }

    // s = c1^x mod p
    BigInteger s = c1.modPow(x, p);

    // sInv = s^(-1) mod p
    BigInteger sInv = modInverse(s, p);
    if (sInv.equals(BigInteger.valueOf(-1))) {
        throw new ArithmeticException("Không tìm được nghịch đảo modulo.");
    }

    // m = c2 * sInv mod p
    return c2.multiply(sInv).mod(p);
}
}
//END.