 #!/usr/bin/env python -W ignore::DeprecationWarning
from numpy import vectorize,array,arange
from pandas_datareader import data
from pandas import set_option, read_csv, DataFrame, to_datetime #pd
import matplotlib.pyplot as mp #(16Mb)
#import matplotlib as mpl #(16Mb)
from mplcursors import cursor#(<1Mb) para mostrar a dica amarela com as coord x e y / Shows an yellow tip with c,y coordinates
from mplfinance.original_flavor import candlestick_ohlc
#import mplfinance as flpt
from matplotlib.dates import date2num, DateFormatter #mpdates #e esse sao para desenhar os candlesticks / it draws the candlesticks
import talib #3Mb + 2Mb da inst. do tar.gz  / technical analysis lib in Python that comunicates with TA-Lib installed in your system

#set_option('mode.chained_assignment', None) #para nao mostrar msg de erro desnecessarias / To don't show false error messages

try:
 f=open('p.txt','r')	#carrega Lista de PADROES / Loads PATTERN list
 p=eval(f.read())
 f.close();
except:
 print('\u25baArquivo de padroes p.txt nao encontrado!') #p.txt not found

try:
 f=open('i.txt','r')	#LISTA de indicadores / Loads INDICATORS list
 ind=eval(f.read())
 f.close();
except:
 #print(ascii('►')) #acha o unicode corespondente a um asc
 print('\u25baArquivo de indicadores i.txt nao encontrado!') # i.txt not found

op=-1 #opcao escolhida no menu / Selected option in initial menu
papel='TCSA3.SA' #default stock - avoids error
data_ini='a' #initial date
data_fim='b' #end date
dados='' #tabela de dados brutos do arquivo csv / a table with direct data from csv file
eixoX='' #X axis of graph
cot='' #tabela de cotacoes no formato DataFrame / a table with values converted from csv to Pandas dataframe
cot2=''#tabela de cotacoes temporarias, apenas para o proc 3:busca_acoes_por_padrao
	   #It stores temporary data, used only in option 3:busca_acoes_por_padrao (search_stocks_by_pattern)

def gravar_csv(a,f): # save to csv file, where a is a dataframe
 a.to_csv(f)
 print(a)
 return a

def ler_csv(f): #Reads from csv
 cotacoes=read_csv(f)
 return cotacoes

def lista_csv(ext='.csv'): #lista todos os arquivos csv ja baixados / lists all csv stocks files
 import os				
 tmp=''
 arr=[]
 c=0
 for f in os.listdir(): 
  if f.endswith(ext):
   tmp+=str(c).rjust(3)+':'+f.ljust(9)+'\t'
   c+=1
   arr.append(f)
   if c % 3==0: tmp+='\n'
 print(tmp)
 return arr

def grafico(arr,seq,l='t'): #Creates graphic from an array of points
 '''desenha um gráfico com o conjunto de pontos
 arr=[1,2,3,4] por exemplo'''
 mp.plot(seq,arr,label=l)
 mp.xlabel('time', size=6)
 mp.ylabel('value')

def mostra_grafico(): #Shows the graphic with additional options
 global papel,estilo,fig;
 #mp.margins()
 fig.suptitle(papel)
 mp.legend()
 mp.grid()
 #mp.tight_layout()
 mp.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.10)
 cursor(hover=True)
 mp.xticks(rotation=45) #gira o texto da data / Rotates date text
 mp.rcParams.update({'font.size': 6})
 mp.rc('axes', labelsize=6)    # fontsize of the x and y labels
 mp.style.context(estilos[estilo])
 mp.style.use(estilos[estilo])
 mp.show()

def formata_data(d): #Writes dates vertically, converting yyyy-mm-dd -> dd-mm-yy
 tmp=d
 for i in range(len(d)):
  tmp[i]=d[i][8:]+'\n'+d[i][5:7]+'\n'+d[i][2:4]
 return tmp

def des_formata_data(d): #writes data horizontally, converting dd-mm-yy -> yyyy-mm-dd
 tmp=d
 for i in range(len(d)):
  tmp[i]='20'+d[i][6:]+'-'+d[i][3:5]+'-'+d[i][:2]
 return tmp

