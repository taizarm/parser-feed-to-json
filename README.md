# RSS Feed Parser to JSON
This project is responsible for reading a specific RSS Feed and transforming it into a JSon file.

## How to install
1) Clone this repository
````
git clone https://github.com/taizarm/parser-feed-to-json.git
````
2) Enter in the root folder of project
3) Create a virtualenv
```
virtualenv -p python3 .venv
```
4) Start virtualenv
```
source .venv/bin/activate
```
5) Install the requirements
````
pip install -r requirements.txt
````
6) Done!

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
