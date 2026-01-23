"""
Architector-LLM Backend
Main HTTP server for handling documentation generation requests
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv
from pipeline import DocumentationPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize pipeline
pipeline = DocumentationPipeline()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8765))
BACKEND_HOST = os.getenv('BACKEND_HOST', 'localhost')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'architector-llm-backend'
    })

@app.route('/generate', methods=['POST'])
def generate_documentation():
    """
    Main endpoint for generating architecture documentation
    
    Request Body:
    {
        "codebase_path": "/path/to/codebase",
        "semantic_version": "1.0.0"  (optional)
    }
    
    Response:
    {
        "status": "success",
        "output_dir": "docs/arch/v1.0.0_2026-01-22_abc123",
        "saved_files": {
            "documentation": "path/to/README.md",
            "diagram_source": "path/to/architecture.mmd",
            "metadata": "path/to/generation_info.json"
        },
        "metrics": {
            "processing_time": 45.2,
            "files_analyzed": 42,
            "total_classes": 15,
            "total_functions": 87,
            "llm_tokens_used": 3245
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'codebase_path' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing codebase_path in request'
            }), 400
        
        codebase_path = data['codebase_path']
        semantic_version = data.get('semantic_version', None)  # Allow None for auto-detection
        
        if not os.path.exists(codebase_path):
            return jsonify({
                'status': 'error',
                'message': f'Codebase path does not exist: {codebase_path}'
            }), 404
        
        logger.info(f'Starting documentation generation for: {codebase_path}')
        if semantic_version:
            logger.info(f'Using provided version: {semantic_version}')
        else:
            logger.info('Version will be auto-detected from project files')
        
        # Execute the complete pipeline (version auto-detected if None)
        result = pipeline.generate(codebase_path, semantic_version)
        
        if result['status'] == 'success':
            # Return relative path instead of absolute
            output_dir_relative = os.path.relpath(result['output_dir'], codebase_path)
            
            return jsonify({
                'status': 'success',
                'output_dir': output_dir_relative,
                'output_dir_absolute': result['output_dir'],
                'saved_files': result['saved_files'],
                'metrics': result['metrics']
            })
        else:
            return jsonify(result), 500
        
    except Exception as e:
        logger.error(f'Error generating documentation: {str(e)}', exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get the status of a documentation generation job"""
    # TODO: Implement job status tracking
    return jsonify({
        'job_id': job_id,
        'status': 'processing',
        'progress': 50
    })

def main():
    """Start the Flask server"""
    logger.info(f'Starting Architector-LLM Backend Server on {BACKEND_HOST}:{BACKEND_PORT}')
    app.run(host=BACKEND_HOST, port=BACKEND_PORT, debug=False)

if __name__ == '__main__':
    main()
