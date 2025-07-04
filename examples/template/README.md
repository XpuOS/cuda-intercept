# Template Generator

This example shows how to use our script to generate a interception template for the CUDA driver library.

## Prerequisites

- CUDA driver library (`libcuda.so`)
- CUDA header file (`cuda.h`)
- Python 3.8+
- libclang (install using `pip install libclang`)

## Step 1: Generate the intercept template

```bash
export GEN_SCRIPT_DIR=../../scripts # path to the gen.py script
export CUDA_HEADER_DIR=/usr/local/cuda/include # path to the CUDA header file
export CUDA_LIB_PATH=/usr/lib/x86_64-linux-gnu/libcuda.so # path to the CUDA library
export GCC_HEADER_PATH=/usr/lib/gcc/x86_64-linux-gnu/11/include # path to the GCC header file

python3 ${GEN_SCRIPT_DIR}/gen.py -s ${CUDA_HEADER_DIR}/cuda.h --platform cuda --lib ${CUDA_LIB_PATH} --prefix cu -I ${GCC_HEADER_PATH}
```

For convenience, we'd better copy the CUDA header file to the current directory.
```bash
cp ${CUDA_HEADER_DIR}/cuda.h .
```

## Step 2: Generate cuGetProcAddress related code

```bash
python3 ${GEN_SCRIPT_DIR}/cuda_func_map.py -f ${CUDA_HEADER_DIR}/cudaTypedefs.h -I ${GCC_HEADER_PATH} -I ${CUDA_HEADER_DIR} >> intercept.cpp
```

TODO: automatically generate cuGetProcAddress related code (replace the existing code in intercept.cpp)


