from collections import namedtuple
from operator import neg, add, sub
from itertools import cycle, islice
from functools import reduce

ax_inv = (0, 5, 4, 3, 2, 1)
cn_inv = (3, 4, 5, 0, 1, 2)
is_ext = (1, 1, 0, 0, 0, 1)
st_ang = (0, 2, 1, 0, 2, 1)

Block = namedtuple("Block", "dim ang pos")
Module = namedtuple("Module", "name g pulse shift pos")

def block(dim, ang=0):
    return Block(dim, ang, (0, 0, 0))

def module(pulse, name=-1, g=-1):
    return Module(name, g, pulse, None, None)

def ang_rt(ang0, ang):
    return (ang0 + ang) % 6

def pos_rt(pos0, ang):
    pos = islice(cycle(pos0), st_ang[ang], 3)
    if ang % 2:
        pos = map(neg, pos)
    return tuple(pos)
    
def pos_add(pos0, pos):
    return tuple(map(add, pos0, pos))

def pos_cmp(pos):
    pos0 = pos[0::2]
    pos1 = islice(cycle(pos[1::2], 1, 3))
    return map(sub, pos0, pos1)

def pos_part(dim, ang, on_base_pos):
    r, d = dim
    part = [0] * 6

    part[ang] += d * is_ext[on_base_pos]
    part[ang_rt(on_base_pos, ang)] += r 
    return tuple(pos_cmp(part))

def module_set(base, module, on_base_pos, shif=(0, 0)):
    pos_ = pos_add(base.pos,
            pos_part(base.dim, base.ang, on_base_pos))
    return module._replace(pos=pos_)

def block_move(base, block, on_base_pos, on_base_ang):
    ang_ = ang_rt(base.ang, on_base_ang)
    pos_ = [base.pos,
            pos_part(base.dim, base.ang, on_base_pos),
            pos_rt(block.pos, ang_)]
    pos_ = reduce(pos_add, pos_) 
    ang_ = ang_rt(ang_, block.ang)
    return block._replace(ang=ang_, pos=pos_)

def blocks_move(base, blocks, *args):
    args = ((arg, arg) if arg is int else arg \
            for arg in args)
    blocks = zip(blocks, args)
    return [block_move(base, block, arg[0], arg[1]) 
            for block, arg in blocks]

def sgn(x):
    return (x > 0) - (x < 0)

def pos_norm(pos):
    max_i = max(range(3), key=lambda i: abs(pos[i]))
    pos_p = set(range(3))
    pos_p.remove(max_i)
    sgn0 = sgn(max_i)
    sgn1 = sum(map(sgn, pos_p))
    dif = min(pos_p) if sgn0 == sgn1 else max(pos_p) 
    pos_ = map(
            lambda i: pos[i] + dif if i == max_i else pos[i] - dif, 
            range(3))
    pos_ = tuple(pos_)
    r = pos_[max_i]
    a = sum(pos_) + r * (max_i - 1)
    pos_ = r, a
    return pos_

def block_nodes(block):
    r, d = block.dim
    ang = block.ang
    ang_c = ang
    ang_l = ang_rt(ang, 1)
    ang_r = ang_rt(ang, 5)
    pos = block.pos

    nodes = []
    for i in range(1, r + 1):
        for j in range(d + 1 + r * 2 - i): 
            pos_ = [0] * 6
            pos_[ang_c] += j - r
            pos_[ang_l] += i
            nodes.append(pos_add(pos, pos_cmp(pos_)))
    for i in range(r + 1):
        for j in range(d + 1 + r * 2 - i): 
            pos_ = [0] * 6
            pos_[ang_c] += j - r
            pos_[ang_r] += i
            nodes.append(pos_add(pos, pos_cmp(pos_)))
    return map(pos_norm, nodes)

class Snail():
    def get_data(self):
        nodes = set()
        blocks = self.get_blocks()
        for block in blocks:
            nodes |= set(block_nodes(block_nodes))
        nodes = list(nodes)
        modules = self.get_modules()
        indexes = map(
                lambda m: nodes.index(pos_norm(m.pos)), 
                modules)
        modules = list(map(lambda i, m: m.replace(pos=i)), 
                    indexes, modules)
        return nodes, modules

