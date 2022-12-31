# pat
(portuguese) Padrões em Análise Técnica (english) Technical Analysis Patterns 

	I N S T A L L A T I O N
►    System's Dependences: ◄<br>
Linux (Tested with Linux Mint - Ubuntu based)<br>
->TA-Lib<br>
Download ta-lib-0.4.0-src.tar.gz and: (https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download?use_mirror=sonik)<br>
$ untar and cd<br>
$ ./configure --prefix=/usr (it takes some seconds)<br>
$ make (it takes about 1 minute)<br>
$ sudo make install<br>
    If you build TA-Lib using make -jX it will fail but that's OK! Simply rerun make -jX followed by [sudo] make install.<br>
    
►    Python's Dependences: ◄<br>
->Main library (which communicates with TA-Lib):<br>
	You can install from PyPI:<br>
	$ pip install TA-Lib (or download and install from https://mrjbq7.github.io/ta-lib/)<br>
	Ps: I use pip3<br>
	<br>
	Or checkout the sources and run setup.py yourself:<br>
	$ python setup.py install<br>
<br>
->YFinance		       : $ pip3 install yfinance<br>
->Pandas Data Reader   : $ pip3 install pandas_datareader<br>
->MatPlotLib		   : $ pip3 install matplotlib<br>
->MPLCursors		   : $ pip3 install mplcursors<br>
->MPLFinance		   : $ pip3 install mplfinance<br>
<br>

	Q U I C K   G U I D E :

$ python3 pat3.py		(or python pat3.py - in some older systems)<br>
Just follows the interactive menu:<br>
╔═══════════════════════════════════════╕<br>
║::: MENU ::::						 │<br>
║1-Defina acao e periodo (stock and period) 	         │<br>
║2-Ache N padroes em uma acao (find n stock patterns)    │<br>
║3-Ache um padrao em N acoes (find a pattern in n stocks)│<br>
║4-Grafico com indicadores (Indicators graphic)          │<br>
║5-Mostrar tabela da acao escolhida (Shows stock table)  │<br>
║6-Mudar estilo do grafico (change graph style)          │<br>
║7-Sobre...   (About...)                                 │<br>
║8-Sair       (Exit)                                     │<br>
╙────────────────────────────────────────┘<br>

