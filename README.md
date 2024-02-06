Apply `python-cxxfilt` to a flamegraph output.

Installing into a `virtualenv`:

```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r reqs.txt
```

Run with:

```
./do.py flamegraph.svg > flamegraph.filtered.svg
```
