#L645 Final Project
#Nov 28 2011
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
"""['concern climbing
Everest has become too common , and perhaps abit too commercial
','(NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))',10]"""
import re

class mention_frame:
   def __init__(self, number, sent, pos, bracket, nps_finder):
      self.sent_number = number
      self.sent = sent
      self.pos_tags = pos
      self.bracket = bracket
      self.nps = nps_finder

   def get_nps(self):
      ret_nps = {}
      def insert_nps(key, val):
         ret_nps[key] = val
      map(lambda key: insert_nps(key,map(lambda x,y,z: [x,x+y,z], self.nps[key][0],self.nps[key][1],self.nps[key][2])), self.nps.keys())
      return ret_nps

   def get_sent(self,start,end):
      return ' '.join(self.sent[start:end])

def Smaller_NPs(NP,flag):
   recur_level_NP = 0
   def find_small_np(brackets):
      if not (re.search("\(NP",NP[1]) if flag=='np' else re.search("\(",NP[1])):
         return
      else:
         all_nps = re.findall('\(NP*',NP[1]) if flag=='np' else re.findall('\(*',NP[1])
   nps = NP[1].index('(NP') if flag==np else NP[1].index('(')
   stars = NP[1].find('*')
   print NP[1].find('*',stars)
   all_nps = re.search('\(NP',NP[1]) if flag=='np' else re.search('\(',NP[1])

def find_rindex(sent, begin, stop, i, number):
   if i >= number or stop > len(sent)-1:
      return stop
   pos = sent.find(')',stop+1)
   n_add = abs(number - sent.count('(',begin,pos))
   return find_rindex(sent, begin, pos, sent.count(')',begin,pos+1)-1, number+n_add)

def count_stars(sent,start,end):
   num_stars = sent.count('*')
   stars_before = sent.count('*',0,start)
   stars_after = sent.count('*',end,len(sent)) if end!=None else 0
   return stars_before, num_stars-(stars_before+stars_after)

def search_tag(sent,search_tag):
   num_np = sent.count('%s'%search_tag) 
   ret_nps = [[],[],[]]
   start = sent.find('%s'%search_tag) 
   for i in range(num_np):
      if start == -1:
         return None,None,None
      temp_end = sent.find(')',start) #first closing bracket
      end = find_rindex(sent,start+1,temp_end,0,sent.count('(',start+1,temp_end))
      end+=1
      words,span = count_stars(sent,start,end)
      ret_nps[0].append(words)
      ret_nps[1].append(span)
      ret_nps[2].append(sent[start:end])
      start = sent.find('%s'%search_tag,start+1) 
   return ret_nps #contains [[#words_before],[#span],[diff_nps(largest_to_smallest]] per sentence

def insert_tokens(sent_feat,token, num):
   if num in sent_feat.keys():
      temp  = sent_feat[num]
      temp.append(token)
      sent_feat[num] = temp
   else:
      sent_feat[num] = [token]
   return sent_feat

def extract_features(sent_features, tokens):
   sent_features = insert_tokens(sent_features, tokens[3], 3)
   sent_features = insert_tokens(sent_features, tokens[4], 4)
   sent_features = insert_tokens(sent_features, tokens[5], 5)
   if len(tokens) > 12:
      for i in range(12,len(tokens)-1):
         sent_features = insert_tokens(sent_features, tokens[i], i)
   coref_col = len(tokens)-1
   sent_features = insert_tokens(sent_features, tokens[coref_col], coref_col)
   return sent_features

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
          for key in sent_features.keys():
             if key == 5:
                ret_nps[5] = search_tag(''.join(sent_features[5]),"(NP")
             else:
                ret_nps[key] = search_tag(''.join(sent_features[key]),"(")
          sent_dict[sent_num] = mention_frame(sent_num,sent_features[3],sent_features[4],sent_features[5],ret_nps)
          nps = sent_dict[sent_num].get_nps()
          for key in nps.keys():
             for np in nps[key]:
                print np[0],np[1]
                print sent_dict[sent_num].get_sent(np[0],np[1])
                print ''.join(np[2])
          sent_num += 1
          sent_features = {}
          
def main():
   #"""
   data = open("../conll_st_Data/train/en_train_dev_gold.txt")
   lines = iter(data.readlines())
   sent_features = ['','','']
   lines.next()
   parse_sentences(lines)
   """
   test = "(NP(NP**)**)(VP*(ADJP*(PP*(NP***))))*"
   ret_np = get_nps(test,"NP")
   print ret_np
   #"""

if __name__ == "__main__":
   main()
