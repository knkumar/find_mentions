#L645 Final Project
#Nov 28 2011
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
"""['concern climbing
Everest has become too common , and perhaps abit too commercial
','(NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))',10]"""
import re
import pickle

TRAIN = False

if TRAIN:
   data = open("../conll_st_Data/train/en_train_dev_gold.txt","rb")
   sent_out = open("sent_dict.pkl","wb")
else:
   data = open("../conll_st_Data/test/en.finalCoNLL_test.txt","rb")
   sent_out = open("test_dict.pkl","wb")

class mention_frame:
   def __init__(self, number, sent, pos, bracket, nps_finder):
      self.sent_number = number
      self.sent = sent
      self.pos_tags = pos
      self.bracket = bracket
      self.nps = nps_finder

   def get_nps(self):
      ret_np = {}
      def insert_nps(key, val):
         ret_np[key] = val
      map(lambda key: insert_nps(key,map(lambda x,y,z: [x,x+y,z], self.nps[key][0],self.nps[key][1],self.nps[key][2])), self.nps.keys())
      return ret_np

   def get_sent(self,start,end):
      return ' '.join(self.sent[start:end])

   def get_sent_full(self):
      return ' '.join(self.sent)

#find the closing brackets for the curernt tag
def find_rindex(sent, begin, stop, i, number):
   if i >= number or stop > len(sent)-1:
      return stop
   pos = sent.find(')',stop+1)
   n_add = abs(number - sent.count('(',begin,pos))
   return find_rindex(sent, begin, pos, sent.count(')',begin,pos+1)-1, number+n_add)

#count the stars between the bracket = count the number of words spanned
def count_stars(sent,start,end,tag):
   num_stars = sent.count('%s'%tag)
   stars_before = sent.count('%s'%tag,0,start)
   stars_after = sent.count('%s'%tag,end,len(sent)) if end!=None else 0
   return stars_before, num_stars-(stars_before+stars_after)

#the search tag holder - returns a list of nps
def search_tag(sent,search_tag,count_tag):
   num_np = sent.count('%s'%search_tag) 
   ret_nps = [[],[],[]]
   start = sent.find('%s'%search_tag) 
   for i in range(num_np):
      if start == -1:
         return None,None,None
      temp_end = sent.find(')',start) #first closing bracket
      end = find_rindex(sent,start+1,temp_end,0,sent.count('(',start+1,temp_end))
      end+=1
      words,span = count_stars(sent,start,end,'%s'%count_tag)
      ret_nps[0].append(words)
      ret_nps[1].append(span)
      ret_nps[2].append(sent[start:end])
      start = sent.find('%s'%search_tag,start+1) 
   return ret_nps #contains [[#words_before],[#span],[diff_nps(largest_to_smallest)] per sentence

#insert the tokens into the dictionary
def insert_tokens(sent_feat,token, num):
   if num in sent_feat.keys():
      temp  = sent_feat[num]
      temp.append(token)
      sent_feat[num] = temp
   else:
      sent_feat[num] = [token]
   return sent_feat

#extract interesting features from the data
def extract_features(sent_features, tokens):
   sent_features = insert_tokens(sent_features, tokens[3], 3)
   sent_features = insert_tokens(sent_features, tokens[4], 4)
   sent_features = insert_tokens(sent_features, tokens[5], 5)
   sent_features = insert_tokens(sent_features, tokens[10], 10)
   if len(tokens) > 10:
      for i in range(11,len(tokens)-1):
         sent_features = insert_tokens(sent_features, tokens[i], i)
   coref_col = len(tokens)-1
   sent_features = insert_tokens(sent_features, tokens[coref_col], coref_col)
   return sent_features

def display_nps(sent_dict):
   f = open("nps.txt","a")
   nps = sent_dict.get_nps()
   f.write("\n+++++%s+++++\n"%(sent_dict.sent_number))
   f.write(sent_dict.get_sent_full())
   for key in nps.keys():
      for np in nps[key]:
         f.write('\n%s|%s\t'%(np[0],np[1]))
         f.write(''.join(np[2]))
   f.write('\n')
   f.close()

#parse every sentence and add it to the object dict
def parse_sentences(lines):
   sent_features = {}
   sent_dict = {}
   ret_nps = {}
   sent_num = 0
   for line in lines:
       tokens = line.strip().split()
       if len(tokens) !=0:
          if len(tokens) < 12:
             sent_features = {}
             continue
          sent_features = extract_features(sent_features,tokens)
       else:
          co_ref = max(sent_features.keys())
          for key in sent_features.keys():
             if key < 4:
                continue
             elif key == 5 or key == 10:
                ret_nps[5] = search_tag(''.join(sent_features[5]),"(","*")
                #ret_nps['prn'] = search_tag(''.join(sent_features[5]),"(PRN","*")
                ret_nps[10] = search_tag(''.join(sent_features[10]),"(","*")
             elif key == co_ref:
                ret_nps[key] = search_tag(''.join(sent_features[key]),"(","-")
             else:
                ret_nps[key] = search_tag(''.join(sent_features[key]),"(","*")
          sent_dict[sent_num] = mention_frame(sent_num,sent_features[3],sent_features[4],sent_features[5],ret_nps)
          display_nps(sent_dict[sent_num])
          sent_num += 1
          sent_features = {}
          ret_nps={}
   return sent_dict

          
def main():
   #"""
   lines = iter(data.readlines())
   sent_features = ['','','']
   lines.next()
   sent_dict = parse_sentences(lines) # contains parses for all the sentences
   #sent_num : {column_no : [[words],[spans],[nps|args]]}
   print sent_dict[64]
   pickle.dump(sent_dict,sent_out)
   data.close()
   sent_out.close()
   """
   test = "(NP(NP**)**)(VP*(ADJP*(PP*(NP***))))*"
   ret_np = get_nps(test,"NP")
   print ret_np
   #"""

if __name__ == "__main__":
   main()
