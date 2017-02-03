# Various scripts written in Scala

## Json Parsing
The corresponding source code is [JsonParser.scala](JsonParser.scala).

To run it, in sbt console use the following command:
```
ch.epfl.ada.JsonParser.preprocess(MONTH_NUMBER)
```
where `MONTH_NUMBER` is the corresponding month that we would like to preprocess its json files.

## Visualization Data Preparation
The corresponding source code is [VizDataPrep.scala](VizDataPrep.scala).


To run it, in sbt console use the following command:

```
ch.epfl.ada.VizDataPrep.writeVizData()
```

## Unique locations
The corresponding scripts for retrieving unique locations are provided in [SparkScript.sc](SparkScript.sc).