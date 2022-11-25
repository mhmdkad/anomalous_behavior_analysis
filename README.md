# anomalous_behavior_analysis
## Purpose
Analyze incoming streams of customer behavior data in a content delivery network environment. Detect novel usage patterns in near real-time. Store the data. Transfer the data to glacier storage (slow, but high capacity storage) in a different platform. Create multiple dashboards with relevant visualizations.
## Pipeline Architecture
![Pipeline](./final_arch.jpg)
<br>
Summary:<br> A mock stream will be created using the excel file, it will be streamed into a topic in Kafka. We will have multiple consumers subscribed to this topic (each sketch will be a consumer reading the data from the topic in real time). Each student will create 2 consumers (2 sketches), they will be written in Flink or KStreams which are libraries we can use for real time processing (will be decided by tonight). The sketches will save the data in a table in HBase. In Hbase we will also have a table that will store the raw data in order to be able to synthesize it and save the synthesized data in a new table (we will use a library in python in order to synthesize the data). Then there will be a visualization open source technology connected to HBASE which will show visualizations in real time.

## How to Run this pipeline
Check file called HOW TO in this repo.
