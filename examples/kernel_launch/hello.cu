#include "cuda_runtime.h"
#include <stdio.h>

__global__ void hello() {
    printf("Hello, World!\n");
}


int main() {
    hello<<<1, 1>>>();
    cudaDeviceSynchronize();
    return 0;
}