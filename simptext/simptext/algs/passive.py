# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize


from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

import base
#from algs import base
from pattern.en import tenses, conjugate

PUNCTUATION = (';', ':', ',', '.', '!', '?')


def simp_passive_sent(tokens, node_list):
    dict1 = {
        'me': 'I',
        'him': 'He',
        'her': 'She',
        'them': 'They',
        'i': 'me',
        'he': 'him',
        'she': 'her',
        'they': 'them'
    }

    strs = ""
    """
    # the original tokens in the sent
    #import pdb; pdb.set_trace()
    print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        # A passive nominal subjec
        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubjpass_ind = nd[4]['nsubjpass'][0]
            det_ind = 0
            #amod_ind_list = [] # the list of adjectival modifier  
            for _nd in node_list:
                if nsubjpass_ind == _nd[0]:
                    if ('det' in _nd[4].keys()):
                        det_ind = _nd[4]['det'][0]
                        #amod_ind_list = _nd[4]['amod']

            #import pdb; pdb.set_trace()
            nsubjpass = tokens[nsubjpass_ind]
            # amod
            """
            amod_list = ""
            if len(amod_ind_list) > 0:
                for i in amod_ind_list:
                    amod_list = amod_list + " " + tokens[i]
                nsubjpass = amod_list + " " + nsubjpass
            """
            amod_list = base.get_dependency_list(tokens, node_list, nsubjpass_ind)

            nsubjpass = amod_list + " " + nsubjpass
            
            # det

            #import pdb; pdb.set_trace()
            if det_ind:
                nsubjpass = tokens[det_ind] + " " + nsubjpass
            elif str(nsubjpass.lower().strip()) in dict1:
                nsubjpass = dict1[str(nsubjpass.lower().strip())]
            else:
                pass

            auxpass_ind = 0
            if ('auxpass' in nd[4].keys()):
                auxpass_ind = nd[4]['auxpass'][0]

            #det_ind = 0
            subj = ""
            if ('nmod' in nd[4].keys()):
                # bugs: the case
                nmod_ind_list = nd[4]['nmod']

                case_ind = 0
                case_ind_2 = 0
                for nmod_ind in nmod_ind_list:
                    _case_ind = 0       
                    for nd in node_list[1:]:
                        if nmod_ind == nd[0]:
                            if ('case' in nd[4].keys()):
                                _case_ind = nd[4]['case'][0]
                                break
                    # check whether the agent is explicitly stated using "by"
                    if _case_ind > 0:
                        if tokens[_case_ind] == 'by':
                            case_ind = _case_ind
                            break
                        else:
                            case_ind_2 = _case_ind
                            
                #import pdb; pdb.set_trace()
                if case_ind == 0:
                    return strs
                #if tokens[case_ind] != 'by':
                #    return strs

                nmod_dict = {}
                for _nd in node_list[1:]: #BUG
                    if nmod_ind == _nd[0]:
                         nmod_dict = _nd[4]
                         break

                #import pdb; pdb.set_trace()
            #if ('case' in nmod_dict.keys()): # 'by'
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                det_ind = 0
                nsubj_compound_list = []
                if ('det' in nmod_dict):
                    det_ind = nmod_dict['det'][0]
                if ('compound' in nmod_dict):
                    nsubj_compound_list = nmod_dict['compound']

                for i in nsubj_compound_list:
                    subj = subj + " " + tokens[i]

                if det_ind:
                    subj = base.upper_first_char(tokens[det_ind]) + " " + subj + tokens[nmod_ind]
                elif tokens[nmod_ind] in dict1:
                    subj = dict1[tokens[nmod_ind]]
                else:
                    subj = subj + " " + tokens[nmod_ind]

                #import pdb; pdb.set_trace()
                verb = root
                if len(tenses(root)) > 0:
                    if auxpass_ind != 0:
                        if subj.strip().lower() == 'they':
                            verb = conjugate(root, tenses(tokens[auxpass_ind])[0][0], 2)
                        else:
                            verb = conjugate(root, tenses(tokens[auxpass_ind])[0][0], 3)
                    else:
                        if subj.strip().lower() == 'they':
                            verb = conjugate(root, tenses(root)[0][0], 2)
                        else:
                            verb = conjugate(root, tenses(root)[0][0], 3)

                #import pdb; pdb.set_trace()
                if case_ind_2 > 0:
                    _case_str = " ".join(tokens[case_ind_2:case_ind])
                    strs = subj + " " + verb + " " + nsubjpass.lower() + " " + _case_str + " ."
                else:
                    strs = subj + " " + verb + " " + nsubjpass.lower() + " ."

                return strs
            """
                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                tokens.insert(nsubj_ind + 1, verb)

                #root_ind = tokens.index(root)
                #_str1 = tokens[nsubj_ind:root_ind]

                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 =  ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2
            """
                #strs = str1 + ' . ' + str2
            #return strs


    return strs


def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w
    #for row in result.triples():
    #    print(row)


    #import pdb; pdb.set_trace()
    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)


    #import pdb; pdb.set_trace()
    #strs = simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    strs = simp_passive_sent(tokens, node_list)

    return strs

def main():

    sent = "Peter was hit by a bus."
    #sent = "An apple was eaten by Peter."
    #sent = "The work was done by her."
    #sent = "They was hit by the bus."
    sent = "The work was done by them."
    sent = "Peter is blamed by them."
    #sent = "Peter was refreshed ."
    #sent = "Peter is being blamed by him."
    #sent = "Peter  was also called Pete  ."
    #sent = "It is situated on the banks of river ghaghra  ."
    #sent = "Food is procured with its suckers  . "
    #print(simp_coordi_sent(sent))
    #sent = "He was born at Plessiel , a hamlet of Drucat near Abbeville , to a long-established family of Picardy , the great-nephew of the painter Eustache Le Sueur ."
    #sent = "The paper was written by Mr. Smith ."
    #sent = "the recent bad issues were brought by Peter."
    #sent = "The books were given to John by Peter ."
    sent = "He was  frightened by the sound ."
    print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
