from random import *
from point import Point
class Curve(object):
    a = 0
    b = 0
    p = 0
    def __init__(self, p):
        self.p = p
        self.a = randint(1,p-1)
        self.b = randint(1,p-1)
    def __repr__(self):
        a_string = str(self.a)
        b_string = str(self.b)
        p_string = str(self.p)
        l = []
        l.append("E(F(")
        l.append(p_string)
        l.append(")): y^2 = x^3 + ")
        l.append(a_string)
        l.append("*x + ")
        l.append(b_string)
        return "".join(l)

    def discriminant(self):
        return -16*(pow(self.a,3,self.p)*27+pow(self.b,2,self.p)*4) % self.p

    def make_curve(p):
        curve = Curve(p)
        if(curve.discriminant() != 0):
            return curve
        else:
            return Curve.make_curve(p)

    def random_point(self):
        x = 0
        while True:
            x = randint(1, self.p-1)
            y_squared = (pow(x,3,self.p)+self.a*x+self.b)%self.p
            arr = prime_mod_sqrt(y_squared,self.p)
            if(len(arr) == 0):
                continue
            else:
                y = arr[0]
                return Point.make_point(x,y,1, self.p)

    def add_points(self,P1, P2):
        O = Point.make_point(0,1,0,self.p)
        slope = 0
        if(P1 == O):
            return P2
        elif(P2 == O):
            return P1
        elif((P1.x == P2.x) & (P1.y == (-1*P2.y) % self.p)):
            return O
        elif(P1 == P2):
            top = (3*P1.x*P1.x+self.a) % self.p
            bottom = (2*P1.y % self.p)
            slope = (top*xgcd(self.p,bottom) % self.p)
        else:
            slope = ((P2.y-P1.y) % self.p)*xgcd(self.p, (P2.x-P1.x)%self.p) % self.p
        x3 = (slope*slope-P1.x-P2.x) % self.p
        return Point.make_point(x3,(slope*(P1.x-x3)-P1.y) % self.p,1,self.p)

    def multiply(self, k, P):
        s = bin(k)
        l = list(s)
        soln = Point.make_point(0,1,0,self.p)
        temp = P
        length = len(s)
        for i in range(1,length-2):
            if(l[length-i] == '1'):
                soln = Curve.add_points(self,soln,temp)
            temp = Curve.add_points(self,temp,temp)
        return soln

def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  y0

def prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation
        x^2 = a mod p
    and return list of x solution
    http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """
    a %= p

    # Simple case
    if a == 0:
        return [0]
    if p == 2:
        return [a]

    # Check solution existence on odd prime
    if legendre_symbol(a, p) != 1:
        return []

    # Simple case
    if p % 4 == 3:
        x = pow(a, ((p + 1)//4)>>1, p)
        return [x, p-x]

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Search for a solution
    x = pow(a, (q + 1)>>1, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in range(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return [x, p-x]

def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org/wiki/Legendre_symbol
    """
    ls = pow(a, (p - 1)>>1, p)
    if ls == p - 1:
        return -1
    return ls
