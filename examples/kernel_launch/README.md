# Kernel Launch Interception

This example shows how to use our template to intercept the kernel launch API of CUDA.

## Build

Prerequisites:
- CUDA
- g++


```bash
make
```

It will generate the following files:

- `libcuda_intercept.so`: the intercept library
- `hello`: the test program
- `libcuda.so` and `libcuda.so.1`: the soft links to the intercept library


## How to program?

There are only **two steps** to intercept a CUDA driver API. You can use `diff intercept.cpp ../template/intercept.cpp` to see the difference.

### Define your own function

You need to define your own function that has the same signature as the original function.

```c++
// MODIFICATION 1: define your own function
CUresult myLaunchKernel(CUfunction f, unsigned int gridDimX, unsigned int gridDimY, unsigned int gridDimZ, unsigned int blockDimX, unsigned int blockDimY, unsigned int blockDimZ, unsigned int sharedMemBytes, CUstream hStream, void **kernelParams, void **extra) {
    // Your code here
    XINFO("Launch kernel: %p, grid (%u, %u, %u), block (%u, %u, %u), sharedMemBytes %u, stream %p", f, gridDimX, gridDimY, gridDimZ, blockDimX, blockDimY, blockDimZ, sharedMemBytes, hStream);
    // call the original function
    return Driver::LaunchKernel(f, gridDimX, gridDimY, gridDimZ, blockDimX, blockDimY, blockDimZ, sharedMemBytes, hStream, kernelParams, extra);
}
```

### Redirect the original function to your own function

You need to redirect the original function to your own function. You can just replace the `Driver::LaunchKernel` with your own function name (e.g., `myLaunchKernel`).

```c++
// MODIFICATION 2: redirect cuLaunchKernel to myLaunchKernel
// DEFINE_EXPORT_C_REDIRECT_CALL(Driver::LaunchKernel, CUresult, cuLaunchKernel, CUfunction, f, unsigned int, gridDimX, unsigned int, gridDimY, unsigned int, gridDimZ, unsigned int, blockDimX, unsigned int, blockDimY, unsigned int, blockDimZ, unsigned int, sharedMemBytes, CUstream, hStream, void **, kernelParams, void **, extra);
DEFINE_EXPORT_C_REDIRECT_CALL(myLaunchKernel, CUresult, cuLaunchKernel, CUfunction, f, unsigned int, gridDimX, unsigned int, gridDimY, unsigned int, gridDimZ, unsigned int, blockDimX, unsigned int, blockDimY, unsigned int, blockDimZ, unsigned int, sharedMemBytes, CUstream, hStream, void **, kernelParams, void **, extra);
```

## How to run?

There are **two ways** to use the interceptor.

The first way to achieve API interception is to use the `LD_PRELOAD` environment variable to load the intercept library.

```bash
> LD_PRELOAD=./libcuda_intercept.so ./hello
[INFO @ T167088 @ 08:29:32.559952] Launch kernel: 0x6265f733aef0, grid (1, 1, 1), block (1, 1, 1), sharedMemBytes 0, stream (nil)
Hello, World!
```


The second way to achieve API interception is to use the `LD_LIBRARY_PATH` environment variable to load the intercept library before the original library.

This requires our intercept library to have the same name as the original library (i.e., `libcuda.so`), and the intercept library should be in the `LD_LIBRARY_PATH` path (before the original library).

```bash
> LD_LIBRARY_PATH=./ ./hello
[INFO @ T167372 @ 08:30:01.063661] Launch kernel: 0x5b4f5cd364d0, grid (1, 1, 1), block (1, 1, 1), sharedMemBytes 0, stream (nil)
Hello, World!
```









