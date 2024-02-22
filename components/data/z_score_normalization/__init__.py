import numpy as np
from scipy.stats import zscore
from components.data.metabolite_count_matrix import MetaboliteCountMatrix, metabolite_count_matrix, metanndata_from_file
from components.core.file import upsert_file
import sys

def z_score_normalize_metabolite_count_matrix(m: MetaboliteCountMatrix):
  df = metanndata_from_file(m)
  
  debug = 1;

  if(debug > 0): print(f"type of df: {type(df)}", file=sys.stderr);
  if(debug > 0): print(f"before z-score: type of df.X: {type(df.X)}, shape of df.X: {df.X.shape}", file=sys.stderr);

  # z-score normalization: axis = 0 means do along columns (each column is a variable) i.e., across the rows
  df.X = zscore(df.X, axis=0, ddof=1, nan_policy = 'omit')

  if(debug > 0): print(f"after z-score: type of df.X: {type(df.X)}, shape of df.X: {df.X.shape}", file=sys.stderr);

  # filter out metabolites with any null variances
  df = df[:, ~np.isnan(df.X).any(axis=0)]

  if(debug > 0): print(f"type of df: {type(df)}", file=sys.stderr);
  if(debug > 0): print(f"type of z-score df.X: {type(df.X)}, shape of df.X: {df.X.shape}", file=sys.stderr);
  if(debug > 0): print(f"z-score df.X: {df.X}", file=sys.stderr);

  # check that df^2 sums to 1 for each column
  nr = np.shape(df.X)[0];
  nc = np.shape(df.X)[1];
  #print("Number of rows in z-score matrix: " + str(1) + ", number of columns: " + str(2) + "\n", file=sys.stderr);
  if(debug > 0): print("Number of rows in z-score matrix: " + str(nr) + ", number of columns: " + str(nc) + "\n", file=sys.stderr);
  zss = np.sum(np.square(df.X), axis=0); # zss should have nc elements, each equal to nr -1 (within machine precision)
  if(debug > 0): print("sum of squares of z-scores:" + str(zss) + "\n", file=sys.stderr);

  with upsert_file('.h5ad') as f:
    df.write_h5ad(f.file)

  return metabolite_count_matrix(f)
