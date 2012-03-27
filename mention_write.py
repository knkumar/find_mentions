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

def find_index(string, tag):
   try:
      ind = string.index(tag)
   except:
      return None
   return ['%s|%s'%(ind,ind+1)]

def find_single_spans(nps, tag):
   spans = []
   np_list = map(lambda x,y,z: [x,x+y,z], nps[0],nps[1],nps[2])
   for np_item in np_list:
      m = re.match(tag,np_item[2])
      if not m or m.span()[0] == -1:
         continue
      spans.append('%s|%s'%(np_item[0],np_item[1]))
   return spans

def find_spans(nps,tag):
   spans = [] # [[start,end]...]
   for npkey in nps.keys():
       np_list = map(lambda x,y,z: [x,x+y,z], nps[npkey][0],nps[npkey][1],nps[npkey][2])
       for np_item in np_list:
          m = re.match(tag,np_item[2])
          if not m or m.span()[0] == -1:
             continue
          spans.append('%s|%s'%(np_item[0],np_item[1]))
   return spans

def make_union(arg_list):
   return reduce(lambda a,b:a|b ,map(lambda x: set(x), arg_list))

def make_intersection(arg_list):
   return reduce(lambda a,b: a&b , map(lambda x: set(x), arg_list))

def check_in_span(span1,span2):
   #return true if span1 in span2
   start = span1[0]
   end = span1[1]
   for span in span2:
      if span[0] <= start and span[1] >= end:
         return True
   return False
      
def remove_spans(pos,neg,in_out,cc=False):
   #input : ["start|end"...]
   bucket_pos = []
   pos_list = map(lambda x: x.split('|'), pos)
   neg_list = map(lambda x: x.split('|'), neg)
   for pitem in pos_list:
      if not (check_in_span(pitem,neg_list) if in_out == 'in' else check_in_span(neg_list[0],[pitem])):
         if cc:
            if int(pitem[1])-int(pitem[0]) == 1:
               bucket_pos.append(pitem)
            else:
               bucket_pos.append(pitem)
   return map(lambda x: '%s|%s'%(x[0],x[1]), bucket_pos)

def display_span(cc_spans,how_spans,also_spans,so_spans,pos_argmdis_spans,pos_argmadv_spans,neg_prn_spans,neg_adjp_spans,pos_np_spans):
   pass
       
def make_span(sent,pos,nps):
   max_span
   for key in nps.keys():
      np_list = map(lambda x,y,z: [x,x+y,z], nps[key][0],nps[key[1],nps[key][2]])
      if len(np_list) > max_span:
         max_span = len(np_list)
   return max_span

def check_nps(sent, pos, nps):
   return make_span(sent,pos,nps)
                        
def find_mentions(sent_dict):
   all_spans = {}
   for key in sent_dict.keys(): # for every sentence
      nps = sent_dict[key].nps
      sent = sent_dict[key].sent
      pos = sent_dict[key].pos_tags
      all_spans[key] = check_nps(sent, pos, nps)
   return all_spans

def copy_back(cluster,sent_dict, fname):
   f = open(fname, 'w')
   for key in cluster.keys():
      f.write('\n++++++++++sentence %s+++++++++++\n'%key)
      sent = sent_dict[key].sent
      sent_w = ' '.join(sent)
      f.write("%s\n"%sent_w)
      for item in cluster[key]:
         cols = item.split('|')
         f.write('%s|%s\t%s\n'%(cols[0], cols[1], ' '.join(sent[int(cols[0]):int(cols[1])]) ))
   f.close()
          
def main():
   #"""
   sent_out = open("test_dict.pkl","rb")
   sent_dict = pickle.load(sent_out)
   #print sent_dict[sent_dict.keys()[100]].nps
   all_pos = find_mentions(sent_dict)
   copy_back(all_pos,sent_dict,'singleton_test.txt')

if __name__ == "__main__":
   main()
