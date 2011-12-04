#L645 Final Project
#Nov 28 2011
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
"""['concern climbing
Everest has become too common , and perhaps abit too commercial
','(NP*(SBAR(S(S(VP*(NP*)))(VP*(VP*(ADJP(ADJP**)**(ADVP*)(ADJP(ADVP(NP**)*)*))))))))',10]"""
import re

def Smaller_NPs(NP):
   recur_level_NP = 0
   print NP[0]
   print NP[1]
   def find_small_np(brackets):
      if not (re.search("\(NP",NP[1])):
         return
      else:
         all_nps = re.findall('\(NP*',NP[1])
   nps = NP[1].index('(NP')
   stars = NP[1].find('*')
   stars
   print NP[1].find('*',stars)
   all_nps = re.search('\(NP',NP[1])

def find_rindex(sent, begin, stop, i, number):
   if i >= number or stop >= len(sent):
      return stop
   pos = sent.find(')',stop+1)
   n_add = abs(number - sent.count('(',begin,pos))
   #print sent[stop:pos]
   return find_rindex(sent, begin, pos, sent.count(')',begin,pos)-1, number+n_add)

def count_stars(sent,start,end):
   num_stars = sent.count('*')
   stars_before = sent.count('*',0,start)
   stars_after = sent.count('*',end,len(sent)) if end!=None else 0
   return stars_before, num_stars-(stars_before+stars_after)

def get_nps(sent):
   num_np = sent.count('(NP')
   ret_nps = [[],[],[]]
   start = sent.find('(NP')
   for i in range(num_np):
      if start == -1:
         return None,None,None
      temp_end = sent.find(')',start) #first closing bracket
      end = find_rindex(sent,start+1,temp_end,0,sent.count('(',start+1,temp_end))
      if end == temp_end: end+=1
      words,span = count_stars(sent,start,end)
      ret_nps[0].append(words)
      ret_nps[1].append(span)
      ret_nps[2].append(sent[start:end])
      start = sent.find('(NP',start+1)
   return ret_nps #contains [[#words_before],[#span],[diff_nps(largest_to_smallest]] per sentence
   
def parse_sentences(lines):
   sent_features = [[],[],[]]
   for line in lines:
       tokens = line.strip().split()
       if len(tokens) !=0:
          if len(tokens) < 10:
             sent_features = [[],[],[]]
             continue
          tokens[2]
          sent_features[0].append(tokens[3]+' ')
          sent_features[1].append(tokens[4]+' ')
          sent_features[2].append(tokens[5])
       else:
          ret_nps = get_nps(''.join(sent_features[2]))
          print ''.join(sent_features[0])
          print ''.join(sent_features[1])
          print ''.join(sent_features[2])
          for np in ret_nps[2]:
             print np
          sent_features = [[],[],[]]
          
def main():
   data = open("conll_st_Data/train/en_train_dev_gold.txt")
   lines = iter(data.readlines())
   sent_features = ['','','']
   lines.next()
   parse_sentences(lines)
   #test = "(TOP(NP(NP(NP***)(PP*(NP(NP***)(PP*(NP*)))))*(NP(NP**)(PP*(NP**)))))"
   #start,nwords,np = get_nps(test)
   #print start,nwords,np

if __name__ == "__main__":
   main()
