# CUDA Intercept

This is a toolkit for intercepting CUDA driver APIs. You can use it to inject your code before or after the original CUDA driver functions, or even replace the original CUDA driver functions with your own code. 


## Usage

see [how-to-generate-template](examples/template/README.md) and [how-to-intercept-cuda-function](examples/kernel_launch/README.md).

## TODOs

- [ ] Usful Demos
- [ ] Logging Example
- [ ] Simplify the header files
- [ ] Executable Example


## Cite

This toolkit is extracted from [XSched](https://github.com/XpuOS/xsched) project. If you find this toolkit useful, please cite it as follows:

```bibtex
@inproceedings{Shen2025xsched,
  title = {{XSched}: Preemptive Scheduling for Diverse {XPU}s},
  author = {Weihang Shen and Mingcong Han and Jialong Liu and Rong Chen and Haibo Chen},
  booktitle = {19th USENIX Symposium on Operating Systems Design and Implementation (OSDI 25)},
  year = {2025},
  address = {Boston, MA},
  url = {https://www.usenix.org/conference/osdi25/presentation/shen-weihang},
  publisher = {USENIX Association},
  month = jul
}
```