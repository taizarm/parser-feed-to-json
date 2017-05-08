# RSS Feed Parser to JSON
This project is responsible for reading a specific RSS Feed and transforming it into a JSon file.

## How to install


## How to run standalone
Run the command:
```
python parser/parser.py
```

## How to run tests and see coverage

Be sure virtual env is activated. Run the command:

```
py.test --cov=parser tests/
```


If the coverage is not 100%, run this command to see the lines without tests:

```
coverage report -m
```
