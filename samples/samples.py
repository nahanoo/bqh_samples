import re
import pandas as pd
import pkg_resources


class Samples():
    """This is a class used for parsing. It combines samples
    of Illumina and Pacbio"""
    def __init__(self):
        self.sample_sheet = pkg_resources.resource_filename('samples','sample_sheet.csv')
        self.df = pd.read_csv(self.sample_sheet,dtype=str)

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
      
        """For every strain and treatment we create a  list of dictionaries with
        the information about directory, sample name, treatment and sequencing platform"""
        keys = ['dir_name','name','strain','platform','timepoint','treatment','cosm']
        meta = {key:None for key in keys}

        keys = ['Agrobacterium tumefaciens','Comamonas testosteroni',\
            'Microbacterium saperdae','Ochrobactrum anthropi']
        self.strains = {k:list() for k in keys}

        keys = [1,2,3,4]
        self.treatments = {k:list() for k in keys}        
        self.samples = {name:meta for name in self.df['sample_name']}

        for i,row in self.df.iterrows():
            meta['dir_name'] = row['dir_name']
            meta['name'] = row['sample_name']
            meta['strain'] = row['strain']
            meta['platform'] = row['platform']
            meta['timepoint'] = row['timepoint']
            meta['treatment'] = row['treatment']
            meta['cosm'] = row['cosm']
            
            self.samples[row['sample_name']] = meta
            self.treatments[int(row['treatment'])].append(meta)
            self.strains[row['strain']].append(meta)