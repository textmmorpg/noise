from opensimplex import noise3
import time
import pickle
startTime = time.time()

size = 100

data1 = [[[noise3(i, y, r) for i in range(size)] for y in range(size)] for r in range(size)]
data2 = [[[noise3(i, y, r) for i in range(size)] for y in range(size)] for r in range(size)]
data3 = [[[noise3(i, y, r) for i in range(size)] for y in range(size)] for r in range(size)]

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


with open('simplex1.pickle', 'wb') as handle:
    pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('simplex2.pickle', 'wb') as handle:
    pickle.dump(data2, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('simplex3.pickle', 'wb') as handle:
    pickle.dump(data3, handle, protocol=pickle.HIGHEST_PROTOCOL)
