DROP EXTENSION IF EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS timescaledb;
DROP TABLE IF EXISTS "air_quality";

CREATE TABLE "air_quality"(
    sensor_id TEXT,
    record_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    score integer,
    temperature real,
    humidity real,
    carbon_dioxide integer,
    volatile_organic_compounds integer,
    particulate_matter_2_5 integer
);

-- https://docs.timescale.com/timescaledb/latest/how-to-guides/hypertables/about-hypertables#best-practices-for-time-partitioning
-- From my experience, 1-year of 10-second interval data for one awair sensor is approximately 400mb
-- Based on the recommended best practices, INTERVAL = (Main_Memory * 25%) / (400mb / year)
-- On my 2-gig ram VM, this is ~1-year. Change it based on your system
SELECT create_hypertable('air_quality', 'record_datetime', chunk_time_interval => INTERVAL '1 year');
CREATE UNIQUE INDEX idxtest ON "air_quality" ("sensor_id", "record_datetime");