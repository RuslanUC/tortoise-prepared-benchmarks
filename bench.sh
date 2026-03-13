#!/bin/bash

export PYTHONUNBUFFERED=1

POSTGRES_CONTAINER="tortoise-bench-postgresql"
MYSQL_CONTAINER="tortoise-bench-mysql"
SQLITE_OUTFILE="/tmp/sqlite_outfile1"
MYSQL_OUTFILE="/tmp/mysql_outfile1"
POSTGRES_OUTFILE="/tmp/pg_outfile1"

export UVLOOP=1
export PASSWORD=123456

echo "Will remove '$POSTGRES_CONTAINER' and '$MYSQL_CONTAINER' docker containers! Type 'yes' to continue:"
read yesorno
if [ "$yesorno" != "yes" ]; then
    exit 1;
fi

docker rm -f "$POSTGRES_CONTAINER" "$MYSQL_CONTAINER"

docker run -d --rm -p 5432:5432 -e "POSTGRES_PASSWORD=123456" -e "POSTGRES_DB=tbench" --name "$POSTGRES_CONTAINER" postgres:14.20-trixie || exit 1
docker run -d --rm -p 3306:3306 -e "MYSQL_ROOT_PASSWORD=123456" -e "MYSQL_DATABASE=tbench" --name "$MYSQL_CONTAINER" mysql:8 || exit 1

uv sync || exit 1

echo "Running benchmarks for sqlite..."

rm -f "$SQLITE_OUTFILE"
uv run -m bench regular | tee -a "$SQLITE_OUTFILE"
uv run -m bench compiled | tee -a "$SQLITE_OUTFILE"

echo "Running benchmarks for mysql..."

rm -f "$MYSQL_OUTFILE"
DBTYPE=mysql uv run -m bench regular | tee -a "$MYSQL_OUTFILE"
DBTYPE=mysql uv run -m bench compiled | tee -a "$MYSQL_OUTFILE"

echo "Running benchmarks for postgres..."

rm -f "$POSTGRES_OUTFILE"
DBTYPE=postgres uv run -m bench regular | tee -a "$POSTGRES_OUTFILE"
DBTYPE=postgres uv run -m bench compiled | tee -a "$POSTGRES_OUTFILE"

rm -f images/sqlite_test1.png images/mysql_test1.png images/pg_test1.png

uv run generate_charts.py
cp /tmp/orm-benchmarks/images/sqlite_test1.png images/sqlite_test1.png
cp /tmp/orm-benchmarks/images/mysql_test1.png images/mysql_test1.png
cp /tmp/orm-benchmarks/images/pg_test1.png images/pg_test1.png

docker rm -f "$POSTGRES_CONTAINER" "$MYSQL_CONTAINER"
