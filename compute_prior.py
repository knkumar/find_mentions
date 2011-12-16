#L645 Final Project
#2 things - separate out verb coreference and noun phrases with coreference
#this file - noun phrases with corteference
import re
import pickle

prior = "prior.txt"

          
def main():
   fpos = open(prior,"rb")
   fpout = open("prior_prob.txt","wb")
   pos_total = 0
   for line in fpos.readlines():
      cols = line.split()
      pos_total = pos_total+float(cols[1])
      print pos_total
   fpos.close()
   fpos = open(prior,"rb")
   for line in fpos.readlines():
      cols = line.split()
      fpout.write("%s\t%s\n"%(cols[0],float(cols[1])/pos_total))   
   fpout.close()
   fpos.close()
if __name__ == "__main__":
   main()
