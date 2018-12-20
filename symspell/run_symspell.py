#referred https://github.com/mammothb/symspellpy

import os
from collections import Counter
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module
import pickle as pkl

def read_qspell():
    file='../corpus-webis-qspell-17.csv'
    data=[]
    valid=[]
    lens=[]
    with open(file) as f:
        for line in f:
            part=line.strip().rstrip(';').split(';')
            data.append(part[1])
            valid.append(part[2:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
                # print(part)
    print(file, len(data),Counter(lens))
    return data,valid


def read_jdb():
    train_file='../v1.0/train.txt'
    test_file_1='../v1.0/test-split1.txt'
    test_file_2='../v1.0/test-split2.txt'
    test_file_3='../v1.0/test-split3.txt'
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


def read_jdb_input_file(file):
    data=[]
    valid=[]
    lens=[]
    # with open('../../v1.0/train.txt') as f:
    with open(file) as f:
        for line in f:
            part=line.strip().split('\t')
            data.append(part[0])
            valid.append(part[1:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
            #     print(valid[-1])
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

def read_trec_input():
    file='./data.txt'
    data=[]
    valid=[]
    lens=[]
    with open(file) as f:
        for line in f:
            part=line.strip().split('\t')
            data.append(part[0])
            valid.append(part[1:])
            lens.append(len(valid[-1]))
            # if lens[-1]>1:
            #     print(valid[-1])
    print(file, len(data),Counter(lens))
    return data,valid



def run_eval(data,prediction,valid):

    num_data=len(prediction)
    total=0.1
    acc=0.1
    # print('in eval')
    for i in range(len(prediction)):
        # x=input()
        if data[i] not in valid[i]:
            print(data[i],'\t',prediction[i],'\t',valid[i])
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

    # # lookup suggestions for single-word input strings
    # input_term = "memebers"  # misspelling of "members"
    # # max edit distance per lookup
    # # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    # max_edit_distance_lookup = 2
    # suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    # suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
    #                                max_edit_distance_lookup)
    # # display suggestion term, term frequency, and edit distance
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.count,
    #                               suggestion.distance))

    # # lookup suggestions for multi-word input strings (supports compound
    # # splitting & merging)
    # input_term = ("whereis th elove hehad dated forImuch of thepast who "
    #               "couqdn'tread in sixtgrade and ins pired him")
    # # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2


    f_wrong=open('wrong'+file[2:],'w')
    f=open(file,'w')
    pred=[]
    for i,input_term in enumerate(data):


        suggestions = sym_spell.lookup_compound(input_term,
                                                max_edit_distance_lookup)
        # display suggestion term, edit distance, and term frequency
        for suggestion in suggestions:
        #     print("{}, {}, {}".format(suggestion.term, suggestion.count,
        #                               suggestion.distance))
            # op=[suggestion.term, suggestion.count,
                                      # suggestion.distance]
            pred.append(suggestion.term)
            f.write(suggestion.term)
            # f.write(str(suggestion.count)+'\t')
            # f.write(str(suggestion.distance))
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


def predict_all():


    X,Y,test_x,test_y=read_jdb()

    test_x_pred=run_symsp(test_x,'./jdb_op_test.txt',test_y)
    with open('./jdb_test.pkl', 'wb') as handle:
        pkl.dump(test_x_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)


    X_pred=run_symsp(X,'./jdb_op_train.txt',Y)
    with open('./jdb.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)

    X.extend(test_x)
    Y.extend(test_y)

    X_pred=run_symsp(X,'./jdb_op_all.txt',Y)
    with open('./jdb_all.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)

    
    X,Y=read_trec_input()
    X_pred=run_symsp(X,'./op.txt',Y)
    with open('./trec.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)




    X,Y=read_qspell()    
    X_pred=run_symsp(X,'./qspell_op.txt',Y)
    with open('./qspell.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)

    X,Y=read_end2end()
    X_pred=run_symsp(X,'./end_op.txt',Y)
    with open('./end.pkl', 'wb') as handle:
        pkl.dump(X_pred, handle, protocol=pkl.HIGHEST_PROTOCOL)
    

def eval_all():
    
    X,Y,test_x,test_y=read_jdb()
    print('Base: ',run_eval(X,X,Y))

    with open('./jdb_all.pkl', 'rb') as handle:
        pred_load=pkl.load(handle)
    X.extend(test_x)
    Y.extend(test_y)
    print('Method X : ',run_eval(X,pred_load,Y))


    with open('./jdb.pkl', 'rb') as handle:
        pred_load=pkl.load(handle)
    print('Method X : ',run_eval(X,pred_load,Y))


    with open('./jdb_test.pkl', 'rb') as handle:
        pred_test_load=pkl.load(handle)    
    print('Method,test: ',run_eval(test_x,pred_test_load,test_y))
    
    X,Y=read_trec_input()
    with open('./trec.pkl', 'rb') as handle:
        pred_trec_load=pkl.load(handle)    
    # print('Base: ',run_eval(X,X,Y))
    print('Method X: ',run_eval(X,pred_trec_load,Y))
    
    X,Y=read_qspell()
    with open('./qspell.pkl', 'rb') as handle:
        pred_qspell_load=pkl.load(handle)    
    # print('Base: ',run_eval(X,X,Y))
    print('Method X: ',run_eval(X,pred_qspell_load,Y))

    X,Y=read_end2end()
    with open('./end.pkl', 'rb') as handle:
        pred_qspell_load=pkl.load(handle)    
    # print('Base: ',run_eval(X,X,Y))
    print('Method X: ',run_eval(X,pred_qspell_load,Y))    

# def main():

predict_all()
eval_all()

# if __name__ == "__main__":
#     main()

# def read_dict(file):#reading birbeck dictionary of misspelled words
#     # file='./missp/missp.dat'
#     dict_word={}
#     with open(file,'r') as f:
#         for line in f:
#             word=line.strip()
#             if '$' in word:
#                 key=word[1:]
#             else:
#                 if word not in dict_word:
#                     dict_word[word]=key
#     return dict_word


# def read_dict_h(file):#reading birbeck dictionary of misspelled words
#     dict_word={}
#     with open(file,'r') as f:
#         for line in f:
#             word=line.strip()
#             print(word)
#             if '$' in word:
#                 key=word[1:]
#             else:
#                 if word not in dict_word:
#                     dict_word[word]=key
#     return dict_word


# def run_dictmethod(X):
#     pred=[]
#     for query in X:
#         modified_query=[]
#         for word in query.split():
#             if word in birbeck:
#                 modified_query.append(birbeck[word])
#             else:
#                 modified_query.append(word)
#         pred.append(' '.join(modified_query))
#     return pred

# def read_all_dict():
#     birbeck=read_dict('./missp/missp.dat')
#     # birbeck=read_dict('./missp/missp.dat')
#     aspell=read_dict('./missp/aspell.dat')
#     # print(aspell)
#     wiki=read_dict('./missp/wikipedia.dat')
#     # print(wiki)
#     holbrook=read_dict_h('./missp/holbrook-missp.dat')

#     birbeck.update(aspell)
#     birbeck.update(wiki)

#     print(birbeck)
#     print(len(birbeck))

#     return birbeck
    
# def dict_method():

#     X,Y,test_x,test_y=read_jdb()
#     pred=run_dictmethod(X)
#     acc=run_eval(X,pred,Y)
#     print('Acc:',acc)


#     X.extend(test_x)
#     Y.extend(test_y)
#     pred=run_dictmethod(X)
#     acc=run_eval(X,pred,Y)
#     print('Acc:',acc)

#     X,Y=read_trec_input()
#     pred=run_dictmethod(X)
#     acc=run_eval(X,pred,Y)
#     print('Acc:',acc)

#     X,Y=read_qspell()    
#     pred=run_dictmethod(X)
#     acc=run_eval(X,pred,Y)
#     print('Acc:',acc)


# dict_method()
# birbeck=read_all_dict()
# dict_method()
