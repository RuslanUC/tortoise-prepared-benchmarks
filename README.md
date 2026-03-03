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

Benchmark results for [bf411ee](https://github.com/RuslanUC/tortoise-orm/commit/bf411ee206bfa1262d523c11ae314ec55b3a8eef):
![](images/sqlite_test1.png)

