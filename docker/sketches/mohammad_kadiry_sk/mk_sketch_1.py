#!/usr/bin/env python

"""Consumes stream for printing all messages to the console.
"""

import argparse
import json
import sys
import time
import socket
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
import random


def msg_process(msg):
    # Print the current time and the message.
    time_start = time.strftime("%Y-%m-%d %H:%M:%S")
    val = msg.value()
    dval = json.loads(val)
    device_used = dval['Device']
    if device_used == 'Android' :
        return True
    else:
        return False


class MorrisAlpha:
    def __init__(self, a=.05, bits=8, default=5):
        self.X = 0
        self.a = a
        self.bits = bits
        self.default = default
    def update(self):
        if self.X < self.default:
            self.X += 1
        elif self.X < (2 ** self.bits) - 1 and \
             random.random() < 1/((1 + self.a)**self.X):
            self.X += 1
    def query(self):
        if self.X <= self.default:
            return self.X
        return 1/self.a * (((1 + self.a)**self.X) - 1)

def main():

    # stream parsinng code 
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')

    args = parser.parse_args()

    conf = {'bootstrap.servers': 'localhost:29094',
            'default.topic.config': {'auto.offset.reset': 'smallest'},
            'group.id': socket.gethostname()}

    consumer = Consumer(conf)

    running = True

    # Sketch code
    morris = MorrisAlpha()

    # open a stream to send sketch queries
    conf = {'bootstrap.servers': "localhost:29094",
            'client.id': socket.gethostname()}
    producer = Producer(conf)

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
                # msg_process(msg)
                update_morries_counter = msg_process(msg)
                if update_morries_counter:
                    # updare the counter
                    morris.update()
                    # send the result to a tream 
                    morris_count = str(morris.query())
                    producer.produce('mk_sketch_1', key='Morris', value= morris_count)
                    producer.flush()
                print(morris.query())

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
