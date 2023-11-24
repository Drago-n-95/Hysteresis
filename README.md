# Analysis of data taken from VFTB and VSM

When the script for VFTB is started the user will be prompted to load a file with ".rmp" extension.

When the script for VSM is started the user will be prompted to load consecutively 3 files - with ".hys" (currently the script works only with the .hys file which is corrected for paramagnetic component), 
".irm" and ".coe" extensions respectively. If one of the files is not loaded the figures will not be generated.

## VFTB heating/cooling curves
Plots the heating and cooling curve, as well as the first derivative of that curve

![2-5_VFTB_heating_curve](https://github.com/Drago-n-95/Hysteresis/assets/52564717/19159629-0498-4ed4-bb30-b68676026312)

## VSM data analysis
Plots 4 figures:

1. Hysteresis loop, corrected for paramagnetic component. The values for Ms, Mrs and Bc are displayed, as well as
a figure with the uncorrected hysteresis loop.

2. IRM acquisition curve - value for IRM is displayed in the figure

3. Back-field curve - value for Bcr is displayed in the figure

4. Day plot, using the Ms, Mrs, Bc and Bcr values gotten from the Hysteresis loop and the back-field curve

![2-5_VSM_analysis](https://github.com/Drago-n-95/Hysteresis/assets/52564717/fff59593-2e5b-4a74-be0a-9041096be7ca)

