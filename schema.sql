DROP EXTENSION IF EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS timescaledb;
DROP TABLE IF EXISTS "air_quality";

CREATE TABLE "air_quality"(
    sensor_id TEXT,
    record_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    score smallint,
    temperature real,
    humidity real,
    co2 smallint,
    voc smallint,
    pm25 smallint
);

SELECT create_hypertable('air_quality', 'record_datetime');
CREATE UNIQUE INDEX idxtest ON "air_quality" ("sensor_id", "record_datetime");