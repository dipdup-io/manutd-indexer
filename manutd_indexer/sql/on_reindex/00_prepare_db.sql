CREATE OR REPLACE VIEW dipdup_token_metadata_view AS
SELECT
    tm.network,
    tm.contract,
    tm.token_id,
    m.value AS metadata,
    GREATEST(m.level, tm.level)::bigint << 30 | tm.token_id::bigint AS update_id,
    tm.created_at,
    GREATEST(m."timestamp", tm."timestamp") AS updated_at
FROM
    big_map_token_metadata_state AS tm
JOIN
    big_map_metadata_state AS m
USING (join_key);
