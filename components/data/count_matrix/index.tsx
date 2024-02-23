import React from 'react'
import { MetaNode } from '@/spec/metanode'
import { FileURL, FileC } from '@/components/core/file'
import python from '@/utils/python'
import { z } from 'zod'
import { datafile_icon, file_transfer_icon, transpose_icon } from '@/icons'
import dynamic from 'next/dynamic'
import { downloadUrl } from '@/utils/download'

const Matrix = dynamic(() => import('@/app/components/Matrix'))

// How the schema validation works: https://codex.so/zod-validation-en
// Define codec here later
//export const CountMatrixC = ;
//export type CountMatrixType = z.infer<typeof CountMatrixC>

// Mano: This file is based on Daniel's original file gene_count_matrix/index.tsx
// Mano: Generalized to generate for both Gene and Metabolite in one go
export const TCountMatrix = [
  { id: 'Gene' },
  { id: 'Metabolite' },
].map(({id}) => MetaNode(`[${id}]CountMatrix`)
  .meta({
    label: `${id} Count Matrix`,
    description: `A ${id.toLowerCase()} count matrix file`,
    icon: [datafile_icon],
  })
  .codec(FileC.merge(z.object({
    shape: z.tuple([z.number(), z.number()]),
    columns: z.array(z.string()),
    index: z.array(z.string()),
    values: z.array(z.array(z.union([z.number(), z.literal('nan'), z.literal('inf'), z.literal('-inf')]))),
    ellipses: z.tuple([z.union([z.number(), z.null()]), z.union([z.number(), z.null()])]),
  })))
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
) // matches map
// The two resolver names will be: GeneCountMatrix & MetaboliteCountMatrix
export const GeneCountMatrix = TCountMatrix[0];
export const MetaboliteCountMatrix = TCountMatrix[1];
  
export const TCountMatrixFromFile = [
  { id: 'Gene'},
  { id: 'Metabolite' },
].map(({id}, i) => MetaNode(`[${id}]CountMatrixFromFile`)
 .meta({
    label: `Resolve a ${id} Count Matrix from a File`,
    description: `Ensure a file contains a ${id.toLowerCase()} count matrix, load it into a standard format`,
    icon: [file_transfer_icon],
  })
  .inputs({ file: FileURL })
  .output(TCountMatrix[i])
  .resolve(async (props) => await python(
    'components.data.count_matrix.count_matrix',
    { kargs: [props.inputs.file] },
    message => props.notify({ type: 'info', message }),
  ))
  .story(props =>
    `The file${props.inputs && props.inputs.file.description ? ` containing ${props.inputs.file.description}` : ''} was parsed as a ${id.toLowerCase()} count matrix.`
  )
  .build()
)
export const GeneCountMatrixFromFile = TCountMatrixFromFile[0];;
export const MetaboliteCountMatrixFromFile = TCountMatrixFromFile[0];;

export const TTranspose = [
  { id: 'Gene'},
  { id: 'Metabolite' },
].map(({id}, i) => MetaNode(`[${id}]Transpose`)
 .meta({
    label: 'Transpose',
    description: 'Re-orient the matrix',
    icon: [transpose_icon],
  })
  .inputs({ file: TCountMatrix[i] })
  .output(TCountMatrix[i])
  .resolve(async (props) => await python(
    'components.data.count_matrix.transpose',
    { kargs: [props.inputs.file] },
    message => props.notify({ type: 'info', message }),
  ))
  .story(props =>
    `The ${id.toLowerCase()} count matrix was then transposed.`
  )
  .build()
)
export const GeneTranspose = TTranspose[0];
export const MetaboliteTranspose = TTranspose[0];
