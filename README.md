## installations
```
py -m venv .venv 
```

```
pip install wheel
pip install -r requirements.txt
```
```
python -m luigi --module tasks LoadData --last-date-of-report  --local-scheduler
```

```
python -m luigi --module tasks LoadData --local-scheduler
```
python -m luigi --module tasks TransformData --local-scheduler
