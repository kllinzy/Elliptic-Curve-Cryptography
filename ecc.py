from curve import *
from random import *
import math
import sys
from point import Point
from public_key import Public_Key

def ECencode(s,curve):
    a = curve.a
    b = curve.b
    p = curve.p
    s = str(s)
    x0 = 0
    for i in range(0,len(s)):
        x0 = x0+ord(s[i])*256**i
    for i in range(1000):
        x = 1000*x0 + i % p
        t = x^3+a*x+b % p
        res = prime_mod_sqrt(t,p)
        if(len(res) != 0):
            return Point.make_point(x,res[0],1,p)

def encode_string(s,curve,length):
    arr = []
    l = list(chunkstring(s,length))
    for i in range(0,len(l)):
        arr.append(ECencode(l[i],curve))
    return arr

def encrypt_long(arr,key):
    curve = key.curve
    p = curve.p
    P = key.P
    Q = key.Q
    l = randint(1,p-1)
    res = [curve.multiply(l,P)]
    lQ = curve.multiply(l,Q)
    for i in range(0,len(arr)):
        res.append(curve.add_points(lQ,arr[i]))
    return res

def decrypt_long(arr,key,k):
    res = []
    curve = key.curve
    neg_kC1 = curve.multiply(k,arr[0]).negate()
    for i in range(1,len(arr)):
        ans = curve.add_points(arr[i],neg_kC1)
        res.append(ans)
    return res

def decode_string(arr):
    v = []
    for i in range(0,len(arr)):
        v.append(ECdecode(arr[i]))
    return ''.join(v)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def ECdecode(P):
    n = (P.x-P.x%1000)//1000
    v = []
    while n != 0:
        v.append(chr(n % 256))
        n //= 256
    return ''.join(v)

def encrypt(s, key):
    curve = key.curve
    p = curve.p
    return encrypt_long(encode_string(s,curve,int(math.log(p/1000-1,256))),key)

def decrypt(arr,key,k):
    return decode_string(decrypt_long(arr,key,k))

def miller_rabin(n,k):
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    if n == 3:
        return True

    r, s = 0, n - 1
    while(s >> 1 == 0 ):
        r += 1
        s = s>>1
    for _ in range(0,k):
        a = randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(0,r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def random_prime(low,high):
    result = 0
    while(True):
        result = randint(low,high)
        if(miller_rabin(result, 45)):
            break
    return result

#print()
#print("Elliptic Curve Cryptosystem: written by Kyle Linzy")
#print("*Note* press ctrl-c to exit the loop and the demo")
#print()
#low = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
#high = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000-1

#p = random_prime(low, high)
#k = randint(1,p-1)
#public_key = Public_Key.make_public_key(p,k)
#print(public_key)
#print()
#while (True):
#    s = input("Enter a message to be encrypted\n")
#    print()
#    encrypted = encrypt(s,public_key)
#    print("Encrypted array of points on the curve:\n", encrypted)
#    print()
#    print("Decrypted string:\n", decrypt(encrypted, public_key,k))
#    print()
