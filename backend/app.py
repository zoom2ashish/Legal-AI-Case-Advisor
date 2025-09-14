#!/usr/bin/env python3
"""
Legal AI Case Advisor - MVP Flask Application
Phase 1: Basic Legal Research Workflow
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime
import json

# Import our custom modules
from database.sqlite_legal_manager import LegalDataManager
from utils.legal_security import AttorneyClientPrivilegeManager
from agents.mvp_research_agent import MVPResearchAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize legal system components
try:
    db_manager = LegalDataManager("./database/legal_data.db")
    privilege_manager = AttorneyClientPrivilegeManager()
    research_agent = MVPResearchAgent(db_manager, privilege_manager)
    logger.info("Legal AI system components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize legal system: {str(e)}")
    db_manager = None
    privilege_manager = None
    research_agent = None

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Legal AI Case Advisor MVP',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'database': db_manager.health_check() if db_manager else False,
            'privilege_manager': privilege_manager.health_check() if privilege_manager else False,
            'research_agent': research_agent.health_check() if research_agent else False
        }
    })

@app.route('/api/legal-research', methods=['POST'])
def conduct_legal_research():
    """Conduct legal research with privilege protection"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        jurisdiction = data.get('jurisdiction', 'federal')
        attorney_id = data.get('attorney_id')
        client_id = data.get('client_id')
        
        # Validate query length
        if len(query.strip()) < 3:
            return jsonify({'error': 'Query must be at least 3 characters long'}), 400
        
        # Check if research agent is available
        if not research_agent:
            return jsonify({'error': 'Legal research service unavailable'}), 503
        
        # Conduct legal research
        research_result = research_agent.conduct_legal_research(
            query=query,
            jurisdiction=jurisdiction,
            attorney_id=attorney_id,
            client_id=client_id
        )
        
        # Check for errors in research result
        if 'error' in research_result:
            return jsonify({'error': research_result['error']}), 500
        
        # Return research results
        return jsonify({
            'success': True,
            'research_result': research_result,
            'disclaimers': [
                "This research is for informational purposes only and does not constitute legal advice.",
                "Consult with qualified legal counsel for specific legal matters.",
                "AI-generated content should be reviewed by licensed attorneys."
            ]
        })
        
    except Exception as e:
        logger.error(f"Legal research endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/legal-research/summary', methods=['POST'])
def get_research_summary():
    """Get summary of legal research results"""
    try:
        data = request.get_json()
        
        if not data or 'research_result' not in data:
            return jsonify({'error': 'Research result is required'}), 400
        
        research_result = data['research_result']
        
        if not research_agent:
            return jsonify({'error': 'Legal research service unavailable'}), 503
        
        summary = research_agent.get_research_summary(research_result)
        
        if 'error' in summary:
            return jsonify({'error': summary['error']}), 500
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Research summary endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/attorney/session', methods=['POST'])
def create_attorney_session():
    """Create secure attorney session"""
    try:
        data = request.get_json()
        
        if not data or 'attorney_id' not in data:
            return jsonify({'error': 'Attorney ID is required'}), 400
        
        attorney_id = data['attorney_id']
        client_id = data.get('client_id')
        
        if not privilege_manager:
            return jsonify({'error': 'Privilege management service unavailable'}), 503
        
        # Create secure session
        session_result = privilege_manager.create_secure_session(
            attorney_id=attorney_id,
            client_id=client_id
        )
        
        return jsonify({
            'success': True,
            'session': session_result
        })
        
    except Exception as e:
        logger.error(f"Attorney session endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/attorney/verify', methods=['POST'])
def verify_attorney_session():
    """Verify attorney session"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['session_id', 'session_token', 'attorney_id']):
            return jsonify({'error': 'Session ID, token, and attorney ID are required'}), 400
        
        session_id = data['session_id']
        session_token = data['session_token']
        attorney_id = data['attorney_id']
        client_id = data.get('client_id')
        
        if not privilege_manager:
            return jsonify({'error': 'Privilege management service unavailable'}), 503
        
        # Verify session
        verification_result = privilege_manager.verify_privileged_access(
            session_id=session_id,
            session_token=session_token,
            attorney_id=attorney_id,
            client_id=client_id
        )
        
        if not verification_result.get('authorized', False):
            return jsonify({'error': 'Session verification failed'}), 401
        
        return jsonify({
            'success': True,
            'verification': verification_result
        })
        
    except Exception as e:
        logger.error(f"Attorney verification endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/database/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics"""
    try:
        if not db_manager:
            return jsonify({'error': 'Database service unavailable'}), 503
        
        stats = db_manager.get_database_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Database stats endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/ethics/audit', methods=['GET'])
def get_ethics_audit():
    """Get ethics compliance audit summary"""
    try:
        attorney_id = request.args.get('attorney_id')
        days = int(request.args.get('days', 30))
        
        if not db_manager:
            return jsonify({'error': 'Database service unavailable'}), 503
        
        audit_summary = db_manager.get_ethics_audit_summary(attorney_id, days)
        
        return jsonify({
            'success': True,
            'audit_summary': audit_summary,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Ethics audit endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/attorney/history', methods=['GET'])
def get_attorney_history():
    """Get attorney case history"""
    try:
        attorney_id = request.args.get('attorney_id')
        client_id = request.args.get('client_id')
        
        if not attorney_id:
            return jsonify({'error': 'Attorney ID is required'}), 400
        
        if not db_manager:
            return jsonify({'error': 'Database service unavailable'}), 503
        
        history = db_manager.get_attorney_case_history(attorney_id, client_id)
        
        return jsonify({
            'success': True,
            'history': history,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Attorney history endpoint error: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5001))  # Changed default port to 5001 to avoid macOS AirPlay conflict
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Legal AI Case Advisor MVP on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)