# MidRISH
Code for implementing MidRISH!

# Dependencies
* MRTrix
* ScilPy
* Python3.8

# I. Template Creation
Choose data to be included in the template. [] reccomends 16-20 matched subjects at minimum. I have used the maximal matched subset of my data. 
First, we model the signal as it's spherical harmonic representation. The user sets the max order for this data. This is based on (1) the number of directions and (2) the distribution of those directions. If the directions are not well distributed, you may have to go down an order. 
Then, we calculate the rotationally invariant spherical harmonics (RISH). 
Finally, we compute a template that combines all RISH features. 

# II. Template Application
Once a template has been created, we can harmonize our data! 
In this code, we do the following steps:
* Estimate signal with Nth order spherical harmonic representation.
* Apply MidRISH template.
* Reconstruct signal function (b0 images will all be ones).
* Fit a tensor model.

# Caveat: My data has different b-values, what do I do?
My data is within 500 < b < 1500 

-> For RISH to be most effective, we believe we need to project the signal to the same b-value. 

My data has bigger differences than this...

-> Unfortunatly, we cannot support large b-value jumps at this time (ex. b=1000, b=2000) :(
