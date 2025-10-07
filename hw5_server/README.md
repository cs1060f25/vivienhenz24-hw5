# hw5_server
Stub HTTP and SSH servers for Homework 5.
Prototyped with Codeium Windsurf and the DeepSeek V3 model.
Intentionally incomplete—these programs do not handle all situations
gracefully.

## ssh_server.py
Usage:
```
python3 ssh_server.py # defaults to 2222, admin, admin
python3 ssh_server.py --port 2224 
python3 ssh_server.py --port 2224 --username myuser --password mypass
```

If `paramiko` is not installed for your active Python interpreter, the script will look for the project's virtual environment at `../venv/bin/python` and automatically re-run itself with that interpreter. You can also launch it explicitly with `../venv/bin/python ssh_server.py` after activating the repository root.

## http_server.py
Usage:
```
python3 http_server.py # defaults to 8080, admin, admin
python3 http_server.py --port 8081 
python3 http_server.py --port 8081 --username user --password pass
```
