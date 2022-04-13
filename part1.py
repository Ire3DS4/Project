import pandas as pd
from part2 import *  # import all the classes containing operations of Part 2

class CentralRegistry:  # Selects correct method based on user input
    def __init__(self):  # Data Readers & Registry
        self.__data1 = pd.read_csv('disease_evidences.tsv', delimiter="\t")
        self.__data2 = pd.read_csv('gene_evidences.tsv', delimiter="\t")
        self.__operations = ['Numerical metadata',
                             'General semantics',
                             'List of gene IDs',
                             'List of sentences given gene symbol/ID related to COVID-19',
                             'List of diseases',
                             'List of sentences given disease name/ID related to COVID-19',
                             'Top 10 genes-diseases associations',
                             'Disease list given gene symbol/ID',
                             'Gene list given disease name/ID']
        self.__links = ['MD', 'Sem', 'RecG', 'ListGUser', 'RecD', 'ListDUser', 'Top10', 'GtoDUser', 'DtoGUser']

    def returnregistry(self):  # needed for HTML homepage
        return self.__operations

    def returnlinks(self):  # needed for HTML homepage / avoid long names of self.__operations
        return self.__links

    def link_metadata(self):  # 2.1
        return Metadata(self.__data1, self.__data2).numMetadata()

    def link_semantics(self):  # 2.2
        return Semantics(self.__data1, self.__data2).columLabel()

    def link_genes(self):  # 2.3
        return Genes(self.__data2).detection()

    def link_diseases(self):  # 2.5
        return Disease(self.__data1).detection()

    def link_sentence_genes(self):  # 2.4 
        return GeneCovid(self.link_genes(), self.__data2) 

    def link_sentence_diseases(self):  # 2.6 
        return DiseaseCovid(self.link_diseases(), self.__data1)

    def link_top10(self):  # 2.7
        return Top10(self.__data1, self.__data2).record_association()
        
    def link_diseases_from_genes(self):  # 2.8
        return AssociatedDiseases(self.__data1, self.__data2)

    def link_genes_from_diseases(self):  # 2.9
        return AssociatedGenes(self.__data1, self.__data2)