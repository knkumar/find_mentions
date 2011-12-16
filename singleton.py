#L645 Final Project
#Nov 28 2011
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
"""['concern climbing
Everest has become too common , and perhaps abit too commercial
','(NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))',10]"""
import re
import pickle

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

# all checks returns 1 is true (include) 0 is false (exclude)
def pos_rules_check(pos_tags):
   # input is a list of pos tags spanning the bracketing - add checks to include or exclude
   # eg: ['NP','N','VP']
   for pos_tag in pos_tags:
      pass
   return 1

def word_rules_check(words):
   # input is a list of words - check which to include or exclude
   # eg: ['the','man','is','blue']
   for word in words:
      pass
   return 1

def nps_rules_check(bracket_string,prn):
   # input is a bracket string 
   # eg: (NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))
   # search for relevant features and return 0(exclude) or 1(include)
   argm_dis = re.find_iter('ARGM-DIS',bracket_string)
   prn = re.finditer('PRN',bracket_string)
   if bracket_string.find('(ADVP**)') != -1 or bracket_string.find('(VP (PP*(NP**))'):
      pass
                        
def find_singletons(sent_dict):
   pos_cluster = []
   neg_cluster = []
   for key in sent_dict.keys():
      nps = sent_dict[key].nps
      sent = sent_dict[key].sent
      pos = sent_dict[key].pos
      coref = max(nps.keys())
      coref_spans = map(lambda x,y: '%s|%s'%(x,x+y), nps[coref][0],nps[coref][1])
      for npkey in nps.keys():
         # key:[words, span, brackets]
         np_list = map(lambda x,y,z: [x,x+y,z], nps[npkey][0],nps[npkey][1],nps[npkey][2])
         for np in np_list:
            bracket = ''.join(np['np'])
            prn = ''.join(np['prn'])
            if pos_rules_check(pos[np[0]:np[1]]) or word_rules_check(sent[np[0]:np[1]]) or nps_rules_check(bracket,prn):
               if '%s|%s'%(np[0],np[1]) in coref_spans:
                  neg_cluster.append(bracket)           
               else:
                  pos_cluster.append(bracket)            
   return pos_cluster, neg_cluster

def copy_back(cluster, fname):
   f = open(fname, 'w')
   for item in cluster:
      f.write('%s\n'%item)
   f.close()
          
def main():
   #"""
   sent_out = open("sent_dict.pkl","rb")
   sent_dict = pickle.load(sent_out)
   print sent_dict[sent_dict.keys()[100]].nps
   pos,neg = find_singletons(sent_dict)
   copy_back(pos,'pos_single.txt')
   copy_back(neg,'neg_single.txt')

if __name__ == "__main__":
   main()
