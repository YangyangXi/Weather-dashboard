"""Test Utilities Module"""
import os
import sys

def setup_test_path():
    """Setup test path"""
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 