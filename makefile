l_amat.zip:
	wget -c https://data.fcc.gov/download/pub/uls/complete/l_amat.zip


.PHONY: data
data:
	mkdir -p data
	pushd data; unzip ../l_amat.zip

