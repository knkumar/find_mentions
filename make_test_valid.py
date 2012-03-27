#L645 Final Project
#Dec 24 2011
#This file writes the "test file" with the mention/coref information as input to the scorer

# The way we do this is to mark every start with (0 and every end with 0)
# if there are more than 2 coref-spans starting on the same word, then the longer span start first followed by | - (0|(0 and end with 0) or 0)|0)

import re
import pickle
import numpy as np

out = open("../conll_st_Data/test/final_test.txt","wb")

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
   for i in range(len(tokens)):
      sent_features = insert_tokens(sent_features, tokens[i], i)
   return sent_features

def flatten_spans(mention_spans,num):
   spans = []
   for key in mention_spans[num].keys():
      for item in mention_spans[num][key]:
         if item[0] == item[1]:
            spans.append([ item[0], item[1]])
         else:
            spans.append([ item[0], item[1] ])
   return spans

def mark_spans(sent_features, span, coref):
   start = sent_features[coref][span[0]]
   try:
      end = sent_features[coref][span[1]]
   except:
      span[1] = span[1]-1
      end = sent_features[coref][span[1]]
   if start==end:
      if start == '-':
         sent_features[coref][span[0]] = '(0)'
      elif re.match(".*0\)",start):
         sent_features[coref][span[0]] = start+'(0)'
      else:
         sent_features[coref][span[0]] = start+'|(0)'
   else:
      if start == '-':
         sent_features[coref][span[0]] = '(0'
      elif re.match(".*0\)",start):
         sent_features[coref][span[0]] = start+'(0'
      else:
         sent_features[coref][span[0]] = start+'|(0'
      if end == '-':
         sent_features[coref][span[1]] = '0)'
      elif re.match("\(0.*",end):
         sent_features[coref][span[1]] = '0)'+end
      else:
         sent_features[coref][span[1]] = '0)|'+end
   return sent_features[coref]

def mark_all_spans(sent_features, mention_spans, singleton_span, num):
   coref = max(sent_features.keys())
   spans = flatten_spans(mention_spans,num)
   for span in spans:
      sent_features[coref] = mark_spans(sent_features, span, coref)
   return sent_features

def write_back(sent_features):
   #print sent_features
   line = {}
   values = np.array(sent_features.values())
   for i in range(len(sent_features.values()[0])):
      out.write('   '.join(values[:,i])+"\n")
   out.write("\n")

def mark_coref(lines, mention_span, singleton_span):
   # need a dict for every line in the input, enter the coref_column according to the spans for the sent_num in mention_span
   sent_features = {}
   sent_num = 0
   for line in lines:
      #for every line in input
       tokens = line.strip().split()
       #get all the columns for that word
       if len(tokens) !=0:
          if len(tokens) < 12:
             # if this is a new sentence
             ## write this as it is :)
             out.write(line)
             sent_features = {}
             continue
          sent_features = extract_features(sent_features,tokens)
          # first mark all endings
          # if coref_column has - insert (0 --- if coref_column has (0 insert |(0
       else:
          sent_features = mark_all_spans(sent_features, mention_span, singleton_span, sent_num)
          write_back(sent_features)
          sent_num += 1
          sent_features = {}

          
def main():
   #"""
   data = open("../conll_st_Data/test/en.finalCoNLL_test.txt","rb")
   mention_span = pickle.load(open("result.pkl","rb"))
   singleton_span = pickle.load(open("singleton.pkl","rb"))
   lines = iter(data.readlines())
   sent_features = ['','','']
   lines.next()
   mark_coref(lines,mention_span,singleton_span) # contains parses for all the sentences
   #sent_num : {column_no : [[words],[spans],[nps|args]]}
   #pickle.dump(sent_dict,sent_out)
   data.close()
   """
   test = "(NP(NP**)**)(VP*(ADJP*(PP*(NP***))))*"
   ret_np = get_nps(test,"NP")
   print ret_np
   #"""

if __name__ == "__main__":
   main()