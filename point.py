class Point(object):
    x = 0
    y = 0
    z = 0
    p = 0

    def __init__(self,x,y,z, p):
        self.x = x
        self.y = y
        self.z = z
        self.p = p

    def __repr__(self):
        s = ""
        x_string = str(self.x)
        y_string = str(self.y)
        z_string = str(self.z)
        l = []
        l.append("(")
        l.append(x_string)
        l.append(", ")
        l.append(y_string)
        l.append(", ")
        l.append(z_string)
        l.append(")")
        return "".join(l)

    def __eq__(self,other):
        return self.__dict__ == other.__dict__

    def make_point(x,y,z,p):
        point = Point(x,y,z,p)
        return point

    def negate(self):
        self.y = (-1*self.y) % self.p
        return self
