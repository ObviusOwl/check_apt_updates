# Python  compatibility

As we need to support centos 7, which ships only with python 2, the code base needs
to be compatible with python 2.7+ and python 3.4+.

Check out this guide: http://python-future.org/compatible_idioms.html

# Package manager back-ends

## APT

The documentation of APT's python API is quite good:

```
sudo apt install python-apt-doc
firefox file:///usr/share/doc/python-apt-doc/html/index.html
```

## YUM

The documentation of YUM's python API is very poor:

- http://yum.baseurl.org/api/yum/

One can use the code of YUM cli and packagekit as help:

- http://yum.baseurl.org/
- https://github.com/hughsie/PackageKit/blob/master/backends/yum/yumBackend.py

As YUM cli is written in python, there is no need to install extra packages to use the API.

## DNF

- https://dnf.readthedocs.io/en/latest/api.html