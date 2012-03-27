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

def get_data(sent_dict,key):
   nps = sent_dict[key].nps
   keys = map(lambda x: int(x), nps.keys())
   coref = max(keys)
   sent = sent_dict[key].sent
   coref_spans = map(lambda x,y: '%s|%s'%(x,x+y), nps[coref][0],nps[coref][1])
   return nps, coref,sent, coref_spans


def insert(cluster, key):
   key = ''.join(key.split('*'))
   if key in cluster.keys():
      cluster[key] = cluster[key]+1
   else:
      cluster[key] = 1
   return cluster

def make_classes(np_list, coref, coref_spans, npkey, pos_cluster, neg_cluster):
   # np_list = [start,end,bracket_list]
   for np in np_list:
      if not np:
         continue
      if npkey != coref:
         bracket = '%s'%(''.join(np[2])) # bracket string
         if '%s|%s'%(np[0],np[1]) in coref_spans:
            pos_cluster = insert(pos_cluster,bracket)
         else:
            neg_cluster = insert(neg_cluster,bracket)            
   return pos_cluster,neg_cluster

def find_nice_features(sent_dict):
   pos_cluster = {}
   neg_cluster = {}
   #named_entity = {}
   for key in sent_dict.keys():
      #cannot consider features to be independent
      nps,coref,sent,coref_spans = get_data(sent_dict,key)
      #print '%s:'%coref
      for npkey in nps.keys():
         if npkey == "PRN":
            continue
         # key:[words, span, brackets]
         np_list = map(lambda x,y,z: [x,x+y,z], nps[npkey][0],nps[npkey][1],nps[npkey][2])
         pos_cluster, neg_cluster = make_classes(np_list, coref, coref_spans, npkey, pos_cluster,neg_cluster)
   return pos_cluster, neg_cluster

def copy_back(cluster, fname):
   f = open(fname, 'w')
   for key in cluster.keys():
      f.write('%s\t%s\n'%(key,cluster[key]))
   f.close()
          
def main():
   #"""
   sent_out = open("sent_dict.pkl","rb")
   sent_dict = pickle.load(sent_out)
   pos,neg = find_nice_features(sent_dict)
   copy_back(pos,'pos.txt')
   copy_back(neg,'neg.txt')

if __name__ == "__main__":
   main()
