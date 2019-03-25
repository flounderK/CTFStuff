#!/bin/bash
# This is a quick script to fix some of the issues with building the coursework for RPISec's Modern Binary Exploitation.
# To use the script just place this in the root directory of the git repo and run it

sed -i "s/IF(IS_DIRECTORY \${curdir}\/\${child})/IF(IS_DIRECTORY \${curdir}\/\${child} AND NOT \${child} STREQUAL \"CMakeFiles\")/g" ./CMakeLists.txt
sed -i "s/#include <cstring>/#include <cstring>\n#include <stdio.h>/g" ./src/lecture/cpp/cpp_lec02.cpp
cmake .
sed -i "s/CXX_FLAGS =  -m32 -O0 -fno-inline-functions/CXX_FLAGS =  -m32 -O0 -fno-inline-functions -std=c++11/g" ./src/lecture/cpp/CMakeFiles/cpp_lec02.dir/flags.make
make all && make install
