inv = {0:0, 1:5, 2:4, 3:3, 4:2, 5:1}

ext = [1, 1, 0, 0, 0, 1]

def inv_pos(pos):
    return inv[pos[0]], inv[pos[1]]

def track_to_crystal(track0, vec, crystal, pos_):
    pos = (vec + pos_[0]) % 6
    track = track0 + [(pos, crystal.r)]
    if ext[pos]:
        track.append((vec1, crystal.d))
    return track, (vec + pos_[1]) % 6

def track_to_module(track0, vec, crystal, pos):
    pos = (vec + pos) % 6
    track = track0 + [(pos, crystal.r)]
    if ext[pos]:
        track.append((vec1, crystal.d))
    return track

class Crystal:
    def __init__(self, r, d, dub):
        self.r = r
        self.d = d
        self.dub = dub
        self.modules = {}
        self.crystals = {}

    def add_crystal(self, crystal, *args):
        args = (arg if arg is tuple else arg, arg for arg in args)
        self.crystals.fromkeys(args, crystal)
        if dub:
            args = map(inv_pos, args)
            self.crystals.fromkeys(args, crystal.inv_copy())

    def add_module(self, module, *args):
        self.modules.fromkeys(args, module)

    def inv_copy(self):
        cp = Crystal(self.r, self.d, self.dub)
        cp.modules = {inv[k], v for k, v in self.modules}
        cp.crystals = {inv_pos(k), v.inv_copy() for k, v in self.crystals}
        return cp

    def crystalis_abs(self, track0, vec):
        return [track_to_crystal(track0, vec, self, k) + tuple(v) for k, v in self.crystals]

    def modules_abs(self, track0, vec):
        return [track_to_module(track0, vec, self, k) + tuple(v) for k, v in self.crystals]

