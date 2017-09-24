#!/usr/bin/env bash

#Script para extrair dados dos arquivos historicos da Bovespa
#Arquivos COTAHIST_A20XX.ZIP devem ser colocados no diretorio ./data

touch ./data/cotacoes
for index in "TIMP3F" "010INTEL" "010FACEBOOK" "010TELEBRAS" "VIVT3F" "010MICROSOFT" "GEOO34F" "010POSITIVO" "020ITAUTEC" "010TECTOY" "010ORACLE"
do
	for year in 16 15
	do
		zcat ./COTAHIST_A20${year}.ZIP | grep ${index} >> ./data/cotacoes
	done
done
gzip -f ./data/cotacoes
