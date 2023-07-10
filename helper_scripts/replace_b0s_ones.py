
import nibabel as nib
import numpy as np
from dipy.io import read_bvals_bvecs

def replace_b0s(args):
    #collect bvals/bvecs into lists
    # this is lazy, should just read b-vals so we don't have to pass b-vecs
    bvals,bvecs = read_bvals_bvecs(
        args.bvals, args.bvecs
    )

    from_scan = nib.load( args.FROM ).get_fdata()
    to_scan_nib = nib.load(args.TO)
    to_scan = nib.load( args.TO ).get_fdata()
    to_scan_obj = nib.load( args.TO ).header

    for idx, b in enumerate(bvals):
        if b < args.bval_thold:
            to_scan[...,idx] = np.ones((from_scan[...,idx]).shape)

    nib.save(
        nib.Nifti1Image(to_scan, to_scan_nib.affine, to_scan_nib.header),
        args.output
    )


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description=
"""
Moves b0s from '--from' into '--to', saving as '--output'
b-vals/b-vecs must be the same for both scans
"""
    )

    parser.add_argument("--from", dest="FROM")
    parser.add_argument("--to", dest="TO")
    parser.add_argument("--output")

    parser.add_argument("--bvals", default=None)
    parser.add_argument("--bvecs", default=None)
    parser.add_argument("--bval-thold", default=25.0, type=float)

    args = parser.parse_args()

    replace_b0s(args)
