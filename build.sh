#!/bin/bash
apt-get update && apt-get install -y \
    unixodbc \
    tdsodbc \
    freetds-bin \
    freetds-common