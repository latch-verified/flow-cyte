from wf.task import task

from latch.resources.workflow import workflow
from latch.types.directory import LatchOutputDir
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter
from dataclasses import dataclass
from latch.types import LatchDir, LatchFile, Section, Params, Text
from latch.resources.launch_plan import LaunchPlan
from typing import Annotated, Iterable, List, Optional, Tuple, Union

@dataclass
class FCS:
    file: LatchFile
    condition_val: str

@dataclass
class AutofluorescenceOp:
    blank_file: LatchFile
    fluor_channels: List[str]

@dataclass
class BleedthroughLinearOp:
    fluor_channel: str
    control_file: LatchFile

@dataclass
class QuadOp:
    gate_name: str
    xchannel: str
    xthreshold: float
    ychannel: str
    ythreshold: float
    # subset: str
    # subset_val: bool

@dataclass
class ThresholdOp:
    gate_name: str
    channel: str
    threshold: float
    # subset: str
    # subset_val: bool

metadata = LatchMetadata(
    display_name="Cytoflow",
    author=LatchAuthor(
        name="LatchBio",
    ),
    parameters={
        "experiment_name": LatchParameter(
            display_name="Experiment name",
            batch_table_column=True,  # Show this parameter in batched mode.
            description="Name of the experiment"
        ),
        "fcs_files": LatchParameter(
            display_name="Input Flow Cytometry Files",
            batch_table_column=True,  # Show this parameter in batched mode.
            samplesheet=True,
        ),
        "condition_name": LatchParameter(
            display_name="Condition name",
            batch_table_column=True,  # Show this parameter in batched mode.
        ), 
        "autofluoresence": LatchParameter(
            display_name="Compute Autofluoresence",
            batch_table_column=True,  # Show this parameter in batched mode.
            detail="This will let us measure the “background” fluorescence (or autofluorescence) of the samples.",
            description="Channel: The fluorescent channels to calibrate. \
                Blank File: The FCS file with the blank (unstained or untransformed) cells, for autofluorescence correction."
        ),
        "bleedthrough": LatchParameter(
            display_name="Compute Compensation",
            batch_table_column=True,  # Show this parameter in batched mode.
            detail="Apply matrix-based bleedthrough correction to a set of fluorescence channels.",
            description="Provide the single-color control files and the name of the channels they should be measured in."
        ),
        "quad_gate": LatchParameter(
            display_name="Add Quadrant Gate",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
        "threshold_gate": LatchParameter(
            display_name="Add Threshold Gate",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
        "marker_size": LatchParameter(
            display_name="Set Plot Marker Size",
            batch_table_column=True,  # Show this parameter in batched mode.
            detail="The size of the marker that will be used in scatterplots."
        ),
        "marker_alpha": LatchParameter(
            display_name="Set Plot Marker Transparency",
            batch_table_column=True,  # Show this parameter in batched mode.
            detail="The opacity of the marker that will be used in scatterplots."
        ),
        "output_to_registry": LatchParameter(
            display_name="Add Table ID to Output to Registry",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
        "output_directory": LatchParameter(
            display_name="Output Directory",
            detail="Specify the folder to output workflow results to.",
            batch_table_column=True,  # Show this parameter in batched mode.
        ),
    },
    flow=[
        Section(
            "Basic Inputs",
            Text("Specify the name for this experiment. For each FCS file, add its path and its value for the specified condition name."),
            Params("experiment_name", "condition_name", "fcs_files")),
        Section(
            "Workflow Logic",
            Text("Select compensation corrections and gates to apply to FCS files."),
            Params(
                "autofluoresence",
                "bleedthrough",
                "quad_gate",
                "threshold_gate")),
        Section(
            "Outputs",
            Text("Select the output directory for the generated workflow files."),
            Params("output_to_registry", "output_directory"))]
)

@workflow(metadata)
def cytoflow(
    experiment_name: str,
    fcs_files: List[FCS],
    condition_name: str,
    autofluoresence: Optional[AutofluorescenceOp],
    bleedthrough: Optional[List[BleedthroughLinearOp]],
    threshold_gate: Optional[ThresholdOp],
    quad_gate: Optional[QuadOp],
    output_to_registry: Optional[str],
    output_directory: LatchOutputDir,
    marker_size: float = 0.5,
    marker_alpha: float = 0.7,
) -> LatchOutputDir:
    
    """
    This workflow uses cytoflow, a Python package, to analyze flow cytometry data. 

    # Cytoflow: Flow Cytometry Analysis

    Correct for compensation and produce simple gates from FCS files

    # About the Tool

    This workflow uses [Cytoflow]("https://cytoflow.readthedocs.io/en/stable/"), a Python package, to analyze flow cytometry data. Cytoflow was written by Brian Teague to address shortcomings in currently-available flow software.

    # TASBE: Test Data

    This workflow comes with test data provided in the original Cytoflow documentation, which is from a paper by [Li et al]("http://www.nature.com/nchembio/journal/v11/n3/full/nchembio.1736.html"). 
    This experiment characterizes a TALE transcriptional repressor and is a multi-plasmid transient transfection in mammalian cells, depicted below:

    ![image](https://github-production-user-asset-6210df.s3.amazonaws.com/52743495/296085122-3038e7a2-8723-456d-8866-2bd2766198f8.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240112%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240112T032553Z&X-Amz-Expires=300&X-Amz-Signature=e3711d760db4fc333f40a5aab2dea506bfb92ddc3841d9858869c44ae8c73812&X-Amz-SignedHeaders=host&actor_id=52743495&key_id=0&repo_id=742141777)

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


    




    """

    return task(
        experiment_name=experiment_name,
        fcs_files=fcs_files, 
        condition_name=condition_name,
        autofluoresence=autofluoresence,
        bleedthrough=bleedthrough,
        threshold_gate=threshold_gate,
        quad_gate=quad_gate,
        output_to_registry=output_to_registry,
        marker_alpha=marker_alpha,
        marker_size=marker_size,
        output_directory=output_directory)

LaunchPlan(
    cytoflow,
    "Test TABSE Data",
    {   
        "experiment_name": "test_experiment",
        "condition_name": "Dox",
        "fcs_files":[FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_1.fcs"), condition_val="0.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_2.fcs"), condition_val="0.1"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_3.fcs"), condition_val="0.2"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_4.fcs"), condition_val="0.5"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_5.fcs"), condition_val="1.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_6.fcs"), condition_val="2.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_7.fcs"), condition_val="5.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_8.fcs"), condition_val="10.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_9.fcs"), condition_val="20.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_10.fcs"), condition_val="50.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_11.fcs"), condition_val="100.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_12.fcs"), condition_val="200.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_13.fcs"), condition_val="500.0"),
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_14.fcs"), condition_val="1000.0"), 
                     FCS(file=LatchFile("s3://latch-public/test-data/24199/tasbe/TAL14_15.fcs"), condition_val="2000.0")], 
        "autofluoresence": AutofluorescenceOp(blank_file="s3://latch-public/test-data/24199/tasbe/controls/Blank-1_H12_H12_P3.fcs",
                                              fluor_channels=["Pacific Blue-A", "FITC-A", "PE-Tx-Red-YG-A"]),
        "bleedthrough": [BleedthroughLinearOp(fluor_channel="FITC-A", control_file="s3://latch-public/test-data/24199/tasbe/controls/EYFP-1_H10_H10_P3.fcs"),
                         BleedthroughLinearOp(fluor_channel="PE-Tx-Red-YG-A", control_file="s3://latch-public/test-data/24199/tasbe/controls/mkate-1_H8_H08_P3.fcs"),
                         BleedthroughLinearOp(fluor_channel="Pacific Blue-A", control_file="s3://latch-public/test-data/24199/tasbe/controls/EBFP2-1_H9_H09_P3.fcs")],
        "quad_gate": QuadOp(gate_name="Quad", xchannel="Pacific Blue-A", xthreshold=637.6907814597589, ychannel="PE-Tx-Red-YG-A", ythreshold=1130.7109998300425)

    }
)