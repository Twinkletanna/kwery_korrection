"""
Refer: https://github.com/PandaWhoCodes/pyautocorrect and https://github.com/phatpiglet/autocorrect/ and https://pypi.org/project/autocorrect/
Works in mappy2 env but might have to shift this to py3.
WHat about Unicode?
"""

import eval_all
import gzip
import pyautocorrect
from tqdm import *
import pickle as pkl

def pyauto(queries,type_data):
    suggestions=[]
    for i in tqdm(range(len(queries))):
        correction = pyautocorrect.correct(queries[i])
        if isinstance(correction, basestring) == True:
                suggestions.append(correction)
        else: #It returned False
                suggestions.append(queries[i])
                
    with open('./pyauto'+type_data+'.pkl', 'wb') as handle:
            pkl.dump(suggestions, handle, protocol=pkl.HIGHEST_PROTOCOL)
            
    return suggestions

X,Y,test_x,test_y=eval_all.read_jdb()
pred=pyauto(X,'jdb')
print (eval_all.run_eval(X,pred,Y))

#X.extend(text_x)
#Y.extend(test_y)
pred=pyauto(test_x,'jdb_all')
print(eval_all.run_eval(test_x,pred,test_y))

X,Y=eval_all.read_trec()
pred=pyauto(X,'trec')
print(eval_all.run_eval(X,pred,Y))

X,Y=eval_all.read_qspell()
pred=pyauto(X,'qspell')
print(eval_all.run_eval(X,pred,Y))

X,Y=eval_all.read_end2end()
pred=pyauto(X,'end')
print(eval_all.run_eval(X,pred,Y))
