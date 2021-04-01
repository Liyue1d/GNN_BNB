#!/bin/bash
swig -c++ -python -py3 -o src/TwoOpt_wrap.cpp -outdir lib int/TwoOpt.i
g++ -I ../../c++/TwoOpt/inc -fpic -c ../../c++/TwoOpt/src/TwoOpt.cpp -o obj/TwoOpt.o
g++ -I /usr/include/python3.5/ -I /usr/local/lib/python3.5/dist-packages/numpy/core/include -I ../../c++/TwoOpt/inc -fpic -c src/TwoOpt_wrap.cpp -o obj/TwoOpt_wrap.o
g++ -shared -o lib/_TwoOpt.so obj/TwoOpt.o obj/TwoOpt_wrap.o
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${HOME}/workspace/c++/TwoOpt/lib
