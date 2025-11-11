#!/usr/bin/env python3
"""
Simple HTTP server for local testing of GitHub Pages site.
This solves CORS issues when opening HTML files directly.

Usage:
    python3 server.py

Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
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

