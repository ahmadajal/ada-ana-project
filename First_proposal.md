# Project proposal
Nooshin Mirzadeh, Amir Shaikhha and Asmae Tounsi

## Abstract
In this project, we aim to analyze geolocated social media data in order to produce a Swiss clone of the Maps developed by the goodcitylife team, more specifically, a happy map of the city of Lausanne.	
The goal of this work is to proceed in building a map of Lausanne that is supposed to suggest not only the shortest route when providing directions to a specific place, but also the happiest one. We are going to analyze a geolocated dataset of tweets from 2012, instagram and news from Jan to Aug 2016 and transfer them into quantitative measures of the locations’ perceptions, upon which the more pleasant routes could be defined.

## Architecture
In this system, we extract the information related to different places in a city from tweets or instagram photos, and connect them to the city map. Based on this assumption, we propose a system with three main components:
  1. **Data Extractor**: The first component is responsible for extracting the necessary and relevant information (e.g., keywords, tags, location information, etc.) from the provided data.
  2. **Data Analyzer**: The second component uses this extracted information to associate a particular property with each location (e.g., using machine learning for specifying whether a location is smelly or beautiful). 
  3. **Visualizer**: The last component is responsible for visualizing the result information (e.g., specifying on a map the happiness of the different locations of a city).
  
## Data Description
To be able to give points to different locations in a city, we need two different sets of data: 
  1. **Mapping Data**: It includes the information about the city’s street segments. This information is freely available online on OpenStreetMap (OSM). We will use the Lausanne map for this purpose. 
  2. **Input Data**: To extract the information of different locations in the city, we will analyze the geolocated tweets in Switzerland. This dataset is available for the course from 2012. Moreover, the instagram images in Switzerland are available as well. We need to extract the information about the happiness (or smell) of different locations based on the geolocated tweets. To do that, first, we need to classify the tweets based on their language. We expect tweets in French, English, and German in Lausanne. 

## Feasibility and Risks
Considering that we are going to be supervised by one of the goodcitylife team’s members, and that some papers related to their project have been published and describe the methods and approaches used, the project seems to be feasible.
To be more accurate, we consider the different requirements for the project. 
  * **Data**: the dataset is available by the course in Switzerland, and there is no need to collect data in this project.
  * **Infrastructure**: We are provided by IC clusters, and we are able to run the algorithms on big data.
  * **Background**: We have worked with Spark, and have the basic knowledge from the course.
  * **Time**: We have almost three months to finish the project. We assumed some realistic planning in the following section. 
  
However, the project poses some risks and challenges for us, mostly related to the input dataset:

  * **The language of the tweets**: Dealing with the tweets data requires certainly some Natural language processing, and the tweets geolocated in Lausanne are more likely to be in French, English and German. As only one member of the team speaks French fluently , and none of us speaks German, one of the risks will be the “Language of the tweets”.
  * **Analyzing Big Data**: For this project, we will have a dataset of geolocated tweets, Instagram posts and news from 2012. Dealing with such a big dataset can surely pose some risks to first understand the data, address data quality, find algorithms to display meaningful results and deal with the outliers.
  * **The amount of geolocated data**: The location information in tweets, instagram posts and news might not be complete or precise. One of the risks will be that the geolocation informations in the dataset would not cover enough places of the city, making the creation of the city graph, and the validation of the results harder.
  
## Deliverables
We envision the following deliverables for our project. There are some deliverables that are optional, in the sense that if we are finished with the other parts soon enough we can proceed with the optional parts.

  1. Twitter data investigation: in this phase we would like to investigate the tweeter data for the following purposes. a) see the distribution of the languages used in the tweets in Switzerland, b) see the distribution of the location of these tweets, and c) visualizing the mentioned information. At this phase, we need to access the twitter data and use Spark in order to pre-filter and investigate the relevant data.
  2. Data analysis on a sample data: based on the information collected from the previous phase, we pick a sample of data in order to perform the full pipeline on a single machine. As an example, we only use a sample of tweets related to a particular neighbourhood (e.g., Lausanne city center), and perform the machine learning task to assign properties to different locations. Finally, visualizing this information on a map.
  3. Data analysis on the whole data: at this phase we implement the data extraction and the data analytics parts for the big data (e.g., by using Spark on the IC cluster).
  4. (Optional) Performing a route recommending, based on the associated properties to different locations, and based on the user preferences.
  5. (Optional) Extend the first component of the pipeline to use the instagram data as well. This phase involves extracting tags from the instagram pictures. However, the rest of the pipeline, does not need that much changes.
  6. (Optional) Adding more cities to the project.

## Timeplan

We would like to be in a reasonable state of the phase 2 until mid December. Hopefully by then we will have better ideas of how many of the phases we can deliver by the end of the semester.

  * Twitter data investigation :  2 weeks (first deadline: 20.11.2016)
  * Data analysis on a sample data : 4 weeks (first deadline: 18.12.2016) 
  * Data analysis on the whole data : 3 weeks (first deadline: 15.01.2017)
  * Route performing : 2 weeks [optional]
  * Extension - Instagram data : 2 weeks [optional]
  * Extension - more cities : 2 weeks [optional]
  
The first three parts of the project are interdependent, and can not be done in parallel. Therefore, if we have time to move into the optional parts, we are planning to do the route performing and the Instagram data extension in parallel.
