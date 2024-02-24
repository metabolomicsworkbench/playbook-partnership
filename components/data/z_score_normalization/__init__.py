import numpy as np
from scipy.stats import zscore
from components.data.gene_count_matrix import GeneCountMatrix, gene_count_matrix, anndata_from_file
from components.core.file import upsert_file
import sys;

def z_score_normalize_gene_count_matrix(m: GeneCountMatrix):
  debug = 1;
  if(debug > 0): print(f"type of GeneCountMatrix: {type(GeneCountMatrix)}", file=sys.stderr);

  df = anndata_from_file(m)

  if(debug > 0): print(f"type of df: {type(df)}", file=sys.stderr);
  if(debug > 0): print(f"before z-score: type of df.X: {type(df.X)}, shape of df.X: {df.X.shape}", file=sys.stderr);

  # z-score normalization
  df.X = zscore(df.X, axis=0)

  # filter out genes with any null variances
  df = df[:, ~np.isnan(df.X).any(axis=0)]

  with upsert_file('.h5ad') as f:
    df.write_h5ad(f.file)

  return gene_count_matrix(f)