from sets import Set
from copy import deepcopy

# s = Set([1, 2, 3])
# print s
# s.add(2)
# print min(list(s))
# print s.remove(min(s))
# print s

# test = [1, 2, 3, 4]
# print "original:", test
# testCpy = list(test)
# print "copy", testCpy
# testCpy.append(5)
# print "original after", test
# print "copy after", testCpy

rotations = [[0, 'l'], [0, 'r'], [1, 'l'], [1, 'r'], [2, 'l'], [2, 'r'], [3, 'l'], [3, 'r']]
rotationsCopy = list(rotations)
rotationsCopy[0] = [0, 'rr']
print rotations
print rotationsCopy
print rotations[0][0]

class test():
    def __init__(self, test):
        self.test = list(test)
        self.test.append([4, 'r'])
        print self.test


rotCollection = [[[0, 'l'], [0, 'r'], [1, 'l'], [1, 'r'], [2, 'l'], [2, 'r'],[3, 'll'], [3, 'r']],
[[0, 'l'], [0, 'r'], [1, 'l'], [1, 'r'], [2, 'l'], [2, 'r'], [3, '2'], [3, 'r']]]
print rotations in rotCollection
