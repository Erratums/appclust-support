#!/usr/bin/env python3
"""
Simple HTTP server for local testing of GitHub Pages site.
This solves CORS issues when opening HTML files directly.
Also handles SPA routing by serving index.html for client-side routes.

Usage:
    python3 server.py

Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
import sys
import urllib.parse

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Parse the path
        parsed_path = urllib.parse.urlparse(path)
        original_path = parsed_path.path
        
        # Handle root path
        if original_path == '/' or original_path == '':
            return super().translate_path('/index.html')
        
        # Check if it's a client-side route (starts with /article/)
        if original_path.startswith('/article/'):
            # Serve index.html for SPA routing
            return super().translate_path('/index.html')
        
        # Translate the path normally first
        translated = super().translate_path(path)
        
        # Check if the translated file exists
        if os.path.exists(translated) and os.path.isfile(translated):
            # File exists, return it
            return translated
        elif os.path.exists(translated) and os.path.isdir(translated):
            # Directory exists, return it (will be handled by list_directory)
            return translated
        else:
            # File doesn't exist - serve index.html for SPA fallback
            return super().translate_path('/index.html')
    
    def end_headers(self):
        # Add CORS headers to allow local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Custom log format
        sys.stderr.write("%s - - [%s] %s\n" %
                        (self.address_string(),
                         self.log_date_time_string(),
                         format % args))

if __name__ == "__main__":
    # Change to the directory where the script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}/")
        print(f"📁 Serving directory: {os.getcwd()}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

