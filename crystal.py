from snail import *

class Max(Snail):
    def update(self):
        body = block((2, 1))
        tail = block((1, 5))
        head = module((2, 1))
        head = module_set(body, head, 0)
        tail = blocks_move(body, [tail], 3)
        tail.append(body)
        self.blocks = tail
        self.modules = [head]
        print(head)
        print(tail)

model = Max()
model.update()
for node in sorted(model.get_data()[0]):
    print(node)

