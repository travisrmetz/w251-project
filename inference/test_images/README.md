# Celestial Inference at the Edge
## W251 - Final Project - Tozzi/Metz - Summer 2020
### Generating Random Test Images to Use in Inference Testing

This folder contains programs for creating test images used in inference testing.  

The `test_image.yml` file specifies the geographic box and number of images to generate, and provides the directory for storage.

`bash generate_test.sh` is used to initiate the generation.  It first deletes any prior images that had been generated.

`generate_test.py` writes Stellarium script and actually gets screenshot captures saved.