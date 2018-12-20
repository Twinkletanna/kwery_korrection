"""
Look at https://norvig.com/spell-correct.html
https://github.com/barrust/pyspellchecker
https://pyspellchecker.readthedocs.io/en/latest/

Working in mappy2. But might need to shift to python3
"""
import random
import pyautocorrect
from tqdm import tqdm
from spellchecker import SpellChecker

from tqdm import *
import eval_all
from spellchecker import SpellChecker
import pickle as pkl
def peterspell(queries,type_data):
    spell = SpellChecker()
    suggestions=[]
    for i in tqdm(range(len(queries))):
        query_words=queries[i].split()
        correction=[]
        for word in query_words:
            correction.append(spell.correction(word))
	
        if isinstance(correction, basestring) == True:
                suggestions.append(queries[i])
        else: #It returned False
                suggestions.append(correction)
                
    with open('./npeterspell'+type_data+'.pkl', 'wb') as handle:
            pkl.dump(suggestions, handle, protocol=pkl.HIGHEST_PROTOCOL)

    with open('./npeterspell'+type_data+'.txt','w')as f:
	for line in suggestions:
	    f.write(' '.join(line)+'\n')    
        
    return suggestions

#X,Y,text_x,test_y=eval_all.read_jdb()
#pred=peterspell(X,'jdb')
#print (eval_all.run_eval(X,pred,Y))

#X.extend(text_x)
#Y.extend(test_y)
#pred=peterspell(text_x,'jdb_all')
#print(eval_all.run_eval(text_x,pred,test_y))

#X,Y=eval_all.read_trec()
#pred=peterspell(X,'trec')
#print(eval_all.run_eval(X,pred,Y))

X,Y=eval_all.read_qspell()
pred=peterspell(X,'qspell')
print(eval_all.run_eval(X,pred,Y))

#X,Y=eval_all.read_end2end()
#pred=peterspell(X,'end')
#print(eval_all.run_eval(X,pred,Y))
