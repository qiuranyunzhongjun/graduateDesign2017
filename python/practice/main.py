from numpy import *

a1 = array([[1,2,3,4],[5,6,7,8]])
a2 = array((1,2,3,4))
a3 = vstack((a2,a2))
a4 = a1 + a3

print('ok')