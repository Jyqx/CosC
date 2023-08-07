from stack import Stack
from queue122 import Queue

s = Stack()
s.push(1)
s.push(2)
s.push(3)
len(s)
s.pop()
s.peek()

d = Queue() # make d an empty Queue
d.enqueue(27)
d.enqueue(9)
d.enqueue(22)
a = d.dequeue()
d.enqueue(26)
b = d.dequeue()
d.enqueue(2)
d.enqueue(12)
c = d.dequeue()

print(a, b, c)