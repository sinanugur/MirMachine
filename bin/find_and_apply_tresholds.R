#!/usr/bin/Rscript


require(tidyverse)

#compiled_results_table=read.csv("analyses/results/predictions/tables/compiled_results_per_species_per_mirna.tsv",header = T,sep = "\t",stringsAsFactors = F) %>% dplyr::select(-species) %>% dplyr::rename(species=node)
compiled_results_table=read.csv("analyses/results/predictions/tables/compiled_results_per_species_per_mirna.tsv",header = T,sep = "\t",stringsAsFactors = F) 

mirna_cutoffs_df =read_tsv("analyses/results/predictions/mirmachine_trusted_cutoffs.tsv") %>% distinct(mirna,trusted)



write_tsv(compiled_results_table %>%  left_join(mirna_cutoffs_df %>% distinct(mirna,trusted)) %>% filter(bitscore >=trusted),"analyses/results/predictions/tables/filtered_compiled_results_per_species_per_mirna.tsv")


write_tsv(compiled_results_table %>%  left_join(mirna_cutoffs_df %>% distinct(mirna,trusted)) %>%
            filter(bitscore >=trusted) %>% 
            dplyr::count(species,mirna) %>% spread(species,n),"analyses/results/predictions/tables/mirna_species_hits.tsv")
