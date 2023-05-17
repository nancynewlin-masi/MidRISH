import nibabel as nib
import numpy as np
import sys

#example: /nfs/masi/newlinnr/VMAP_cr3/028_VMAP_209306/template_subj.nii.gz
saveloca2b = sys.argv[3]
savelocb2a = sys.argv[4]
# read in template 0-6
a = nib.load(sys.argv[1]).get_fdata()
b = nib.load(sys.argv[2]).get_fdata()

b2a = a/b;
a2b = b/a;
a2b[a==0]=1
a2b[b==0]=1
b2a[a==0]=1
b2a[b==0]=1
aff = nib.load(sys.argv[1]).affine
nib.save(nib.Nifti1Image(a2b, aff), saveloca2b)
nib.save(nib.Nifti1Image(b2a, aff), savelocb2a)

print("Successfully combined template and saved at",saveloca2b)
print("Successfully combined template and saved at",savelocb2a)

