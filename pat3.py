from mylib import *

from time import sleep

while True:
 res=menu()
 op=res[0]
 papel=res[1]
 data_ini=res[2]
 data_fim=res[3]
 if len(res[4])>0:cot =res[4]
 if len(res[5])>0:cot2=res[5]
 if op==2: #busca padroes por acao / Find patterns by ticker
  cont=0
  print('::::: Estudo do papel '+papel+' ::::::'+data_ini+' - '+data_fim+'::')
  tmp=''
  for i in range(len(p)):
   result=[]
   ex_locals={}
   c ='preresult=talib.'+p[i][0]+'(cot[\'Open\'].values,cot[\'High\'].values,cot[\'Low\'].values,cot[\'Close\'].values)\n'
   c+='result=writeln(\''+str(p[i][1])+'\',preresult,cot[\'Date\'])'
   exec(c, None, ex_locals)
   result=ex_locals['result']
   if len(result)>2:
    tmp+=result+'\n'
   result=ex_locals['preresult']  #desenhando padrao encontrado no grafico / Drawing the found pattern at graphic
   if (p[i][3]!='' and tem_val_dif_de_0(result)):
    cont+=1 #contador para manter espacamento entre os simbolos no grafico / An counter to separate symbols at graphic
    adic_grafico(result,cont,p[i],dados) # o 2º param eh o marcador / the 2nd param is the marker
  adic_grafico(result,100,p[i],dados) # adiciona os candles da cotacao / Adds candlesticks
  mostra_grafico() #Shows the graphic (until now it only exists in RAM memory)
  print(tmp)
  print('Obs:Analisados '+str(len(p))+' padroes.')
 
 elif op==3:  busca_acoes_por_padrao() #Finds stocks that corresponds to an pattern
 elif op==4:  busca_por_indicador(cot,cot2) #Apply an indicator to an stock
 elif op==5:  print(cot);print(cot2); #Shows the internal table with stock prices
 elif op==7:  about();sleep(1); #info developer / version
 elif op==8:  exit();
 elif op==9:  print( talib.get_functions() ) #Internal functions of TA-Lib : Curiosity or debug porpouses only

