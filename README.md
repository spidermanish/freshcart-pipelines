# freshcart-pipelines

DE Assignment: From Git to Gold

## Run the tests

    pip install -r requirements.txt
    pytest -q

## Run the stream (needs a RabbitMQ broker; set AMQP_URL for a remote one)

    python stream/driver.py Ravi 'bangalore.koramangala.*'
    python stream/dispatcher.py

No secrets are stored in this repository: passwords are typed at runtime.