def dif0 (a): #ve se um array tem algum valor diferente de 0 / Sees if 'a' array has a value different of 0
 r=[] #e retorna um array com os indices que se encaixam no padrao /and return another array with indexes within this pattern
 for i in range(len(a)):
  if (a[i]!=0):
   r.append(i)
 return r

def dif0_date(a,datas): #return an array with data from matching patterns (those found in previous function 'dif0')
 tmp=''
 for i in range(len(a)):
  if a[i]!=0 :
   tmp=tmp+datas[i]+' '
 return tmp+'.'
 
def writeln(nome,result,d): # a kind of 'handsome' print
 e=20 #espacamento / alignment space size
 tmp=''
 if len(dif0(result))>0:
  tmp=tmp+nome.ljust(e)+':'+dif0_date(result,d).ljust(10)
 return tmp

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def menu(): #Main menu
 global op, papel, data_ini, data_fim,dados,cot,cot2,estilo,estilos,fig,ax;
 op2=10
 print('╔════════════════════════════════════════════════════════╕')
 print('║::: MENU ::::                       	                 │')
 print('║1-Defina acao e periodo (stock and period) 	         │')
 print('║2-Ache N padroes em uma acao (find n stock patterns)    │')
 print('║3-Ache um padrao em N acoes (find a pattern in n stocks)│') 
 print('║4-Grafico com indicadores (Indicators graphic)          │')
 print('║5-Mostrar tabela da acao escolhida (Shows stock table)  │')
 print('║6-Mudar estilo do grafico (change graph style)          │')
 print('║7-Sobre...   (About...)                                 │')
 print('║8-Sair       (Exit)                                     │')
 print('╙────────────────────────────────────────────────────────┘')
 op=int(input('Escolha uma opcao: (Choose an option)') or '0')
 if (op==1):
  print('Arquivos já baixados: / Files already downloaded: ')
  lista=lista_csv()
  print('Acoes do brasil adicione.SA no final. Ex: ABEV3.SA\r')
  print('Write stocks names as presented in Yahoo Finance ')
  papel=input("Nome do papel: (enter para o 1º da lista) \n Stock ticker: }(enter for first of the list)") or "0";
  try:
   tmp = int(papel)
   papel=lista[tmp][:-4]
   print('Papel escolhido (Choose ticker)'+papel)
  except:
   print('')
  
  try:
   with open(papel+'.csv', 'r') as f:
    dados=ler_csv(papel+'.csv')
  except IOError:
    print('Arquivo nao encontrado! (file not found)')
    #data_ini=str(input('Data de inicio (yyyy-mm-dd) : (start date) ') or '2021-06-20')
    #data_fim=str(input('Data final: (yyyy-mm-dd) : (end date) ') or '2021-07-22')
    #a=data.DataReader(papel, 'yahoo', data_ini, data_fim)
    #gravar_csv(a,papel+'.csv')
    #dados=ler_csv(papel+'.csv')
    print('Baixe manualmente os arquivos ')
    print('1-Acesse finance.yahoo.com ')
    print('2-Na caixa de pesquisa, digite o codigo da acao (Ex:MGLU3.SA)')
    print('3-Clique na aba \'hitorical data\'')
    print('4-Em \'time period\' coloque as datas inicial e final.Clique em \'Done\'.')
    import os
    directory_path = os.getcwd()
    print('5-Clique em download e salve na pasta deste programa: '+directory_path)
    print('\nYou need to download manually:')
    print('1-Go to finance.yahoo.com\n2-In search box, type the name of ticker')
    print('3-Click in the \'historical data\' tab')
    print('4-At \'time period\' enter initial and final date. Click at \'done\'.')
    print('5-Click at download and save to the folder of this script: '+directory_path)
    exit();
  cot =DataFrame(data=dados)
  cot2=DataFrame(data=dados)
 elif (op==6):
  for i in range(len(estilos)):
   print(str(i).ljust(3)+' : '+estilos[i].ljust(20),end='')
   if i % 2 == 1:print('\n')
  print('estilo atual: (Current style) '+str(estilo))
  estilo=int(input('Digite o codigo do estilo grafico: (0-2x) ou enter para manter o atual: (Enter style code or press enter to keep the current one) ') or estilo)
  mp.style.context(estilos[estilo])
  mp.style.use(estilos[estilo])
  print('Estilo do grafico: (Graph style) '+estilos[estilo])
  temp=mp.subplots()
  fig,ax = temp # creating Subplots
  grava_variavel_arq('o.cfg','graphical style',estilo)
  print('\u25baReinicie o programa para as alteracoes terem efeito. \n (For effective change, restart the program) ')
 res=[op,papel,data_ini,data_fim,cot,cot2] 
 return res

