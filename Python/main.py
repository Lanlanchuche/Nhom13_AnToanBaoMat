import tkinter as tk
from tkinter import messagebox, ttk
import random
import math


def is_prime(n:int):
    '''
     Đây là hàm kiểm tra số nguyên tố
        para: n (số cần kiểm tra)
        return: bool (True: n là số nguyên tố, False: n không là số nguyên tố)
    '''
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    square_root = int(math.sqrt(n))
    for i in range(3, square_root + 1, 2):
        if n % i == 0:
            return False
    return True

def power(a, b, n):
    '''
    Đây là hàm tính a^b mod n
    para:
            a: cơ số
            b: số mũ
            n: hệ số module
    return: kết quả a^b mod n
    '''
    result = 1
    a = a % n
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % n
        a = (a * a) % n
        b //= 2
    return result

def gcd(a, b):
    '''
    Đây là hàm tính ước chung lớn nhất gcd của 2 số a và b
    para:
        a
        b
    return: tuple 3 bộ số ucln, x, y
    '''
    if a == 0:
        return b, 0, 1
    ucln, x1, y1 = gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return ucln, x, y
def mod_reverse(a, m):
    '''
    Đây là hàm tính nghich đảo module của a theo m
    '''

if __name__ == '__main__':
    print('Hello world')

