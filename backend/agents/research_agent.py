#!/usr/bin/env python3
"""
Legal Research Agent for Legal AI System
Conducts comprehensive legal research including case law, statutes, and legal precedents
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import time

from .base_legal_agent import BaseLegalAgent

logger = logging.getLogger(__name__)

class LegalResearchAgent(BaseLegalAgent):
    """
    Specialized agent for conducting comprehensive legal research
    Handles case law analysis, statutory research, and legal issue identification
    """
    
    def __init__(self, knowledge_store, legal_db):
        """Initialize legal research agent"""
        super().__init__(knowledge_store, legal_db, "legal_research")
        self.research_specialties = [
            "case_law_analysis",
            "statutory_interpretation", 
            "regulatory_research",
            "legal_precedent_identification",
            "jurisdiction_analysis"
        ]
    
    def conduct_legal_research(self, query: str, jurisdiction: str = "federal",
                              attorney_id: str = None, client_id: str = None,
                              research_context: Dict = None) -> Dict[str, Any]:
        """
        Conduct comprehensive legal research on a given query
        
        Args:
            query: Legal research question or issue
            jurisdiction: Legal jurisdiction (federal, state, etc.)
            attorney_id: ID of requesting attorney
            client_id: ID of client (if applicable)
            research_context: Additional context for research
            
        Returns:
            Dict containing comprehensive research results
        """
        start_time = time.time()
        
        try:
            # Validate attorney-client relationship if both IDs provided
            if attorney_id and client_id:
                if not self._validate_attorney_client_relationship(attorney_id, client_id):
                    raise PermissionError("Invalid attorney-client relationship")
            
            # Create specialized research prompt
            research_prompt = self._create_research_system_prompt(query, jurisdiction, research_context)
            
            # Generate legal research response
            ai_response = self._generate_legal_response(
                research_prompt, 
                research_context,
                attorney_id,
                client_id
            )
            
            # Extract structured legal research data
            structured_data = self._extract_legal_structured_data(ai_response, "legal_research")
            
            # Search legal knowledge base for relevant authorities
            legal_authorities = self._search_legal_authorities(query, jurisdiction)
            
            # Assess urgency and timeline
            urgency_assessment = self._assess_legal_urgency_indicators(query)
            
            # Compile comprehensive research results
            research_results = {
                'query': query,
                'jurisdiction': jurisdiction,
                'ai_analysis': ai_response,
                'legal_issues': structured_data.get('legal_issues', []),
                'case_authorities': legal_authorities.get('cases', []),
                'statutory_authorities': legal_authorities.get('statutes', []),
                'regulatory_authorities': legal_authorities.get('regulations', []),
                'legal_principles': structured_data.get('legal_principles', []),
                'research_recommendations': structured_data.get('recommendations', []),
                'citation_analysis': self._analyze_citations(legal_authorities),
                'precedent_strength': self._assess_precedent_strength(legal_authorities),
                'urgency_assessment': urgency_assessment,
                'research_confidence': structured_data.get('confidence_level', 5),
                'follow_up_research': self._suggest_follow_up_research(structured_data),
                'timestamp': datetime.now().isoformat()
            }
            
            # Format final response
            formatted_response = self._format_legal_response(
                ai_response,
                {
                    'research_results': research_results,
                    'legal_authorities_found': len(legal_authorities.get('cases', [])) + 
                                             len(legal_authorities.get('statutes', [])),
                    'research_type': 'comprehensive_legal_research',
                    'jurisdiction_coverage': jurisdiction
                },
                attorney_id,
                client_id
            )
            
            # Log research interaction
            processing_time = time.time() - start_time
            self._log_legal_interaction(
                attorney_id or 'unknown',
                client_id or 'unknown',
                'legal_research',
                {'query': query, 'jurisdiction': jurisdiction},
                formatted_response,
                processing_time
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Legal research failed: {str(e)}")
            return self._create_error_response(str(e), attorney_id, client_id)
    
    def _create_research_system_prompt(self, query: str, jurisdiction: str, 
                                     context: Dict = None) -> str:
        """Create specialized prompt for legal research"""
        specific_instructions = f"""
You are conducting legal research for the following query in {jurisdiction} jurisdiction:

RESEARCH QUERY: {query}

Please provide comprehensive legal research covering:

1. LEGAL ISSUE IDENTIFICATION:
   - Identify the primary legal issues and questions
   - Determine the applicable area(s) of law
   - Note any procedural or substantive law distinctions

