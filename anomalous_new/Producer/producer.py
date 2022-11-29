from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from datetime import datetime
import pandas as pd
import json
import time

class MyProducer:
    '''Avro producer for Kafka'''

    def __init__(self):

        # This is the Avro Schema for messages
        self.value_schema_str = """
        {  "name": "Join Time",
           "type": "record",
           "fields" : [
             {"name" : "Start Time", "type" : "long"}
           ]
        }"""
        self.value_schema = avro.loads(self.value_schema_str)

        self.avroProducer = AvroProducer({
            'bootstrap.servers': 'broker:29092',
            'on_delivery': self.delivery_report,
            'schema.registry.url': 'http://schema-registry:8081'
            }, default_value_schema=self.value_schema)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush().
            Source: https://github.com/confluentinc/confluent-kafka-python
        """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def main():

    #read data
    df_data = pd.read_csv("data.csv", parse_dates=["Start Time"], index_col="Start Time")
    # df = pd.read_csv("data.csv")
    # df_data = pd.pivot_table(df,values='actuals',index='load_date',columns='metric_name')
    # metrics_df.reset_index(inplace=True)
    # metrics_df.fillna(0,inplace=True)
    # metrics_df
    # df_disk = pd.read_csv("ec2_disk_write_bytes_c0d644.csv", parse_dates=["timestamp"], index_col="timestamp")
    # df_cpu = pd.read_csv("ec2_cpu_utilization_c6585a.csv", parse_dates=["timestamp"], index_col="timestamp")

    # concatenate data
    # df_concat = pd.concat([df_network, df_disk, df_cpu], axis=1)
    # df_concat.columns= ["network", "disk", "cpu"]

    # timeseries overlap from 2022-07-12 till 2022-07-12
    # mask_earliest = df_data.index > pd.Timestamp('2022-07-12 00:04:00')
    # mask_latest = df_data.index < pd.Timestamp('2022-07-25 14:20:00')
    # df_concat = pd.concat([mask_earliest, mask_latest])

    # disk is measured at multiples of 5 minutes, whereas cpu and network is measured at minutes 04, 09, 14 etc.
    # therefore we do a foreward fill with disk and delete nans
    # df_concat["disk"] = df_concat.disk.ffill()
    # df_concat = df_concat.dropna(axis=0)

    # reset index as we want to include the timestamp in json
    df_data.reset_index(inplace=True)

    # convert to json
    json_records = json.loads(df_data.to_json(orient="records"))

    # Producer
    producer = MyProducer().avroProducer

    # publish to kafka topic
    # as this is simulation, between pushes is a break of 1 second (instead of 5 minutes, as is the case in the data)
    for record in json_records:
        producer.produce(topic='anomalous_behaviour', value=record)
        producer.flush()
        time.sleep(1)


if __name__ == '__main__':
    main()
