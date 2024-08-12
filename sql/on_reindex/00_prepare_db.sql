CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

ALTER TABLE big_map_metadata_history DROP CONSTRAINT big_map_metadata_history_pkey;
ALTER TABLE big_map_metadata_history ADD PRIMARY KEY (id, timestamp);
SELECT create_hypertable('big_map_metadata_history', 'timestamp');
SELECT set_chunk_time_interval('big_map_metadata_history', INTERVAL '3 months');

ALTER TABLE big_map_token_metadata_history DROP CONSTRAINT big_map_token_metadata_history_pkey;
ALTER TABLE big_map_token_metadata_history ADD PRIMARY KEY (id, timestamp);
SELECT create_hypertable('big_map_token_metadata_history', 'timestamp');
SELECT set_chunk_time_interval('big_map_token_metadata_history', INTERVAL '3 months');
