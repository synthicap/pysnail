inv = [0, 5, 4, 3, 2, 1]
axi = [3, 4, 5, 0, 1, 2]
ext = [1, 1, 0, 0, 0, 1]

def inv_pos(pos):
    return inv[pos[0]], inv[pos[1]]

def rotate(x, y):
    return (x + y) % 6;

def cur_pos_abs(pos_abs, ang, element, pos):
    pos_abs = pos_abs.copy()
    pos_abs[rotate(ang, pos)] += element.r
    if ext[pos]:
        pos_abs[ang] += element.d
    return pos_abs

class Element:
    def __init__(self, r, d, dub = False, module = {}, elements = {}):
        self.r = r
        self.d = d
        self.dub = dub
        self.modules = modules
        self.elements = elements

    def add_element(self, element, *args):
        args = (arg if arg is tuple else arg, arg for arg in args)
        self.elements.fromkeys(args, element)
        if dub:
            args = map(inv_pos, args)
            self.elements.fromkeys(args, element.inv_copy())

    def add_module(self, module, *args):
        self.modules.fromkeys(args, module)

    def inv_copy(self):
        return Element(self.r, self.d, self.dub, 
                {inv[k], v for k, v in self.modules},
                {inv_pos(k), v.inv_copy() for k, v in self.elements})

    def elements_abs(self, pos_abs, ang):
        return [(cur_pos_abs(pos_abs, ang, self, k[0]), rotate(k[1], ang), v) 
                for k, v in self.elements]

    def modules_abs(self, pos_abs, ang):
        return [(cur_pos_abs(pos_abs, ang, self, k), v) for k, v in self.modules]

    def raw_nodes(self, pos_abs, ang):
        

