# What does Twitter Say about Swiss Happiness?
Nooshin Mirzadeh, Amir Shaikhha and Asmae Tounsi

## Abstract
In this project, we aim to analyze twitter's data in order to produce a Swiss Map based on the happiness of each canton.  
The goal of this work is to proceed in building a map of Switzerland that is supposed to show the happiness of people in each canton based on their tweets over time. We are going to analyze a dataset of tweets from Jan to Aug 2016 and transfer them into quantitative measures of the locations’ perceptions.


## Architecture
In this system, we extract the information related to different places in a city from tweets, and connect them to the canton map. Based on this assumption, we propose a system with the following main components:
  1. **Data Extractor**: The first component is responsible for extracting the necessary and relevant information (e.g., keywords, tags, location information, etc.) from the provided data. For this purpose, we use Spark. You can find more information in the [preprocessing directory] (preprocessing). 
  2. **Sentiment Analyzer**: The second component uses this extracted information to associate a particular polarity with each tweet. The code and documentation of this part can be found in [src_text] (src_text).
  3. **Pre Visualizer**: The third part is to aggregate the polarity of the tweets based on cantons, day, and month. So we have the prepared data for the visualization. To see how the data is reliable, we also provide some statistic analysis. You can find this information in [src_viz] (src_viz).
  4. **Visualizer**: The last component is responsible for visualizing the result information (e.g., specifying on a map the happiness of the different cantons). You can find this information in [visualization] (visualization). 
  
## Data Description
To extract the information of different locations in Switzerland, we will analyze the tweets in Switzerland. This dataset is available for the course from Jan to Aug 2016.

## Challenges
- **Big Data**: We need to use large-scale platforms, e.g., Spark
- **Lack of information**: Missing geo-located data. This is the main reason that forces us to change the whole project. 
- **Locations provided by users**:There are more than 21000 unique locations which include general and meaningless data, e.g., Switzerland, From Everywhere, , المملكة العربية السعودية, スイス.
- **Multi-lingual tweets**: Three official languages with various people from other countries with more various languages. Unfortuantely, The available resources in non-English languages are limited.

## Interactive Visualization
To see the result, please open the [swiss_happiness.html] (visualization/swiss_happiness.html) in your browser. 