2. CASE LAW ANALYSIS:
   - Find relevant case precedents with proper citations
   - Distinguish binding vs. persuasive authority
   - Analyze key holdings and legal reasoning
   - Note any circuit splits or conflicting decisions

3. STATUTORY ANALYSIS:
   - Identify applicable federal and state statutes
   - Provide exact statutory citations and text
   - Analyze statutory interpretation issues
   - Note any recent amendments or changes

4. REGULATORY CONSIDERATIONS:
   - Identify relevant regulations and administrative guidance
   - Note agency interpretations and enforcement policies
   - Consider regulatory compliance requirements

5. JURISDICTIONAL ANALYSIS:
   - Determine proper jurisdiction and venue
   - Consider choice of law issues
   - Note any federal vs. state law conflicts

6. PRACTICAL RECOMMENDATIONS:
   - Suggest litigation strategy considerations
   - Identify potential defenses or counterclaims
   - Recommend additional research areas
   - Note any ethical considerations

Provide proper legal citations in Bluebook format.
Include assessment of legal precedent strength and applicability.
Note any time-sensitive issues or deadlines.
"""
        
        if context:
            specific_instructions += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"
        
        return self._create_legal_system_prompt(specific_instructions)
    
    def _search_legal_authorities(self, query: str, jurisdiction: str) -> Dict[str, List]:
        """Search legal knowledge base for relevant authorities"""
        try:
            # Search case law
            case_results = self.knowledge_store.search_case_law(query, jurisdiction, limit=10)
            
            # Search statutes
            statute_results = self.knowledge_store.search_statutes(query, jurisdiction, limit=5)
            
            # Search regulations
            regulation_results = self.knowledge_store.search_regulations(query, jurisdiction, limit=5)
            
            # Search legal precedents
            precedent_results = self.knowledge_store.search_precedents(query, jurisdiction, limit=15)
            
            return {
                'cases': case_results,
                'statutes': statute_results,
                'regulations': regulation_results,
                'precedents': precedent_results
            }
            
        except Exception as e:
            logger.error(f"Failed to search legal authorities: {str(e)}")
            return {'cases': [], 'statutes': [], 'regulations': [], 'precedents': []}
    
    def _analyze_citations(self, legal_authorities: Dict) -> Dict[str, Any]:
        """Analyze the strength and relevance of legal citations"""
        try:
            total_authorities = (len(legal_authorities.get('cases', [])) + 
                               len(legal_authorities.get('statutes', [])) + 
                               len(legal_authorities.get('regulations', [])))
            
            # Categorize by authority type
            binding_cases = [case for case in legal_authorities.get('cases', []) 
                           if case.get('precedent_type') == 'binding']
            persuasive_cases = [case for case in legal_authorities.get('cases', []) 
                              if case.get('precedent_type') == 'persuasive']
            
            citation_analysis = {
                'total_authorities_found': total_authorities,
                'binding_precedents': len(binding_cases),
                'persuasive_precedents': len(persuasive_cases),
                'statutory_authorities': len(legal_authorities.get('statutes', [])),
                'regulatory_authorities': len(legal_authorities.get('regulations', [])),
                'authority_strength': self._calculate_authority_strength(legal_authorities),
                'citation_completeness': self._assess_citation_completeness(legal_authorities)
            }
            
            return citation_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze citations: {str(e)}")
            return {'total_authorities_found': 0, 'authority_strength': 'unknown'}
    
    def _calculate_authority_strength(self, legal_authorities: Dict) -> str:
        """Calculate overall strength of legal authorities"""
        binding_count = len([case for case in legal_authorities.get('cases', []) 
                           if case.get('precedent_type') == 'binding'])
        total_cases = len(legal_authorities.get('cases', []))
        statute_count = len(legal_authorities.get('statutes', []))
        
        if binding_count >= 3 and statute_count >= 1:
            return 'strong'
        elif binding_count >= 1 or (total_cases >= 3 and statute_count >= 1):
            return 'moderate'
        elif total_cases >= 1 or statute_count >= 1:
            return 'weak'
        else:
            return 'insufficient'
    
    def _assess_citation_completeness(self, legal_authorities: Dict) -> str:
        """Assess completeness of legal citations"""
        total_authorities = sum(len(auth_list) for auth_list in legal_authorities.values())
        
        if total_authorities >= 10:
            return 'comprehensive'
        elif total_authorities >= 5:
            return 'adequate'
        elif total_authorities >= 2:
            return 'limited'
        else:
            return 'insufficient'
    
    def _assess_precedent_strength(self, legal_authorities: Dict) -> Dict[str, Any]:
        """Assess the strength of legal precedents"""
        cases = legal_authorities.get('cases', [])
        
        if not cases:
            return {'overall_strength': 'none', 'analysis': 'No case precedents found'}
        
        binding_cases = [case for case in cases if case.get('precedent_type') == 'binding']
        recent_cases = [case for case in cases 
                       if case.get('decision_year', 0) >= (datetime.now().year - 5)]
        
        strength_factors = {
            'binding_precedents': len(binding_cases),
            'recent_precedents': len(recent_cases),
            'total_precedents': len(cases),
            'jurisdiction_matches': len([case for case in cases 
                                       if case.get('jurisdiction') == 'federal']),
            'highly_cited_cases': len([case for case in cases 
                                     if case.get('citation_count', 0) > 100])
        }
        
        # Calculate overall precedent strength
        if strength_factors['binding_precedents'] >= 2 and strength_factors['recent_precedents'] >= 1:
            overall_strength = 'very_strong'
        elif strength_factors['binding_precedents'] >= 1 or strength_factors['recent_precedents'] >= 2:
            overall_strength = 'strong'
        elif strength_factors['total_precedents'] >= 3:
            overall_strength = 'moderate'
        elif strength_factors['total_precedents'] >= 1:
            overall_strength = 'weak'
        else:
            overall_strength = 'none'
        
        return {
            'overall_strength': overall_strength,
            'strength_factors': strength_factors,
            'analysis': self._generate_precedent_strength_analysis(strength_factors, overall_strength)
        }
    
    def _generate_precedent_strength_analysis(self, factors: Dict, strength: str) -> str:
        """Generate analysis of precedent strength"""
        analyses = {
            'very_strong': f"Strong precedential support with {factors['binding_precedents']} binding cases and {factors['recent_precedents']} recent decisions.",
            'strong': f"Good precedential support with {factors['binding_precedents']} binding cases or {factors['recent_precedents']} recent decisions.",
            'moderate': f"Moderate precedential support with {factors['total_precedents']} relevant cases found.",
            'weak': f"Limited precedential support with only {factors['total_precedents']} relevant case(s).",
            'none': "No relevant precedents found. Additional research may be needed."
        }
        return analyses.get(strength, "Precedent strength analysis unavailable.")
    
    def _suggest_follow_up_research(self, structured_data: Dict) -> List[str]:
        """Suggest additional research areas"""
        suggestions = []
        
        legal_issues = structured_data.get('legal_issues', [])
        confidence = structured_data.get('confidence_level', 5)
        
        if confidence < 7:
            suggestions.append("Consider broader keyword search to identify additional authorities")
        
        if len(legal_issues) > 3:
            suggestions.append("Complex case with multiple issues - consider focused research on each issue")
        
        suggestions.extend([
            "Review recent law review articles and legal commentary",
            "Check for pending legislation or regulatory changes",
            "Consider researching similar cases in other jurisdictions",
            "Review practice guides and continuing legal education materials"
        ])
        
        return suggestions[:4]  # Limit to top 4 suggestions
    
    def search_case_law(self, case_query: str, jurisdiction: str = "all") -> Dict[str, Any]:
        """Specialized case law search"""
        try:
            # Search knowledge base for cases
            case_results = self.knowledge_store.search_case_law(case_query, jurisdiction, limit=20)
            
            # Analyze and categorize results
            categorized_results = {
                'binding_authority': [],
                'persuasive_authority': [],
                'adverse_authority': [],
                'related_cases': []
            }
            
            for case in case_results:
                if case.get('precedent_type') == 'binding':
                    categorized_results['binding_authority'].append(case)
                elif case.get('precedent_type') == 'persuasive':
                    categorized_results['persuasive_authority'].append(case)
                else:
                    categorized_results['related_cases'].append(case)
            
            return {
                'query': case_query,
                'jurisdiction': jurisdiction,
                'total_cases_found': len(case_results),
                'categorized_results': categorized_results,
                'search_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Case law search failed: {str(e)}")
            return {'error': str(e), 'total_cases_found': 0}
    
    def _create_error_response(self, error_message: str, attorney_id: str = None, 
                              client_id: str = None) -> Dict[str, Any]:
        """Create error response for failed research"""
        return self._format_legal_response(
            f"Legal research encountered an error: {error_message}. "
            "Please consult with qualified legal counsel for assistance with your research needs.",
            {
                'error': True,
                'error_message': error_message,
                'research_results': None,
                'requires_manual_research': True
            },
            attorney_id,
            client_id
        )