#!/bin/bash

set -e

base_dir=$(pwd)
core_count=$(nproc --all)

python_version="3.9.18"
python_source_url="https://www.python.org/ftp/python/$python_version/Python-$python_version.tar.xz"
python_tar="$base_dir/python.tar.xz"

if ! [ -f "$python_tar" ]; then
  wget -O "$base_dir/python.tar.xz" "$python_source_url" 
fi
source_dir="$base_dir/Python-$python_version"
build_prefix="$source_dir/prefix"
build_static="$source_dir/build_static"
rm -rf "$source_dir"
tar -xf "$base_dir/python.tar.xz"
mkdir "$build_prefix"
mkdir "$build_static"

#generate new setup.local to statically link builtin modules
python3 "$base_dir/parse_setup.py" "$source_dir/Modules/Setup" > "$source_dir/Modules/Setup.local"

cd "$source_dir"
./configure LDFLAGS="-static" --disable-shared --prefix="$source_dir/prefix"
make LDFLAGS="-static" LINKFORSHARED=" " -j$core_count
make install -j$core_count

#find modules in stdlib and add them to main.py
stdlib_modules=$(find "$source_dir/Lib/" -mindepth 1 -maxdepth 1 -exec basename {} .py ';')
stdlib_modules=$(echo "$stdlib_modules" | sed "/site-packages/d")
stdlib_modules=$(echo "$stdlib_modules" | xargs | tr -s "[:blank:]" ",")
cat $base_dir/main.py | sed "s/pass #modules_here/import $stdlib_modules/" > $build_static/main.py

#use freeze.py to build our new main.py
cd $build_static
$build_prefix/bin/python3 $source_dir/Tools/freeze/freeze.py -p "$build_prefix" ./main.py
make -j$core_count
mv ./main $base_dir/main

echo "build done! check ./main for your executable"
echo "you can run upx if you want to reduce the size even further"