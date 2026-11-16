"""Publishes one random ride/food request every 2 seconds to the rapido-dispatch topic exchange."""
import json
import os
import random
import time
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"
# zones per city: includes every zone used in D1, so D1's keys can really occur
ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield", "adyar"],
}
TYPES = ["ride", "food"]
BAD_EVERY = 10          # D3: every 10th message is sent without its zone


def main():
    url = os.environ.get("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic")

    msg_id = 0
    try:
        while True:
            msg_id += 1
            city = random.choice(list(ZONES))
            zone = random.choice(ZONES[city])
            kind = random.choice(TYPES)
            routing_key = f"{city}.{zone}.{kind}"          # lowercase: bindings are case-sensitive
            message = {
                "id": msg_id,
                "city": city,
                "zone": zone,
                "type": kind,
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            if msg_id % BAD_EVERY == 0:
                del message["zone"]                        # a bad message: same key, no zone in the body
            channel.basic_publish(exchange=EXCHANGE, routing_key=routing_key,
                                  body=json.dumps(message))
            bad = "" if "zone" in message else "  (BAD: no zone)"
            print(f"[dispatcher] sent id={msg_id} key={routing_key}{bad}", flush=True)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        connection.close()


if __name__ == "__main__":
    main()