"""
Simple Analytics Backend for Architector-LLM Research
Flask server to receive and store analytics data

Installation:
    pip install flask flask-cors

Usage:
    python analytics_backend.py
    
Endpoints:
    POST /register - Register new participant
    POST /analytics - Log session data
    POST /delete - Delete participant data
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for VS Code extension

# Data directory
DATA_DIR = Path('analytics_data')
DATA_DIR.mkdir(exist_ok=True)

PARTICIPANTS_FILE = DATA_DIR / 'participants.jsonl'
SESSIONS_FILE = DATA_DIR / 'sessions.jsonl'


@app.route('/architector/register', methods=['POST'])
def register_participant():
    """Register a new research participant"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['participantId', 'fullName', 'email', 'designation', 'experienceLevel']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Add server timestamp
        data['registeredAt'] = datetime.utcnow().isoformat()
        
        # Append to participants file
        with open(PARTICIPANTS_FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        print(f"✅ Registered participant: {data['fullName']} ({data['email']})")
        
        return jsonify({
            'status': 'success',
            'participantId': data['participantId'],
            'message': 'Thank you for participating in our research!'
        }), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/architector/analytics', methods=['POST'])
def log_analytics():
    """Log session analytics data"""
    try:
        data = request.json
        
        # Validate required fields
        if 'participantId' not in data or 'sessionId' not in data:
            return jsonify({'error': 'Missing participantId or sessionId'}), 400
        
        # Add server timestamp
        data['receivedAt'] = datetime.utcnow().isoformat()
        
        # Append to sessions file
        with open(SESSIONS_FILE, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        print(f"📊 Logged session: {data['sessionId']} for participant {data['participantId']}")
        print(f"   Project: {data.get('projectLanguage', 'unknown')} | " +
              f"Success: {data.get('success', False)} | " +
              f"Quality: {data.get('qualityScore', 'N/A')}")
        
        return jsonify({
            'status': 'success',
            'sessionId': data['sessionId']
        }), 200
        
    except Exception as e:
        print(f"❌ Analytics error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/architector/delete', methods=['POST'])
def delete_participant():
    """Delete participant data (right to be forgotten)"""
    try:
        data = request.json
        participant_id = data.get('participantId')
        
        if not participant_id:
            return jsonify({'error': 'Missing participantId'}), 400
        
        # Read and filter participants
        participants = []
        if PARTICIPANTS_FILE.exists():
            with open(PARTICIPANTS_FILE, 'r') as f:
                participants = [json.loads(line) for line in f if line.strip()]
            
            # Remove participant
            participants = [p for p in participants if p['participantId'] != participant_id]
            
            # Rewrite file
            with open(PARTICIPANTS_FILE, 'w') as f:
                for p in participants:
                    f.write(json.dumps(p) + '\n')
        
        # Read and filter sessions
        sessions = []
        if SESSIONS_FILE.exists():
            with open(SESSIONS_FILE, 'r') as f:
                sessions = [json.loads(line) for line in f if line.strip()]
            
            # Remove sessions
            sessions = [s for s in sessions if s['participantId'] != participant_id]
            
            # Rewrite file
            with open(SESSIONS_FILE, 'w') as f:
                for s in sessions:
                    f.write(json.dumps(s) + '\n')
        
        print(f"🗑️  Deleted data for participant: {participant_id}")
        
        return jsonify({
            'status': 'success',
            'message': 'All data deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"❌ Deletion error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/architector/stats', methods=['GET'])
def get_stats():
    """Get summary statistics (for researcher use)"""
    try:
        # Count participants
        participant_count = 0
        if PARTICIPANTS_FILE.exists():
            with open(PARTICIPANTS_FILE, 'r') as f:
                participant_count = sum(1 for line in f if line.strip())
        
        # Analyze sessions
        session_count = 0
        success_count = 0
        total_quality = 0
        quality_count = 0
        languages = {}
        
        if SESSIONS_FILE.exists():
            with open(SESSIONS_FILE, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue
                    session = json.loads(line)
                    session_count += 1
                    
                    if session.get('success'):
                        success_count += 1
                    
                    if 'qualityScore' in session:
                        total_quality += session['qualityScore']
                        quality_count += 1
                    
                    lang = session.get('projectLanguage', 'unknown')
                    languages[lang] = languages.get(lang, 0) + 1
        
        stats = {
            'participants': participant_count,
            'sessions': session_count,
            'successRate': round(success_count / session_count * 100, 1) if session_count > 0 else 0,
            'averageQuality': round(total_quality / quality_count, 1) if quality_count > 0 else 0,
            'languageDistribution': languages
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Architector Analytics Backend'}), 200


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Architector-LLM Analytics Backend Server")
    print("=" * 70)
    print(f"📁 Data directory: {DATA_DIR.absolute()}")
    print(f"📝 Participants file: {PARTICIPANTS_FILE.name}")
    print(f"📊 Sessions file: {SESSIONS_FILE.name}")
    print("=" * 70)
    print("📡 Endpoints:")
    print("   POST http://localhost:5000/architector/register")
    print("   POST http://localhost:5000/architector/analytics")
    print("   POST http://localhost:5000/architector/delete")
    print("   GET  http://localhost:5000/architector/stats")
    print("   GET  http://localhost:5000/health")
    print("=" * 70)
    print("⚡ Starting server on http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("=" * 70)
    
    # Run server
    app.run(host='0.0.0.0', port=5000, debug=True)