def busca_por_indicador(cot,cot2): #opcao 4
 #opcoes gerais para os graficos
 eixoX=formata_data(cot['Date'])
 grafico(cot['Close'],eixoX,'Cotacao') #plota a propria cotacao
 
 for i in range(len(ind)):
  print(str(i)+' : '+ind[i][0]+' '+ind[i][1])
 nind=int(input('QUANTOS indicadores voce quer por?\nDigite 0 para nenhum ou enter para 1 : \n How many indicators you want to insert?\n Press 0 to none or enter to keep the most recent one ') or '1')
 for i in range(nind):
  cind=int(input('\u25baQUAL indicador? padrao=5 (MA) : \u25ba \n Which indicator? default=5 (MA) ') or '5') #codigo do indicador
  print(ind[cind][3]+'\n'+ind[cind][4])
  if cind==0:
   result = talib.BBANDS(cot['Close'].values, 5,2,2,0)
   grafico(result[0]	,eixoX,'Bandas de Boillinger B1')
   grafico(result[1]	,eixoX,'Bandas de Boillinger B2')
   grafico(result[2]	,eixoX,'Bandas de Boillinger B3')	
  elif cind==1:
   result = talib.DEMA(cot['Close'].values, int(len(cot['Close'])/5))
   grafico(result	,eixoX, ind[cind][1])
  elif cind==2:
   result = talib.EMA(cot['Close'].values, int(len(cot['Close'])/5))
   grafico(result	,eixoX, ind[cind][1])
  elif cind==3:
   result = talib.HT_TRENDLINE(cot['Close'].values)
   print(result)
   grafico(result	,eixoX, ind[cind][1])
  elif cind==4:
   result = talib.KAMA(cot['Close'].values, int(len(cot['Close'])/5))
   grafico(result	,eixoX, ind[cind][1])
  elif cind==5:
   v1=input('Quantos dias? Padrao=21 : \n How many days? default=21 ') or '21'
   result = talib.MA(cot['Close'].values, int(v1))
   grafico(result	,eixoX, ind[cind][1]+' '+v1+'d')
  elif cind==6:
   v1=float(input('Fast Limit? Default=0.50:') or '0.50')
   v2=float(input('Slow Limit? Default=0.05:') or '0.05')
   result = talib.MAMA(numpy.array(cot['Close'].values),v1,v2)
   grafico(result[0],eixoX, ind[cind][1]+' F')
   grafico(result[1],eixoX, ind[cind][1]+' S')
  elif cind==7:
   vector=numpy.vectorize(numpy.float)
   v1=numpy.arange(0, len(cot['High']),1,float)#.reshape(len(cot['High']),1)
   v1=vector(v1)
   v2=int(input('Min. period? Default=2 :') or '2')
   v3=int(input('Max. period? Default=30 :') or '30')
   result = talib.MAVP(numpy.array(cot['Close'].values),v1,v2,v3,0)
   grafico(result,eixoX, ind[cind][1])
  elif cind==8:
   v1=int(input('Time Period? Default=14 :') or '14')
   result = talib.MIDPOINT(numpy.array( cot['Close'] ), v1)
   grafico(result,eixoX, ind[cind][1])
  elif cind==9:
   v1=int(input('Time Period? Default=14 :') or '14')
   result = talib.MIDPRICE(cot['High'].values,cot['Low'].values , v1)
   grafico(result,eixoX, ind[cind][1])
  elif cind==10:
   v1=int(input('Acceleration? Default=0 :') or '0')
   v2=int(input('Maximum? Default=0 :') or '0')
   result = talib.SAR(cot['High'].values,cot['Low'].values ,v1,v2)
   grafico(result,eixoX, ind[cind][1])
  elif cind==11:
   v1=int(input('Start Value: Default=0 :') or '0')
   v2=int(input('Offset on reverse: Default=0 :') or '0')
   v3=int(input('Acceleration init long: Default=0 :') or '0')
   v4=int(input('Acceleration long: Default=0 :') or '0')
   v5=int(input('Acceleration max long: Default=0 :') or '0')
   v6=int(input('Acceleration init short: Default=0 :') or '0')
   v7=int(input('Acceleration short: Default=0 :') or '0')
   v8=int(input('Acceleration max short: Default=0 :') or '0')
   result = talib.SAREXT(cot['High'].values,cot['Low'].values ,v1,v2,v3,v4,v5,v6,v7,v8)
   grafico(result,eixoX, ind[cind][1])
  elif cind==12:
   v1=int(input('Time period? Default=30 :') or '30')
   result = talib.SMA(cot['Close'].values ,v1)
   grafico(result,eixoX, ind[cind][1])
  elif cind==13:
   v1=int(input('Time period? Default=5 min=2 max='+str(int(len(cot['Close'].values)/5))+' :') or '5')
   result = talib.T3(cot['Close'].values ,v1,0)
   grafico(result,eixoX, ind[cind][1])
  elif cind==14:
   v1=int(input('Time period? Default=30 min=2 max='+str(int(len(cot['Close'].values)/3))+':') or '30')
   result = talib.TEMA(cot['Close'].values ,v1)
   grafico(result,eixoX, ind[cind][1])
  elif cind==15:
   v1=int(input('Time period? Default=30 min=2 max='+str(int(len(cot['Close'].values)-1))+':') or '30')
   result = talib.TRIMA(cot['Close'].values ,v1)
   grafico(result,eixoX, ind[cind][1])
  elif cind==16:
   v1=int(input('Time period? Default=30 min=2 max='+str(int(len(cot['Close'].values)-1))+':') or '30')
   result = talib.WMA(cot['Close'].values ,v1)
   grafico(result,eixoX, ind[cind][1])
  else:
   print('invalid option')
 mostra_grafico()
 cot['Date']=des_formata_data(cot['Date'])

