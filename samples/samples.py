from os.path import join
import pandas as pd
import pkg_resources


class Samples():
    """This is a class used for parsing. It combines samples
    of Illumina and Pacbio"""
    def __init__(self):
        self.sample_sheet = pkg_resources.resource_filename('samples','sample_sheet.csv')
        self.df = pd.read_csv(self.sample_sheet,dtype=str)
        
        self.work = '/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data/'

        #Adding abbreviations for convenience
        self.abbreviations = dict()
        self.abbreviations['Comamonas testosteroni'] = 'ct'
        self.abbreviations['Agrobacterium tumefaciens'] = 'at'
        self.abbreviations['Microbacterium saperdae'] = 'ms'
        self.abbreviations['Ochrobactrum anthropi'] = 'oa'
        self.abbreviations['ct'] = 'Comamonas testosteroni'
        self.abbreviations['at'] = 'Agrobacterium tumefaciens'
        self.abbreviations['ms'] = 'Microbacterium saperdae'
        self.abbreviations['oa'] = 'Ochrobactrum anthropi'
      
        strains = ['Agrobacterium tumefaciens','Comamonas testosteroni',\
            'Microbacterium saperdae','Ochrobactrum anthropi']
        self.strains = {k:list() for k in strains}

        self.treatments = {'Agrobacterium tumefaciens':[1,3,4],
            'Comamonas testosteroni':[2,3,4],
            'Microbacterium saperdae':[3,4],
            'Ochrobactrum anthropi':[4]}

        work = '/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data'
        self.references = {'Agrobacterium tumefaciens':join(work,'at','reference.fasta'),
            'Comamonas testosteroni':join(work,'ct','reference.fasta'),
            'Microbacterium saperdae':join(work,'ms','reference.fasta'),
            'Ochrobactrum anthropi':join(work,'oa','reference.fasta')}

        """For every strain and treatment we create a  list of dictionaries with
        the information about directory, sample name, treatment and sequencing platform"""
        keys = ['dir_name','name','strain','platform','timepoint','treatment','cosm']
        for i,row in self.df.iterrows():
            meta = {key:None for key in keys}
            meta['dir_name'] = row['dir_name']
            meta['name'] = row['sample_name']
            meta['strain'] = row['strain']
            meta['platform'] = row['platform']
            meta['timepoint'] = row['timepoint']
            meta['treatment'] = int(row['treatment'])
            meta['cosm'] = int(row['cosm'])
            self.strains[row['strain']].append(meta)