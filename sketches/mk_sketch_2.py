#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

import argparse
import json
import sys
import time
import socket
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
import mmh3
from statistics import mean, median


NUM_OF_HASH_FUNCTIONS = 10
fileTailLengths = [0]*NUM_OF_HASH_FUNCTIONS
SIZE_GROUP = 5


def msg_process(msg):
    # Print the current time and the message.
    time_start = time.strftime("%Y-%m-%d %H:%M:%S")
    val = msg.value()
    dval = json.loads(val)
    # print(time_start, dval)
    return time_start, dval['User_ID_N']


def get_tail_length(bitArr):
    """ Calculates the number of 0s at the end of the bitstring """
    bitStr = str(bitArr)
    return len(bitArr) - len(bitStr.rstrip('0'))

def process_line(line):
    """ takes a string, applies 10 hash functions on it 
    returns a list of tail lengths for each hash function """
# =============================================================================
# get the hash values for each fxn and convert it to bit string
# =============================================================================
    binaryHashValues = [format(mmh3.hash(line, seed=i, signed=False), '032b') for i in range(0,NUM_OF_HASH_FUNCTIONS)]
# =============================================================================
# get the tail length for each hash fxn
# =============================================================================
    tailLengths = [get_tail_length(val) for val in binaryHashValues]
    return tailLengths

def process_one_file(dval):

    global fileTailLengths

    #get the tail length for each hash function
    tailLengths = process_line(dval)
    #get the maximum tail length for each hash function
    for i in range(0,NUM_OF_HASH_FUNCTIONS):
        fileTailLengths[i] = max(fileTailLengths[i], tailLengths[i])

    return fileTailLengths


def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    #parser.add_argument('k', type=str,
    #                    help='The number of bits of hash to use as a bucket number.')

    args = parser.parse_args()
    
    conf = {'bootstrap.servers': 'localhost:9092',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': socket.gethostname()}

    consumer = Consumer(conf)

    running = True

    # Flajolet Martin
    # ---------------

    # open a stream to send sketch queries
    conf = {'bootstrap.servers': "localhost:9092",
            'client.id': socket.gethostname()}
    producer = Producer(conf)

    R_old = 0

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
                # Sketch update 
                time_start, dval = msg_process(msg)
                process_one_file(dval)
                R = mean([median(fileTailLengths[i:i+SIZE_GROUP]) for i in range(0,NUM_OF_HASH_FUNCTIONS, SIZE_GROUP)])
               
                if(R==R_old):
                    pass
                else:
                    # send the result to a tream 
                    flajolet_count = str(round(2**R))
                    producer.produce('mk_sketch_2', key='Flajolet', value= flajolet_count)
                    producer.flush()

                R_old = R
                #print("R is ", R)
                time_start = time.strftime("%Y-%m-%d %H:%M:%S")
                print(time_start, " Unique count of users ID is ", 2**R)
               

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
