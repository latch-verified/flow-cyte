# Latch BCyto Pod

Latch hosts a public pod template of BCyto, a tool that allows for the analysis of flow cytometry data (in the form of FCS files). **BCyto** is an open-source project that provides an user-friendly, high-performance interface for Flow Cytometry analysis in R.

Using the BCyto Pod on Latch allows user to easily explore their FCS files on the same platform that they are running concurrent analyses.

<p align="center">
  <img width="40%" alt="Screenshot 2024-03-14 at 10 30 27 PM" src="https://github.com/latch-verified/flow-cyte/assets/52743495/8bbfdef4-581f-4e00-b93c-2b5467333989">
</p>

## Running BCyto

After making a copy of the BCyto public pod template, launch RStudio.

<p align="center">
<img width="40%" alt="Screenshot 2024-03-14 at 10 30 05 PM" src="https://github.com/latch-verified/flow-cyte/assets/52743495/41d877a3-478e-4c44-962f-757d0bd06c5c">
</p>

To launch the BCyto app, simply open the R Console and run the following command:

`BCyto::runBCyto()`

## Uploading FCS Data

If it is your first time running this pod, run the following commands in a Terminal to link files you store in Latch Data with this pod's file system. These commands only need to be run once.

```         
mount-ldata
systemctl start latch-ldata-automount
ln -s /ldata /root
```

Now, all files stored on Latch can be found in `/root/ldata`. **WARNING:** deleting files in `ldata` will delete them completely from Latch! `ldata` is a link to Latch Data, so any changes made in this pod will be reflected in Latch Data.

You can learn more [here](https://wiki.latch.bio/wiki/pods/getting-started).

## User Guide

As outlined in the [BCyto GitHub Repository](https://github.com/BonilhaCaio/BCyto):

**BCyto** will initially be opened in the *File* tab, where the user can load FCS files or a BCyto file, which contains all saved data from a previous analysis.

-   In the example below, a BCyto file from a [test dataset](http://github.com/BonilhaCaio/test-data-1) was uploaded. In the *Plot* tab, the user can generate dot plots, contour plots or histograms under selection of parameters such as sample and parameter. For the selection of desired populations, gates can be drawn directly in the plot with the use of rectangle, polygon, quadrant or interval tools. The gate hierarchy is shown in the *Parent* section in a second interactive plot.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide1.png?raw=true" width="100%"/>

-   The compensation can be checked in the *Compensation* tab, as shown below. For addressing compensation issues to improve the quality of the analysis, new matrices can be automatically generated with [AutoSpill](https://doi.org/10.1038/s41467-021-23126-8) or manually created through the interactive table.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide2.png?raw=true" align="center" width="65%"/>

-   Backgating based on the hierarchy of gates generated from user input can be easily visualised in the *Ancestry plots* tab under selection of the desired sample and population.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide3.png?raw=true" align="center" width="90%"/>

-   Overlaid or offset histograms for the generation of representative data can be created through the *Overlays* tab.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide4.png?raw=true" width="45%" align="left"/> <img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide5.png?raw=true" align="right" width="45%"/>

-   The *Proliferation* tab provides automated detection and quantification of division peaks from assays with cell proliferation dyes.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide6.png?raw=true" width="50%"/>

-   Plots such as the one below are generated using the *t-SNE* tab. Concatenation is performed within the software under quick selection of samples and does not require re-upload of external files. Highlights can be markers, populations or previous delimited groups.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide7.png?raw=true" width="35%"/>

-   Finally, quantifiable data can be selected, visualised and exported through the *Results* tab.

<img src="https://github.com/BonilhaCaio/BCyto/blob/main/inst/guide/Guide8.png?raw=true" width="60%"/>

## Credits

Bonilha CS. BCyto: A shiny app for flow cytometry data analysis. Molecular and Cellular Probes (2022), doi: <https://doi.org/10.1016/j.mcp.2022.101848>
