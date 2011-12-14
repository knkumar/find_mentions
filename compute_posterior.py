#L645 Final Project
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
import re
import pickle

pos = "pos.txt"
neg = "neg.txt"
          
def main():
   fpos = open(pos,"rb")
   fneg = open(neg,"rb")
   fpout = open("posterior_pos.txt","wb")
   fnout = open("posterior_neg.txt","wb")
   pos_total = 0
   neg_total = 0
   for line in fpos.readlines():
      cols = line.split()
      pos_total = pos_total+float(cols[1])
      print pos_total
   for line in fneg.readlines():
      cols = line.split()
      neg_total = neg_total+float(cols[1])
   fpos.close()
   fneg.close()
   fpos = open(pos,"rb")
   fneg = open(neg,"rb")
   for line in fpos.readlines():
      cols = line.split()
      fpout.write("%s\t%s\n"%(cols[0],float(cols[1])/pos_total))   
   for line in fneg.readlines():
      cols = line.split()
      fnout.write("%s\t%s\n"%(cols[0],float(cols[1])/neg_total))
   fpout.close()
   fnout.close()
   fpos.close()
   fneg.close()
if __name__ == "__main__":
   main()