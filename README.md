# What Comes to Mind

## Overview
This repository contains the experiment files, data, preprocessing scripts, and analyses used to produce the paper, "XX" by Tracey Mills and Jonathan Phillips. 

## Directory Structure
This repository is organized as follows:

What Comes to Mind
* studies
* raw_data
   * study1
   * study2
   * study3
   * study4
      * generation
      * comparisons
      * ratings   
   * study5
   * study6
* preprocessing
   * study4
* clean_data
   * study1
   * study2
   * study3
   * study4
   * study5
   * study6
* data_analysis


## Mapping of studies in paper to file structure
The project was comprised of 6 studies, denoted in this repo and in the manuscript as studies 1-6.
Study 4 is comprised of 3 components, denoted throughout the repo as _generation_, _comparisons_, and _ratings_:
* _generation_ corresponds to the portion of the study in which participants freely generate category members
* _comparisons_ corresponds to the portion of the study in which participants list similarities and differences between category members
* _ratings_ corresponds to the portion of the study in which participants rate how well various features describe different category members


## Data and Analyses
Preprocessing is done on the raw data from each study to produce the clean data for analysis. The analysis code for each study can be found in the data_analysis directory. In this directory, analyses on the data from each study are conducted in the data_analysis.py file.