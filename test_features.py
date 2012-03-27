#L645 Final Project
#Nov 28 2011

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
   pos = sent_dict[key].pos_tags
   sent = sent_dict[key].sent
   return nps,sent


def insert(cluster, key, tab):
   if key in cluster.keys():
      temp = cluster[key]
      temp.append(tab)
      cluster[key] = temp
   else:
      cluster[key] = [tab]
   return cluster

def find_classes(np_list, npkey, pos_cluster, neg_cluster,prior,mention):
   # mentions = {sent_no: [[start,end],....]}
   for np in np_list:
      pos_prob = 1.0
      neg_prob = 1.0
      bracket = ''.join(np[2].split('*'))
      if bracket in pos_cluster.keys():
         pos_prob = pos_prob*float(pos_cluster[bracket])
      if bracket in neg_cluster.keys():
         neg_prob = neg_prob*float(neg_cluster[bracket])
      pos_prob = pos_prob*prior
      neg_prob = neg_prob*(1-prior)
      if pos_prob >= neg_prob:
         mention = insert(mention,npkey,[np[0],np[1]])
   return mention

def add_named_entities(np_list, npkey, mention):
   for np in np_list:
      mention = insert(mention,npkey,[np[0],np[1]])
   return mention
   

def find_nice_features(pos, neg, prior, sent_dict):
   mention_span = {}
   for skey in sent_dict.keys():
      mention = {}
      nps,sent = get_data(sent_dict,skey)
      for npkey in nps.keys():
         if npkey == "PRN":
            continue
         np_list = map(lambda x,y,z: [x,x+y,z], nps[npkey][0],nps[npkey][1],nps[npkey][2])
         if npkey == 11:
            mention_span[skey] = add_named_entities(np_list, npkey, mention)
         else:
            mention_span[skey] = find_classes(np_list, npkey, pos,neg, prior, mention)
   return mention_span

def load(fname):
   ld = {}
   f = open(fname,'rb')
   for l in f.readlines():
      cols = l.split()
      ld[cols[0]] = cols[1]
   return ld

def copy_back(cluster,sent_dict, fname):
   f = open(fname, 'wb')
   for key in cluster.keys():
      s = sent_dict[key].sent
      f.write('\n++++++%s++++++\n'%sent_dict[key].sent_number)
      f.write(' '.join(s)+"\n")
      for npkey in cluster[key].keys():
         for item in cluster[key][npkey]:
            if item[0] == item[1]:
               f.write('%s\t%s|%s\n'%(' '.join( s[ int(item[0]) : int(item[1])+1 ] ), item[0], item[1] ))
            else:
               f.write('%s\t%s|%s\n'%(' '.join( s[ int(item[0]) : int(item[1]) ] ), item[0], item[1] ))
   f.close()

def main():
   #"""
   sent_out = open("test_dict.pkl","rb")
   pfile = open('prior.txt')
   pos = load('posterior_pos.txt')
   neg = load('posterior_neg.txt')
   prior = float(pfile.readline())
   sent_dict = pickle.load(sent_out)
   mention_span = find_nice_features(pos,neg,prior,sent_dict)
   #mention_span = {sent_num : {col_num : [[start],[end][]}}
   final_out = open("result.pkl","wb")
   pickle.dump(mention_span,final_out)
   copy_back(mention_span,sent_dict,'mention_test_with_prior.txt')

if __name__ == "__main__":
   main()
