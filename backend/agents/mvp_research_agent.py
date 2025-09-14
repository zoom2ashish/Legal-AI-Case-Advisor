#!/usr/bin/env python3
"""
Legal Research Agent for MVP
Conducts basic legal research with case law analysis and precedent discovery
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

class MVPResearchAgent:
    """Conducts basic legal research for MVP"""
    
    def __init__(self, db_manager, privilege_manager):
        """Initialize the legal research agent"""
        self.db_manager = db_manager
        self.privilege_manager = privilege_manager
        
        # Configure Gemini AI for legal research
        try:
            if GEMINI_AVAILABLE:
                api_key = os.getenv('GEMINI_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-pro')
                    logger.info("Gemini AI configured for legal research")
                else:
                    logger.warning("GEMINI_API_KEY not found - using mock responses")
                    self.model = None
            else:
                logger.warning("google-generativeai not available - using mock responses")
                self.model = None
        except Exception as e:
            logger.error(f"Failed to configure Gemini AI: {str(e)}")
            self.model = None
    
    def conduct_legal_research(self, query: str, jurisdiction: str = "federal", 
                             attorney_id: str = None, client_id: str = None) -> Dict[str, Any]:
        """
        Conduct comprehensive legal research
        """
        try:
            start_time = datetime.now()
            
            # Log research activity
            if attorney_id:
                self.privilege_manager.log_legal_research_activity(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    query=query,
                    jurisdiction=jurisdiction
                )
            
            # Search case law database
            case_results = self.db_manager.search_case_law(query, jurisdiction, limit=10)
            
            # Search statutes
            statute_results = self.db_manager.search_statutes(query, jurisdiction, limit=5)
            
            # Search precedents
            precedent_results = self.db_manager.search_precedents(query, jurisdiction, limit=8)
            
            # Generate AI analysis if available
            ai_analysis = self._generate_ai_analysis(query, case_results, statute_results, precedent_results, jurisdiction)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Compile research results
            research_result = {
                'query': query,
                'jurisdiction': jurisdiction,
                'timestamp': datetime.now().isoformat(),
                'case_law_results': case_results,
                'statute_results': statute_results,
                'precedent_results': precedent_results,
                'ai_analysis': ai_analysis,
                'processing_time_seconds': processing_time,
                'total_results': len(case_results) + len(statute_results) + len(precedent_results),
                'confidence_score': self._calculate_confidence_score(case_results, statute_results, precedent_results)
            }
            
            # Store research results if attorney provided
            if attorney_id:
                self.db_manager.store_legal_research(attorney_id, client_id, query, research_result, jurisdiction)
            
            logger.info(f"Legal research completed for query: '{query}' in {processing_time:.2f}s")
            return research_result
            
        except Exception as e:
            logger.error(f"Failed to conduct legal research: {str(e)}")
            return {
                'error': f'Legal research failed: {str(e)}',
                'query': query,
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_ai_analysis(self, query: str, case_results: List[Dict], 
                            statute_results: List[Dict], precedent_results: List[Dict], 
                            jurisdiction: str) -> Dict[str, Any]:
        """Generate AI-powered legal analysis"""
        try:
            if not self.model:
                return self._generate_mock_analysis(query, case_results, statute_results, precedent_results)
            
            # Prepare context for AI analysis
            context = self._prepare_analysis_context(query, case_results, statute_results, precedent_results, jurisdiction)
            
            # Create legal research prompt
            prompt = f"""
            You are a legal research specialist. Analyze the following legal research query and provide comprehensive analysis.
            
            Query: "{query}"
            Jurisdiction: {jurisdiction}
            
            Research Results:
            {context}
            
            Provide analysis covering:
            1. Key legal principles and precedents
            2. Relevant statutory authority
            3. Potential arguments and counterarguments
            4. Strategic recommendations with proper legal citations
            5. Risk assessment and case strength factors
            
            Maintain attorney-client privilege. Include appropriate legal disclaimers.
            Focus on practical legal advice for solo practitioners.
            """
            
            # Generate AI response
            response = self.model.generate_content(prompt)
            
            # Parse AI response
            ai_analysis = {
                'analysis_type': 'ai_generated',
                'key_legal_principles': self._extract_legal_principles(response.text),
                'statutory_authority': self._extract_statutory_authority(response.text),
                'strategic_recommendations': self._extract_recommendations(response.text),
                'risk_assessment': self._extract_risk_assessment(response.text),
                'full_analysis': response.text,
                'disclaimers': [
                    "This analysis is for informational purposes only and does not constitute legal advice.",
                    "Consult with qualified legal counsel for specific legal matters.",
                    "AI-generated content should be reviewed by licensed attorneys."
                ]
            }
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"Failed to generate AI analysis: {str(e)}")
            return self._generate_mock_analysis(query, case_results, statute_results, precedent_results)
    
    def _prepare_analysis_context(self, query: str, case_results: List[Dict], 
                                statute_results: List[Dict], precedent_results: List[Dict], 
                                jurisdiction: str) -> str:
        """Prepare context for AI analysis"""
        context_parts = []
        
        # Add case law context
        if case_results:
            context_parts.append("CASE LAW:")
            for case in case_results[:3]:  # Limit to top 3 cases
                context_parts.append(f"- {case['case_name']} ({case['citation']}): {case.get('holding', 'No holding available')}")
        
        # Add statute context
        if statute_results:
            context_parts.append("\nSTATUTES:")
            for statute in statute_results[:2]:  # Limit to top 2 statutes
                context_parts.append(f"- {statute['title']} ({statute['citation']}): {statute.get('summary', 'No summary available')}")
        
        # Add precedent context
        if precedent_results:
            context_parts.append("\nPRECEDENTS:")
            for precedent in precedent_results[:3]:  # Limit to top 3 precedents
                context_parts.append(f"- {precedent['legal_principle']} (Weight: {precedent['precedent_weight']}/10)")
        
        return "\n".join(context_parts)
    
    def _generate_mock_analysis(self, query: str, case_results: List[Dict], 
                              statute_results: List[Dict], precedent_results: List[Dict]) -> Dict[str, Any]:
        """Generate mock analysis when AI is not available"""
        return {
            'analysis_type': 'database_only',
            'key_legal_principles': [
                f"Research query '{query}' returned {len(case_results)} case law results",
                f"Found {len(statute_results)} relevant statutes",
                f"Identified {len(precedent_results)} legal precedents"
            ],
            'statutory_authority': [statute['citation'] for statute in statute_results[:3]],
            'strategic_recommendations': [
                "Review the case law results for relevant precedents",
                "Consider the statutory authority for your legal position",
                "Analyze precedent weight and binding authority"
            ],
            'risk_assessment': "Manual review of results recommended",
            'full_analysis': f"Database search completed for '{query}' with {len(case_results + statute_results + precedent_results)} total results.",
            'disclaimers': [
                "This is a database search result - AI analysis not available",
                "Manual legal analysis required for specific advice",
                "Consult with qualified legal counsel for legal matters."
            ]
        }
    
    def _extract_legal_principles(self, text: str) -> List[str]:
        """Extract legal principles from AI response"""
        # Simple extraction - would be more sophisticated in production
        principles = []
        lines = text.split('\n')
        for line in lines:
            if 'principle' in line.lower() or 'rule' in line.lower():
                principles.append(line.strip())
        return principles[:5]  # Limit to 5 principles
    
    def _extract_statutory_authority(self, text: str) -> List[str]:
        """Extract statutory authority from AI response"""
        # Simple extraction - would be more sophisticated in production
        authorities = []
        lines = text.split('\n')
        for line in lines:
            if any(code in line.lower() for code in ['usc', 'cfr', 'statute', 'section']):
                authorities.append(line.strip())
        return authorities[:3]  # Limit to 3 authorities
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract strategic recommendations from AI response"""
        # Simple extraction - would be more sophisticated in production
        recommendations = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['recommend', 'suggest', 'consider', 'should']):
                recommendations.append(line.strip())
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _extract_risk_assessment(self, text: str) -> str:
        """Extract risk assessment from AI response"""
        # Simple extraction - would be more sophisticated in production
        lines = text.split('\n')
        for line in lines:
            if 'risk' in line.lower():
                return line.strip()
        return "Risk assessment not available in AI response"
    
    def _calculate_confidence_score(self, case_results: List[Dict], 
                                  statute_results: List[Dict], 
                                  precedent_results: List[Dict]) -> float:
        """Calculate confidence score based on search results"""
        try:
            total_results = len(case_results) + len(statute_results) + len(precedent_results)
            
            if total_results == 0:
                return 0.0
            
            # Base confidence on number of results
            base_score = min(0.8, total_results * 0.1)
            
            # Boost confidence if we have high-weight precedents
            if precedent_results:
                high_weight_precedents = [p for p in precedent_results if p.get('precedent_weight', 0) >= 7]
                if high_weight_precedents:
                    base_score += 0.2
            
            # Boost confidence if we have recent cases
            if case_results:
                recent_cases = [c for c in case_results if c.get('citation_count', 0) >= 5]
                if recent_cases:
                    base_score += 0.1
            
            return min(1.0, base_score)
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence score: {str(e)}")
            return 0.5
    
    def get_research_summary(self, research_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of research results"""
        try:
            summary = {
                'query': research_result.get('query'),
                'jurisdiction': research_result.get('jurisdiction'),
                'total_results': research_result.get('total_results', 0),
                'confidence_score': research_result.get('confidence_score', 0),
                'processing_time': research_result.get('processing_time_seconds', 0),
                'key_findings': [],
                'top_cases': [],
                'relevant_statutes': [],
                'important_precedents': []
            }
            
            # Extract key findings
            ai_analysis = research_result.get('ai_analysis', {})
            if ai_analysis:
                summary['key_findings'] = ai_analysis.get('key_legal_principles', [])[:3]
            
            # Extract top cases
            case_results = research_result.get('case_law_results', [])
            for case in case_results[:3]:
                summary['top_cases'].append({
                    'name': case.get('case_name'),
                    'citation': case.get('citation'),
                    'court': case.get('court'),
                    'relevance': case.get('citation_count', 0)
                })
            
            # Extract relevant statutes
            statute_results = research_result.get('statute_results', [])
            for statute in statute_results[:2]:
                summary['relevant_statutes'].append({
                    'title': statute.get('title'),
                    'citation': statute.get('citation'),
                    'jurisdiction': statute.get('jurisdiction')
                })
            
            # Extract important precedents
            precedent_results = research_result.get('precedent_results', [])
            for precedent in precedent_results[:3]:
                summary['important_precedents'].append({
                    'principle': precedent.get('legal_principle'),
                    'weight': precedent.get('precedent_weight'),
                    'authority': precedent.get('binding_authority')
                })
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate research summary: {str(e)}")
            return {'error': f'Summary generation failed: {str(e)}'}
    
    def health_check(self) -> bool:
        """Check if the research agent is functioning properly"""
        try:
            # Test database connection
            if not self.db_manager.health_check():
                return False
            
            # Test privilege manager
            if not self.privilege_manager.health_check():
                return False
            
            # Test basic search functionality
            test_results = self.db_manager.search_case_law("test", limit=1)
            
            return True
            
        except Exception as e:
            logger.error(f"Research agent health check failed: {str(e)}")
            return False
