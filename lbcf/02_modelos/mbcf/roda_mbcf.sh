#!/bin/bash
# Compila o MBCF (CF.DT) dos autores com o main.cpp adaptado e roda as duas florestas.
# Executar no WSL/Linux, a partir da raiz do repositorio:  bash lbcf/02_modelos/mbcf/roda_mbcf.sh
set -e
R=$(pwd)
W=~/tcc_cmp/mbcf

# 1. codigo dos autores, do zip original; troca apenas o main.cpp
rm -rf $W && mkdir -p $W && cd $W
unzip -q $R/upstream/lbcf/Code/Model/CF_DT/CF_DT_RCT.zip
cp $R/lbcf/02_modelos/mbcf/main.cpp MBCF_RCT/core/main.cpp

# 2. compilacao como no README dos autores (rm -r *, cmake .., make); ver DIVERGENCIAS A1, A2
mkdir -p MBCF_RCT/core/build && cd MBCF_RCT/core/build
rm -rf ./*
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. > /dev/null
make -j8 > /dev/null

# 3. uma floresta por braco: MBCF_uplift_1 (Mens), MBCF_uplift_2 (Womens)
O=$R/resultados/lbcf/predicoes/mbcf
mkdir -p $O
./MBCF_RCT $R/dados/lbcf $O     # alvo add_executable(MBCF_RCT ...) do CMakeLists.txt dos autores
