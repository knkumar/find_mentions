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
   coref = max(nps.keys())
   sent = sent_dict[key].sent
   coref_spans = map(lambda x,y: '%s|%s'%(x,x+y), nps[coref][0],nps[coref][1])
   return nps, coref,sent, coref_spans


def insert(cluster, key):
   if key in cluster.keys():
      cluster[key] = cluster[key]+1
   else:
      cluster[key] = 1
   return cluster

def make_classes(np_list, coref, coref_spans, npkey, prior_cluster):
   # np_list = [start,end,bracket_list]
   for np in np_list:
      if not np:
         continue
      if npkey != coref:
         bracket = '%s'%(''.join(np[2])) # bracket string
         prior_cluster = insert(prior_cluster,bracket)
   return prior_cluster

def find_nice_features(sent_dict):
   prior_cluster = {}
   #named_entity = {}
   for key in sent_dict.keys():
      #cannot consider features to be independent
      nps,coref,sent,coref_spans = get_data(sent_dict,key)
      for npkey in nps.keys():
         if npkey == "PRN":
            continue
         # key:[words, span, brackets]
         np_list = map(lambda x,y,z: [x,x+y,z], nps[npkey][0],nps[npkey][1],nps[npkey][2])
         prior_cluster = make_classes(np_list, coref, coref_spans, npkey, prior_cluster)
   return prior_cluster

def copy_back(cluster, fname):
   f = open(fname, 'w')
   for key in cluster.keys():
      f.write('%s\t%s\n'%(key,cluster[key]))
   f.close()
          
def main():
   #"""
   sent_out = open("sent_dict.pkl","rb")
   sent_dict = pickle.load(sent_out)
   print sent_dict[sent_dict.keys()[100]].nps
   prior = find_nice_features(sent_dict)
   copy_back(prior,'prior.txt')

if __name__ == "__main__":
   main()