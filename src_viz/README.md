# Preparing the data for visualization

## Data mapping

The corresponding code is in the notebook "Mapping_Locations.ipynb".

It generates a file "data/location_to_canton.csv", containing the maximum of locations in the unique locations file "data/locations.txt" that can be mapped to a canton, with their corresponding cantons.

## Statistical analysis and Pre-visualization

The corresonding source code is "viz_data.py".
For each month, we have the following pipeline : 

- Read the english, german and french scored tweets

- map the tweets to their canton using  "data/location_to_canton.csv"

- statistical analysis of the aggregated data of the month :
    - group the data by canton
    - do some statistical tests to compare the tweets' population of each canton to the others
    - writing the results in a json file 
    
- statistical analysis of the aggregated data of each day, and writing the results in json files



