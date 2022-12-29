# pat
(portuguese) Padrões em Análise Técnica (english) Technical Analysis Patterns 

	I N S T A L L A T I O N
►    System's Dependences: ◄
Linux
->TA-Lib
Download ta-lib-0.4.0-src.tar.gz and: (https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download?use_mirror=sonik)
$ untar and cd
$ ./configure --prefix=/usr (it takes some seconds)
$ make (it takes about 1 minute)
$ sudo make install
    If you build TA-Lib using make -jX it will fail but that's OK! Simply rerun make -jX followed by [sudo] make install.
    
►    Python's Dependences: ◄
->Main library (which communicates with TA-Lib):
	You can install from PyPI:
	$ pip install TA-Lib (or download and install from https://mrjbq7.github.io/ta-lib/)
	Ps: I use pip3
	
	Or checkout the sources and run setup.py yourself:
	$ python setup.py install

->YFinance		       : $ pip3 install yfinance
->Pandas Data Reader   : $ pip3 install pandas_datareader
->MatPlotLib		   : $ pip3 install matplotlib
->MPLCursors		   : $ pip3 install mplcursors
->MPLFinance		   : $ pip3 install mplfinance

QUICK GUIDE:
$ python3 pat3.py		(or python pat3.py - in some older systems)
Just follows the interactive menu:
╔════════════════════════════════════════════════════════╕
║::: MENU ::::                       	                 │
║1-Defina acao e periodo (stock and period) 	         │
║2-Ache N padroes em uma acao (find n stock patterns)    │
║3-Ache um padrao em N acoes (find a pattern in n stocks)│
║4-Grafico com indicadores (Indicators graphic)          │
║5-Mostrar tabela da acao escolhida (Shows stock table)  │
║6-Mudar estilo do grafico (change graph style)          │
║7-Sobre...   (About...)                                 │
║8-Sair       (Exit)                                     │
╙────────────────────────────────────────────────────────┘

