import os
from typing import Iterable, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from plotly.offline import iplot
import logging
import sys
import os


# --------------------
# FR and CDR RMSD
# --------------------
# histogram
def plot_cdr_rmsd_hist(df: pd.DataFrame,
                       bins: Iterable,
                       save_fig_name: str = None):
    """
    Args:
        df: (DataFrame) CDR Loop RMSD, weights, pair name
        bins: (Iterable) should have the same length as df.shape[0]
        save_fig_name: (str) figure name
    """
    cdrs = 'fr,l1,l2,l3,h1,h2,h3'.split(',')
    fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)
    axes = axes.flatten()
    for i, c in enumerate(cdrs[1:]):
        ax = axes[i]
        sns.histplot(df, x=f'{c}_rmsd', label=f"{c.upper()} unweighted", weights=1 / df.shape[0], bins=bins, kde=True,
                     alpha=0.2, ax=ax)
        sns.histplot(df, x=f'{c}_rmsd', label=f"{c.upper()} weighted", weights=df.weights, color='orange', bins=bins,
                     kde=True, alpha=0.2, ax=ax)
        ax.legend();
        ax.grid(0.1);
        ax.set_ylabel('Frequency'), ax.set_xlabel('RMSD');
        ax.set_title(c.upper())
    fig.tight_layout()
    fig.show()
    if save_fig_name:
        os.makedirs('plots', exist_ok=True)
        fig.savefig(f"plots/{save_fig_name}.png", dpi=300, transparent=True)
        fig.savefig(f"plots/{save_fig_name}.pdf", transparent=True)


# bar plot
def plot_num_pairs_per_line_bar(df: pd.DataFrame,
                                title: str = None,
                                xlabel: str = None,
                                ylabel: str = None,
                                save_fig_name: str = None,
                                size=None):
    assert 'line_id' in df.columns

    fig = go.Figure()
    fig.add_bar(
        x=[int(i) for i in df.value_counts('line_id').index],
        y=df.value_counts('line_id'))
    fig.update_layout(title=dict(text=title, x=0.5, y=0.9, xanchor='center', yanchor='top', font=dict(size=15)),
                      xaxis=dict(title=xlabel),
                      yaxis=dict(title=ylabel),
                      showlegend=False)
    fig.update_layout(width=size[0], height=size[1]) if size else fig.update_layout(width=None, height=None)
    # show image
    iplot(fig)
    # save image
    if save_fig_name:
        os.makedirs('plots', exist_ok=True)
        fig.write_image(f"plots/{save_fig_name}.png")
        fig.write_image(f"plots/{save_fig_name}.pdf")


# violin plot
def plot_cdr_rmsd_violin(df: pd.DataFrame,
                         col_names: List[str]=None,
                         title: str = None,
                         xlabel: str = None,
                         ylabel: str = None,
                         size=None,
                         save_fig_name: str = None):
    fig = go.Figure()

    if not col_names:
        col_names = [f"{i}_rmsd" for i in 'fr,l1,l2,l3,h1,h2,h3'.split(',')]

    for col in col_names:
        fig.add_trace(go.Violin(y=df[col],
                                name=col[:2].upper(),
                                box_visible=True,
                                meanline_visible=True))
    fig.update_layout(
        title=dict(text=title, x=0.5, y=0.9, xanchor='center', yanchor='top', font=dict(size=15), ),
        xaxis=dict(title=xlabel, ),
        yaxis=dict(title=ylabel, ),
        showlegend=True, )
    fig.update_layout(width=size[0], height=size[1]) if size else fig.update_layout(width=None, height=None)

    # show figure
    iplot(fig)

    # save figure
    if save_fig_name:
        os.makedirs('plots', exist_ok=True)
        fig.write_image(f"plots/{save_fig_name}.png")
        fig.write_image(f"plots/{save_fig_name}.pdf")


# plot fr_rmsd percentiles
def plot_col_quantile_scatter(df: pd.DataFrame,
                              x_col: str,
                              quantile_num: int,
                              title: str = None,
                              xlabel: str = None,
                              ylabel: str = None):
    assert x_col in df.columns
    quantile_num += 1
    x = np.arange(quantile_num)
    y = np.quantile(df[x_col], np.linspace(0, 1, quantile_num))

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    sns.scatterplot(x=x, y=y, ax=ax)
    ax.grid(alpha=0.2)
    ax.set_title(title);
    ax.set_xlabel(xlabel);
    ax.set_ylabel(ylabel)

    return fig, ax, x, y


def annotate_point(ax, x, y, i, offset=(0, 0)):
    ax.annotate(f"({i}, {y[i]:.3f})", xy=(i + offset[0], y[i] + offset[1]))


def highlight_point(ax, x, y, i, c):
    ax.scatter(x[i], y[i], color=c)


def setup_logger(save_dir,
                 file_name="run.log",
                 distributed_rank=0,
                 level=logging.DEBUG):
    formatter = logging.Formatter(
        fmt='%(asctime)s {%(name)s:%(lineno)d} [%(levelname)s] [%(threadName)s] - %(message)s',
        datefmt='%H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(level)
    # don't log results for the non-master process
    if distributed_rank > 0:
        return logger
    # 1. output to sys.stdout
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 2. output to log file
    if save_dir:
        fh = logging.FileHandler(os.path.join(save_dir, file_name), mode='w')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
