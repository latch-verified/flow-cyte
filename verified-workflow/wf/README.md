<html>
<h1 align="center">
  Cytoflow: Flow Cytometry Analysis
</h1>

<p align="center">
  Correct for compensation and produce simple gates from FCS files
</strong>
</p>

</html>

# About the Tool

This workflow uses [Cytoflow](https://cytoflow.readthedocs.io/en/stable/), a Python package, to analyze flow cytometry data. Cytoflow was written by Brian Teague to address shortcomings in currently-available flow software.

# TASBE: Test Data

This workflow comes with test data provided in the original Cytoflow documentation, which is from a paper by [Li et al](http://www.nature.com/nchembio/journal/v11/n3/full/nchembio.1736.html). 
This experiment characterizes a TALE transcriptional repressor and is a multi-plasmid transient transfection in mammalian cells, depicted below:

![image](https://github.com/latchbio/wf-cytoflow/assets/52743495/3038e7a2-8723-456d-8866-2bd2766198f8)

The small molecule doxycycline (“Dox”) drives the transcriptional activator rtTA3 to activate the transcriptional repressor (“R1” in the diagram), which then represses output of the yellow fluorescent protein EYFP. rtTA3 also drives expression of a blue fluorescent protein, eBFP, which serves as a proxy for the amount of repressor. 
Finally, since this is a transient transfection, there’s a huge amount of variability in the level of transfection; so transfection level with a constitutively expressed red fluorescent protein, mKate, is also measured.

The corresponding fluorescent channels in the data are:
* EYFP - Yellow - FITC-A channel
* eBFP - Blue - Pacific Blue-A channel
* mKate - Red - PE-Tx-Red-YG-A channel

# Workflow Functionalities

This workflow has the following features:

* Gaussian mixture gate
* Autofluorescence correction
* Spectral bleedthrough correction
* Threshold and quadrant gates
* Output CSV of FCS Data

# Input Parameters

The following parameters are required to run this workflow:
* **experiment_name:** The name of the experiment
* **condition_name:** The name of the varying condition across FCS files (e.g. stain or concentration)
* **fcs_files:** For every FCS file, the value of the varying condition needs to be added (e.g. 0.01 might be the value for one FCS file that has a concentration of 0.01 for an added molecule)
* **output_directory:** Directory where output files from the analysis will be stored
* **marker_size:** Marker size for matplotlib marker that is used in scatterplots (default = 0.5)
* **marker_alpha:** Marker size for matplotlib marker that is used in scatterplots (default = 0.7, value must be between 0.0 and 1.0)

# Output Files

For any workflow, the following files are outputted:
* Scatterplot of FSC-A and SSC-A channels
* Scatterplot with Gaussian mixture overlayed over FSC-A and SSC-A channels, showing where the bulk distribution of cells is
* CSV of all FCS data. This matrix will contain the channel values for all cells in an easy-to-read CSV format
* Histogram plots for every channel's distribution across each FCS file

For quadrant gates, a scatterplot will be outputted labelling the percentages of each quadrant. A CSV is also outputted with the number of cells in each quadrant.
For threshold gates, a histogram plot is saved.

# More on Compensation Correction

One common issue in flow cytometry is the fact that spectrally adjacent channels often overlap. 
For example, if trying to measure a green fluorophore like FITC and a yellow fluorophore like PE, a significant amount of FITC fluorescence will also be picked up by my PE channel.
The following two processes help correct for this, but require control files to be provided.

## Autofluorescence correction

To account for autofluorescence, we measure a tube of blank cells (unstained, untransfected, untransformed – not fluorescing.) The autofluorescence operation finds the (arithmetic) median of the blank cells’ distributions in the fluorescence channels and subtracts it from all the observations in the experimental data.

The diagnostic plot outputted by the software shows the fluorescence histograms and the medians. Make sure that they’re unimodal and the median is at the peak.

#### Input Data Requirement
A blank control – one with your cells but without any fluorophores. This will let us measure the “background” fluorescence (or autofluorescence) of the samples.

## Spectral bleedthrough correction
This is a traditional matrix-based compensation for bleedthrough. For each pair of channels, the module estimates the proportion of the first channel that bleeds through into the second, then performs a matrix multiplication to compensate the raw data.
This works best on data that has had autofluorescence removed first; if that is the case, then the autofluorescence will be subtracted from the single-color controls too.

#### Input Data Requirement
A set of single-color controls – for each fluorophore, one control that is stained with (or expresses) only that fluorophore and no others. These let us measure how much signal “bleeds through” into the non-target channels. These controls should be as bright as (but no brigher than) your brightest experimental sample.
