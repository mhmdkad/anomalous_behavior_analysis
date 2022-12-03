#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

import argparse
import json
import sys
import time
import socket
from confluent_kafka import Consumer, KafkaError, KafkaException
import math


def msg_process(msg):
    # Print the current time and the message.
    time_start = time.strftime("%Y-%m-%d %H:%M:%S")
    val = msg.value()
    dval = json.loads(val)
    # print(time_start, dval)
    return time_start, dval

def flajoletMartin(dval, total_zeroes, total_buckets, k):
    h = hash(str(dval)) #convert the value into a string because python hashes integers to themselves
    bucket = h & (total_buckets - 1) #Finds the bucket where the number of ending zero's are appended 
    bucket_hash = h >> k #move the bits of the hash to the right to use the binary digits without the bucket digits 
    total_zeroes[bucket] = max(total_zeroes[bucket], zero_counter(bucket_hash))
    
    return math.ceil(2 ** (float(sum(total_zeroes)) / total_buckets) * total_buckets * 0.79402), total_zeroes

def zero_counter(number):
    """Counts the number of consecutive 0's at the end of the number"""
    x = 0
    while (number >> x) & 1 == 0:
        x = x + 1
    return x


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()

    conf = {'bootstrap.servers': 'localhost:9092',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': socket.gethostname()}

    consumer = Consumer(conf)

    running = True

    # Flajolet Martin
    # ---------------
    """Estimates the number of unique elements in the input set values.
    Inputs:
    data: The data for which the cardinality has to be estimated.
    k: The number of bits of hash to use as a bucket number. The number of buckets is 2^k
    
    Output:
    Returns the estimated number of unique items in the dataset
    """

    k = 4
    total_buckets = 2 ** k
    total_zeroes = []
    for i in range(total_buckets):
        total_zeroes.append(0)


    try:
        while running:
            consumer.subscribe([args.topic])

            msg = consumer.poll(1)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    sys.stderr.write('Topic unknown, creating %s topic\n' %
                                     (args.topic))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                time_start, dval = msg_process(msg)
                distint_values, total_zeroes = flajoletMartin(dval, total_zeroes, total_buckets, k)
                print(distint_values)
               

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
