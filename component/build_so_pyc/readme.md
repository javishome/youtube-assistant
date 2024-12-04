# Hướng dẫn mã hoá code sang file .pyc và .so

## Mã hoá thành thư viện .so
### _B1: Cài đặt Cython_
```sh
pip install cython
```   
### _B2: Tạo project cython_
Gồm có ít nhất 3 file:
``` - __init__.py - my_module.py - setup.py ```
- File ```my_module.py``` chứa mã nguồn cần được dịch thành file ```.so``` vd:
    ````sh
    def hello_world():
        print('Hello')
- File ```setup.py``` là file cấu hình build 
    ```sh
    from distutils.core import Extension, setup
    from Cython.Build import cythonize
    # define an extension that will be cythonized and compiled
    ext = Extension(name="hello_module", sources=["my-module.py"])
    setup(ext_modules=cythonize(ext))
    ```
- File ```__init__``` là file chương trình, sử dụng file thư viện được dịch, và được mã hoá thành file .npy
    ```sh
    from .hello_module import *
    hello_module.hello_world()
### _B3: Compile code thành file .so_
```sh
python setup.py build_ext --inplace
```
File extension được build ra sẽ có tên dạng ``` name_module.cpython-39-aarch64-linux-gnu.so```, đổi tên file thành tên dễ sử dụng hơn vd: ```name_module.so```, file ```__init__``` sẽ sử dụng chính thư viện này bằng khai báo ```from .name_module import *```
### _B4: Mã hoá code bằng file .pyc_
Sử dụng lệnh:
```sh
python3 -m compileall __init__
```
File chương trình được mã hoá thành file ```.pyc``` nằm trong thư mục ```__pycache__```
## Lưu ý
- Cần thực hiện các thao tác trên HC
- Tên file không nhất thiết phải đặt theo fomat trên
- Link tham khảo: [Build .so](https://vinasupport.com/su-dung-cython-de-bao-ve-compile-source-code-python/), [Build .pyc](https://stackoverflow.com/questions/5607283/how-can-i-manually-generate-a-pyc-file-from-a-py-file)