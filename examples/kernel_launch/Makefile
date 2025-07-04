CC = g++

all: libcuda.so libcuda.so.1 libcuda_intercept.so hello

libcuda.so: libcuda_intercept.so
	ln -s libcuda_intercept.so libcuda.so

libcuda.so.1: libcuda_intercept.so
	ln -s libcuda_intercept.so libcuda.so.1

libcuda_intercept.so: intercept.cpp cuda.h driver.h
	${CC} -shared -fPIC intercept.cpp -o libcuda_intercept.so -I../../include -I. --std=c++17 -DRELEASE_MODE

hello: hello.cu
	nvcc -o hello hello.cu

clean:
	rm -f libcuda.so libcuda.so.1 libcuda_intercept.so hello
