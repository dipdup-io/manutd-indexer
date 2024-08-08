CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

ALTER TABLE metadata DROP CONSTRAINT metadata_pkey;
ALTER TABLE metadata ADD PRIMARY KEY (id, timestamp);
SELECT create_hypertable('metadata', 'timestamp');
SELECT set_chunk_time_interval('metadata', INTERVAL '3 months');

ALTER TABLE token_metadata DROP CONSTRAINT token_metadata_pkey;
ALTER TABLE token_metadata ADD PRIMARY KEY (id, timestamp);
SELECT create_hypertable('token_metadata', 'timestamp');
SELECT set_chunk_time_interval('token_metadata', INTERVAL '3 months');
