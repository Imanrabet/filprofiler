# The Fil memory profiler for Python

Your code reads some data, processes it, and uses too much memory.
In order to reduce memory usage, you need to learn what code is responsible, and specifically what code is responsible for peak memory usage.

And that's exactly what Fil will help you find.
Fil an open source memory profiler designed for data processing applications written in Python, and includes native support for Jupyter.

At the moment it only runs on Linux and macOS.

For more information, including an example of the output, see https://pythonspeed.com/products/filmemoryprofiler/

* [Installation](#installation)
* [Using Fil](#using-fil)
    * [Measuring peak (high-water mark) memory usage in Jupyter](#peak-jupyter)
    * [Measuring peak memory usage for Python scripts](#peak-python)
    * [Debugging out-of-memory crashes in your code](#oom)
* [Reducing memory usage in your code](#reducing-memory-usage)
* [What Fil tracks](#what-fil-tracks)

## Installation

### Prerequisites

To install the latest version of Fil you'll need Pip 19 or newer.
You can check like this:

```
$ pip --version
pip 20.0.2
```

If you're using something older than that, do:

```
$ pip install --upgrade pip
```

If _that_ doesn't work, try running that a virtualenv or Conda env.

### Installing Fil

Assuming you're on macOS or Linux, and are using Python 3.6 or later:

```
$ pip install filprofiler
```

## Using Fil

### <a name="peak-jupyter">Measuring peak (high-water mark) memory usage in Jupyter</a>

To measure memory usage of some code in Jupyter you need to do three things:

1. Use an alternative kernel, "Python 3 with Fil".
   You can choose this kernel when you create a new notebook, or you can switch an existing notebook in the Kernel menu; there should be a "Change Kernel" option in there in both Jupyter Notebook and JupyterLab.
2. Load the extension by doing `%load_ext filprofiler`.
3. Add the `%%filprofile` magic to the top of the cell with the code you wish to profile.


![Screenshot of JupyterLab](images/jupyter.png)

### <a name="peak-python">Measuring peak (high-water mark) memory usage for Python scripts</a>

Instead of doing:

```
$ python yourscript.py --input-file=yourfile
```

Just do:

```
$ fil-profile run yourscript.py --input-file=yourfile
```

And it will generate a report.

### <a name="oom">Debugging out-of-memory crashes</a>

First, run `free` to figure out how much memory is available—in this case about 6.3GB—and then set a corresponding limit on virtual memory with `ulimit`:

```shell
$ free -h
       total   used   free  shared  buff/cache  available
Mem:   7.7Gi  1.1Gi  6.3Gi    50Mi       334Mi      6.3Gi
Swap:  3.9Gi  3.0Gi  871Mi
$ ulimit -Sv 6300000
```

Then, run your program under Fil, and it will generate a SVG at the point in time when memory runs out:

```shell
$ fil-profile run oom.py 
...
=fil-profile= Wrote memory usage flamegraph to fil-result/2020-06-15T12:37:13.033/out-of-memory.svg
```

## <a name="reducing-memory-usage">Reducing memory usage in your code</a>

You've found where memory usage is coming from—now what?

If you're using data processing or scientific computing libraries, I have written a relevant [guide to reducing memory usage](https://pythonspeed.com/datascience/).

## What Fil tracks

Fil will track memory allocated by:

* Normal Python code.
* C code using `malloc()`/`calloc()`/`realloc()`/`posix_memalign()`.
* C++ code using `new` (including via `aligned_alloc()`).
* Anonymous `mmap()`s.
* Fortran 90 explicitly allocated memory (tested with gcc's `gfortran`).

Still not supported, but planned:

* `mremap()` (resizing of `mmap()`).
* File-backed `mmap()`.
  The usage here is inconsistent since the OS can swap it in or out, so probably supporting this will involve a different kind of resource usage.
* Other forms of shared memory, need to investigate if any of them allow sufficient allocation.
* Anonymous `mmap()`s created via `/dev/zero` (not common, since it's not cross-platform, e.g. macOS doesn't support this).
* `memfd_create()`.
* Possibly `memalign`, `valloc()`, `pvalloc()`, `reallocarray()`.

## License

Copyright 2020 Hyphenated Enterprises LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
