# Mesmo projeto descrito no Notebook, podendo ser executado no terminal

# Tempo estimado: 2 minutos e 7 segundos com 50.000 matches / 100.000 hitóricos

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

with open('/Users/rafaelferri/Arquivos/Clash/matches.txt') as file:
    CR = [ x.strip() for x in file.readlines()]

deserialize_cr = [json_normalize(eval(r1))for r1 in CR[0:50000]]
CRM = pd.concat(deserialize_cr, ignore_index = True)
CRM.columns = ['Left Clan','Left Deck','Left Player','Left Trophy','Right Clan','Right Deck','Right Player','Right Trophy','Result','Time','Type']

CRM['Left Crowns Won'] = [int(stars[0]) for stars in CRM['Result']]
CRM['Right Crowns Won'] = [int(stars[1]) for stars in CRM['Result']]

CRM['Left Result'] = [int(1) if(left>right) else int(-1) if(left<right) else int(0) for left, right in zip(CRM['Left Crowns Won'], CRM['Right Crowns Won'])]
CRM['Right Result'] = [int(-1) if(left>right) else int(1) if(left<right) else int(0) for left, right in zip(CRM['Left Crowns Won'], CRM['Right Crowns Won'])]
CRM.drop('Result', axis=1, inplace=True)

CRMl = CRM[['Left Clan','Left Deck','Left Player','Left Trophy','Left Crowns Won','Right Crowns Won','Left Result','Time','Type']]
CRMl.columns = ['Clan','Deck','Player','Trophy','Crowns Won','Crowns Lost','Result','Time','Type']

CRMr = CRM[['Right Clan','Right Deck','Right Player','Right Trophy','Right Crowns Won','Left Crowns Won','Right Result','Time','Type']]
CRMr.columns = ['Clan','Deck','Player','Trophy','Crowns Won','Crowns Lost','Result','Time','Type']

CRMf = pd.concat([CRMl, CRMr])
CRMf.index = range(len(CRMf))

# Abrindo as informações dos Decks
Army_colNames = np.hstack([["Troop "+str(i+1) for i in range(8)], ["Level "+str(i+1) for i in range(8)]])
Army = pd.DataFrame(data=[np.hstack([[army[0] for army in x], [int(army[1]) for army in x]]) for x in CRMf['Deck']], columns=Army_colNames)

CRMf = pd.concat([CRMf, Army], axis=1, join='inner')
CRMf.drop(['Deck'], axis=1, inplace=True)

# Melhores Clãs

ClasVitorias = CRMf.groupby('Clan')['Result'].sum().sort_values(ascending=False)
ClasVitorias10 = ClasVitorias[ClasVitorias > 10]

ClasContagem = CRMf.groupby('Clan')['Clan'].count().sort_values(ascending=False)

PercVitoriaCla = (ClasVitorias10 / ClasContagem)*100
PercVitoriaCla = pd.DataFrame(PercVitoriaCla.sort_values(ascending=False), columns=['Perc.'])


# Match entre melhores clãs e maiores troféus

#Abrindo as informações de troféus e selecionando os melhores
CRMf['Trophy'] = [int(trophy) for trophy in CRMf['Trophy']]
MediaTrofeus = CRMf.groupby('Clan')['Trophy'].mean()
PlayersCla = CRMf.groupby('Clan')['Player'].nunique()
ClasMaisTrofeus = (PlayersCla * MediaTrofeus)

# Top Clãs e seus decks
TopClas = pd.concat([PercVitoriaCla, ClasMaisTrofeus], axis=1, join='inner')
TopClas.columns = ['Percentual', 'Trophy']
Top10Clans = TopClas[(TopClas['Percentual']>20.0) & (TopClas['Trophy']>100000.0)].sort_values(by=['Trophy', 'Percentual'], ascending=False).head(10)

TopClansDecks = CRMf[(CRMf['Clan']==Top10Clans.index[0]) | (CRMf['Clan']== Top10Clans.index[1]) | (CRMf['Clan']== Top10Clans.index[2]) | (CRMf['Clan']== Top10Clans.index[3]) | (CRMf['Clan']== Top10Clans.index[4]) | (CRMf['Clan']== Top10Clans.index[5]) | (CRMf['Clan']== Top10Clans.index[6]) | (CRMf['Clan']== Top10Clans.index[7]) | (CRMf['Clan']== Top10Clans.index[8]) | (CRMf['Clan']== Top10Clans.index[9])]
print('*'*30)
print('Decks dos Melhores Clãs')
print('*'*30)
print(TopClansDecks[['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8', 'Result']].groupby(['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8']).count().sort_values(by='Result',ascending=False).head(10))

# Players bons de defesa (e seus decks)

CRMf['Crowns Won'] = [int(crowns) for crowns in CRMf['Crowns Won']]
CRMf['Crowns Lost'] = [int(crowns) for crowns in CRMf['Crowns Lost']]
PlayersDef = CRMf[(CRMf['Result']==1) & (CRMf['Crowns Lost']==0)]
Top10PlayersD = pd.DataFrame(PlayersDef.groupby('Player')['Result'].sum().sort_values(ascending=False).head(11))

PlayersDefDecks = PlayersDef[(PlayersDef['Player']==Top10PlayersD.index[1]) | (PlayersDef['Player']==Top10PlayersD.index[2]) | (PlayersDef['Player']==Top10PlayersD.index[3]) | (PlayersDef['Player']==Top10PlayersD.index[4]) | (PlayersDef['Player']==Top10PlayersD.index[5]) | (PlayersDef['Player']==Top10PlayersD.index[6]) | (PlayersDef['Player']==Top10PlayersD.index[7]) | (PlayersDef['Player']==Top10PlayersD.index[8]) | (PlayersDef['Player']==Top10PlayersD.index[9]) | (PlayersDef['Player']==Top10PlayersD.index[10])]
print('*'*30)
print('Melhores Decks de Defesa')
print('*'*30)
print(PlayersDefDecks[['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8', 'Result']].groupby(['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8']).count().sort_values(by='Result',ascending=False).head(10))

# Players bons de ataque (e seus decks)

PlayersAtk = CRMf[(CRMf['Result']==1) & (CRMf['Crowns Won']==3)]
Top10PlayersA = PlayersAtk.groupby('Player')['Result'].sum().sort_values(ascending=False).head(11)
print('*'*30)
print('Melhores Decks de Ataque')
print('*'*30)
PlayersAtkDecks = PlayersAtk[(PlayersAtk['Player']==Top10PlayersA.index[1]) | (PlayersAtk['Player']==Top10PlayersA.index[2]) | (PlayersAtk['Player']==Top10PlayersA.index[3]) | (PlayersAtk['Player']==Top10PlayersA.index[4]) | (PlayersAtk['Player']==Top10PlayersA.index[5]) | (PlayersAtk['Player']==Top10PlayersA.index[6]) | (PlayersAtk['Player']==Top10PlayersA.index[7]) | (PlayersAtk['Player']==Top10PlayersA.index[8]) | (PlayersAtk['Player']==Top10PlayersA.index[9]) | (PlayersAtk['Player']==Top10PlayersA.index[10])]
print(PlayersAtkDecks[['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8', 'Result']].groupby(['Troop 1', 'Troop 2', 'Troop 3', 'Troop 4', 'Troop 5', 'Troop 6', 'Troop 7', 'Troop 8']).count().sort_values(by='Result',ascending=False).head(10))
