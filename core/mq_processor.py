#!/usr/bin/env python
import json
import logging

import pika
import pymongo
from core.repository.mongo_client import MongoClient
from scrapy.conf import settings

logger = logging.getLogger(__name__)


def run():
    try:
        credentials = pika.PlainCredentials(settings['MQ_USER'], settings['MQ_PASSWORD'])
        parameters = pika.ConnectionParameters(settings['MQ_HOST'], settings['MQ_PORT'], '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        mongo_client = MongoClient()
        mqcollection = mongo_client.mqcollection()
        data_to_send_list = mqcollection.find().sort([("finished_time", pymongo.ASCENDING)]).limit(20)
        for data_to_send in data_to_send_list:
            del data_to_send['_id']
            channel.queue_declare(queue=data_to_send['data_source'], durable=True)
            channel.basic_publish(exchange='', routing_key=data_to_send['data_source'], body=json.dumps(data_to_send), properties=pika.BasicProperties(delivery_mode=2))
            logger.info('{} is already sent to rabbitmq.'.format(data_to_send['reference_no']))
            mqcollection.delete_one({'reference_no': data_to_send['reference_no']})
        mongo_client.close()
        connection.close()

    except Exception as e:
        logger.error('MQ processor run failed.{}'.format(str(e)))
