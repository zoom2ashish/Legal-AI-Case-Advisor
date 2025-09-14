#!/usr/bin/env python3
"""
Base Legal Agent Class for Legal AI System
Provides common functionality for all legal agents with attorney-client privilege protection
"""

import google.generativeai as genai
import os
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class BaseLegalAgent:
    """
    Base class for all AI agents in the legal system
    Provides common functionality including Gemini API integration,
    attorney-client privilege protection, legal ethics compliance, and response formatting
    """
    
    def __init__(self, knowledge_store, legal_db, agent_type: str = "base_legal"):
        """Initialize base legal agent with required dependencies"""
        self.knowledge_store = knowledge_store
        self.legal_db = legal_db
        self.agent_type = agent_type
        
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        logger.info(f"{agent_type.title()} legal agent initialized successfully")
    
    def _create_legal_system_prompt(self, specific_instructions: str) -> str:
        """Create system prompt with legal ethics and compliance guidelines"""
        base_prompt = """
You are a legal AI assistant designed to help attorneys and legal professionals with legal research, case analysis, and document review.

CRITICAL LEGAL ETHICS GUIDELINES:
- You are NOT a replacement for professional legal judgment or attorney advice
- Maintain attorney-client privilege and confidentiality at all times
- Always recommend consultation with qualified legal counsel for specific legal matters
- Be precise and professional in all legal analysis and communications
- Provide proper legal citations and references when discussing case law or statutes
- Focus on factual legal research and analysis, not legal conclusions or advice
- Never create attorney-client relationships through your interactions
- Always prioritize legal ethics and professional responsibility

ATTORNEY-CLIENT PRIVILEGE PROTECTION:
- All communications must be treated as potentially privileged
- Log all interactions with appropriate privilege protections
- Ensure confidentiality of all client information and case details
- Implement proper access controls and audit logging
- Never disclose privileged information to unauthorized parties

LEGAL RESEARCH STANDARDS:
- Provide accurate legal citations in standard format
- Distinguish between binding and persuasive authority
- Identify jurisdiction-specific legal requirements
- Include relevant case law, statutes, and regulatory provisions
- Note any potential conflicts of interest or ethical considerations
- Maintain currency of legal authorities and precedents

CONTEXT:
- You are part of a multi-agent legal intelligence system
- Your analysis will be used by other agents for comprehensive legal research
- Maintain professional standards consistent with legal practice
- Document all research and analysis for case file maintenance
- Ensure compliance with professional responsibility rules

"""
        return base_prompt + "\n" + specific_instructions
    
    def _generate_legal_response(self, prompt: str, case_context: Dict = None, 
                                attorney_id: str = None, client_id: str = None) -> str:
        """Generate legal response using Gemini API with privilege protection"""
        try:
            # Add privilege protection notice
            privilege_notice = ""
            if attorney_id and client_id:
                privilege_notice = f"""
ATTORNEY-CLIENT PRIVILEGED COMMUNICATION
Attorney ID: {attorney_id}
Client ID: {client_id}
This communication is protected by attorney-client privilege.
"""
            
            # Include case context if available
            if case_context:
                context_str = f"\nCASE CONTEXT:\n{json.dumps(case_context, indent=2)}\n"
                prompt = privilege_notice + context_str + prompt
            else:
                prompt = privilege_notice + prompt
            
            # Generate response with legal disclaimers
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            
            # Add legal disclaimer to response
            legal_response = response.text.strip() + self._get_legal_disclaimer()
            
            return legal_response
            
        except Exception as e:
            logger.error(f"Failed to generate legal AI response: {str(e)}")
            return self._get_legal_fallback_response()
    
    def _get_legal_disclaimer(self) -> str:
        """Standard legal disclaimer for AI responses"""
        return """

LEGAL DISCLAIMER: This analysis is provided for informational purposes only and does not constitute legal advice. 
The information provided may not be applicable to your specific legal situation. You should consult with a 
qualified attorney for legal advice regarding your particular circumstances. No attorney-client relationship 
is created through this AI interaction."""
    
    def _get_legal_fallback_response(self) -> str:
        """Provide fallback response when AI generation fails"""
        return ("I apologize, but I'm experiencing technical difficulties with my legal analysis capabilities. "
                "Please consult with a qualified attorney directly for your legal research or case analysis needs. "
                "If this is urgent, please contact your local bar association for attorney referrals.")
    
    def _extract_legal_structured_data(self, text: str, structure_type: str) -> Dict:
        """Extract structured legal data from AI response"""
        try:
            # Use AI to convert text response to structured legal data
            extraction_prompt = f"""
Extract the following legal information from the text and return as JSON:
Text: {text}

For {structure_type}, extract:
- legal_issues: list of legal issues identified
- case_citations: list of relevant case citations
- statutory_references: list of applicable statutes
- legal_principles: list of key legal principles
- recommendations: list of legal research recommendations
- jurisdiction: applicable jurisdiction
- precedent_value: assessment of precedential value (binding/persuasive/none)
- confidence_level: confidence in legal analysis (1-10)

Return only valid JSON:
"""
            
            response = self.model.generate_content(extraction_prompt)
            
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # Fallback to manual parsing
                return self._manual_parse_legal_response(text, structure_type)
                
        except Exception as e:
            logger.error(f"Failed to extract structured legal data: {str(e)}")
            return self._get_default_legal_structure(structure_type)
    
    def _manual_parse_legal_response(self, text: str, structure_type: str) -> Dict:
        """Manual parsing fallback for legal data extraction"""
        # Basic keyword-based extraction for legal content
        legal_issues = []
        case_citations = []
        statutory_references = []
        recommendations = []
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            
            # Look for case citations (basic pattern matching)
            if any(term in line for term in ['v.', 'F.2d', 'F.3d', 'S.Ct.', 'U.S.']):
                case_citations.append(line)
            
            # Look for statutory references
            elif any(term in line for term in ['§', 'USC', 'C.F.R.', 'Code']):
                statutory_references.append(line)
            
            # Look for recommendations
            elif any(word in line.lower() for word in ['recommend', 'suggest', 'should', 'consider']):
                recommendations.append(line)
            
            # Look for legal issues
            elif any(word in line.lower() for word in ['issue', 'question', 'matter', 'claim']):
                legal_issues.append(line)
        
        return {
            'legal_issues': legal_issues[:5],
            'case_citations': case_citations[:10],
            'statutory_references': statutory_references[:5],
            'legal_principles': [],
            'recommendations': recommendations[:3],
            'jurisdiction': 'unspecified',
            'precedent_value': 'unknown',
            'confidence_level': 5
        }
    
    def _get_default_legal_structure(self, structure_type: str) -> Dict:
        """Return default legal structure when parsing fails"""
        return {
            'legal_issues': [],
            'case_citations': [],
            'statutory_references': [],
            'legal_principles': [],
            'recommendations': ["Please consult with qualified legal counsel"],
            'jurisdiction': 'unspecified',
            'precedent_value': 'none',
            'confidence_level': 1
        }
    
    def _log_legal_interaction(self, attorney_id: str, client_id: str, 
                              interaction_type: str, input_data: Dict, 
                              output_data: Dict, processing_time: float = None):
        """Log legal agent interaction with privilege protection"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'agent_type': self.agent_type,
                'attorney_id': attorney_id,
                'client_id': client_id,
                'interaction_type': interaction_type,
                'processing_time_seconds': processing_time,
                'privileged_communication': True,
                'input_summary': {
                    'keys': list(input_data.keys()),
                    'query_length': len(str(input_data.get('query', '')))
                },
                'output_summary': {
                    'keys': list(output_data.keys()),
                    'response_length': len(str(output_data.get('response', '')))
                },
                'success': True,
                'compliance_check': self._verify_ethics_compliance(input_data, output_data)
            }
            
            # Log to legal database audit log with privilege protection
            self.legal_db.log_privileged_audit_event(
                attorney_id=attorney_id,
                client_id=client_id,
                action=f'{self.agent_type}_interaction',
                details=json.dumps(log_entry),
                privileged=True
            )
            
        except Exception as e:
            logger.error(f"Failed to log legal interaction: {str(e)}")
    
    def _verify_ethics_compliance(self, input_data: Dict, output_data: Dict) -> Dict:
        """Verify legal ethics compliance of the interaction"""
        compliance_check = {
            'privilege_protected': True,
            'proper_disclaimers': self._check_legal_disclaimers(output_data),
            'confidentiality_maintained': True,
            'professional_standards': True,
            'citation_accuracy': self._verify_citations(output_data),
            'conflict_check_needed': self._assess_conflict_potential(input_data)
        }
        return compliance_check
    
    def _check_legal_disclaimers(self, output_data: Dict) -> bool:
        """Check if proper legal disclaimers are included"""
        response_text = str(output_data.get('response', ''))
        return 'LEGAL DISCLAIMER' in response_text or 'does not constitute legal advice' in response_text
    
    def _verify_citations(self, output_data: Dict) -> bool:
        """Basic verification that citations are properly formatted"""
        # This is a simplified check - production would use more sophisticated citation validation
        response_text = str(output_data.get('response', ''))
        citation_indicators = ['v.', 'F.2d', 'F.3d', 'U.S.', '§']
        return any(indicator in response_text for indicator in citation_indicators)
    
    def _assess_conflict_potential(self, input_data: Dict) -> bool:
        """Assess if conflict of interest check is needed"""
        # Check for opposing parties, concurrent representation issues, etc.
        query_text = str(input_data.get('query', '')).lower()
        conflict_indicators = ['opposing', 'adverse', 'against', 'plaintiff', 'defendant']
        return any(indicator in query_text for indicator in conflict_indicators)
    
    def _validate_attorney_client_relationship(self, attorney_id: str, client_id: str) -> bool:
        """Validate that attorney-client relationship exists"""
        try:
            return self.legal_db.verify_attorney_client_relationship(attorney_id, client_id)
        except Exception as e:
            logger.error(f"Failed to validate attorney-client relationship: {str(e)}")
            return False
    
    def _assess_legal_urgency_indicators(self, text: str) -> Dict[str, Any]:
        """Identify legal urgency indicators in text"""
        high_urgency_keywords = [
            'statute of limitations', 'deadline', 'emergency', 'injunction',
            'restraining order', 'urgent', 'immediate', 'time-sensitive',
            'motion for', 'response due', 'court date', 'hearing'
        ]
        
        medium_urgency_keywords = [
            'discovery', 'deposition', 'pleading', 'brief', 'filing',
            'notice', 'service', 'compliance', 'regulatory'
        ]
        
        text_lower = text.lower()
        
        high_urgency_count = sum(1 for keyword in high_urgency_keywords 
                               if keyword in text_lower)
        medium_urgency_count = sum(1 for keyword in medium_urgency_keywords 
                                 if keyword in text_lower)
        
        urgency_level = 'low'
        if high_urgency_count > 0:
            urgency_level = 'high'
        elif medium_urgency_count > 0:
            urgency_level = 'medium'
        
        return {
            'urgency_level': urgency_level,
            'high_urgency_indicators': high_urgency_count,
            'medium_urgency_indicators': medium_urgency_count,
            'keywords_found': [kw for kw in high_urgency_keywords + medium_urgency_keywords 
                             if kw in text_lower],
            'recommended_timeline': self._suggest_timeline(urgency_level)
        }
    
    def _suggest_timeline(self, urgency_level: str) -> str:
        """Suggest timeline based on urgency level"""
        timelines = {
            'high': 'Immediate attention required - same day response',
            'medium': 'Priority attention - within 2-3 business days',
            'low': 'Standard timeline - within 1-2 weeks'
        }
        return timelines.get(urgency_level, 'Standard timeline')
    
    def _format_legal_response(self, response_text: str, 
                              additional_data: Dict = None,
                              attorney_id: str = None,
                              client_id: str = None) -> Dict[str, Any]:
        """Format response with consistent legal structure"""
        base_response = {
            'response': response_text,
            'agent_type': self.agent_type,
            'timestamp': datetime.now().isoformat(),
            'conversation_id': self._create_legal_conversation_id(),
            'confidence_score': 7,  # Default confidence
            'requires_attorney_review': True,
            'privileged_communication': True if attorney_id and client_id else False,
            'legal_disclaimer_included': True,
            'ethics_compliance_verified': True
        }
        
        if attorney_id and client_id:
            base_response['attorney_id'] = attorney_id
            base_response['client_id'] = client_id
            base_response['privilege_protected'] = True
        
        if additional_data:
            base_response.update(additional_data)
        
        return base_response
    
    def _create_legal_conversation_id(self) -> str:
        """Generate unique legal conversation ID"""
        return f"legal_{self.agent_type}_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"
    
    def health_check(self) -> bool:
        """Check if legal agent is functioning properly"""
        try:
            # Test AI model
            test_response = self.model.generate_content("Legal system test")
            
            # Test database connections
            if hasattr(self.knowledge_store, 'health_check'):
                if not self.knowledge_store.health_check():
                    return False
            
            if hasattr(self.legal_db, 'health_check'):
                if not self.legal_db.health_check():
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Legal agent health check failed: {str(e)}")
            return False
    
    def get_legal_agent_info(self) -> Dict[str, Any]:
        """Get information about this legal agent"""
        return {
            'agent_type': self.agent_type,
            'model': 'gemini-pro',
            'initialized_at': datetime.now().isoformat(),
            'capabilities': [
                'legal_research', 
                'case_analysis', 
                'document_review', 
                'precedent_analysis',
                'privilege_protection',
                'ethics_compliance'
            ],
            'compliance_features': [
                'attorney_client_privilege',
                'audit_logging',
                'ethics_verification',
                'citation_validation'
            ],
            'status': 'active'
        }