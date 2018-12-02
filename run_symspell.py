import os
from collections import Counter
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

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

def run_symsp(data,file):
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

    # lookup suggestions for single-word input strings
    input_term = "memebers"  # misspelling of "members"
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                   max_edit_distance_lookup)
    # display suggestion term, term frequency, and edit distance
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.count,
                                  suggestion.distance))

    # lookup suggestions for multi-word input strings (supports compound
    # splitting & merging)
    input_term = ("whereis th elove hehad dated forImuch of thepast who "
                  "couqdn'tread in sixtgrade and ins pired him")
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2


    f=open(file,'w')
    # data,pred=read_trec_input()
    # op=[]
    for input_term in data:


        suggestions = sym_spell.lookup_compound(input_term,
                                                max_edit_distance_lookup)
        # display suggestion term, edit distance, and term frequency
        for suggestion in suggestions:
        #     print("{}, {}, {}".format(suggestion.term, suggestion.count,
        #                               suggestion.distance))
            # op=[suggestion.term, suggestion.count,
                                      # suggestion.distance]
            f.write(suggestion.term+'\t')
            f.write(str(suggestion.count)+'\t')
            f.write(str(suggestion.distance))
            f.write('\n')

    f.close()


def main():
    X,Y,test_x,test_y=read_jdb()
    run_symsp(X,'./jdb_op_train.txt')
    run_symsp(test_x,'./jdb_op_test.txt')

    X,Y=read_trec_input()
    run_symsp(X,'./op.txt')


    X,Y=read_qspell()    
    run_symsp(X,'./qspell_op.txt')



if __name__ == "__main__":
    main()

