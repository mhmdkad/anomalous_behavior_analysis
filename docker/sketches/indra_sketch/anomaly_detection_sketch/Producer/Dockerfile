# build docker image:
# docker build . -t kafka-producer

# run docker container:
# docker run --network="kafka_cluster_default" -it kafka-producer

FROM python:3.9.5

ADD ./requirements.txt ./
ADD ./producer.py ./
ADD ./data.csv ./

RUN pip install -r requirements.txt

CMD ["python",  "producer.py"]
