# Anomalous Customer Behavior Analysis

## Architecture:
The plan of this project is to stream data about customers behavior and apply real-time analysis on it. <br/>
First, with the given tabular data, another data will be generated having similar statistical properties as the input dataset. <br/>
This later will be streamed through Kafka where minimum 8 sketches will be implemented representing real-time analysis of the streamed data and then will be stored in HBase database. <br/>
For visualizing the sketche's results, different dashboards will be implemented, Grafana, kibana or tableau can be used for the purpose. <br/>
Everything used from step of streaming will be containerized as Docker containers.
