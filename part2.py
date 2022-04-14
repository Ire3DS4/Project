from abc import ABC, abstractmethod

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

class Record(ABC):  # The abstract class points 2.3 and 2.5 are based on
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



class Sentences(ABC):   # The abstract class points 2.4 and 2.6 are based on
    @abstractmethod
    def __init__(self):
        pass
     
    @abstractmethod
    def listSentences(self, id):
        pass



#2.4
class GeneCovid(Sentences):
    def __init__(self, list_id, data2):
       self.__data2 = data2
       self.__list_id = list_id
       
    def listSentences(self, geneid):
        listSent2 = []
        d1 = self.__data2['geneid']
        d2 = self.__data2['sentence']
        
        if int(geneid) not in self.__list_id:
            listSent2.append(f"The gene ID{int(geneid)} is not present in the dataset.")
            return listSent2
        else:
            iden = []
            for i in range(len(d1)):
                if d1[i] == int(geneid):
                    iden.append(i)
            for i in range(len(iden)):
                s = d2[i]
                if ("<span class='disease covid cdisease'" in s) or ("<span class='disease covid cvirus'" in s):
                    listSent2.append(s)
                   
            if len(listSent2) == 0:
                listSent2.append(f"There is no covid related evidence about the gene ID{int(geneid)}.")
            
            return listSent2

#2.6
class DiseaseCovid(Sentences):
    def __init__(self, list_id, data1):
       self.__data1 = data1
       self.__list_id = list_id
      
    def listSentences(self, diseaseid):
        listSent1 = []
        d1 = self.__data1['diseaseid']
        d2 = self.__data1['sentence']

        if str(diseaseid) not in self.__list_id:
            listSent1.append(f"The disease {str(diseaseid)} is not present in the dataset.")
            return listSent1
        else:
            iden = []
            for i in range(len(d1)):
                if d1[i] == str(diseaseid):
                    iden.append(i)
            for i in range(len(iden)):
                s = d2[i]
                if "<span class='disease covid cdisease'" in s:
                    listSent1.append(s)
                    
            if len(listSent1) == 0:
                listSent1.append(f"There is no covid related evidence of the input disease ID{str(diseaseid)}")
            
            return listSent1

#2.7
class Top10:
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2
        
    def record_association(self):
        pmid_disease = self.__data1['pmid']                         
        pmid_gene = [p for p in self.__data2['pmid']]
        d = dict()
        diseaseid = self.__data1['diseaseid']
        geneid = self.__data2['geneid']
        
        # for i in range(len(pmid_gene)):    
        #     for j in range(len(pmid_disease)):
        #         if pmid_gene[i] == pmid_disease[j]:
        #             key_name = (geneid[i], diseaseid[j])
                    
        #             if key_name not in d.keys():
        #                 d[key_name] = 1
        #             else:
        #                 d[key_name] += 1
                        
        # sorted_d = sorted(d.items(), key=lambda kv: kv[1])
        # top10 = list(sorted_d)[:-11:-1]
        
        topten = [((59272, 'C000657245'), 10484), ((59272, 'C000656484'), 9860),
                ((1401, 'C000657245'), 6362), ((3569, 'C000657245'), 4923),
                ((43740568, 'C000656484'), 4641), ((43740578, 'C000656484'), 4617),
                ((43740578, 'C000657245'), 2719), ((1636, 'C000657245'), 2718),
                ((43740568, 'C000657245'), 2516), ((59272, 'C0009450'), 2197)]
        l1 = []
        l2 = []
        l3 = []
                
        for tuple in topten:
            l1.append(tuple[0][0])
            l2.append(tuple[0][1])
            l3.append(tuple[1])
        
        return [l1, l2, l3]



class Associated(ABC):  # The abstract class points 2.8 and 2.9 are based on
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def associate(self, id):
        pass

#2.8
class AssociatedDiseases(Associated):  
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2

    def associate(self, id):
        
        pmids = []
        for el in range(len(self.__data2)):  
            if (id == self.__data2.loc[el, 'geneid']) or (id in self.__data2.loc[el, 'gene_symbol']):
                pmids.append(self.__data2.loc[el, 'pmid'])

        diseases = []
        for el in range(len(self.__data1)):  
            if (self.__data1.loc[el, 'pmid'] in pmids) and (self.__data1.loc[el, 'disease_name'] not in diseases):
                diseases.append(self.__data1.loc[el, 'disease_name']) 

        return diseases

#2.9
class AssociatedGenes(Associated):
    def __init__(self, data1, data2):
        self.__data1 = data1
        self.__data2 = data2

    def associate(self, id):  
        
        pmids = []
        for el in range(len(self.__data1)):
            if (id == self.__data1.loc[el, 'diseaseid']) or (id in self.__data1.loc[el, 'disease_name']):
                pmids.append(self.__data1.loc[el, 'pmid'])
        
        genes = []
        for el in range(len(self.__data2)):
            if (self.__data2.loc[el, 'pmid'] in pmids) and (self.__data2.loc[el, 'gene_symbol'] not in genes):
                genes.append(self.__data2.loc[el, 'gene_symbol'])

        return genes