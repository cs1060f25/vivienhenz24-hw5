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

## Usage

### Testing the Vulnerability Scanner
1. Start the vulnerable servers:
   ```bash
   cd hw5_server
   python3 http_server.py --port 8080 &
   python3 ssh_server.py --port 2222 &
   ```

2. Run the vulnerability scanner:
   ```bash
   python3 vulnerability_scanner.py
   ```

3. For verbose output:
   ```bash
   python3 vulnerability_scanner.py -v
   ```

### Testing SQL Injection
```bash
curl -X POST https://cat-hw4.vercel.app/county_data -H "Content-Type: application/json" -d @test.json
curl -X POST https://cat-hw4.vercel.app/county_data -H "Content-Type: application/json" -d @attack.json
```

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

The vulnerability scanner requires:
- `python-nmap` - For port scanning
- `requests` - For HTTP connections
- `paramiko` - For SSH connections

Install with:
```bash
pip install python-nmap requests paramiko
```

## Security Notice

This code is for educational purposes only. The techniques demonstrated should only be used on systems you own or have explicit permission to test. Unauthorized testing of systems is illegal and unethical.
