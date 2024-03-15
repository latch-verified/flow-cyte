<html>
<p align="center">
  <img src="https://user-images.githubusercontent.com/31255434/182674961-b5b9ce91-ef56-48e7-80d1-cca029d25f78.jpg" alt="Latch Verified" width="100">
</p>

<h1 align="center">
  Flow Cytometry
</h1>

<p align="center">
<strong>
Latch Verified
</strong>
</p>

<p align="center">
  Explore flow cytometry data with gating software and automated plotting worklfows
</p>

<p align="center">
  <a href="https://github.com/latch-verified/bulk-rnaseq/releases/latest">
    <img src="https://img.shields.io/github/release/latch-verified/bulk-rnaseq.svg" alt="Current Release" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/LICENSE-MIT-brightgreen.svg" alt="License" />
  </a>
  <img src="https://img.shields.io/github/commit-activity/w/latch-verified/bulk-rnaseq.svg?style=plastic" alt="Commit Activity" />
  <img src="https://img.shields.io/github/commits-since/latch-verified/bulk-rnaseq/latest.svg?style=plastic" alt="Commits since Last Release" />
</p>

<h3 align="center">
  <a href="https://console.latch.bio/explore/66156/info">Hosted Interface</a>
  <span> · </span>
  <a href="https://docs.latch.bio">SDK Documentation</a>
  <span> · </span>
  <a href="https://join.slack.com/t/latchbiosdk/shared_invite/zt-193ibmedi-WB6mBu2GJ2WejUHhxMOuwg">Slack Community</a>
</h3>

</html>

## Verified Flow Cytometry

This collection of tools available on the Latch platform allows scientists to analyze their flow cytometry files and metadata. The main capabilities of this suite are:

* Applying gates to FCS files
* Generating statistics from gate information (e.g. percent of cells belonging to the gate) and cell distribution
* Correcting for fluoresence and linear bleedthrough
* Plotting density and scatterplots
* Generating easy-to-read CSV files from FCS file analyses

## Toolbox

Latch has made available three resources for FCS file analysis:
* [Verified datasets](https://github.com/latchbio/wf-cytoflow/tree/documentation/verified-data): For easy testing of tools
* [Workflow](https://github.com/latchbio/wf-cytoflow/tree/documentation/verified-workflow/wf): Bulk-import workflow for analyzing hundreds of FCS files at a time using Cytoflow [^1]
* [Pod](https://github.com/latchbio/wf-cytoflow/tree/documentation/verified-pod): Hosted GUI of Cytoflow [^1] for point-and-click gating

## Cytoflow

Cytoflow is an open-source tool for FCS file analysis built on Python that is leveraged in both the Pod and Workflow on Latch. Cytoflow goes beyond simple cell counting and has a unique emphasis on metadata -- a user can specify the conditions for each sample up front, then use those conditions to facet the analysis. Cytoflow also allows users to generate a Jupyter notebook from any steps taken in its GUI, so plots can be replicated easily after your session ends!

<html>
<p align="center">
  <img src="https://github.com/latchbio/wf-cytoflow/assets/52743495/2fb34cb0-1831-4c10-8c89-390421cc255e" width="500" height="500">
</p>
</html>

Cytoflow has the following capabilities:
* Set-up complex experiments with corresponding metadata
* Apply gating strategies and statistics
* Produce publication-ready plots 
* Reshare results as a Cytoflow workflow or as a Jupyter notebook with colleagues


[^1]: https://github.com/cytoflow/cytoflow 
