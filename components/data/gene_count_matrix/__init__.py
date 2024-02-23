import typing
import numpy as np
import anndata as ad
from components.core.file import File, file_as_path, file_as_stream, upsert_file

from components.data.count_matrix import CountMatrix, anndata_from_gctx, anndata_from_gct, anndata_from_file
from components.data.count_matrix import np_jsonifyable, count_matrix, transpose

# using class and functions defined in components.data.count_matrix to define what was defined in details in this file
class GeneCountMatrix(CountMatrix):
  no_additional_fields: None

def anndata_from_gctx(file: File):
   return(anndata_from_gctx(file))

def anndata_from_gct(file: File):
   return(anndata_from_gct(file))

def anndata_from_file(file: File):
   return(anndata_from_file(file))

def gene_count_matrix(file: File) -> GeneCountMatrix:
    return(count_matrix(file))

def transpose(m: File):
   return(transpose(m))

# Mano: original code is block-commented beloew
"""
class GeneCountMatrix(File, typing.TypedDict):
  shape: typing.Tuple[int, int]
  index: typing.List[str]
  columns: typing.List[str]
  values: typing.List[typing.List[typing.Union[int, typing.Literal['nan'], typing.Literal['inf'], typing.Literal['-inf']]]]
  ellipses: typing.Tuple[typing.Union[int, None], typing.Union[int, None]]

def anndata_from_gctx(file: File):
  with file_as_path(file, 'r') as fr:
    import h5py
    f = h5py.File(fr, 'r')
    return ad.AnnData(
      X=f['0']['DATA']['0']['MATRIX'],
      obs=f['0']['META']['0']['ROW'],
      var=f['0']['META']['0']['COL'],
    )

def anndata_from_gct(file: File):
  with file_as_stream(file, 'r') as fr:
    import pandas as pd
    version = fr.readline()
    shape = list(map(int, fr.readline().split('\t')))
    columns = fr.readline().split('\t')
    df = pd.read_csv(fr, sep='\t', header=columns)
    return ad.AnnData(
      X=df.iloc[-shape[1]:],
      obs=df.iloc[:-shape[1]],
    )

def anndata_from_file(file: File):
  ''' Read from a bunch of different formats, get an anndata file
  '''
  if file['filename'].endswith('.h5ad'):
    with file_as_path(file, 'r') as fr:
      return ad.read_h5ad(fr)
  elif file['filename'].endswith('.csv'):
    with file_as_stream(file, 'r') as fr:
      return ad.read_text(fr, delimiter=',').transpose()
  elif file['filename'].endswith('.tsv'):
    with file_as_stream(file, 'r') as fr:
      return ad.read_text(fr, delimiter='\t').transpose()
  elif file['filename'].endswith('.txt') or file['filename'].endswith('.tab') or file['filename'].endswith('.data'):
    with file_as_stream(file, 'r') as fr:
      return ad.read_text(fr, delimiter=None).transpose()
  elif file['filename'].endswith('.xlsx'):
    with file_as_path(file, 'r') as fr:
      return ad.read_excel(fr).transpose()
  elif file['filename'].endswith('.gctx'):
    return anndata_from_gctx(file)
  elif file['filename'].endswith('.gct'):
    return anndata_from_gct(file)
  elif file['filename'].endswith('.h5'):
    with file_as_path(file, 'r') as fr:
      return ad.read_hdf(fr).transpose()
  else:
    raise NotImplementedError

def np_jsonifyable(x):
  x_ = x.astype('object')
  x_[np.isnan(x)] = 'nan'
  x_[np.isposinf(x)] = 'inf'
  x_[np.isneginf(x)] = '-inf'
  return x_.tolist()

def gene_count_matrix(file: File) -> GeneCountMatrix:
  ''' We'll preserve the file url but include various properties useful
  for visualization. If the file is invalid, reading it will fail.
  '''
  d = anndata_from_file(file)
  # we want to see the gene count matrix preview in transposed form
  d = d.transpose()
  if d.shape[0] >= 10:
    top = 5
    bottom = 5
  elif d.shape[0] > 5:
    top = 5
    bottom = d.shape[0] - top
  else:
    top = d.shape[0] - 1
    bottom = 1
  if d.shape[1] >= 10:
    left = 5
    right = 5
  elif d.shape[1] > 5:
    left = 5
    right = d.shape[1] - left
  else:
    left = d.shape[1] - 1
    right = 1

  index = np.concatenate([d.obs_names[:top], d.obs_names[-bottom:]]).tolist()
  columns = np.concatenate([d.var_names[:left], d.var_names[-right:]]).tolist()
  values = np_jsonifyable(np.concatenate([
    np.concatenate([d.X[:top, :left], d.X[:top, -right:]], axis=1),
    np.concatenate([d.X[-bottom:, :left], d.X[-bottom:, -right:]], axis=1),
  ]))
  ellipses = [
    top if len(index) != d.shape[0] else None,
    left if len(columns) != d.shape[1] else None,
  ]
  return dict(
    file,
    shape=d.shape,
    index=index,
    columns=columns,
    values=values,
    ellipses=ellipses,
  )

def transpose(m: File):
  d = anndata_from_file(m)
  d = d.T
  with upsert_file('.h5ad') as f:
    d.write_h5ad(f.file)
  return gene_count_matrix(f)
"""