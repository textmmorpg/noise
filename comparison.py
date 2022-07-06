from opensimplex import noise3
import time
startTime = time.time()

size = 100

image = [[[[noise3(i, y, r)] for i in range(size)] for y in range(size)] for r in range(size)]

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
