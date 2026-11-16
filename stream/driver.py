"""A driver: python driver.py NAME PATTERN. Receives every request whose routing key matches PATTERN."""
import json
import os
import sys

import pika

EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python driver.py NAME PATTERN")
    name, pattern = sys.argv[1], sys.argv[2]

    url = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic")

    # a private queue: the broker names it, and deletes it when this driver disconnects
    queue = channel.queue_declare(queue="", exclusive=True).method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)
    channel.basic_qos(prefetch_count=1)          # at most one unacknowledged message at a time

    def on_message(ch, method, properties, body):
        try:
            request = json.loads(body)
        except ValueError:                             # not even valid JSON: also bad
            request = {}
        if "zone" not in request:
            print(f"[{name}] REJECTED id={request.get('id')} key={method.routing_key} (no zone)",
                  flush=True)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)   # discard it
            return
        print(f"[{name}] got id={request['id']} key={method.routing_key} "
              f"zone={request['zone']}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)                      # done with it

    channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
    print(f"[{name}] waiting on {pattern}", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()