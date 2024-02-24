import React from 'react'
import { MetaNode } from '@/spec/metanode'
import python from '@/utils/python'
import { MetaboliteCountMatrix } from '@/components/data/metabolite_count_matrix'
import { GeneCountMatrix } from '@/components/data/gene_count_matrix'
//import { MetaboliteCountMatrix } from '@/components/data/count_matrix'
//import { GeneCountMatrix } from '@/components/data/count_matrix'
import { norm_icon } from '@/icons'

import { FileURL, FileC } from '@/components/core/file'
import { z } from 'zod'
import { datafile_icon, file_transfer_icon, transpose_icon } from '@/icons'
import dynamic from 'next/dynamic'
import { downloadUrl } from '@/utils/download'

import { CountMatrixC } from '@/components/data/count_matrix'

const Matrix = dynamic(() => import('@/app/components/Matrix'))

/*
export const CountMatrixC = FileC.merge(z.object({
  shape: z.tuple([z.number(), z.number()]),
  columns: z.array(z.string()),
  index: z.array(z.string()),
  values: z.array(z.array(z.union([z.number(), z.literal('nan'), z.literal('inf'), z.literal('-inf')]))),
  ellipses: z.tuple([z.union([z.number(), z.null()]), z.union([z.number(), z.null()])]),
}))
*/

export const CorrelationMatrix = MetaNode('CorrelationMatrix')
  .meta({
    label: 'Correlation Matrix',
    description: 'A correlation matrix file',
    icon: [datafile_icon],
  })
  .codec(CountMatrixC)
  .view(props => {
    return (
      <div>
        <Matrix
          index={props.index}
          columns={props.columns}
          values={props.values}
          ellipses={props.ellipses}
          shape={props.shape}
          downloads={{
            'URL': () => downloadUrl(props.url, props.filename)
          }}
        />
      </div>
    )
  })
  .build()

export const ComputeMetaboliteCorrelationMatrix = MetaNode('ComputeMetaboliteCorrelationMatrix')
  .meta({
    label: 'Compute Correlation Matrix for a Metabolite Count Matrix',
    description: 'Compute Correlation Matrix for a Metabolite Count Matrix, return a Correlation matrix',
    icon: [norm_icon],
  })
  .inputs({ matrix: MetaboliteCountMatrix})
  .output(CorrelationMatrix)
  .resolve(async (props) => await python(
    'components.data.count_matrix_corr.compute_corr_count_matrix',
    { kargs: [props.inputs.matrix]  },
    message => {props.notify({ type: 'info', message }); console.log(message);},
  ))
  .story(props =>
    `Correlation for the metabolite count matrix was computed.`
  )
  .build()

  export const ComputeGeneCorrelationMatrix = MetaNode('ComputeGeneCorrelationMatrix')
  .meta({
    label: 'Compute Correlation Matrix for a Gene Count Matrix',
    description: 'Compute Correlation Matrix for a Gene Count Matrix, return a Correlation matrix',
    icon: [norm_icon],
  })
  .inputs({ matrix: GeneCountMatrix})
  .output(CorrelationMatrix)
  .resolve(async (props) => await python(
    'components.data.count_matrix_corr.compute_corr_count_matrix',
    { kargs: [props.inputs.matrix]  },
    message => {props.notify({ type: 'info', message }); console.log(message);},
  ))
  .story(props =>
    `Correlation for the gene count matrix was computed.`
  )
  .build()

  export const ComputeMetaboliteGeneCorrelationMatrix = MetaNode('ComputeMetaboliteGeneCorrelationMatrix')
  .meta({
    label: 'Compute Correlation Matrix between Metabolite and Gene Count Matrices',
    description: 'Compute Correlation Matrix between Metabolite and Gene Count Matrices, return a Correlation matrix',
    icon: [norm_icon],
  })
  .inputs({ matrix1: MetaboliteCountMatrix, matrix2: GeneCountMatrix})
  .output(CorrelationMatrix)
  .resolve(async (props) => await python(
    'components.data.count_matrix_corr.compute_corr_count_matrix2',
    { kargs: [props.inputs.matrix1, props.inputs.matrix2]  },
    message => {props.notify({ type: 'info', message }); console.log(message);},
  ))
  .story(props =>
    `Correlation between the metabolite and gene count matrices was computed.`
  )
  .build()
