# FROM dipdup/dipdup:8
# FROM ghcr.io/dipdup-io/dipdup:8
FROM ghcr.io/dipdup-io/dipdup:aux-8.0.0

# COPY --chown=dipdup pyproject.toml README.md .
# RUN pip install .

COPY --chown=dipdup . manutd_indexer
WORKDIR manutd_indexer