#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
import nibabel as nib
import numpy as np
from nibabel import load, save, Nifti1Image
import argparse
from scilpy.io.utils import (add_force_b0_arg, add_overwrite_arg,
                             add_sh_basis_args, assert_inputs_exist,
                             assert_outputs_exist)


# In[ ]:


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('in_odf',
                   help='Path of the ODF volume, generated from dipy pipeline')

    p.add_argument('out_odf',
                   help='Name of the output.')
    
    
    
    return p


# In[3]:


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()	

    assert_inputs_exist(parser, args.in_odf)
    assert_outputs_exist(parser, args, args.out_odf)

    fodf_data = nib.load(args.in_odf)
    fodf = fodf_data.get_fdata()
    
    len_seq = np.shape(fodf)[-1]
    
    if len_seq == 45:
    	     
    	tran = np.ones([45])
    	index = [1,4,6,8,11,13,15,17,19,22,24,26,28,30,32,34,37,39,41,43]
    	tran[index] = -1
    	
    	new_odf = fodf*tran 
        

    	out = Nifti1Image(new_odf, header=fodf_data.header, affine=fodf_data.affine)
    	save(out, args.out_odf)
    
    
    
    elif len_seq == 28:
    	     
    	tran = np.ones([28])
    	index =   [1,4,6,8,11,13,15,17,19,22,24,26]
    	tran[index] = -1
    	
    	new_odf = fodf*tran 
        

    	out = Nifti1Image(new_odf, header=fodf_data.header, affine=fodf_data.affine)
    	save(out, args.out_odf)
    	
    elif len_seq == 15:
    	     
    	tran = np.ones([15])
    	index =   [1,4,6,8,11,13]
    	tran[index] = -1
    	
    	new_odf = fodf*tran 
        

    	out = Nifti1Image(new_odf, header=fodf_data.header, affine=fodf_data.affine)
    	save(out, args.out_odf)
    
    	
    else:
    	print('ODF order should be 4 or 6 or 8.')
    

# In[5]:
if __name__ == '__main__':

    main()


