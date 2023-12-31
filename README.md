# Static Python Builder
This is a set of scripts to statically compile Python 3.9.18 into a binary that's only 5.1MB in size (after packing with UPX), complete with the entire standard library.

The purpose of this is to compile the smallest possible Python runtime for use in [shimboot](https://github.com/ading2210/shimboot), but this can be used for other applications as well.

## Explanation:
Statically compiling the interpreter alone isn't very hard, as you just need to [add a few arguments](https://wiki.python.org/moin/BuildStatically) when building it. However, the resulting binary does not contain the portions of the standard library which are written in pure Python. 

To compile the rest of the standard library, the built in [Freeze](https://wiki.python.org/moin/Freeze) tool is used, which can transpile a Python program into C. A compatible command-line interface is written in `main.py`, which we can run through Freeze. To include the standard library, we can just trick Freeze into thinking they are imported via an unreachable `if` statement containing an `import` of the entire standard library.

Then, Freeze is run, which generates a bunch of C files and a Makefile. Finally, we just run `make` to compile it, producing our static executable. Running it through [UPX](https://upx.github.io/) makes it even smaller, down to the final 11MB.

## Usage:
If you want to compile this for yourself, you just have to clone this repo, cd into it, and run `build.sh`. This will include the entire standard library, with a few exceptions.

If you want to customize which modules are included, edit `patch_main.py`, and add them to the `exclude` list.

If you have trouble compiling Python in the first place, you may want to exclude the problematic builtin modules in `patch_setup.py`.

## Example:
```
$ ./build.sh
...
build done! check ./main for your executable
you can run upx if you want to reduce the size even further
$ upx ./main --best
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2023
UPX 4.2.1       Markus Oberhumer, Laszlo Molnar & John Reiser    Nov 1st 2023

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
  15764056 ->   5282888   33.51%   linux/amd64   main                          

Packed 1 file.
$ ./main --version
Python 3.9.18, python-static 1.0.0
$ du -sh ./main
5.1M    ./main
$ ldd ./main
        not a dynamic executable
```

## Copyright:
This repository is licensed under the GNU GPL v3. Unless otherwise indicated, all code has been written by me, [ading2210](https://github.com/ading2210).

### Copyright Notice:
```
ading2210/python-static: A set of scripts to build a tiny statically linked Python runtime.
Copyright (C) 2023 ading2210

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```