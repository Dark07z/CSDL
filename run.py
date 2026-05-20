#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hệ thống Quản lý Thư viện
Library Management System
Entry point for the application
"""

import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   HỆ THỐNG QUẢN LÝ THƯ VIỆN                              ║
    ║   Library Management System                              ║
    ║                                                          ║
    ║   Starting server...                                     ║
    ║   Access the application at: http://localhost:5000      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
