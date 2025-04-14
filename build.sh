#!/bin/bash
set -e  # Detiene el script si hay algún error

# Instalar el driver ODBC sin requerir root
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
mkdir -p ~/.microsoft/apt
mv microsoft.gpg ~/.microsoft/apt/microsoft.gpg

echo "deb [arch=amd64 signed-by=~/.microsoft/apt/microsoft.gpg] https://packages.microsoft.com/ubuntu/20.04/prod focal main" > ~/.microsoft/apt/microsoft.list

# Instalar dependencias necesarias
apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    odbcinst \
    odbcinst1debian2

# Instalar msodbcsql17 sin requerir root
apt-get download msodbcsql17
dpkg -x msodbcsql17*.deb ~/mssql
export PATH="$PATH:~/mssql/opt/microsoft/msodbcsql17/bin"