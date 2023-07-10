# Usage: bash get_RISH_features.sh [path to dwi] [path to bvec] [path to bval] [path to B0 image] [output path] [highest possible harmonic order for data]
export DWI=${1}
export BVEC=${2}
export BVAL=${3}
export B0=${4}
export OUTDIR=${5}
export SH_ORDER=${6}

export SH=${OUTDIR}/sh_norm.nii.gz

#echo "B-Value mapping if needed"
python3.8 bvaluemap.py ${DWI} ${B0} ${OUTDIR}/dwi_b1000.nii.gz 700 1000
export DWI=${OUTDIR}/dwi_b1000.nii.gz
export BVAL=${OUTDIR}/dwi_b1000.bval

# Spherical harmonic decomposition (calculated by least-squares linear fitting to amplitude data (diffusion signal))
rm ${OUTDIR}/sh_b4correction.nii.gz

echo "Spherical harmonic decomposition: amp2sh ${DWI} ${SH}"
amp2sh ${DWI} ${OUTDIR}/sh_b4correction.nii.gz  -fslgrad ${BVEC} ${BVAL} -normalise -lmax ${SH_ORDER}

echo "Fix the basis functions using dipy2mrtrix"
python3.8 dipy2mrtrix.py ${OUTDIR}/sh_b4correction.nii.gz ${SH}

echo "Remove ${OUTDIR}/sh_b4correction.nii.gz"
rm ${OUTDIR}/sh_b4correction.nii.gz

# Calculate Rotationally Invariant Spherical harmonic features
echo "Calculate RISH features"
python3.8  calculaterish.py ${OUTDIR} ${SH_ORDER} ${SH}

