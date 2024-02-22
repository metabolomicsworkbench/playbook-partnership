import React from 'react'
import { MetaNode } from '@/spec/metanode'
import python from '@/utils/python'
import { MetaboliteCountMatrix } from '@/components/data/metabolite_count_matrix'
import { norm_icon } from '@/icons'


export const ComputeCorrelationMatrix = MetaNode('ComputeCorrelationMatrix')
  .meta({
    label: 'Compute Correlation Matrix for a Metabolite Count Matrix',
    description: 'Compute Correlation Matrix for a Metabolite Count Matrix, return a Correlation matrix',
    icon: [norm_icon],
  })
  .inputs({ matrix: MetaboliteCountMatrix })
  .output(MetaboliteCountMatrix)
  .resolve(async (props) => await python(
    'components.data.metabolite_count_matrix_corr.compute_corr_metabolite_count_matrix',
    { kargs: [props.inputs.matrix]  },
    message => {props.notify({ type: 'info', message }); console.log(message);},
  ))
  .story(props =>
    `Correlation for the metabolite count matrix was computed.`
  )
  .build()
