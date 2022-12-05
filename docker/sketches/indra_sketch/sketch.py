#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

import argparse
import json
import sys
import time
import socket
from confluent_kafka import Consumer, KafkaError, KafkaException
import numpy as np
from probables import (BloomFilter)
# import mmh3


def msg_process(msg):
    # Print the current time and the message.
    time_start = time.strftime("%Y-%m-%d %H:%M:%S")
    val = msg.value()
    dval = json.loads(val)
    device = dval['Device']
    blm = BloomFilter(est_elements=1000, false_positive_rate=0.05)
    blm.add('Android TV')
    a = blm.check(device)  # should return False
    if a is True:
    # blm.check('google.com')  # should return True
        print(time_start, 'Definitely is', a, 'using Android TV')
    else:
        print(time_start, 'Probably not using Android TV Device')
    
    # return time_start, dval['User_ID_N']
    

def main():

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    #parser.add_argument('k', type=str,
    #                    help='The number of bits of hash to use as a bucket number.')

    args = parser.parse_args()
    
    conf = {'bootstrap.servers': 'localhost:29094',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': socket.gethostname()}

    consumer = Consumer(conf)

    running = True

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
                msg_process(msg)
               

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
