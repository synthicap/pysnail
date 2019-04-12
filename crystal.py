from snail import *
from engine import add_snail, simulation_run
import sys

class Max(Snail):
    def update(self):
        body = block((2, 1))
        horn = block((1, 0))
        tail = block((1, 2))
        head = module((2, 1))
        head = module_set(body, head, 0)
        tail = blocks_move(body, [tail], 3)
        tail.append(body)
        tail.extend(blocks_move(body, [horn], 1))
        tail.extend(blocks_move(body, [horn], 5))
        self.blocks = tail
        self.modules = [head]

model = Max()
model.update()
for node in sorted(model.get_data()[0]):
    print(node)

add_snail(model)
simulation_run(sys.argv)

