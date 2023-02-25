# webscrapping
A place with a bunch of webscrapping Python scripts.

Each case study is stored in a folder within the repository.

Projects in this repo:

## knmi_climate_explorer

The aim was to get meteorology data that is stored on The KNMI Climate Explorer web application, e.g. NOAA Climate Prediction Center North Atlantic Oscillation monthly index. The workflow is:
* Given url, get raw tabular data which is stored as plain text
* Preprocess the data and store it in a dataframe
* Save the dataframe to pickle file