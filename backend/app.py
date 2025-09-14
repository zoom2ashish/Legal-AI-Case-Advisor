#!/usr/bin/env python3
"""
Legal AI Pod - Main Flask Application
Provides REST API for legal research, case analysis, and AI agent orchestration
with attorney-client privilege protection and legal ethics compliance
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import json

# Import our custom modules
from agents.research_agent import LegalResearchAgent
from agents.case_agent import CaseAnalysisAgent
from agents.document_agent import DocumentReviewAgent
from agents.precedent_agent import PrecedentMiningAgent
from database.chromadb_legal_manager import LegalKnowledgeStore
from database.sqlite_legal_manager import LegalDataManager
from utils.legal_security import AttorneyClientPrivilegeManager
from utils.legal_ethics import LegalEthicsMonitoring

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'legal-dev-secret-key-change-in-production')
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/legal_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize system components
try:
    # Database managers
    legal_knowledge_store = LegalKnowledgeStore()
    legal_db = LegalDataManager()
    
    # Security and ethics
    privilege_manager = AttorneyClientPrivilegeManager()
    ethics_monitor = LegalEthicsMonitoring()
    
    # AI Agents
    research_agent = LegalResearchAgent(legal_knowledge_store, legal_db)
    case_agent = CaseAnalysisAgent(legal_knowledge_store, legal_db)
    document_agent = DocumentReviewAgent(legal_knowledge_store, legal_db)
    precedent_agent = PrecedentMiningAgent(legal_knowledge_store, legal_db)
    
    logger.info("All Legal AI system components initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize Legal AI system components: {str(e)}")
    raise

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Legal AI system monitoring"""
    try:
        # Check database connections
        legal_knowledge_store.health_check()
        legal_db.health_check()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'system': 'Legal AI Pod - Case Intelligence System',
            'components': {
                'legal_database': 'ok',
                'knowledge_store': 'ok',
                'ai_agents': 'ok',
                'privilege_protection': 'ok',
                'ethics_compliance': 'ok'
            }
        }), 200
    except Exception as e:
        logger.error(f"Legal AI health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/attorney/start-session', methods=['POST'])
def start_attorney_session():
    """Initialize a new attorney session with privilege protection"""
    try:
        data = request.get_json()
        attorney_id = data.get('attorney_id')
        client_id = data.get('client_id')
        
        if not attorney_id:
            return jsonify({'error': 'Attorney ID required'}), 400
        
        # Verify attorney-client relationship
        relationship_valid = privilege_manager.verify_attorney_client_relationship(
            attorney_id, client_id
        )
        
        if not relationship_valid and client_id:
            return jsonify({'error': 'Invalid attorney-client relationship'}), 403
        
        # Create secure privileged session
        session_data = privilege_manager.create_privileged_session(
            attorney_id, client_id
        )
        session['attorney_id'] = attorney_id
        session['client_id'] = client_id
        session['session_token'] = session_data['token']
        
        # Log session start for legal compliance
        privilege_manager.log_attorney_access(
            attorney_id=attorney_id,
            client_id=client_id,
            action='session_start',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'session_id': session_data['session_id'],
            'attorney_id': attorney_id,
            'client_id': client_id,
            'privilege_protected': True,
            'message': 'Attorney session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to start attorney session: {str(e)}")
        return jsonify({'error': 'Failed to start session'}), 500

@app.route('/api/legal/research', methods=['POST'])
def conduct_legal_research():
    """Conduct comprehensive legal research through AI agent"""
    try:
        data = request.get_json()
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        legal_query = data.get('query', '')
        jurisdiction = data.get('jurisdiction', 'federal')
        case_context = data.get('case_context', {})
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        if not legal_query:
            return jsonify({'error': 'Legal query is required'}), 400
        
        # Security: Encrypt and audit log the legal research
        encrypted_query = privilege_manager.encrypt_privileged_data(legal_query)
        privilege_manager.log_legal_research_activity(
            attorney_id=attorney_id,
            client_id=client_id,
            query=legal_query,
            jurisdiction=jurisdiction,
            ip_address=request.remote_addr
        )
        
        # Conduct legal research using AI agent
        research_result = research_agent.conduct_legal_research(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_query=legal_query,
            jurisdiction=jurisdiction,
            case_context=case_context
        )
        
        # Store research in privileged database
        legal_db.store_legal_research(
            attorney_id=attorney_id,
            client_id=client_id,
            query=legal_query,
            research_result=research_result,
            jurisdiction=jurisdiction
        )
        
        return jsonify(research_result), 200
        
    except Exception as e:
        logger.error(f"Failed to conduct legal research: {str(e)}")
        return jsonify({'error': 'Failed to complete legal research'}), 500

@app.route('/api/legal/case-analysis', methods=['POST'])
def analyze_legal_case():
    """Analyze legal case strength and strategy through AI agent"""
    try:
        data = request.get_json()
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        case_facts = data.get('case_facts', '')
        legal_issues = data.get('legal_issues', [])
        jurisdiction = data.get('jurisdiction', 'federal')
        case_type = data.get('case_type', 'general')
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        if not case_facts:
            return jsonify({'error': 'Case facts are required'}), 400
        
        # Verify privileged access
        if not privilege_manager.verify_privileged_session(
            attorney_id, client_id, session.get('session_token')
        ):
            return jsonify({'error': 'Unauthorized privileged access'}), 403
        
        # Analyze case using AI agent
        case_analysis = case_agent.analyze_case_strength(
            attorney_id=attorney_id,
            client_id=client_id,
            case_facts=case_facts,
            legal_issues=legal_issues,
            jurisdiction=jurisdiction,
            case_type=case_type
        )
        
        # Store case analysis with privilege protection
        legal_db.store_case_analysis(
            attorney_id=attorney_id,
            client_id=client_id,
            case_facts=case_facts,
            analysis_result=case_analysis,
            privileged=True
        )
        
        return jsonify(case_analysis), 200
        
    except Exception as e:
        logger.error(f"Failed to analyze legal case: {str(e)}")
        return jsonify({'error': 'Failed to complete case analysis'}), 500

@app.route('/api/legal/document-review', methods=['POST'])
def review_legal_document():
    """Review legal document for risks and obligations through AI agent"""
    try:
        data = request.get_json()
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        document_text = data.get('document_text', '')
        document_type = data.get('document_type', 'contract')
        review_focus = data.get('review_focus', 'comprehensive')
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        if not document_text:
            return jsonify({'error': 'Document text is required'}), 400
        
        # Conduct document review using AI agent
        review_result = document_agent.review_legal_document(
            attorney_id=attorney_id,
            client_id=client_id,
            document_text=document_text,
            document_type=document_type,
            review_focus=review_focus
        )
        
        # Store document review with privilege protection
        legal_db.store_document_review(
            attorney_id=attorney_id,
            client_id=client_id,
            document_text=document_text,
            review_result=review_result,
            privileged=True
        )
        
        return jsonify(review_result), 200
        
    except Exception as e:
        logger.error(f"Failed to review legal document: {str(e)}")
        return jsonify({'error': 'Failed to complete document review'}), 500

@app.route('/api/legal/precedent-search', methods=['POST'])
def search_legal_precedents():
    """Search for legal precedents and analogous cases through AI agent"""
    try:
        data = request.get_json()
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        legal_issue = data.get('legal_issue', '')
        jurisdiction = data.get('jurisdiction', 'federal')
        case_facts = data.get('case_facts', '')
        favor_client = data.get('favor_client', True)
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        if not legal_issue:
            return jsonify({'error': 'Legal issue is required'}), 400
        
        # Search for precedents using AI agent
        precedent_result = precedent_agent.discover_relevant_precedents(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_issue=legal_issue,
            jurisdiction=jurisdiction,
            case_facts=case_facts,
            favor_client=favor_client
        )
        
        # Store precedent research
        legal_db.store_precedent_research(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_issue=legal_issue,
            precedent_result=precedent_result,
            jurisdiction=jurisdiction
        )
        
        return jsonify(precedent_result), 200
        
    except Exception as e:
        logger.error(f"Failed to search legal precedents: {str(e)}")
        return jsonify({'error': 'Failed to complete precedent search'}), 500

@app.route('/api/legal/multi-agent-analysis', methods=['POST'])
def comprehensive_legal_analysis():
    """Comprehensive legal analysis using all agents in coordination"""
    try:
        data = request.get_json()
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        legal_matter = data.get('legal_matter', '')
        case_facts = data.get('case_facts', '')
        jurisdiction = data.get('jurisdiction', 'federal')
        analysis_type = data.get('analysis_type', 'comprehensive')
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        if not legal_matter:
            return jsonify({'error': 'Legal matter description is required'}), 400
        
        # Step 1: Research Agent - Legal research and analysis
        research_result = research_agent.conduct_legal_research(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_query=legal_matter,
            jurisdiction=jurisdiction,
            case_context={'case_facts': case_facts}
        )
        
        # Step 2: Case Agent - Case strength analysis
        case_analysis = case_agent.analyze_case_strength(
            attorney_id=attorney_id,
            client_id=client_id,
            case_facts=case_facts,
            legal_issues=research_result.get('legal_issues', []),
            jurisdiction=jurisdiction
        )
        
        # Step 3: Precedent Agent - Precedent discovery
        precedent_analysis = precedent_agent.discover_relevant_precedents(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_issue=legal_matter,
            jurisdiction=jurisdiction,
            case_facts=case_facts
        )
        
        # Step 4: Document Agent - Strategic recommendations
        if 'document_text' in data:
            document_analysis = document_agent.review_legal_document(
                attorney_id=attorney_id,
                client_id=client_id,
                document_text=data['document_text'],
                document_type='strategic_analysis'
            )
        else:
            document_analysis = None
        
        # Compile comprehensive analysis
        comprehensive_analysis = {
            'legal_research': research_result,
            'case_strength_analysis': case_analysis,
            'precedent_discovery': precedent_analysis,
            'document_analysis': document_analysis,
            'multi_agent_synthesis': self._synthesize_legal_analysis(
                research_result, case_analysis, precedent_analysis, document_analysis
            ),
            'overall_assessment': self._generate_overall_legal_assessment(
                research_result, case_analysis, precedent_analysis
            ),
            'strategic_recommendations': self._generate_strategic_recommendations(
                research_result, case_analysis, precedent_analysis
            ),
            'timestamp': datetime.now().isoformat(),
            'privileged_communication': True,
            'comprehensive_analysis': True
        }
        
        # Store comprehensive analysis
        legal_db.store_comprehensive_analysis(
            attorney_id=attorney_id,
            client_id=client_id,
            legal_matter=legal_matter,
            analysis_result=comprehensive_analysis,
            privileged=True
        )
        
        return jsonify(comprehensive_analysis), 200
        
    except Exception as e:
        logger.error(f"Failed to complete comprehensive legal analysis: {str(e)}")
        return jsonify({'error': 'Failed to complete comprehensive analysis'}), 500

def _synthesize_legal_analysis(research_result, case_analysis, precedent_analysis, document_analysis):
    """Synthesize results from multiple agents"""
    synthesis = {
        'key_legal_issues': research_result.get('legal_issues', []),
        'case_strength_score': case_analysis.get('strength_score', 0),
        'precedent_support_level': precedent_analysis.get('precedent_strength', 'unknown'),
        'risk_factors': case_analysis.get('risk_factors', []),
        'favorable_authorities': precedent_analysis.get('favorable_precedents', []),
        'adverse_authorities': precedent_analysis.get('adverse_precedents', []),
        'strategic_advantages': case_analysis.get('strategic_advantages', []),
        'compliance_issues': document_analysis.get('compliance_issues', []) if document_analysis else []
    }
    return synthesis

def _generate_overall_legal_assessment(research_result, case_analysis, precedent_analysis):
    """Generate overall legal assessment"""
    strength_score = case_analysis.get('strength_score', 0)
    precedent_support = len(precedent_analysis.get('favorable_precedents', []))
    
    if strength_score >= 8 and precedent_support >= 3:
        assessment = 'Strong legal position with good precedent support'
    elif strength_score >= 6 and precedent_support >= 2:
        assessment = 'Moderate legal position with some precedent support'
    elif strength_score >= 4:
        assessment = 'Weak legal position requiring strategic development'
    else:
        assessment = 'Challenging legal position with significant hurdles'
    
    return {
        'overall_assessment': assessment,
        'confidence_level': strength_score,
        'precedent_support_count': precedent_support,
        'recommendation': 'Consult with experienced litigator' if strength_score < 6 else 'Proceed with appropriate strategy'
    }

def _generate_strategic_recommendations(research_result, case_analysis, precedent_analysis):
    """Generate strategic recommendations"""
    recommendations = []
    
    if case_analysis.get('strength_score', 0) < 6:
        recommendations.append('Consider settlement negotiations')
        recommendations.append('Strengthen factual development through discovery')
    
    if len(precedent_analysis.get('adverse_precedents', [])) > 2:
        recommendations.append('Develop distinguishing arguments for adverse precedents')
    
    if len(research_result.get('legal_issues', [])) > 3:
        recommendations.append('Focus on strongest legal theories')
    
    recommendations.extend([
        'Update legal research closer to filing deadlines',
        'Consider expert witness testimony if technical issues involved',
        'Document all attorney-client communications properly'
    ])
    
    return recommendations

@app.route('/api/attorney/case-history', methods=['GET'])
def get_attorney_case_history():
    """Retrieve attorney's case history with privilege protection"""
    try:
        attorney_id = session.get('attorney_id')
        client_id = session.get('client_id')
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        # Security check
        if not privilege_manager.verify_privileged_access(
            attorney_id, client_id, session.get('session_token')
        ):
            return jsonify({'error': 'Unauthorized privileged access'}), 403
        
        # Retrieve case history
        case_history = legal_db.get_attorney_case_history(attorney_id, client_id)
        
        # Decrypt privileged data
        decrypted_history = privilege_manager.decrypt_privileged_history(case_history)
        
        return jsonify({
            'attorney_id': attorney_id,
            'client_id': client_id,
            'case_history': decrypted_history,
            'total_cases': len(decrypted_history),
            'privileged_communication': True
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve attorney case history: {str(e)}")
        return jsonify({'error': 'Failed to retrieve case history'}), 500

@app.route('/api/legal/ethics-dashboard', methods=['GET'])
def get_ethics_compliance_dashboard():
    """Get legal ethics compliance dashboard for attorneys"""
    try:
        attorney_id = session.get('attorney_id')
        
        if not attorney_id:
            return jsonify({'error': 'No active attorney session'}), 401
        
        dashboard_data = ethics_monitor.get_ethics_dashboard_data(attorney_id)
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve ethics dashboard: {str(e)}")
        return jsonify({'error': 'Failed to retrieve ethics dashboard'}), 500

@app.route('/api/admin/legal-metrics', methods=['GET'])
def get_legal_system_metrics():
    """Get legal system performance metrics for administrators"""
    try:
        # This would require admin authentication in production
        metrics = ethics_monitor.get_legal_system_metrics()
        
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve legal system metrics: {str(e)}")
        return jsonify({'error': 'Failed to retrieve legal metrics'}), 500

@app.route('/api/legal/knowledge-search', methods=['POST'])
def search_legal_knowledge():
    """Search legal knowledge base with RAG"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        legal_area = data.get('legal_area', 'general')
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        results = research_agent.search_legal_knowledge_base(query, legal_area)
        
        return jsonify({
            'query': query,
            'legal_area': legal_area,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to search legal knowledge base: {str(e)}")
        return jsonify({'error': 'Legal knowledge search failed'}), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Legal API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Legal AI system internal error: {str(error)}")
    return jsonify({'error': 'Legal AI system internal error'}), 500

# Application startup

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Start the Flask application
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Legal AI Pod - Case Intelligence System on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("Attorney-client privilege protection: ENABLED")
    logger.info("Legal ethics compliance monitoring: ENABLED")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )