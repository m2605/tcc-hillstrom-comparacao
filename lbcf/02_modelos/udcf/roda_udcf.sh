#!/bin/bash
# Compila o UDCF dos autores com o main.cpp adaptado e roda as tres variantes.
# Executar no WSL/Linux, a partir da raiz do repositorio:  bash lbcf/02_modelos/udcf/roda_udcf.sh
set -e
R=$(pwd)
W=~/tcc_cmp/udcf

# 1. codigo dos autores, do zip original; troca apenas o main.cpp
rm -rf $W && mkdir -p $W && cd $W
unzip -q $R/upstream/lbcf/Code/Model/LBCF/LBCF_RCT.zip
cp $R/lbcf/02_modelos/udcf/main.cpp UDCF_RCT/core/main.cpp

# 2. compilacao como no README dos autores (rm -r *, cmake .., make); ver DIVERGENCIAS A1, A2
cd UDCF_RCT/core/build
rm -rf ./*
cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 .. > /dev/null
make -j8 > /dev/null

# 3. as tres variantes (ACORDOS 4): nome, imbalance_penalty, stabilize_splits
D=$R/dados/lbcf
O=$R/resultados/lbcf/predicoes
mkdir -p $O
for cfg in "udcf_default 0.01 1" "udcf 0 1" "ablacao 0 0"; do
  set -- $cfg
  ./UDCF_RCT $2 $3 $D/train_data_UDCF.csv $D/test_data_UDCF.csv $O/$1.csv
done
