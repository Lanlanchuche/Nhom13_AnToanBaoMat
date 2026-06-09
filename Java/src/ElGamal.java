import java.util.Random;

public class ElGamal {

    // KIỂM TRA SỐ NGUYÊN TỐ
    public static boolean isPrime(int n) {

        if (n < 2) return false;

        if (n == 2 || n == 3)
            return true;

        if (n % 2 == 0 || n % 3 == 0)
            return false;

        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0)
                return false;
        }

        return true;
    }

    // KIỂM TRA ƯỚC
    public static boolean isFactor(int p, int q) {
        return ((p - 1) % q == 0);
    }

    // NGUYÊN TỐ CÙNG NHAU
    public static boolean gcdEqualsOne(int a, int b) {

        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }

        return a == 1;
    }

    // A^B MOD N
    public static long modPow(long a, long b, long n) {

        long result = 1;
        a %= n;

        while (b > 0) {

            if ((b & 1) == 1)
                result = (result * a) % n;

            a = (a * a) % n;

            b >>= 1;
        }

        return result;
    }

    // NGHỊCH ĐẢO MODULO
    public static long modInverse(long a, long n) {

        long t = 0;
        long newT = 1;

        long r = n;
        long newR = a;

        while (newR != 0) {

            long q = r / newR;

            long temp = t;
            t = newT;
            newT = temp - q * newT;

            temp = r;
            r = newR;
            newR = temp - q * newR;
        }

        if (r > 1)
            return -1;

        if (t < 0)
            t += n;

        return t;
    }

    // KIỂM TRA PHẦN TỬ SINH
    public static boolean isGenerator(int g, int p) {

        int phi = p - 1;
        int temp = phi;

        for (int q = 2; q * q <= temp; q++) {
            if (isFactor(p, q)) {
                if (modPow(g, phi / q, p) == 1) {
                    return false;
                }
                while (temp % q == 0) {
                    temp /= q;
                }
            }
        }

        if (temp > 1 && isFactor(p, temp)) {
            if (modPow(g, phi / temp, p) == 1) {
                return false;
            }
        }

        return true;
    }

    // SINH KHÓA 32-BIT TỐI ĐA
    public static int[] generateKey() {
        Random rd = new Random();

        int p;
        do {
            p = rd.nextInt(Integer.MAX_VALUE - 1000000) + 1000000;
            if (p % 2 == 0) p++; // Đảm bảo là số lẻ
        } while (!isPrime(p));

        // Tìm phần tử sinh g
        int g = 2;
        while (g < p && !isGenerator(g, p)) {
            g++;
            if (g > 1000) break; // Giới hạn tìm kiếm
        }

        // Nếu không tìm thấy trong 1000 số đầu, tìm ngẫu nhiên
        if (!isGenerator(g, p)) {
            do {
                g = rd.nextInt(p - 2) + 2;
            } while (!isGenerator(g, p));
        }

        int x = rd.nextInt(p - 3) + 2;
        int y = (int) modPow(g, x, p);

        return new int[]{p, g, x, y};
    }

    // MÃ HÓA 1 KÝ TỰ
    public static int[] encryptChar(int m, int p, int g, int y, int k) {

        int c1 = (int) modPow(g, k, p);

        int c2 =
                (int) ((m * modPow(y, k, p)) % p);

        return new int[]{c1, c2};
    }

    // GIẢI MÃ 1 KÝ TỰ
    public static int decryptChar(int c1, int c2, int p, int x) {

        long K = modPow(c1, x, p);

        long Kinv = modInverse(K, p);

        return (int) ((c2 * Kinv) % p);
    }
}