from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import argparse
import json
import urllib.parse
from datetime import datetime

# In-memory storage for filed entities
corporations = {}
llcs = {}

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, username, password, *args, **kwargs):
        self.username = username
        self.password = password
        super().__init__(*args, **kwargs)

    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not self.verify_auth(auth_header):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
            self.end_headers()
            return

        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Route handling
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'success')
        elif path == '/corporations':
            self.handle_list_corporations()
        elif path == '/llcs':
            self.handle_list_llcs()
        elif path.startswith('/corporation/'):
            entity_name = path.split('/corporation/')[1]
            self.handle_get_corporation(urllib.parse.unquote(entity_name))
        elif path.startswith('/llc/'):
            entity_name = path.split('/llc/')[1]
            self.handle_get_llc(urllib.parse.unquote(entity_name))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not self.verify_auth(auth_header):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
            self.end_headers()
            return
        
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Invalid JSON'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # Route handling for POST
        if path == '/file/corporation':
            self.handle_file_corporation(data)
        elif path == '/file/llc':
            self.handle_file_llc(data)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def handle_list_corporations(self):
        """List all filed corporations"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'corporations': list(corporations.keys()),
            'count': len(corporations)
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def handle_list_llcs(self):
        """List all filed LLCs"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'llcs': list(llcs.keys()),
            'count': len(llcs)
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def handle_get_corporation(self, entity_name):
        """Get details of a specific corporation"""
        if entity_name in corporations:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(corporations[entity_name], indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'Corporation not found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_get_llc(self, entity_name):
        """Get details of a specific LLC"""
        if entity_name in llcs:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(llcs[entity_name], indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': 'LLC not found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_file_corporation(self, data):
        """File a new corporation"""
        required_fields = ['name', 'county', 'address', 'incorporator', 'shares', 'par_value']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': f'Missing required fields: {", ".join(missing_fields)}'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # Create corporation certificate
        certificate = {
            'document_type': 'CERTIFICATE OF INCORPORATION',
            'law_section': 'Section 402 of the Business Corporation Law',
            'name': data['name'],
            'purpose': data.get('purpose', 'To engage in any lawful act or activity for which a corporation may be organized under the Business Corporation Law.'),
            'county': data['county'],
            'shares': data['shares'],
            'par_value': data['par_value'],
            'registered_agent': 'Secretary of State',
            'address': data['address'],
            'incorporator': data['incorporator'],
            'incorporator_address': data.get('incorporator_address', data['address']),
            'filed_date': datetime.now().isoformat(),
            'status': 'Active'
        }
        
        # Store the corporation
        corporations[data['name']] = certificate
        
        # Send response
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'message': 'Corporation filed successfully',
            'certificate': certificate
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def handle_file_llc(self, data):
        """File a new LLC"""
        required_fields = ['name', 'county', 'address', 'organizer']
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'error': f'Missing required fields: {", ".join(missing_fields)}'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        
        # Create LLC articles
        articles = {
            'document_type': 'ARTICLES OF ORGANIZATION',
            'law_section': 'Section 203 of the Limited Liability Company Law',
            'name': data['name'],
            'county': data['county'],
            'registered_agent': 'Secretary of State',
            'address': data['address'],
            'organizer': data['organizer'],
            'organizer_address': data.get('organizer_address', data['address']),
            'email': data.get('email', ''),
            'filed_date': datetime.now().isoformat(),
            'status': 'Active'
        }
        
        # Store the LLC
        llcs[data['name']] = articles
        
        # Send response
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'message': 'LLC filed successfully',
            'articles': articles
        }
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

    def verify_auth(self, auth_header):
        auth_type, auth_string = auth_header.split(' ')
        if auth_type.lower() != 'basic':
            return False
        decoded = base64.b64decode(auth_string).decode('utf-8')
        username, password = decoded.split(':')
        return username == self.username and password == self.password

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080, username='admin', password='admin'):
    server_address = ('', port)
    handler = lambda *args, **kwargs: handler_class(username, password, *args, **kwargs)
    httpd = server_class(server_address, handler)
    print(f'Starting server on port {port} with username {username}...')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start HTTP server with basic auth')
    parser.add_argument('--port', type=int, default=8080, help='Port number to listen on')
    parser.add_argument('--username', default='admin', help='Username for basic auth')
    parser.add_argument('--password', default='admin', help='Password for basic auth')
    args = parser.parse_args()
    run(port=args.port, username=args.username, password=args.password)
