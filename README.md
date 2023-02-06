# Documentation of Philipp Piccardi's evolution experiment sequencing data

## Meta data

You can find the metadata for every sample including it's data path [here](./samples/sample_sheet.csv).  
Additionally, I wrote a `python` Samples class storing metadata and data paths in dictionaries which turned out very handy for scripting. The parser can be simply installed with `pip`, more info can be found in the section [python parser](#python-parser).

## Software environment

I tried to install all packages with conda (small hint; you can use mamba instead which is a much faster re-implementation of conda). 
You can find the package versions in [evomicrocomm.yml](evomicrocomm.yml) which you can also use to recreate the exact same environment.
All bioinformatic steps were performed using [Snakemake](https://snakemake.readthedocs.io/en/stable/) as a workflow language. It's fairly easy to learn and I can recommend it if you need to chain many command line tools.

## Ancestral strains

Prior to the experiment *Agrobacterium tumefaciens*, *Comamonas testosteroni*, *Microbacterium saperdae* and *Ochrobactrum anthropi* were
sequenced with PacBio and Illumina. The two datasets were used to create hybrid-assemblies of the genomes for each species.  
For more information which bioinformatic step was performed you can check the [Snakemake file](workflows/ancestral/Snakefile).
For now data is stored in `/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data/ancestors`. Below you can find a short description of the relevant files in each species sub-directory.
- `assembly.contigs.fasta`: canu assembly
- `assembly.contigs.racon.fasta`: long read polished assembly
- `assembly.contigs.polypolish.fasta`: short read polished assembly. **Use this fasta file for your analysis**.
- `bakta/`: Annotated genomes in different formats. If you don't have a format preference `assembly.contigs.polypolish.gbff` is probalby a good pick. You can use this file to search for genes and proteins. Remember, these are generated annotations so be careful of the conclusions you draw.

## Illumina data of species evolved in MWF

At timepoints T11, T22, T33 and T44 samples of the microcosms were taken and sequenced with Illumina. Therefore, if species were co-cultured in a microcosm, it's metagenomic data. This caused some issues because some species in co-culture were sequenced with much higher depth than others. Most of the reads map to *Agrobacterium tumefaciens*, the least coverage can be observed for *Microbacterium saperdae*. We also observed a pretty strong GC-bias for some species (especially *Microbacterium saperdae*) which can lead to regions with low to zero coverage. So be careful and double check the coverage at regions for which you do genomic interpretations.  
I did some stats for every sample which can be found in the [illumina sample report](illumina_sample_reports.pdf).

You can find the computational steps I performed to process the data in the [Snakemake file](workflows/illumina/Snakefile).
The data is stored in `/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data` and grouped per timepoint. Within each timepoint directory you can find a subdirectory for every species present in the microcosm.
Below are some useful files listed relative to the species directory:
- `var.vcf` freebayes SNP calling (check Snakefile for parameters)
- `'sniipy/*` fixed mutations
- `spades/contigs.fasta` assembly
- `mapped_reads.sorted.bam` alignments

## PacBio data

At the same time points as for Illumina, samples were taken to sequence with PacBio (except T11). In contrast to the Illumina data, PacBio data was generated based of picked colonies. The Snakemake workflow can be found [here](./workflows/pacbio/Snakefile).  
The data is in subdirectories with the name of the species, timepoint and microcosm in the `/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data/` directory.
Below a list of useful files:
- `assembly.fasta` assembled genome. This files was provided by the sequencing facility and is not part of the workflow
- `bakta/*` Annotation of assembled genomes

## Python parser

Install parser:
```
git clone git@github.com:nahanoo/bqh_samples.git
cd bqh_samples
pip install .
```  
Examples:
```python
from samples import Samples
s = Samples()

# Iterating over all samples of one species:
for sample in s.strains[s.abbreviations['at']]:
    print(sample)

# Outputs
{'dir_name': '/work/FAC/FBM/DMF/smitri/evomicrocomm/genome_size/data/T44.4.5.rep/at',
 'name': 'T44.4.5.rep',
 'strain': 'Agrobacterium tumefaciens',
 'platform': 'illumina',
 'timepoint': 'T44',
 'treatment': 4,
 'cosm': 5}

from os.path import join
# We can use this to filter samples:
for sample in s.strains[s.abbreviations['at']]:
    # Iterating only over illumina samples from treatment 4
    if (sample['platform'] == 'Illumina') & (sample['treatment'] == 4):
        # Prints file path of SNP file
        print(join(sample['dir_name'],'var.vcf'))

# Iterate over all Pacbio samples over all species:
for specie,samples in s.strains:
    for sample in samples:
        if sample['platform'] == 'pacbio':
            print(sample['name'])
```
I started to really appreciate thie python class because it's very convenient to submit files to the cluster and so on.
People probably won't use this but maybe someone will give it a go:)