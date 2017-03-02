from page_rank.observer import *
from page_rank.estimator import *

# time measurement
st_time = time.time()

links = collect(main_link, 100)
matrix = np.zeros((len(links), len(links)))
refill(links, matrix)

print("--- %s seconds ---" % (time.time() - st_time))
print()
print(links)
print(matrix)
print()

previous = [1/len(matrix) for i in range(len(matrix))]
estimated = iterate(previous, matrix)

j = 0
pcs = int(input("Decimals: "))
while not np.array_equal(np.round(previous, pcs), np.round(estimated, pcs)):
    previous = estimated[:]
    estimated = iterate(estimated, matrix)
    j += 1

    if j > 1000: break

print("--- iterations: %s ---" % j)
print()

print(np.round(estimated, pcs))
print()

print(estimated.index(max(estimated)), links[estimated.index(max(estimated))])
print(max(estimated))
