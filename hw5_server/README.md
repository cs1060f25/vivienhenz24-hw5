# hw5_server
Stub HTTP and SSH servers for Homework 5.
Prototyped with Codeium Windsurf and the DeepSeek V3 model.
Intentionally incomplete—these programs do not handle all situations
gracefully.

**NEW:** The HTTP server has been extended to support New York State business entity filings (corporations and LLCs) based on official NY Department of State forms DOS-1239-f and DOS-1336-f.

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

### New Features: NY Entities API
The HTTP server now supports:
- Filing Certificates of Incorporation (NY DOS Form 1239-f)
- Filing Articles of Organization for LLCs (NY DOS Form 1336-f)
- Retrieving filed entity information
- Listing all corporations and LLCs

**Endpoints:**
- `POST /file/corporation` - File a new corporation
- `POST /file/llc` - File a new LLC
- `GET /corporations` - List all corporations
- `GET /llcs` - List all LLCs
- `GET /corporation/{name}` - Get corporation details
- `GET /llc/{name}` - Get LLC details

See `../NY_ENTITIES_API.md` for complete API documentation and examples.
