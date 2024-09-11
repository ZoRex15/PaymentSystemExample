from faststream.nats import JStream


SCHEDULER = JStream(
    name='scheduler',
    declare=False
)

DEBEZIUM_STREAM = JStream(
    name='DebeziumStream',
    declare=False
)