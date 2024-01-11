import httpx

# Maybe I'll eventually spin this out into its own separate library, but its not ready for that yet.


class AwairClient:

    def __init__(self, token: str) -> None:
        headers = {'Authorization': f'Bearer {token}',
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        self.client = httpx.Client(headers=headers)

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def get_devices(self):
        resp = self.client.get(
            "https://developer-apis.awair.is/v1/users/self/devices").json()
        return [AwairDevice(self.client, device) for device in resp['devices']]


class AwairDevice:
    def __init__(self, client, attributes):
        self.device_id = attributes["deviceId"]
        self.uuid = attributes["deviceUUID"]
        self.device_type = attributes["deviceType"]
        self.mac_address = attributes.get("macAddress", None)

        self.latitude = attributes.get("latitude", None)
        self.longitude = attributes.get("longitude", None)
        self.name = attributes.get("name", None)
        self.preference = attributes.get("preference", None)
        self.room_type = attributes.get("roomType", None)
        self.space_type = attributes.get("spaceType", None)
        self.timezone = attributes.get("timezone", None)

        self.client = client

    def air_data_raw(self, **kwargs):
        resp = self.client.get(
            f"https://developer-apis.awair.is/v1/users/self/devices/{self.device_type}/{self.device_id}/air-data/raw", params=kwargs).json()

        output = []

        for point in resp['data']:
            sensor_data = {
                sensor["comp"]: sensor["value"]
                for sensor in point.get("sensors", [])
            }

            data = {"sensor_id": self.device_id,
                    "record_datetime": point['timestamp'],
                    "score": point['score'],
                    "temperature": sensor_data['temp'],
                    "humidity": sensor_data['humid'],
                    "carbon_dioxide": sensor_data['co2'],
                    "volatile_organic_compounds": sensor_data['voc'],
                    "particulate_matter_2_5": sensor_data['pm25']}

            output.append(data)
        return output
