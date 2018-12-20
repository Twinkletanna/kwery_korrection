import os
from collections import Counter
import pickle as pkl

def read_qspell(flag=0):
    file='./corpus-webis-qspell-17.csv'
    data=[]
    valid=[]
    lens=[]
    
    single_file='./qspell_queries.txt'
    s_file=open(single_file,'w')
    with open(file) as f:
        for line in f:
            part=line.strip().rstrip(';').split(';')
            data.append(part[1])
            valid.append(part[2:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
                # print(part)
                
            if flag==1:
                s_file.write(part[1])
                s_file.write('\n')
                
                
    print(file, len(data),Counter(lens))
    return data,valid


def read_jdb_input_file(file,flag=0):
    data=[]
    valid=[]
    lens=[]
    # with open('../../v1.0/train.txt') as f:
    single_file='./jdb_queries.txt'
    s_file=open(single_file,'w')
    
    
    with open(file) as f: #  , open(single_file) as s_file:
        for line in f:
            part=line.strip().split('\t')
            data.append(part[0])
            valid.append(part[1:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
            #     print(valid[-1])
            
            if flag==1:
                s_file.write(part[0])
                s_file.write('\n')
            
    print(file, len(data),Counter(lens))
    return data,valid

def read_jdb():
    direc='./JDBv1.0/'
    train_file=direc+'train.txt'
    test_file_1=direc+'test-split1.txt'
    test_file_2=direc+'test-split2.txt'
    test_file_3=direc+'test-split3.txt'
    train_data,train_pred=read_jdb_input_file(train_file)
    test_data,test_pred=read_jdb_input_file(test_file_1)
    test_data2,test_pred2=read_jdb_input_file(test_file_2)
    test_data.extend(test_data2)
    test_pred.extend(test_pred2)
    test_data3,test_pred3=read_jdb_input_file(test_file_3)
    test_data.extend(test_data3)
    test_pred.extend(test_pred3)

    print("Train:",len(train_data))    
    print("Test:",len(test_data))    
    return train_data,train_pred,test_data,test_pred


def read_trec(flag=0):
    file='./Speller Challenge TREC Dataset/Speller Challenge TREC Dataset.txt'
    data=[]
    valid=[]
    lens=[]

    single_file='./trec_queries.txt'
    s_file=open(single_file,'w')

    with open(file) as f:
        for line in f:
            part=line.strip().split('\t')
            data.append(part[0])
            valid.append(part[1:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
            #     print(valid[-1])
            
            if flag==1:
                s_file.write(part[0])
                s_file.write('\n')

            
    print(file, len(data),Counter(lens))
    return data,valid


def read_end2end(flag=0):
    file='./end_to_end_queries.tsv'
    data=[]
    valid=[]
    lens=[]

    single_file='./end_queries.txt'
    s_file=open(single_file,'w')

    with open(file) as f:
        for line in f:
            part=line.strip().split('\t')
            data.append(part[0])
            valid.append(part[1:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
            #     print(valid[-1])
            
            if flag==1:
                s_file.write(part[0])
                s_file.write('\n')

            
    print(file, len(data),Counter(lens))
    return data,valid
    




def run_eval(data,prediction,valid):

    num_data=len(prediction)
    total=0.1
    acc=0.1
    print('NEW eval')
    for i in range(len(prediction)):
        # x=input()
        if data[i] not in valid[i]:
            # print(data[i],prediction[i],valid[i])
            # print('The data x is not in the prediction')
            total+=1
            if prediction[i] in valid[i]:
                # print('right')
                acc+=1
    print(total, ' out of ', len(prediction),' not in the input')
    print(acc, ' out of ', total,' correct\n')

    
    in_input=num_data-total+0.1
    mod_acc=(acc+in_input)/num_data

    return acc/total, mod_acc, in_input/num_data

# SYMSPELL

def run_symsp(data,file,Y):
    # create object
    initial_capacity = 83000
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    max_edit_distance_lookup = 2


    f_wrong=open('wrong'+file[2:],'w')
    f=open(file,'w')
    pred=[]
    for i,input_term in enumerate(data):
        suggestions = sym_spell.lookup_compound(input_term,max_edit_distance_lookup)
        for suggestion in suggestions:
            pred.append(suggestion.term)
            f.write(suggestion.term+'\t')
            f.write(str(suggestion.count)+'\t')
            f.write(str(suggestion.distance))
            f.write('\n')


            if suggestion.term not in Y[i]:

                # print('Input term:',input_term)
                # print('Candidates: ',Y[i])
                # print('Suggestion: ',suggestion.term)
                # x=input()
                f_wrong.write(input_term)
                f_wrong.write('\t')
                f_wrong.write(suggestion.term)
                f_wrong.write('\t')
                f_wrong.write('\t'.join(Y[i]))
                f_wrong.write('\n')
    f.close()
    return pred


def symspell_predict_all():


    X,Y,test_x,test_y=read_jdb()
    test_x_pred=run_symsp(test_x,'./jdb_op_test.txt',test_y)
    with open('./jdb_test.pkl', 'wb') as handle:
        pkl.dump(test_x_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)

    X_pred=run_symsp(X,'./jdb_op_train.txt',Y)
    with open('./jdb.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)


    
    X,Y=read_trec_input()
    X_pred=run_symsp(X,'./op.txt',Y)
    with open('./trec.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)




    X,Y=read_qspell()    
    X_pred=run_symsp(X,'./qspell_op.txt',Y)
    with open('./qspell.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)
        
        
def eval_jdb_all_curie(X,Y):
    jdb_train='currie_jdb_trainkp=0.75,nl=2,th=0.95_ori_v3.ckpt.pkl'
    jdb_test='currie_jdbkp=0.75,nl=2,th=0.95_ori_v3.ckpt.pkl'
    train=pkl.load(open(jdb_train,'rb'))
    test=pkl.load(open(jdb_test,'rb'))
    
    train.extend(test)
    
    print('Method X : ',run_eval(X,train,Y))
        
        
def eval_file(X,Y,filename,flag=0):

    if flag==1:
        pred_load=[]
        with open(filename,'r') as handle:
            for line in handle:
                pred_load.append(line.strip())
    else:
        print('evaluating')
        with open(filename, 'rb') as handle:
            pred_load=pkl.load(handle)
#     print('hi',pred_load,len(pred_load))
    print('Method X : ',run_eval(X,pred_load,Y))

def symspell_eval_all():
    
    X,Y,test_x,test_y=read_jdb()
    # print('Base: ',run_eval(X,X,Y))
    eval_file(X,Y,'./jdb.pkl')
    eval_file(test_x,test_y,'./jdb_test.pkl')
    
    X,Y=read_trec()
    eval_file(X,Y,'./trec.pkl')
    
    X,Y=read_qspell()
    eval_file(X,Y,'./qspell.pkl')
    
    
def nmt_eval_all():
    
    X,Y,text_x,test_y=read_jdb()
    # print('Base: ',run_eval(X,X,Y))
    eval_file(X,Y,'./OpenNMT-py-master/query_data/jdb_pred.txt',1)
    
    X.extend(text_x)
    Y.extend(test_y)
    eval_file(X,Y,'./OpenNMT-py-master/query_data/jdb_11K_pred.txt',1)
    
    X,Y=read_trec()
    eval_file(X,Y,'./OpenNMT-py-master/query_data/trec_pred.txt',1)
    
    X,Y=read_qspell()
    eval_file(X,Y,'./OpenNMT-py-master/query_data/qspell_pred.txt',1)  

    
def eval_mixture(data,prediction,valid):
    
    num_data=len(data)
#     print(num_data)
    total=0.1
    acc=0.1
    print('MIXTURE eval')
    for i in range(len(data)):
        # x=input()
        if data[i] not in valid[i]:
            # print(data[i],prediction[i],valid[i])
            # print('The data x is not in the prediction')
            total+=1
            
            for j,each in enumerate(prediction):
#                 print(j,i)
                if each[i] in valid[i]:
                    acc+=1
                    break
                    
                    
    print(total, ' out of ', len(data),' not in the input')
    print(acc, ' out of ', total,' correct\n')

    
    in_input=num_data-total+0.1
    mod_acc=(acc+in_input)/num_data

    return acc/total, mod_acc, in_input/num_data
