import logging

import psycopg
import toml
from awair import AwairClient


def fetch_data(token):
    output = []

    with AwairClient(token) as client:
        devices = client.get_devices()

        for device in devices:
            output.extend(device.air_data_raw(fahrenheit=True))

    return output
        

def main(config):
    data = fetch_data(config['awair']['token'])

    with psycopg.connect(config['timescaledb']['connection_string']) as conn:
        with conn.cursor() as cur:
            for point in data:
                cur.execute(f"INSERT INTO {config['timescaledb']['table']} VALUES (%(sensor_id)s, %(record_datetime)s, %(score)s, %(temperature)s, %(humidity)s, %(carbon_dioxide)s, %(volatile_organic_compounds)s, %(particulate_matter_2_5)s) ON CONFLICT DO NOTHING", point)

        conn.commit()


try:
    with open("config.toml") as configFile:
        config = toml.load(configFile)

    if ("timescaledb" not in config or "awair" not in config):
        logging.error(
            "Invalid config.toml file, please use config.example.toml as a guide")
    else:
        main(config)

except FileNotFoundError as e:
    logging.error("Please add a config.toml file")
