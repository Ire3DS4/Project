from abc import ABC, abstractmethod
import pandas as pd


df1 = pd.read_csv('disease_evidences.tsv', delimiter="\t")
df2 = pd.read_csv('gene_evidences.tsv', delimiter="\t")


#2.1
class Metadata:
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2
        
    def numMetadata(self):
        l1 = list(self.__data1.shape)
        l2 = list(self.__data2.shape)
        return l1 + l2

#2.2
class Semantics:
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2
        
    def columLabel(self):
        label1 = list(self.__data1.columns)
        label2 = list(self.__data2.columns)
        return [label1, label2]



class Record(ABC):
    @abstractmethod
    def __init__(self):
        pass
        
    @abstractmethod
    def detection(self):
        pass

#2.3
class Genes(Record):
    def __init__(self, data2):
        self.__data2 = data2
        
    def detection(self):
        l = []
        data2_group = self.__data2.groupby(by='geneid')
        for num in data2_group:
            l.append(num[0])
            
        return l

#2.5
class Disease(Record):
    def __init__(self, data1):
        self.__data1 = data1
            
    def detection(self):
        l = []
        data1_groups = self.__data1.groupby(by='diseaseid')
        for group in data1_groups:
            l.append(group[0])
        
        return l



class Sentences(ABC):
    @abstractmethod
    def __init__(self):
        pass
     
    @abstractmethod
    def listSentences(self):
        pass



#2.4
class GeneCovid(Sentences):
    def __init__(self, geneid, list_id, data2):
       self.__data2 = data2
       self.__geneid = geneid
       self.__list_id = list_id
       
    def listSentences(self):
        listSent2 = []
        d1 = self.__data2['geneid']
        d2 = self.__data2['sentence']

        if self.__geneid not in self.__list_id:
            return f"The gene ID{self.__geneid} is not present in the dataset."
        else:
            iden = []
            
            for i in range(len(d1)):
                if d1[i] == self.__geneid:
                    iden.append(i)
            for i in range(len(iden)):
                s = d2[i]
                if "<span class='disease covid cdisease'" or "<span class='disease covid cvirus'" in s:
                    listSent2.append(s)
                   
            if len(listSent2) == 0:
                return f"There is no covid related evidence about the gene ID{self.__geneid}"
            else:
                return listSent2

#2.6
class DiseaseCovid(Sentences):
    def __init__(self, diseaseid, list_id, data1):
       self.__data1 = data1
       self.__diseaseid = diseaseid
       self.__list_id = list_id
       
    def listSentences(self):
        listSent1 = []
        d1 = self.__data1['diseaseid']
        d2 = self.__data1['sentence']

        if self.__diseaseid not in self.__list_id:
            return f"The disease ID{self.__diseaseid} is not present in the dataset."
        else:
            iden = []
            
            for i in range(len(d1)):
                if d1[i] == self.__diseaseid:
                    iden.append(i)
            for i in range(len(iden)):
                s = d2[i]
                if "<span class='disease covid cdisease'" in s:
                    listSent1.append(s)
                    
            if len(listSent1) == 0:
                return f"There is no covid related evidence of the input disease ID{self.__diseaseid}"
            else:
                return listSent1

#2.7
class Top10:
    def __init__(self, data1, data2):
        self.__data1 = df1
        self.__data2 = df2
        
    def record_association(self):
        pmid_disease = self.__data1['pmid']                         
        pmid_gene = [p for p in self.__data2['pmid']]
        d = dict()
        diseaseid = self.__data1['diseaseid']
        geneid = self.__data2['geneid']
        
        for i in range(len(pmid_gene)):    
            for j in range(len(pmid_disease)):
                if pmid_gene[i] == pmid_disease[j]:
                    key_name = (geneid[i], diseaseid[j])
                    
                    if key_name not in d.keys():
                        d[key_name] = 1
                    else:
                        d[key_name] += 1
                        
        sorted_d = sorted(d.items(), key=lambda kv: kv[1])
        top10 = list(sorted_d)[:-11:-1]

        return top10



class Associated(ABC):  # The abstract class points 8 and 9 are based on
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def associate(self, id):
        pass

#2.8
class AssociatedDiseases(Associated):  # both databases are needed in this case. Linked through pmids.
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2

    def associate(self, id):
        
        pmids = []
        for el in range(len(self.__data2)):  # save all relevant pmids based on user input
            if (id == self.__data2.loc[el, 'geneid']) or (id in self.__data2.loc[el, 'gene_symbol']):
                pmids.append(self.__data2.loc[el, 'pmid'])

        diseases = []
        for el in range(len(self.__data1)):  # switch database and save all diseases linked to saved pmids
            if (self.__data1.loc[el, 'pmid'] in pmids) and (self.__data1.loc[el, 'disease_name'] not in diseases):
                diseases.append(self.__data1.loc[el, 'disease_name'])  # avoid repetition of dame element

        return diseases

#2.9
class AssociatedGenes(Associated):
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2

    def associate(self, id):  # same as before, with the other database
        
        pmids = []
        for el in range(len(self.__data1)):
            if (id == self.__data1.loc[el, 'diseaseid']) or (id in self.__data1.loc[el, 'disease_name']):
                pmids.append(self.__data1.loc[el, 'pmid'])
        
        genes = []
        for el in range(len(self.__data2)):
            if (self.__data2.loc[el, 'pmid'] in pmids) and (self.__data2.loc[el, 'gene_symbol'] not in genes):
                genes.append(self.__data2.loc[el, 'gene_symbol'])

        return genes