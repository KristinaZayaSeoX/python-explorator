import time
import random
LIST = ['1',222,True,False]
def call():
 for x in LIST:
     yield x
r = call()
print(next(r))
for i in call():
    print(i)
    time.sleep(1)




