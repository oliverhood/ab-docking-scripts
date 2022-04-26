# CDR Loop conformational change upon complexation analysis 

## Data
```

```

## Steps to reproduce the results

### create an environment with conda 
```shell
$ conda create abdock python=3.8
$ conda install -c -y conda-forge matplotlib
# plotting tools
$ conda install -c -y plotly plotly
$ conda install -c -y anaconda seaborn
# jupyter notebook 
$ pip install notebook
# install kernel for the notebook 
$ conda install -c -y anaconda ipykernel
$ python -m ipykernel install --user --name abdock --display-name abdock   
```

### Data
```
data
└── 20220324.24Mar2022.ProFit.onVHVLseparately
    ├── results.json
    ├── run.err
    └── run.log
```
- `20220324.24Mar2022.ProFit.onVHVLseparately`: superimpose the bound to unbound antibody structure on the framework region of light chain and heavy chain separately. Also performed superimposition using the framework region of both chains, though RMSD from this is not involved in CDR RMSD distribution, this is only used to filter out problematic structures.
  - `results.json`: data used for CDR RMSD distribution 
  - `run.err`: err info while producing results, not used for CDR RMSD distribution. 
  - `run.log`: log info while producing results, not used for CDR RMSD distribution.
### output 
Directory to write analysis result files including plots.

### Run the noteboook 
```shell
$ cd ~/ab-docking-scripts/chunan  # change this path 
$ conda activate abdock 
$ jupyter notebook 
```
Remember to change path settings in the notebook
