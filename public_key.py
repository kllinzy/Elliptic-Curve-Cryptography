from curve import *
from point import *

class Public_Key(object):
    curve = None
    p = 0
    P = None
    Q = None

    def __init__(self, p, k):
        self.p = p
        self.curve = Curve.make_curve(self.p)
        self.P = self.curve.random_point()
        self.Q = self.curve.multiply(k,self.P)

    def __repr__(self):
        v = []
        v.append(str(self.curve))
        v.append(str(self.P))
        v.append(str(self.Q))
        return "".join(v)

    def make_public_key(p,k):
        public_key = Public_Key(p,k)
        return public_key
