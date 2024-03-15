from latch.resources.tasks import small_task
from latch.types.directory import LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter, MultiselectOption
from dataclasses import dataclass
from typing import Annotated, Iterable, List, Optional, Tuple, Union
from pathlib import Path
import cytoflow as flow
import matplotlib
from matplotlib import colormaps
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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

@small_task
def task(
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
    
    print("Setting up local directories")
    local_output_directory = Path(f"/root/output_data/{experiment_name}")
    local_output_directory.mkdir(parents=True, exist_ok=True)
    local_output_directory = Path(f"/root/output_data")
    print("Sample output directory: ", local_output_directory)
    matplotlib.rc('figure', dpi = 350)

    # INITIALIZE EXPERIMENT
    tubes = []
    for fcs_file in fcs_files:
        tubes.append(flow.Tube(file = fcs_file.file.local_path, conditions = {condition_name : fcs_file.condition_val}))

    import_op = flow.ImportOp(conditions = {condition_name : 'str'}, tubes = tubes)
    ex = import_op.apply()

    # Save initial scatterplot
    flow.ScatterplotView(xchannel = "FSC-A",
                     ychannel = "SSC-A",
                     yscale = "log").plot(ex, alpha=marker_alpha, s=marker_size, marker=".")

    path_png = f"/root/output_data/{experiment_name}/scatterplot.png"
    plt.savefig(path_png, bbox_inches='tight')



    # Initialize channels
    channels = ex.channels


    # Histograms
    print("Making Histograms")
    curr_output_directory = Path(f"/root/output_data/{experiment_name}/histograms/")
    curr_output_directory.mkdir(parents=True, exist_ok=True)

    for channel in channels:
        # LOG
        flow.HistogramView(channel = channel, scale="log", yfacet = condition_name).plot(ex)
        path_png = f"/root/output_data/{experiment_name}/histograms/{channel}.png"
        plt.savefig(path_png, bbox_inches='tight')

    # Extract bulk of data
    gm_1 = flow.GaussianMixtureOp(name = "CellBulk",
                              channels = ["FSC-A", "SSC-A"],
                              scale = {"SSC-A" : "log"},
                              num_components = 2,
                              sigma = 2)
    gm_1.estimate(ex)
    ex_morpho = gm_1.apply(ex)

    flow.ScatterplotView(xchannel = "FSC-A",
                        ychannel = "SSC-A",
                        yscale = "log",
                        huefacet = "CellBulk_2").plot(ex_morpho, s=marker_size, alpha=marker_alpha, marker=".")
    
    path_png = f"/root/output_data/{experiment_name}/gaussian_plot.png"
    plt.savefig(path_png, bbox_inches='tight')


    if autofluoresence:
        print("Autofluorescence")
        curr_output_directory = Path(f"/root/output_data/{experiment_name}/autofluorescence/")
        curr_output_directory.mkdir(parents=True, exist_ok=True)

        af_op = flow.AutofluorescenceOp()
        af_op.blank_file = autofluoresence.blank_file.local_path
        af_op.channels = autofluoresence.fluor_channels

        af_op.estimate(ex_morpho, subset = "CellBulk_2 == True")
        af_op.default_view().plot(ex_morpho)
        path_png = f"/root/output_data/{experiment_name}/autofluorescence/histograms.png"
        plt.savefig(path_png, bbox_inches='tight')

        ex_af = af_op.apply(ex_morpho)
    else:
        ex_af = ex_morpho

    if bleedthrough:
        print("Compensation Analysis")
        curr_output_directory = Path(f"/root/output_data/{experiment_name}/bleedthrough/")
        curr_output_directory.mkdir(parents=True, exist_ok=True)
        bl_op = flow.BleedthroughLinearOp()
        bl_op.controls = {bleedthrough[i].fluor_channel: bleedthrough[i].control_file.local_path for i in range(len(bleedthrough))}
        bl_op.estimate(ex_af, subset = "CellBulk_2 == True")
        bl_op.default_view().plot(ex_af)
        path_png = f"/root/output_data/{experiment_name}/bleedthrough/compensation_matrix.png"
        plt.savefig(path_png, bbox_inches='tight')
        ex_bl = bl_op.apply(ex_af)
    else:
        ex_bl = ex_af

    # THRESHOLD GATE
    if threshold_gate:
        curr_output_directory = Path(f"/root/output_data/{experiment_name}/threshold_gate/")
        curr_output_directory.mkdir(parents=True, exist_ok=True)

        thresh_op = flow.ThresholdOp(name = threshold_gate.gate_name, channel = threshold_gate.channel, threshold = threshold_gate.threshold)
        tv = thresh_op.default_view(scale = 'log')
        tv.plot(ex_bl)

        path_png = f"/root/output_data/{experiment_name}/threshold_gate/threshold_plot.png"
        plt.savefig(path_png, bbox_inches='tight')

        ex_tv = thresh_op.apply(ex_bl)
        print("Threshold Gate:")
        print(ex_tv.data.groupby(threshold_gate.gate_name).size())
    else:
        ex_tv = ex_bl


    # QUAD GATE
    if quad_gate:
        print("Quadrant Gate")
        curr_output_directory = Path(f"/root/output_data/{experiment_name}/quadrant_gate/")
        curr_output_directory.mkdir(parents=True, exist_ok=True)

        q = flow.QuadOp(name=quad_gate.gate_name,
            xchannel=quad_gate.xchannel,
            xthreshold=quad_gate.xthreshold,
            ychannel=quad_gate.ychannel,
            ythreshold=quad_gate.ythreshold)

        qv = q.default_view(huefacet = condition_name,
                    xscale = "log",
                    yscale = "log")

        palette = plt.get_cmap('jet').copy()
        palette.set_under('white', 1.0)

        qv.plot(ex_tv, cmap=palette,line_props={"color" : 'black', "linewidth" : 1},marker=".",s=0.5, alpha=marker_alpha)

        exq = q.apply(ex_tv)
        quad_array = exq.data.groupby(quad_gate.gate_name).size()

        string = quad_gate.gate_name
        sum_q = sum(quad_array)
        print(sum_q)

        q1 = quad_array[0]
        plt.text(0.05, 0.95, f'Q1: {round((q1/sum_q)*100,2)}%',
            horizontalalignment='left',
            verticalalignment='top', color='red',transform=plt.gca().transAxes)

        q2 = quad_array[1]
        plt.text(0.95, 0.95, f'Q2: {round((q2/sum_q)*100,2)}%',
            horizontalalignment='right',
            verticalalignment='top', color='red',transform=plt.gca().transAxes)

        q3 = quad_array[2]
        plt.text(0.05, 0.05, f'Q3: {round((q3/sum_q)*100,2)}%',
            horizontalalignment='left',
            verticalalignment='bottom', color='red', transform=plt.gca().transAxes)

        q4 = quad_array[3]
        plt.text(0.95, 0.05, f'Q4: {round((q4/sum_q)*100,2)}%',
            horizontalalignment='right',
            verticalalignment='bottom', color='red',transform=plt.gca().transAxes)
        
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", markerscale=20, fontsize=10)

        path_png = f"/root/output_data/{experiment_name}/quadrant_gate/scatterplot.png"
        plt.savefig(path_png, bbox_inches='tight')

        quads = ["Q1", "Q2", "Q3", "Q4"]
        names = [f"{quad_gate.gate_name}_1", f"{quad_gate.gate_name}_2",f"{quad_gate.gate_name}_3",f"{quad_gate.gate_name}_4"]
        quad_array = quad_array

        quadrant_data = pd.DataFrame(
            {'quadrant': quads,
            'quadrant_name': names,
            'cells': quad_array
            })
        csv_path = f"/root/output_data/{experiment_name}/quadrant_gate/quadrant_statistics.csv"
        quadrant_data.to_csv(csv_path, index=False)

    else:
        exq = ex_tv

    csv_path = f"/root/output_data/{experiment_name}/cell_matrix.csv"
    exq.data.to_csv(csv_path, index=False)

    return LatchOutputDir(str(local_output_directory), str(output_directory.remote_path))