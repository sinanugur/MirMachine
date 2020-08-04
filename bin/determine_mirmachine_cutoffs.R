#!/usr/bin/Rscript


arguments=commandArgs(TRUE)

require(tidyverse)


mirna_tp_fp=read_tsv(arguments[1])

function_cutpointr=function(bitscore,type) {
  
  cutpointr::cutpointr(x=bitscore,class=type,pos_class = "TP",neg_class = "FP",method=maximize_metric,metric= tpr) %>% pull(optimal_cutpoint)
  
}

function_mcc=function(x,data) {
	  
	  
	  TP=data %>% filter(bitscore >= x,type == "TP") %>% nrow()
  FN=data %>% filter(bitscore < x,type == "TP") %>% nrow()
    FP=data %>% filter(bitscore >= x,type == "FP") %>% nrow()
    
    TPR=TP/(TP+FN+1)
      PPV=TP/(TP+FP)
      
      
      sqrt(TPR*PPV)         
        
}

function_find_max=function(data) {
	  
	  data %>% pull(bitscore) -> vector_
   vector_ %>% map(~function_mcc(.,data)) %>% unlist() %>% which.max() -> index_
      
      return(vector_[index_])
     
}


mirna_tp_fp %>% group_by(mirna) %>% mutate(trusted=function_find_max(data=bind_cols(bitscore=bitscore,type=type))) %>% distinct(mirna,trusted) -> mirmachine_trusted_cutoffs

write_tsv(mirmachine_trusted_cutoffs,arguments[2])


