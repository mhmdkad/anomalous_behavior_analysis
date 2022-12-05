Clone the Git repo and start the Kafka cluster
```
git clone \\this repo
cd anomalous_new/
docker-compose -f ./anomalous_new/docker-compose.yml up -d --build
```

Create a test topic, send and receive messages
```
docker-compose -f anomalous_new/docker-compose.yml exec broker kafka-topics --create --bootstrap-server localhost:9092 --topic test-stream
docker-compose -f anomalous_new/docker-compose.yml exec broker kafka-console-producer --broker-list localhost:9092 --topic test-stream
docker-compose -f anomalous_new/docker-compose.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic test-stream --from-beginning
```

Start Kafka Producer with test data
```
docker build ./producer -t kafka-producer
docker run --network="anomalous_new_default" -it kafka-producer
```

Kafka consumer for anomaly detection training \run in powershell
```
docker build ./Consumer_ML_Training -t kafka-consumer-training
docker run --network="anomalous_new_default" --volume ${pwd}/data:/data:rw -it kafka-consumer-training
```

Kafka Consumer for evaluating the anomaly detection
```
docker build ./Consumer_Prediction -t kafka-consumer-prediction
docker run --network="anomalous_new_default" --volume ${pwd}/data:/data:ro -it kafka-consumer-prediction
```

Scaling anomaly detection
```
docker-compose -f anomalous_new/docker-compose.yml exec broker kafka-topics --alter --zookeeper zookeeper:2181 --topic anomalous_behaviour --partitions 2
docker run --network="anomalous_new_default" --volume ${pwd}/data:/data:ro -it kafka-consumer-prediction
```