import numpy as np
from timeit import default_timer as timer
from numba import vectorize
import sys
import gc


@vectorize(["float32(float32, float32)"], target='cpu')
def VectorAdd_CPU(a, b):
	return a + b


@vectorize(["float32(float32, float32)"], target='cuda')
def VectorAdd_CUDA(a, b):
	return a + b


@vectorize(["float32(float32, float32)"], target='parallel')
def VectorAdd_Parallel(a, b):
	return a + b


def main():
	N = 1000
	step = 100

	count = 3
	while count > 0:
		gc.collect()
		A = np.ones(N, dtype=np.float32)
		B = np.ones(N, dtype=np.float32)

		start = timer()
		VectorAdd_CPU(A, B)
		cpu_cost = timer() - start

		start = timer()
		VectorAdd_Parallel(A, B)
		para_cost = timer() - start

		start = timer()
		VectorAdd_CUDA(A, B)
		cuda_cost = timer() - start

		print(N, "cpu:", cpu_cost, "para:", para_cost, "cuda", cuda_cost)
		N *= step
		count -= 1


if __name__ == '__main__':
	main()