#L645 Final Project
#Nov 28 2011
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
"""['concern climbing
Everest has become too common , and perhaps abit too commercial
','(NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))',10]"""
import re
import pickle
import types

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

def make_span(sent,pos,nps):
   max_span = 0
   for key in nps.keys():
      np_list = map(lambda x,y,z: [x,x+y,z], nps[key][0],nps[key][1],nps[key][2])
      if len(np_list) > max_span:
         max_span = len(np_list)
   return max_span

def check_nps(sent, pos, nps):
   return make_span(sent,pos,nps)
                        
def find_mentions(sent_dict):
   all_spans = {}
   coref_spans = {}
   for key in sent_dict.keys(): # for every sentence
      nps = sent_dict[key].nps
      sent = sent_dict[key].sent
      pos = sent_dict[key].pos_tags
      all_spans[key] = check_nps(sent, pos, nps)
      coref = max(nps.keys())
      coref_span = map(lambda x,y: '%s|%s'%(x,x+y), nps[coref][0], nps[coref][1])
      coref_spans[key] = len(coref_span)
   return all_spans, coref_spans

def copy_back(all_pos,coref_pos, fname):
   f = open(fname, 'w')
   total = 0
   coref = 0
   for key in all_pos.keys():
      total += all_pos[key]
   for key in coref_pos.keys():
      coref += coref_pos[key]
   f.write("%s"%(float(coref)/total))
   f.close()
          
def main():
   #"""
   sent_out = open("test_dict.pkl","rb")
   sent_dict = pickle.load(sent_out)
   #print sent_dict[sent_dict.keys()[100]].nps
   all_pos, coref_pos = find_mentions(sent_dict)
   copy_back(all_pos,coref_pos,'prior.txt')

if __name__ == "__main__":
   main()
