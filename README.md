### Running benchmarks
If you just want to run benchmarks:
```shell
uv sync
uv run -m bench
```

If you want to generate chart:
```shell
uv sync
uv run -m bench regular >/tmp/sqlite_outfile1
uv run -m bench prepared >>/tmp/sqlite_outfile1
```

### Generating charts
```shell
uv run generate_charts.py
```

Benchmark results for [472f36e](https://github.com/RuslanUC/tortoise-orm/commit/472f36ef9ed93f01cfe14e00f9fa167cb5e22ff0):
![](images/sqlite_test1.png)
![](images/pg_test1.png)
![](images/mysql_test1.png)
