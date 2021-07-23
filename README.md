# blender-totally-tubular
Apply averaged cross sectional weights following tubular topography, starting with the edge of one end of the tube selected. Great for fixing weird hair weight painting on individual strands where weights differ on one side of the tube to the other, resulting in a smearing effect. This fixes that.

Another use case is if you make a contorted tube-ish polygonal surface and want to apply weights for an armature, this will even out the weights along the tube so that smearing does not occur.

![Example Video](https://github.com/llealloo/blender-totally-tubular/blob/main/Docs/Example_AutomaticWeights_Tubular.gif)

## To install
* Download the TotallyTubular.py and install through Blender Preferences -> Add-ons -> Install.
* Tick the check box next to "Mesh: Totally Tubular" to enable it in the program. You're done!

## To use
- Get your weight painted tube pretty close
- Select the first ring / cross section of the tube
- Click the "Tubularize Weights" button in the Edit panel in Edit mode

## NOTES
* This script will fail if topology is not tubular and/or if the starting selection does not reside at one end of the tube.
