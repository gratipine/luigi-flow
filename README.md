## Installations
```
py -m venv .venv 
```

```
pip install wheel
pip install -r requirements.txt
```

## Running tasks
```
python -m luigi --module tasks RenderPDF --local-scheduler
```