#!/usr/bin/env python3
"""
This script processes the cuGetProcAddress related code.

It simply:
1. declare  GetProcAddress_v2(const char *symbol, void **pfn, int cudaVersion, cuuint64_t flags, CUdriverProcAddressQueryResult *symbolStatus);
2. replace the original cuGetProcAddress_v2 in to the new function.
3. implement the new function.
"""

import argparse


def process_proc_addr(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # find the line of the original cuGetProcAddress_v2
    found = False
    for i, line in enumerate(lines):
        if "DEFINE_EXPORT_C_REDIRECT_CALL(Driver::GetProcAddress_v2, CUresult, cuGetProcAddress_v2, const char *, symbol, void **, pfn, int, cudaVersion, cuuint64_t, flags, CUdriverProcAddressQueryResult *, symbolStatus);" in line:
            print("found the redirection of cuGetProcAddress_v2, replace it with the new function.")
            template = """
EXPORT_C_FUNC CUresult GetProcAddress_v2(const char *symbol, void **pfn, int cudaVersion, cuuint64_t flags, CUdriverProcAddressQueryResult *symbolStatus);
DEFINE_EXPORT_C_REDIRECT_CALL(GetProcAddress_v2, CUresult, cuGetProcAddress_v2, const char *, symbol, void **, pfn, int, cudaVersion, cuuint64_t, flags, CUdriverProcAddressQueryResult *, symbolStatus);
"""
            lines[i] = template
            found = True
            break
    
    if not found:
        print("Error: cuGetProcAddress_v2 not found in the file.")
        raise Exception("cuGetProcAddress_v2 not found in the file.")

    # append the new function implementation at the end of the file
    template = """
static inline void GetInterceptAddr(const char *symbol, void **pfn, int cuda_version)
{
    auto name_it = intercept_funcs.find(symbol);
    if (name_it == intercept_funcs.end()) return;
    for (auto version_it = name_it->second.rbegin(); version_it != name_it->second.rend(); ++version_it) {
        if (cuda_version >= version_it->first) {
            XDEBG("override func addr: symbol: %s, old: %p, new: %p", symbol, *pfn, version_it->second);
            *pfn = version_it->second;
            return;
        }
    }
}

EXPORT_C_FUNC CUresult GetProcAddress_v2(const char *symbol, void **pfn, int cudaVersion, cuuint64_t flags, CUdriverProcAddressQueryResult *symbolStatus)
{
    XDEBG("GetProcAddress_v2(symbol: %s, cudaVersion: %d, flag: 0x%lx)", symbol, cudaVersion, flags);
    CUresult res = Driver::GetProcAddress_v2(symbol, pfn, cudaVersion, flags, symbolStatus);
    if (res != CUDA_SUCCESS) return res;
    GetInterceptAddr(symbol, pfn, cudaVersion);
    return res;
}
"""

    with open(file_path, 'w') as file:
        file.writelines(lines)
    
        file.write(template)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the cuGetProcAddress related code.')
    parser.add_argument('-f', type=str, required=True, help='Path to the intercept.cpp file')
    args = parser.parse_args()

    process_proc_addr(args.f)


    


