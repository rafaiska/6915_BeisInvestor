#!/usr/bin/env bash

#Script para extrair dados dos arquivos historicos da Bovespa
#Arquivos COTAHIST_A20XX.ZIP devem ser colocados no diretorio ./data

touch ./data/cotacoes
for index in "010INTEL" "010FACEBOOK" "010TELEBRAS" "010MICROSOFT" "020ITAUTEC" "010ORACLE"
do
	for year in 16 15
	do
		cat ./data/COTAHIST_A20${year}.TXT | grep ${index} >> ./data/cotacoes
	done
done
gzip -f ./data/cotacoes
