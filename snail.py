from collections import namedtuple
from operator import neg, add, sub, mul
from itertools import cycle, islice
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
    nums = tuple(filter(lambda c: c, pos))
    if len(nums):
        dif = min(nums, key=abs)
        pos = tuple(map(lambda c: c - dif, pos))
        nums = tuple(filter(lambda c: c, pos))
    else:
        return (0, 0)
    if len(nums)  == 2 and reduce(mul, nums) < 0:
        dif = min(pos, key=abs)
        pos = tuple(map(lambda c: c - dif, pos))
        
    ri = max(range(3), key=lambda i: abs(pos[i]))
    r = pos[ri]
    pos = tuple(map(lambda c: c if c else r, pos))
    ai = min(range(3), key=lambda i: abs(pos[i])) 
    ang = ri * 2
    if r < 0:
        ang = ang_rt(ang, 3)
        r = abs(r)
    if ai != (ri + 1) % 3:
        a = r * 6 - abs(pos[ai]) - r * (6 - ang)
    else:
        a = abs(pos[ai]) + r * ang
    return r, a

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
    args = ((arg, arg) if arg is int else arg
            for arg in args)
    blocks = zip(blocks, args)
    return [block_move(base, block, arg[0], arg[1]) 
            for block, arg in blocks]

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

