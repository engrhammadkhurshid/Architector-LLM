"""
Utility functions for the calculator application
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_operation(operation_name, result):
    """Log calculator operations"""
    logger.info(f"Operation '{operation_name}' completed with result: {result}")


def format_error(error):
    """Format error messages"""
    return f"Error: {str(error)}"


class HistoryManager:
    """Manage calculation history"""
    
    def __init__(self):
        self.history = []
    
    def add_entry(self, operation, result):
        """Add an entry to history"""
        self.history.append({
            'operation': operation,
            'result': result
        })
    
    def get_history(self):
        """Retrieve calculation history"""
        return self.history
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
