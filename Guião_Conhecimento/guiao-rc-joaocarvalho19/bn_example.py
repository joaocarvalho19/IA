
from bayes_net import *

# Exemplo dos acetatos:

"""bn = BayesNet()

bn.add('r',[],0.001)
bn.add('t',[],0.002)

bn.add('a',[('r',True ),('t',True )],0.950)
bn.add('a',[('r',True ),('t',False)],0.940)
bn.add('a',[('r',False),('t',True )],0.290)
bn.add('a',[('r',False),('t',False)],0.001)

bn.add('j',[('a',True )],0.900)
bn.add('j',[('a',False)],0.050)

bn.add('m',[('a',True )],0.700)
bn.add('m',[('a',False)],0.100)

conjunction = [('j',True),('m',True),('a',True),('r',False),('t',False)]

#print(bn.jointProb(conjunction))"""

#--------------------------------------------------

sof = BayesNet()

#ST - sobrecarga de trabalho
#CP - cara de preocupado
#PA - precisa de ajuda
#AC - acumula correio nao lido
#PAL - aplicacao SOF2018f
#UER - utilizacao exagerada do rato


sof.add('st',[],0.6)
sof.add('pal',[],0.05)

sof.add('cp',[('st',True),('pa',False)],0.01)
sof.add('cp',[('st',True),('pa',True)],0.02)
sof.add('cp',[('st',False),('pa',False)],0.001)
sof.add('cp',[('st',False),('pa',True)],0.011)

sof.add('ac',[('st',False)],0.001)
sof.add('ac',[('st',True)],0.9)

sof.add('pa',[('pal',True)],0.25)
sof.add('pa',[('pal',False)],0.004)

sof.add('uer',[('pal',False),('pa',True)],0.1)
sof.add('uer',[('pal',False),('pa',False)],0.01)
sof.add('uer',[('pal',True)],0.9)

conjunctionSOF = [('st',False),('cp',False),('pa',False),('ac',False),('pal',False),('uer',False)]

#conjunctionSOF = [('s',True)]

print(sof.jointProb(conjunctionSOF))