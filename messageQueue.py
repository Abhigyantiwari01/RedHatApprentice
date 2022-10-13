#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()



def initialize_queue():
    channel.queue_declare(queue='order_queue')


def enqueue(body):
    print("ENQUEUED ",body)
    channel.basic_publish(exchange='',routing_key='order_queue',body=body)

def dequeue(cb):
    print("called")
    channel.basic_consume("order_queue",cb,auto_ack=True)