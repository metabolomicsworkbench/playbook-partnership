import numpy as np
from scipy.stats import zscore
from components.data.metabolite_count_matrix import MetaboliteCountMatrix, metabolite_count_matrix, metanndata_from_file
from components.data.gene_count_matrix import GeneCountMatrix, gene_count_matrix
from components.core.file import File, upsert_file
import sys;
import anndata as ad;
import typing;

from components.data.count_matrix import CountMatrix, count_matrix, CorrelationMatrix, anndata_from_file

def compute_corr_matrix(df1, df2 = None):
  r"""
  import sys;
  import os
  from compute_corr_matrix import compute_corr_matrix
  import numpy as np;
  x = np.random.normal(size= (5,3)); y = np.random.normal(size= (5,4)); 
  x
  compute_corr_matrix(x)
  """

  debug = 0;

  # z-score normalization: axis = 0 means do along columns (each column is a variable) i.e., across the rows
  df1 = zscore(df1, axis=0, ddof=1, nan_policy = 'omit')

  if(debug > 0): print(f"after z-score: type of df1: {type(df1)}, shape of df1: {df1.shape}", file=sys.stderr);

  # filter out metabolites with any null variances
  df1 = df1[:, ~np.isnan(df1).any(axis=0)]

  if df2 is None:
    r = np.dot(df1.T, df1)/(df1.shape[0] - 1);
  else:
    #if(df1.shape[0] != (df2.shape[0]): raise exception
    df2 = zscore(df2, axis=0, ddof=1, nan_policy = 'omit')
    df2 = df2[:, ~np.isnan(df2).any(axis=0)]
    r = np.dot(df1.T, df2)/(df1.shape[0] - 1);
    # if df=np.hstack((df1,df2)) and rz = compute_corr_matrix(df), 
    # then r should be same as rz[0:df1.shape[1],df1.shape[1]:df.shape[1]]


  if(debug > 0): print(f"type of r: {type(r)}", file=sys.stderr);
  if(debug > 0): print(f"shape of r: {r.shape}", file=sys.stderr);

  if(debug > 0): print(r, file=sys.stderr);

  # Do you need to crosscheck if all values are -1.0 < r < 1.0 or nan
  return r

def correlation_matrix(file: File) -> CorrelationMatrix:
    return(count_matrix(file))

def compute_corr_count_matrix(m: typing.Union[MetaboliteCountMatrix, GeneCountMatrix]) -> CorrelationMatrix:
  debug = 1;

  df = anndata_from_file(m);
  #if(isinstance(m, GeneCountMatrix)):
  #  df = anndata_from_file(m);
  #elif(isinstance(m, MetaboliteCountMatrix)):
  #  df = metanndata_from_file(m);

  if(debug > 0): print(f"type of df: {type(df)}", file=sys.stderr);  

  rdf = compute_corr_matrix(df.X);
  if(debug > 0): print(f"type of rdf: {type(rdf)}", file=sys.stderr);

  adata = ad.AnnData(rdf); # Ref: https://anndata.readthedocs.io/en/latest/index.html
  adata.var_names = df.var_names;
  adata.obs_names = df.var_names;

  with upsert_file('.h5ad') as f:
    adata.write_h5ad(f.file)

  return count_matrix(f)
