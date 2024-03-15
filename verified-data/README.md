# Verified Datasets

The following datasets are available:
* BD Biosciences - Monocyte RNA and Protein Co-Staining Analysis: Simple staining analysis with two fluorescent channels
* TABSE: Complex transfection analysis with three fluorescent channels

## BD Biosciences - Monocyte RNA and Protein Co-Staining Analysis

Monocyte CD4 mRNA and Protein Expression Analysis 
[Source](http://flowrepository.org/id/FR-FCM-ZZC7)

### Experiment:	
CD14 protein costaining with RNA flow cytometry. The purpose was confirm monocytes as CD4 mRNA high and CD4 protein low, relative to lymphocyte population.
CD14+ population (monocytes) was confirmed as CD4 protein low and CD4 mRNA high by RNA flow cytometry with protein costaining. Results were further supported through imaging results.

### Experiment variables

#### Conditions
* Protein Staining Only	
* PBMC_CD4_Protein_Stained.fcs
* PBMC_CD4_Protein_Unstained.fcs
* RNA with Protein Costaining	
* PBMC_CD4_RNA_Protein_Stained.fcs
* PBMC_CD4_RNA_Protein_Unstained.fcs

#### Sample Type
* PBMC:
PBMC_CD4_Protein_Stained.fcs
PBMC_CD4_RNA_Protein_Stained.fcs
* PBMC no target probe added negative control or unstained
PBMC_CD4_Protein_Unstained.fcs
PBMC_CD4_RNA_Protein_Unstained.fcs


## TASBE

This workflow comes with test data provided in the original Cytoflow documentation, which is from a paper by [Li et al](http://www.nature.com/nchembio/journal/v11/n3/full/nchembio.1736.html). 
This experiment characterizes a TALE transcriptional repressor and is a multi-plasmid transient transfection in mammalian cells, depicted below:

![image](https://github.com/latchbio/wf-cytoflow/assets/52743495/3038e7a2-8723-456d-8866-2bd2766198f8)

The small molecule doxycycline (“Dox”) drives the transcriptional activator rtTA3 to activate the transcriptional repressor (“R1” in the diagram), which then represses output of the yellow fluorescent protein EYFP. rtTA3 also drives expression of a blue fluorescent protein, eBFP, which serves as a proxy for the amount of repressor. 
Finally, since this is a transient transfection, there’s a huge amount of variability in the level of transfection; so transfection level with a constitutively expressed red fluorescent protein, mKate, is also measured.

The corresponding fluorescent channels in the data are:
* EYFP - Yellow - FITC-A channel
* eBFP - Blue - Pacific Blue-A channel
* mKate - Red - PE-Tx-Red-YG-A channel