#indicadores que nao funcionam: #3 HT_TRENDLINE
estilo=0
def le_variavel_arq(f,nome_var_arq): #funcao que retorna o que esta na frente de =
 try:   #na linha que contem a frase nome_var no arquivo f
  a=open(f,'r')
  for i in a:
   linha=i
   pos_igual=linha.find('=')
   if linha[:pos_igual]==nome_var_arq:res=(linha[pos_igual+1:])
  a.close()
 except: print('erro ao ler (failed to read) '+f);
 return res

def grava_variavel_arq(f,nome_var_arq,nome_var):
 index=search_string_in_file(f,nome_var_arq)
 replace_line(f, index[0][0]-1, nome_var_arq+'='+str(nome_var))

estilo=int(le_variavel_arq('o.cfg','graphical style'))
estilos=['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
mp.style.context(estilos[estilo])# 'ggplot'
mp.style.use(estilos[estilo])# 'ggplot'
#fig, (ax,ax2) = mp.subplots(2) # 2 graficos em uma tela
fig, ax = mp.subplots() # creating Subplots

def tem_val_dif_de_0(v): #retorna true se vetor tem valor diferente de zero
 tmp=False	
 for i in range(len(v)):
  if v[i]!=0:
   tmp=True
 return tmp   

def adic_grafico(r,c,p,dados): #parte da opcao 2
 global eixoX, fig, ax, estilo,estilos;
 if c!=100:
  #eixoX=formata_data(cot['Date']) #old config
  #if c==1:grafico(cot['Close'],eixoX,'Cotacao') #plota a propria cotacao
  eixoX=to_datetime(cot['Date'])
  eixoX = eixoX.map(date2num)
  if c==1:
   mp.style.context(estilos[estilo])# 'ggplot'
   mp.style.use(estilos[estilo])# 'ggplot'
   print('Estilo do grafico: (Graph Style) '+estilos[estilo])
  cor='black'
  novoeixoX=[]; r2=[];   #inicializa vetores graficos

  for i in range(len(r)):
   if r[i]!=0:
    r2.append(cot['Close'][i]*( 1-(c-1)*0.02) )
    novoeixoX.append(eixoX[i])
    ax.annotate(p[1].strip().replace(' ',' '),xy=(eixoX[i],cot['Low'][i]*( 1-(c-1)*0.02)),size=6, rotation=45)
    if c==0:print(r)
  marca=p[3].strip()	  
  if   marca=='D':marca=7; cor='red';	#down
  elif marca=='U':marca=6; cor='green';	#up
  elif marca=='R':marca='X';cor='orange'; #reversao tendencia
  elif marca=='S':marca=0; cor='blue'; #estabilidade, indecisao
  #mp.plot(novoeixoX,r2,label='',linestyle='None',marker=marca,markerfacecolor=cor,markeredgecolor=cor,markersize=18)
  ax.scatter(novoeixoX,r2,label='',linestyle='None',marker=marca,c=cor, alpha=1.0)
  ##cot['Date']= des_formata_data(cot['Date'])
 if c==100:  #desenha candlesticks por ultimo
  #fig, ax2 = mp.subplots()
  df=cot
  df = df[['Date', 'Open', 'High', 'Low', 'Close']] 
  df['Date'] = to_datetime(df['Date'])	# convert into datetime object
  df['Date'] = df['Date'].map(date2num)	# apply map function
  candlestick_ohlc(ax, df.values, width = 0.6,
                 colorup = 'green', colordown = 'red', 
                 alpha = 0.1)	# plotting the data
  maxv=cot['Volume'].max()
  minv=cot['Volume'].min()
  maxc=cot['Close'].max()
  minc=cot['Close'].min()
  pos_vol=(cot['Volume'])/((maxv)/(maxc))*0.1+(maxc) #0.9 eh so pra barra de volume nao tocar na cotacao
  #ax2.plot(df['Date'],cot['Volume'],label='Volume', linestyle='solid', alpha=0.2,color='cyan') #adiciona volume old: ax.bar(
  ax.plot(df['Date'],pos_vol,label='Volume', linestyle='solid', alpha=0.2,color='cyan') #adiciona volume old: ax.bar(
  for i in range(len(cot['Date'])):
   ax.annotate(str(round(cot['Volume'][i]/1000000,1))+' M',xy=(df['Date'][i],pos_vol[i]),size=5)
  #ax2.xaxis.set_major_formatter(mpdates.DateFormatter('%d/%m/%Y'))
  ax.xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
  mp.xticks(fontsize=8)
  mp.yticks(fontsize=8)
 
def busca_acoes_por_padrao(): #opcao 3
 global cot2
 for i in range(len(p)):
  print(str(i)+' : '+p[i][1]+' ('+p[i][3]+')')	 
 padrao=int(input('Escolha um padrao de candle: (0-'+str(len(p)-1)+') enter para \'2 crows\':') or '0')
 print(str(padrao));
 print('Acoes a serem pesquisadas:')
 arqs=lista_csv()
 
 for i in range(len(arqs)):
  try:
   with open(arqs[i], 'r') as f:
    dados=ler_csv(arqs[i])
    cot2=DataFrame(data=dados)
  except IOError:
    print('Arquivo nao encontrado!'+arqs[i])
  tmp=''
  result=[]
  ex_locals={}
  c ='preresult=talib.'+str(p[padrao][0])+'(cot2[\'Open\'].values,cot2[\'High\'].values,cot2[\'Low\'].values,cot2[\'Close\'].values)\n'
  c+='result=writeln(\''+str(p[padrao][1])+'\',preresult,cot2[\'Date\'])'
  exec(c, None, ex_locals)
  result=ex_locals['result']
  if len(result)>2:
   tmp+=result
  #result=ex_locals['preresult']  #desenhando padrao encontrado no grafico
  print('::::: buscando padrao '+p[padrao][1]+' no papel '+arqs[i][:-4]+' ::::::::'+tmp)
 print('Obs:Analisadas '+str(len(arqs))+' acoes.')
 #fim
 
def about():
 print('╔══════════════════════════════════════╕')
 print('║ Version  0.6 - dec/2022              │')
 print('║ First version: jul/2021              │')
 #print('║        │')
 print('║by W. Calera - Brasil                 │')
 print('╙──────────────────────────────────────┘')
