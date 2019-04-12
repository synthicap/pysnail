from collections import namedtuple
from operator import neg, add, sub, mul
from itertools import cycle, islice, chain
from functools import reduce

ax_inv = (0, 5, 4, 3, 2, 1)
cn_inv = (3, 4, 5, 0, 1, 2)
is_ext = (1, 1, 0, 0, 0, 1)

Block = namedtuple("Block", "dim ang pos")
Module = namedtuple("Module", "name g pulse shift pos")

def block(dim, ang=0):
    return Block(dim, ang, (0, 0, 0))

def module(pulse, name=-1, g=-1):
    return Module(name, g, pulse, None, None)

def ang_rt(ang, ang_):
    return (ang + ang_) % 6

def pos_rt(pos, ang_):
    pos = islice(cycle(pos), ang_ % 3, ang_ % 3 + 3)
    if ang_ % 2:
        pos = map(neg, pos)
    return tuple(pos)
    
def pos_add(pos, pos_):
    return tuple(map(add, pos, pos_))

def pos_cmp(pos):
    pos0 = pos[0::2]
    pos1 = islice(cycle(pos), 3, 9, 2)
    return tuple(map(sub, pos0, pos1))

def pos_part(dim, ang, on_base_pos):
    r, d = dim
    part = [0] * 6

    part[ang] += d * is_ext[on_base_pos]
    part[ang_rt(on_base_pos, ang)] += r 
    return tuple(pos_cmp(part))

def pos_norm(pos):
    ps = tuple(filter(lambda i: pos[i] > 0, range(3)))
    ns = tuple(filter(lambda i: pos[i] < 0, range(3)))
    if len(ps) + len(ns) == 0:
        return (0, 0)
    if len(ps) * len(ns) == 2:
        dif = max(
            map(lambda i: pos[i], max(ps, ns, key=len)), 
            key=abs)
    elif len(ps) + len(ns) + min(len(ps), len(ns)) == 3:
        dif = min(
            map(lambda i: pos[i], chain(ps, ns)), 
            key=abs)
    else:
        dif = 0

    pos = tuple(map(lambda c: c - dif, pos))
    ri = max(range(3), key=lambda i: abs(pos[i]))
    r = pos[ri]
    pos = tuple(map(lambda i: 0 if i == ri else pos[i], 
                range(3)))
    ai = max(range(3), key=lambda i: abs(pos[i]))
    a = pos[ai]

    ang_r = ri * 2
    if r < 0:
        ang_r = ang_rt(ang_r, 3)
    ang_a = ai * 2
    if a < 0:
        ang_a = ang_rt(ang_a, 3)
    r = abs(r)
    a = abs(a)

    if ang_a == ang_rt(ang_r, 2): 
        a += r * ang_r
    else:
        a = r * ang_r - a
    a %= r * 6
    return (r, a)

def module_set(base, module, on_base_pos, shift_=(0, 0)):
    pos_ = pos_add(base.pos,
            pos_part(base.dim, base.ang, on_base_pos))
    return module._replace(pos=pos_, shift=shift_)

def block_move(base, block, on_base_pos, on_base_ang):
    ang_ = ang_rt(base.ang, on_base_ang)
    pos_ = [base.pos,
            pos_part(base.dim, base.ang, on_base_pos),
            pos_rt(block.pos, ang_)]
    pos_ = reduce(pos_add, pos_) 
    ang_ = ang_rt(ang_, block.ang)
    return block._replace(ang=ang_, pos=pos_)

def blocks_move(base, blocks, on_base_pos, on_base_ang=None):
    if on_base_ang is None:
        on_base_ang = on_base_pos
    blocks = map(
            lambda b: (b, on_base_pos, on_base_ang), 
            blocks) 
    return [block_move(base, block, ob_pos, ob_ang) 
            for block, ob_pos, ob_ang in blocks]

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
        blocks = self.blocks
        for block in blocks:
            nodes |= set(block_nodes(block))
        nodes = list(nodes)
        modules = self.modules
        indexes = map(
                lambda m: nodes.index(pos_norm(m.pos)), 
                modules)
        modules = list(map(lambda i, m: m._replace(pos=i),
                    indexes, modules))
        return nodes, modules

