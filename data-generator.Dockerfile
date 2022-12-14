ARG repo
FROM $repo/spark-py:base

USER root
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install --no-cache-dir numpy \
    && pip install --no-cache-dir wheel \
    && pip install --no-cache-dir pandas \
    && pip install --no-cache-dir google-cloud-storage
COPY --chown=185:185  data-generator.py credentialsFile.json dbldatagen-0.2.1-py3-none-any.whl spark-3.1-bigquery-0.26.0-preview.jar /
USER 185