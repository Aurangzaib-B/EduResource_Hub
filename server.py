#!/usr/bin/env python3
"""
Simple HTTP server for the EduResource Hub website.
This server allows proper loading of JSON files for local development.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def main():
    """Start the local development server."""
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 EduResource Hub Server Starting...")
            print(f"📍 Server running at: http://localhost:{PORT}")
            print(f"📁 Serving files from: {DIRECTORY}")
            print("🌐 Opening website in your default browser...")
            print("⏹️  Press Ctrl+C to stop the server\n")
            
            # Open the website in the default browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:  # Address already in use
            print(f"❌ Port {PORT} is already in use.")
            print(f"💡 Try a different port or stop the process using port {PORT}")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
