import logging

import psycopg
import toml


def main(config):
    # TODO Get influx data

    data = [{"sensor_id": "FakeSensor",
            "record_datetime": 0,
            "score": 0,
            "temperature": 0,
            "humidity": 0,
            "co2": 0,
            "voc": 0,
            "pm25": 0}]

    with psycopg.connect(config['timescaledb']['connection_string']) as conn:
        with conn.cursor() as cur:
            with cur.copy("COPY air_quality FROM STDIN") as copy:
                for point in data:
                    copy.write_row(point)

        conn.commit()


try:
    with open("config.toml") as configFile:
        config = toml.load(configFile)

    if ("timescaledb" not in config or "awair" not in config):
        logging.error(
            "Invalid config.toml file, please use config.example.yaml as a guide")
    else:
        main(config)

except FileNotFoundError as e:
    logging.error("Please add a config.yaml file")
