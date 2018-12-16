from ecc import *

print()
print("Elliptic Curve Cryptosystem: written by Kyle Linzy")
print("*Note* press ctrl-c to exit the loop and the demo")
print()

numZeros = int(input("enter a number of zeros for the prime number (i.e. 3 => 1000).\nMinimum is 6 \nNumber of Zeros = "))

if numZeros < 6:
    numZeros = 6

low = 1
for i in range(1,numZeros):
    low *=10

high = low*10

p = random_prime(low, high)
k = randint(1,p-1)
public_key = Public_Key.make_public_key(p,k)
print(public_key)
print()
while (True):
    s = input("Enter a message to be encrypted\n")
    print()
    encrypted = encrypt(s,public_key)
    print("Encrypted array of points on the curve:\n", encrypted)
    print()
    print("Decrypted string:\n", decrypt(encrypted, public_key,k))
    print()
