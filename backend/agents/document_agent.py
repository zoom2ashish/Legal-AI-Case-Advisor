#!/usr/bin/env python3
"""
Document Review Agent for Legal AI System
Reviews and analyzes legal documents for risks, obligations, and opportunities
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import time
import re

from .base_legal_agent import BaseLegalAgent

logger = logging.getLogger(__name__)

class DocumentReviewAgent(BaseLegalAgent):
    """
    Specialized agent for legal document review and analysis
    Handles contract analysis, risk identification, compliance verification, and clause extraction
    """
    
    def __init__(self, knowledge_store, legal_db):
        """Initialize document review agent"""
        super().__init__(knowledge_store, legal_db, "document_review")
        self.review_capabilities = [
            "contract_analysis",
            "risk_assessment",
            "clause_extraction",
            "compliance_verification",
            "obligation_identification",
            "opportunity_analysis"
        ]
        
        # Document type patterns for classification
        self.document_patterns = {
            'contract': ['agreement', 'contract', 'terms', 'conditions'],
            'lease': ['lease', 'rental', 'tenant', 'landlord'],
            'employment': ['employment', 'job', 'salary', 'benefits'],
            'nda': ['confidentiality', 'non-disclosure', 'proprietary'],
            'purchase': ['purchase', 'buy', 'sale', 'vendor'],
            'license': ['license', 'intellectual property', 'copyright'],
            'merger': ['merger', 'acquisition', 'due diligence']
        }
    
    def review_legal_document(self, document_text: str, document_type: str = None,
                             review_focus: List[str] = None, attorney_id: str = None,
                             client_id: str = None, document_context: Dict = None) -> Dict[str, Any]:
        """
        Comprehensive legal document review and analysis
        
        Args:
            document_text: Full text of the legal document
            document_type: Type of document (contract, lease, etc.)
            review_focus: Specific areas to focus on (risks, obligations, etc.)
            attorney_id: ID of requesting attorney
            client_id: ID of client
            document_context: Additional context about the document
            
        Returns:
            Dict containing comprehensive document analysis
        """
        start_time = time.time()
        
        try:
            # Validate attorney-client relationship
            if attorney_id and client_id:
                if not self._validate_attorney_client_relationship(attorney_id, client_id):
                    raise PermissionError("Invalid attorney-client relationship")
            
            # Auto-detect document type if not provided
            if not document_type:
                document_type = self._classify_document_type(document_text)
            
            # Set default review focus if not provided
            if not review_focus:
                review_focus = ['risks', 'obligations', 'key_terms', 'compliance']
            
            # Create document review prompt
            review_prompt = self._create_document_review_prompt(
                document_text, document_type, review_focus, document_context
            )
            
            # Generate AI document analysis
            ai_response = self._generate_legal_response(
                review_prompt,
                document_context,
                attorney_id,
                client_id
            )
            
            # Extract structured document data
            structured_analysis = self._extract_legal_structured_data(ai_response, "document_review")
            
            # Perform detailed document analysis
            document_analysis = self._perform_detailed_document_analysis(
                document_text, document_type, review_focus
            )
            
            # Extract key clauses and terms
            key_clauses = self._extract_key_clauses(document_text, document_type)
            
            # Identify risks and opportunities
            risk_analysis = self._analyze_document_risks(document_text, document_type)
            opportunity_analysis = self._analyze_document_opportunities(document_text, document_type)
            
            # Assess compliance requirements
            compliance_analysis = self._assess_compliance_requirements(document_text, document_type)
            
            # Generate redline suggestions
            redline_suggestions = self._generate_redline_suggestions(
                document_text, document_type, risk_analysis
            )
            
            # Compile comprehensive document review
            document_review = {
                'document_type': document_type,
                'document_length': len(document_text),
                'review_focus': review_focus,
                'ai_analysis': ai_response,
                'document_classification': self._classify_document_complexity(document_text),
                'key_clauses': key_clauses,
                'risk_analysis': risk_analysis,
                'opportunity_analysis': opportunity_analysis,
                'compliance_analysis': compliance_analysis,
                'obligations_summary': self._extract_obligations_summary(document_analysis),
                'rights_summary': self._extract_rights_summary(document_analysis),
                'financial_terms': self._extract_financial_terms(document_text),
                'timeline_provisions': self._extract_timeline_provisions(document_text),
                'redline_suggestions': redline_suggestions,
                'negotiation_points': self._identify_negotiation_points(risk_analysis, opportunity_analysis),
                'overall_recommendation': self._generate_overall_recommendation(risk_analysis, opportunity_analysis),
                'review_confidence': structured_analysis.get('confidence_level', 6),
                'timestamp': datetime.now().isoformat()
            }
            
            # Format final response
            formatted_response = self._format_legal_response(
                ai_response,
                {
                    'document_review': document_review,
                    'review_type': 'comprehensive_document_review',
                    'document_type': document_type,
                    'risks_identified': len(risk_analysis.get('identified_risks', [])),
                    'opportunities_identified': len(opportunity_analysis.get('identified_opportunities', [])),
                    'requires_attorney_review': self._determine_attorney_review_requirement(risk_analysis)
                },
                attorney_id,
                client_id
            )
            
            # Log document review interaction
            processing_time = time.time() - start_time
            self._log_legal_interaction(
                attorney_id or 'unknown',
                client_id or 'unknown',
                'document_review',
                {'document_type': document_type, 'document_length': len(document_text)},
                formatted_response,
                processing_time
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Document review failed: {str(e)}")
            return self._create_error_response(str(e), attorney_id, client_id)
    
    def _classify_document_type(self, document_text: str) -> str:
        """Automatically classify document type"""
        text_lower = document_text.lower()
        type_scores = {}
        
        for doc_type, patterns in self.document_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                type_scores[doc_type] = score
        
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return 'general_legal_document'
    
    def _create_document_review_prompt(self, document_text: str, document_type: str,
                                     review_focus: List[str], context: Dict = None) -> str:
        """Create specialized prompt for document review"""
        focus_text = ", ".join(review_focus)
        
        # Truncate document if too long for prompt
        if len(document_text) > 8000:
            document_excerpt = document_text[:4000] + "\n\n[DOCUMENT TRUNCATED]\n\n" + document_text[-4000:]
        else:
            document_excerpt = document_text
        
        specific_instructions = f"""
You are conducting comprehensive legal document review for a {document_type} with focus on: {focus_text}.

DOCUMENT TEXT:
{document_excerpt}

Please provide thorough document analysis covering:

1. DOCUMENT OVERVIEW:
   - Document type and purpose
   - Parties involved and their roles
   - Key terms and effective dates
   - Overall document structure assessment

2. KEY CLAUSE ANALYSIS:
   - Critical contractual provisions
   - Payment and performance terms
   - Termination and renewal clauses
   - Dispute resolution mechanisms
   - Liability and indemnification provisions

3. RISK ASSESSMENT:
   - Identify potential legal risks
   - Financial exposure analysis
   - Performance and delivery risks
   - Regulatory compliance risks
   - Enforceability concerns

4. OBLIGATIONS ANALYSIS:
   - Client's obligations and responsibilities
   - Counterparty obligations
   - Performance standards and deadlines
   - Reporting and communication requirements
   - Compliance and regulatory obligations

5. RIGHTS AND BENEFITS:
   - Client's rights and protections
   - Intellectual property rights
   - Termination rights and procedures
   - Remedy and enforcement options
   - Limitation of liability provisions

6. COMPLIANCE VERIFICATION:
   - Regulatory compliance requirements
   - Industry-specific standards
   - Legal formality requirements
   - Documentation completeness

7. NEGOTIATION OPPORTUNITIES:
   - Unfavorable terms requiring revision
   - Missing protective provisions
   - Imbalanced risk allocation
   - Opportunities for better terms

8. RED FLAGS AND CONCERNS:
   - Unusual or problematic clauses
   - Vague or ambiguous language
   - Potential enforceability issues
   - Conflicts with applicable law

Provide specific recommendations with supporting analysis.
Include proper legal terminology and references.
Note any industry-specific considerations.
Assess overall document quality and enforceability.
"""
        
        if context:
            specific_instructions += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"
        
        return self._create_legal_system_prompt(specific_instructions)
    
    def _perform_detailed_document_analysis(self, document_text: str, document_type: str,
                                          review_focus: List[str]) -> Dict[str, Any]:
        """Perform detailed analysis of document components"""
        analysis_results = {
            'word_count': len(document_text.split()),
            'paragraph_count': len(document_text.split('\n\n')),
            'section_analysis': self._analyze_document_sections(document_text),
            'clause_density': self._calculate_clause_density(document_text),
            'complexity_score': self._calculate_complexity_score(document_text),
            'readability_assessment': self._assess_document_readability(document_text)
        }
        
        return analysis_results
    
    def _analyze_document_sections(self, document_text: str) -> Dict[str, Any]:
        """Analyze document sections and structure"""
        # Look for common section headers
        section_patterns = [
            r'SECTION\s+\d+',
            r'Article\s+\d+',
            r'\d+\.\s+[A-Z][^.]+',
            r'WHEREAS',
            r'NOW THEREFORE',
            r'IN WITNESS WHEREOF'
        ]
        
        sections_found = []
        for pattern in section_patterns:
            matches = re.findall(pattern, document_text, re.IGNORECASE)
            sections_found.extend(matches)
        
        return {
            'total_sections': len(sections_found),
            'section_types': sections_found[:10],  # First 10 sections
            'has_preamble': 'whereas' in document_text.lower(),
            'has_signature_block': 'witness whereof' in document_text.lower(),
            'structure_quality': 'well_structured' if len(sections_found) > 3 else 'basic_structure'
        }
    
    def _calculate_clause_density(self, document_text: str) -> float:
        """Calculate density of legal clauses"""
        legal_clause_indicators = [
            'shall', 'hereby', 'notwithstanding', 'provided that', 
            'subject to', 'in accordance with', 'pursuant to'
        ]
        
        words = document_text.lower().split()
        clause_count = sum(1 for word in words if word in legal_clause_indicators)
        
        return round(clause_count / len(words) * 100, 2) if words else 0
    
    def _calculate_complexity_score(self, document_text: str) -> int:
        """Calculate document complexity score (1-10)"""
        complexity_factors = {
            'length': len(document_text) / 1000,  # Per 1000 characters
            'legal_terms': self._count_legal_terms(document_text),
            'cross_references': self._count_cross_references(document_text),
            'conditional_clauses': self._count_conditional_clauses(document_text)
        }
        
        # Weighted complexity calculation
        weighted_score = (
            min(5, complexity_factors['length'] * 0.5) +
            min(3, complexity_factors['legal_terms'] / 10) +
            min(2, complexity_factors['cross_references'] / 5)
        )
        
        return min(10, max(1, int(weighted_score)))
    
    def _count_legal_terms(self, document_text: str) -> int:
        """Count legal terms in document"""
        legal_terms = [
            'heretofore', 'hereinafter', 'aforementioned', 'notwithstanding',
            'pursuant', 'whereby', 'herein', 'thereof', 'therein', 'indemnify'
        ]
        
        text_lower = document_text.lower()
        return sum(1 for term in legal_terms if term in text_lower)
    
    def _count_cross_references(self, document_text: str) -> int:
        """Count cross-references in document"""
        cross_ref_patterns = [
            r'section\s+\d+',
            r'paragraph\s+\d+', 
            r'clause\s+\d+',
            r'exhibit\s+[a-z]',
            r'schedule\s+[a-z]'
        ]
        
        count = 0
        for pattern in cross_ref_patterns:
            count += len(re.findall(pattern, document_text, re.IGNORECASE))
        
        return count
    
    def _count_conditional_clauses(self, document_text: str) -> int:
        """Count conditional clauses"""
        conditional_indicators = ['if', 'unless', 'provided that', 'in the event that', 'subject to']
        text_lower = document_text.lower()
        return sum(1 for indicator in conditional_indicators if indicator in text_lower)
    
    def _assess_document_readability(self, document_text: str) -> Dict[str, Any]:
        """Assess document readability"""
        sentences = document_text.split('.')
        words = document_text.split()
        
        avg_words_per_sentence = len(words) / max(len(sentences), 1)
        
        readability_level = 'complex'
        if avg_words_per_sentence < 15:
            readability_level = 'moderate'
        elif avg_words_per_sentence < 10:
            readability_level = 'simple'
        
        return {
            'average_words_per_sentence': round(avg_words_per_sentence, 1),
            'readability_level': readability_level,
            'total_sentences': len(sentences),
            'assessment': f'Document has {readability_level} readability with {avg_words_per_sentence:.1f} words per sentence'
        }
    
    def _extract_key_clauses(self, document_text: str, document_type: str) -> Dict[str, List]:
        """Extract key clauses based on document type"""
        clause_extractors = {
            'contract': self._extract_contract_clauses,
            'lease': self._extract_lease_clauses,
            'employment': self._extract_employment_clauses,
            'nda': self._extract_nda_clauses,
            'purchase': self._extract_purchase_clauses
        }
        
        extractor = clause_extractors.get(document_type, self._extract_general_clauses)
        return extractor(document_text)
    
    def _extract_contract_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract key contract clauses"""
        clauses = {
            'payment_terms': self._find_clauses_by_keywords(document_text, 
                ['payment', 'invoice', 'due', 'billing', 'fee']),
            'termination_clauses': self._find_clauses_by_keywords(document_text,
                ['terminate', 'termination', 'end', 'expire', 'cancel']),
            'liability_clauses': self._find_clauses_by_keywords(document_text,
                ['liable', 'liability', 'indemnify', 'damages', 'loss']),
            'confidentiality_clauses': self._find_clauses_by_keywords(document_text,
                ['confidential', 'proprietary', 'non-disclosure', 'secret']),
            'dispute_resolution': self._find_clauses_by_keywords(document_text,
                ['dispute', 'arbitration', 'mediation', 'court', 'litigation'])
        }
        
        return clauses
    
    def _extract_lease_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract key lease clauses"""
        clauses = {
            'rent_terms': self._find_clauses_by_keywords(document_text,
                ['rent', 'rental', 'payment', 'monthly', 'lease payment']),
            'security_deposit': self._find_clauses_by_keywords(document_text,
                ['security deposit', 'deposit', 'damage deposit']),
            'maintenance_responsibility': self._find_clauses_by_keywords(document_text,
                ['maintenance', 'repair', 'upkeep', 'condition']),
            'termination_notice': self._find_clauses_by_keywords(document_text,
                ['notice', 'termination', 'end lease', 'vacate']),
            'use_restrictions': self._find_clauses_by_keywords(document_text,
                ['use', 'permitted', 'prohibited', 'restriction'])
        }
        
        return clauses
    
    def _extract_employment_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract key employment clauses"""
        clauses = {
            'compensation': self._find_clauses_by_keywords(document_text,
                ['salary', 'wage', 'compensation', 'pay', 'benefits']),
            'job_duties': self._find_clauses_by_keywords(document_text,
                ['duties', 'responsibilities', 'role', 'position']),
            'termination_conditions': self._find_clauses_by_keywords(document_text,
                ['terminate', 'termination', 'dismiss', 'cause', 'notice']),
            'confidentiality': self._find_clauses_by_keywords(document_text,
                ['confidential', 'proprietary', 'trade secret', 'non-disclosure']),
            'non_compete': self._find_clauses_by_keywords(document_text,
                ['non-compete', 'competition', 'solicit', 'non-solicitation'])
        }
        
        return clauses
    
    def _extract_nda_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract key NDA clauses"""
        clauses = {
            'confidential_information': self._find_clauses_by_keywords(document_text,
                ['confidential information', 'proprietary', 'trade secret']),
            'permitted_use': self._find_clauses_by_keywords(document_text,
                ['permitted use', 'authorized', 'purpose', 'evaluation']),
            'return_obligation': self._find_clauses_by_keywords(document_text,
                ['return', 'destroy', 'delete', 'materials']),
            'duration': self._find_clauses_by_keywords(document_text,
                ['duration', 'term', 'period', 'expire', 'effective']),
            'exceptions': self._find_clauses_by_keywords(document_text,
                ['exception', 'exclude', 'not include', 'public domain'])
        }
        
        return clauses
    
    def _extract_purchase_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract key purchase agreement clauses"""
        clauses = {
            'purchase_price': self._find_clauses_by_keywords(document_text,
                ['purchase price', 'price', 'consideration', 'amount']),
            'delivery_terms': self._find_clauses_by_keywords(document_text,
                ['delivery', 'shipment', 'transfer', 'possession']),
            'warranty': self._find_clauses_by_keywords(document_text,
                ['warranty', 'guarantee', 'representation', 'condition']),
            'inspection': self._find_clauses_by_keywords(document_text,
                ['inspection', 'examine', 'review', 'approve']),
            'risk_of_loss': self._find_clauses_by_keywords(document_text,
                ['risk', 'loss', 'damage', 'insurance', 'title'])
        }
        
        return clauses
    
    def _extract_general_clauses(self, document_text: str) -> Dict[str, List]:
        """Extract general legal clauses"""
        clauses = {
            'definitions': self._find_clauses_by_keywords(document_text,
                ['define', 'definition', 'means', 'include', 'refer']),
            'obligations': self._find_clauses_by_keywords(document_text,
                ['shall', 'must', 'required', 'obligation', 'duty']),
            'conditions': self._find_clauses_by_keywords(document_text,
                ['condition', 'if', 'provided', 'subject to', 'unless']),
            'remedies': self._find_clauses_by_keywords(document_text,
                ['remedy', 'damages', 'breach', 'default', 'cure']),
            'general_provisions': self._find_clauses_by_keywords(document_text,
                ['governing law', 'jurisdiction', 'entire agreement', 'amendment'])
        }
        
        return clauses
    
    def _find_clauses_by_keywords(self, document_text: str, keywords: List[str]) -> List[Dict]:
        """Find clauses containing specific keywords"""
        sentences = document_text.split('.')
        matching_clauses = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Skip very short sentences
                continue
                
            sentence_lower = sentence.lower()
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    matching_clauses.append({
                        'text': sentence,
                        'keyword': keyword,
                        'length': len(sentence),
                        'relevance_score': self._calculate_relevance_score(sentence, keyword)
                    })
                    break
        
        # Sort by relevance and limit results
        matching_clauses.sort(key=lambda x: x['relevance_score'], reverse=True)
        return matching_clauses[:5]  # Top 5 most relevant clauses
    
    def _calculate_relevance_score(self, sentence: str, keyword: str) -> float:
        """Calculate relevance score for a clause"""
        sentence_lower = sentence.lower()
        keyword_lower = keyword.lower()
        
        # Base score for containing the keyword
        score = 1.0
        
        # Bonus for keyword appearing multiple times
        score += sentence_lower.count(keyword_lower) * 0.5
        
        # Bonus for legal language indicators
        legal_indicators = ['shall', 'hereby', 'agrees', 'covenant', 'represent']
        score += sum(0.2 for indicator in legal_indicators if indicator in sentence_lower)
        
        # Penalty for very long sentences (may be less focused)
        if len(sentence) > 200:
            score *= 0.8
        
        return score
    
    def _analyze_document_risks(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """Analyze risks present in the document"""
        risk_categories = {
            'financial_risks': self._identify_financial_risks(document_text),
            'performance_risks': self._identify_performance_risks(document_text),
            'legal_compliance_risks': self._identify_compliance_risks(document_text),
            'liability_risks': self._identify_liability_risks(document_text),
            'termination_risks': self._identify_termination_risks(document_text)
        }
        
        # Calculate overall risk level
        total_risks = sum(len(risks) for risks in risk_categories.values())
        if total_risks >= 10:
            overall_risk_level = 'high'
        elif total_risks >= 5:
            overall_risk_level = 'medium'
        else:
            overall_risk_level = 'low'
        
        return {
            'overall_risk_level': overall_risk_level,
            'total_risks_identified': total_risks,
            'risk_categories': risk_categories,
            'risk_mitigation_suggestions': self._generate_risk_mitigation_suggestions(risk_categories),
            'immediate_attention_required': self._identify_immediate_risks(risk_categories)
        }
    
    def _identify_financial_risks(self, document_text: str) -> List[Dict]:
        """Identify financial risks in the document"""
        financial_risk_indicators = [
            'unlimited liability', 'personal guarantee', 'penalty', 'fine',
            'indemnify', 'attorney fees', 'damages', 'liquidated damages'
        ]
        
        risks = []
        text_lower = document_text.lower()
        
        for indicator in financial_risk_indicators:
            if indicator in text_lower:
                risks.append({
                    'risk_type': 'financial',
                    'indicator': indicator,
                    'severity': self._assess_risk_severity(indicator),
                    'description': f"Document contains {indicator} provision"
                })
        
        return risks
    
    def _identify_performance_risks(self, document_text: str) -> List[Dict]:
        """Identify performance-related risks"""
        performance_risk_indicators = [
            'strict performance', 'time is of the essence', 'material breach',
            'default', 'cure period', 'specific performance'
        ]
        
        risks = []
        text_lower = document_text.lower()
        
        for indicator in performance_risk_indicators:
            if indicator in text_lower:
                risks.append({
                    'risk_type': 'performance',
                    'indicator': indicator,
                    'severity': self._assess_risk_severity(indicator),
                    'description': f"Document contains {indicator} requirement"
                })
        
        return risks
    
    def _identify_compliance_risks(self, document_text: str) -> List[Dict]:
        """Identify compliance-related risks"""
        compliance_risk_indicators = [
            'regulatory compliance', 'law compliance', 'permit required',
            'license required', 'approval required', 'environmental'
        ]
        
        risks = []
        text_lower = document_text.lower()
        
        for indicator in compliance_risk_indicators:
            if indicator in text_lower:
                risks.append({
                    'risk_type': 'compliance',
                    'indicator': indicator,
                    'severity': self._assess_risk_severity(indicator),
                    'description': f"Document requires {indicator}"
                })
        
        return risks
    
    def _identify_liability_risks(self, document_text: str) -> List[Dict]:
        """Identify liability-related risks"""
        liability_risk_indicators = [
            'joint and several', 'unlimited liability', 'consequential damages',
            'punitive damages', 'indemnification', 'hold harmless'
        ]
        
        risks = []
        text_lower = document_text.lower()
        
        for indicator in liability_risk_indicators:
            if indicator in text_lower:
                risks.append({
                    'risk_type': 'liability',
                    'indicator': indicator,
                    'severity': self._assess_risk_severity(indicator),
                    'description': f"Document includes {indicator} provision"
                })
        
        return risks
    
    def _identify_termination_risks(self, document_text: str) -> List[Dict]:
        """Identify termination-related risks"""
        termination_risk_indicators = [
            'terminate without cause', 'immediate termination', 'no cure period',
            'forfeit', 'no refund', 'survive termination'
        ]
        
        risks = []
        text_lower = document_text.lower()
        
        for indicator in termination_risk_indicators:
            if indicator in text_lower:
                risks.append({
                    'risk_type': 'termination',
                    'indicator': indicator,
                    'severity': self._assess_risk_severity(indicator),
                    'description': f"Document allows {indicator}"
                })
        
        return risks
    
    def _assess_risk_severity(self, risk_indicator: str) -> str:
        """Assess severity level of identified risk"""
        high_severity_risks = [
            'unlimited liability', 'personal guarantee', 'punitive damages',
            'immediate termination', 'forfeit', 'joint and several'
        ]
        
        medium_severity_risks = [
            'indemnify', 'material breach', 'attorney fees', 'penalty',
            'strict performance', 'no cure period'
        ]
        
        if risk_indicator in high_severity_risks:
            return 'high'
        elif risk_indicator in medium_severity_risks:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_document_opportunities(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """Analyze opportunities present in the document"""
        opportunity_categories = {
            'negotiation_opportunities': self._identify_negotiation_opportunities(document_text),
            'protective_provisions': self._identify_missing_protections(document_text, document_type),
            'favorable_terms': self._identify_favorable_terms(document_text),
            'improvement_suggestions': self._suggest_document_improvements(document_text, document_type)
        }
        
        total_opportunities = sum(len(opps) for opps in opportunity_categories.values())
        
        return {
            'total_opportunities_identified': total_opportunities,
            'opportunity_categories': opportunity_categories,
            'priority_opportunities': self._prioritize_opportunities(opportunity_categories),
            'implementation_suggestions': self._suggest_opportunity_implementation(opportunity_categories)
        }
    
    def _identify_negotiation_opportunities(self, document_text: str) -> List[Dict]:
        """Identify negotiation opportunities"""
        negotiation_indicators = [
            'may', 'at discretion', 'reasonable', 'mutually agreed',
            'to be determined', 'subject to negotiation'
        ]
        
        opportunities = []
        text_lower = document_text.lower()
        
        for indicator in negotiation_indicators:
            if indicator in text_lower:
                opportunities.append({
                    'type': 'negotiation',
                    'indicator': indicator,
                    'opportunity': f"Terms with {indicator} language may be negotiable",
                    'priority': 'medium'
                })
        
        return opportunities
    
    def _identify_missing_protections(self, document_text: str, document_type: str) -> List[Dict]:
        """Identify missing protective provisions"""
        common_protections = {
            'contract': ['limitation of liability', 'force majeure', 'confidentiality'],
            'lease': ['quiet enjoyment', 'right to cure', 'security deposit protection'],
            'employment': ['severance', 'benefit continuation', 'non-compete limitation'],
            'nda': ['return of materials', 'residual knowledge', 'injunctive relief']
        }
        
        expected_protections = common_protections.get(document_type, [])
        missing_protections = []
        text_lower = document_text.lower()
        
        for protection in expected_protections:
            if protection.lower() not in text_lower:
                missing_protections.append({
                    'type': 'missing_protection',
                    'protection': protection,
                    'opportunity': f"Consider adding {protection} provision",
                    'priority': 'high'
                })
        
        return missing_protections
    
    def _identify_favorable_terms(self, document_text: str) -> List[Dict]:
        """Identify favorable terms in the document"""
        favorable_indicators = [
            'right to cure', 'reasonable notice', 'mutual termination',
            'pro-rated', 'good faith', 'commercially reasonable'
        ]
        
        favorable_terms = []
        text_lower = document_text.lower()
        
        for indicator in favorable_indicators:
            if indicator in text_lower:
                favorable_terms.append({
                    'type': 'favorable_term',
                    'term': indicator,
                    'benefit': f"Document includes favorable {indicator} provision",
                    'priority': 'low'
                })
        
        return favorable_terms
    
    def _suggest_document_improvements(self, document_text: str, document_type: str) -> List[Dict]:
        """Suggest general document improvements"""
        improvements = []
        
        # Check for ambiguous language
        if 'reasonable' in document_text.lower():
            improvements.append({
                'type': 'clarity_improvement',
                'suggestion': 'Define "reasonable" standards more specifically',
                'priority': 'medium'
            })
        
        # Check for missing definitions
        complex_terms = ['material', 'substantial', 'commercially reasonable']
        text_lower = document_text.lower()
        for term in complex_terms:
            if term in text_lower and 'definition' not in text_lower:
                improvements.append({
                    'type': 'definition_needed',
                    'suggestion': f'Add definition for "{term}"',
                    'priority': 'medium'
                })
        
        return improvements
    
    def _prioritize_opportunities(self, opportunity_categories: Dict) -> List[Dict]:
        """Prioritize identified opportunities"""
        all_opportunities = []
        
        for category, opportunities in opportunity_categories.items():
            for opportunity in opportunities:
                opportunity['category'] = category
                all_opportunities.append(opportunity)
        
        # Sort by priority (high > medium > low)
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        all_opportunities.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 0), reverse=True)
        
        return all_opportunities[:10]  # Top 10 priorities
    
    def _suggest_opportunity_implementation(self, opportunity_categories: Dict) -> List[str]:
        """Suggest how to implement identified opportunities"""
        suggestions = [
            "Schedule negotiation session to address high-priority terms",
            "Prepare redlined version with suggested protective provisions",
            "Research industry standards for comparison terms",
            "Consider legal counsel review for complex provisions"
        ]
        
        return suggestions
    
    def _assess_compliance_requirements(self, document_text: str, document_type: str) -> Dict[str, Any]:
        """Assess compliance requirements in the document"""
        compliance_areas = {
            'regulatory_compliance': self._check_regulatory_compliance(document_text),
            'legal_formalities': self._check_legal_formalities(document_text),
            'industry_standards': self._check_industry_standards(document_text, document_type),
            'documentation_requirements': self._check_documentation_requirements(document_text)
        }
        
        # Calculate compliance score
        total_requirements = sum(len(reqs) for reqs in compliance_areas.values())
        compliance_score = max(1, min(10, 10 - total_requirements))
        
        return {
            'overall_compliance_score': compliance_score,
            'compliance_level': self._categorize_compliance_level(compliance_score),
            'compliance_areas': compliance_areas,
            'compliance_recommendations': self._generate_compliance_recommendations(compliance_areas)
        }
    
    def _check_regulatory_compliance(self, document_text: str) -> List[Dict]:
        """Check regulatory compliance requirements"""
        regulatory_indicators = [
            'environmental', 'safety', 'privacy', 'data protection',
            'sec compliance', 'antitrust', 'export control'
        ]
        
        requirements = []
        text_lower = document_text.lower()
        
        for indicator in regulatory_indicators:
            if indicator in text_lower:
                requirements.append({
                    'area': indicator,
                    'requirement': f"Ensure {indicator} compliance",
                    'priority': 'high'
                })
        
        return requirements
    
    def _check_legal_formalities(self, document_text: str) -> List[Dict]:
        """Check legal formality requirements"""
        formality_checks = []
        
        # Check for signature requirements
        if 'signature' not in document_text.lower():
            formality_checks.append({
                'formality': 'signature_block',
                'requirement': 'Add proper signature block',
                'priority': 'high'
            })
        
        # Check for date requirements
        if 'date' not in document_text.lower():
            formality_checks.append({
                'formality': 'effective_date',
                'requirement': 'Include effective date provision',
                'priority': 'medium'
            })
        
        return formality_checks
    
    def _check_industry_standards(self, document_text: str, document_type: str) -> List[Dict]:
        """Check industry standard compliance"""
        # This would be more sophisticated in production
        standards = []
        
        if document_type == 'contract' and 'governing law' not in document_text.lower():
            standards.append({
                'standard': 'governing_law',
                'requirement': 'Include governing law clause',
                'priority': 'medium'
            })
        
        return standards
    
    def _check_documentation_requirements(self, document_text: str) -> List[Dict]:
        """Check documentation requirements"""
        doc_requirements = []
        
        # Check for exhibit references without actual exhibits
        if 'exhibit' in document_text.lower() and len(document_text) < 5000:
            doc_requirements.append({
                'requirement_type': 'exhibits',
                'requirement': 'Verify all referenced exhibits are attached',
                'priority': 'high'
            })
        
        return doc_requirements
    
    def _categorize_compliance_level(self, score: int) -> str:
        """Categorize compliance level"""
        if score >= 8:
            return 'high_compliance'
        elif score >= 6:
            return 'adequate_compliance'
        elif score >= 4:
            return 'needs_improvement'
        else:
            return 'significant_issues'
    
    def _generate_compliance_recommendations(self, compliance_areas: Dict) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        for area, requirements in compliance_areas.items():
            if requirements:
                area_name = area.replace('_', ' ').title()
                recommendations.append(f"Review {area_name}: {len(requirements)} items require attention")
        
        recommendations.append("Conduct legal compliance audit with qualified counsel")
        return recommendations
    
    def _extract_obligations_summary(self, document_analysis: Dict) -> Dict[str, List]:
        """Extract summary of obligations"""
        # This would extract obligations from the document analysis
        return {
            'client_obligations': [
                "Pay fees according to payment schedule",
                "Provide required documentation",
                "Comply with performance standards"
            ],
            'counterparty_obligations': [
                "Deliver services as specified",
                "Maintain confidentiality",
                "Provide required notices"
            ],
            'mutual_obligations': [
                "Act in good faith",
                "Comply with applicable laws",
                "Resolve disputes per agreement terms"
            ]
        }
    
    def _extract_rights_summary(self, document_analysis: Dict) -> Dict[str, List]:
        """Extract summary of rights"""
        return {
            'client_rights': [
                "Right to terminate for cause",
                "Right to cure defaults",
                "Right to receive services per specifications"
            ],
            'counterparty_rights': [
                "Right to payment per terms",
                "Right to terminate for non-payment",
                "Right to protect confidential information"
            ],
            'shared_rights': [
                "Right to legal remedies for breach",
                "Right to modify agreement by mutual consent"
            ]
        }
    
    def _extract_financial_terms(self, document_text: str) -> Dict[str, Any]:
        """Extract financial terms from document"""
        financial_terms = {}
        
        # Look for monetary amounts
        money_pattern = r'\$[\d,]+(?:\.\d{2})?'
        amounts = re.findall(money_pattern, document_text)
        if amounts:
            financial_terms['monetary_amounts'] = amounts[:5]  # First 5 amounts
        
        # Look for payment terms
        payment_terms = self._find_clauses_by_keywords(document_text, 
            ['payment due', 'net 30', 'payment terms', 'billing'])
        if payment_terms:
            financial_terms['payment_terms'] = [term['text'] for term in payment_terms[:3]]
        
        return financial_terms
    
    def _extract_timeline_provisions(self, document_text: str) -> Dict[str, Any]:
        """Extract timeline and deadline provisions"""
        timeline_provisions = {}
        
        # Look for dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b|\b\w+ \d{1,2}, \d{4}\b'
        dates = re.findall(date_pattern, document_text)
        if dates:
            timeline_provisions['specific_dates'] = dates[:5]
        
        # Look for time periods
        time_periods = self._find_clauses_by_keywords(document_text,
            ['days', 'months', 'years', 'deadline', 'due date'])
        if time_periods:
            timeline_provisions['time_periods'] = [period['text'] for period in time_periods[:3]]
        
        return timeline_provisions
    
    def _generate_redline_suggestions(self, document_text: str, document_type: str,
                                    risk_analysis: Dict) -> List[Dict]:
        """Generate redline suggestions for document improvement"""
        suggestions = []
        
        # High-risk items should be addressed
        high_risks = []
        for category, risks in risk_analysis.get('risk_categories', {}).items():
            high_risks.extend([risk for risk in risks if risk.get('severity') == 'high'])
        
        for risk in high_risks:
            suggestions.append({
                'type': 'risk_mitigation',
                'suggestion': f"Add limitation or qualification to {risk['indicator']} provision",
                'priority': 'high',
                'rationale': f"Mitigate {risk['risk_type']} risk"
            })
        
        # Standard protective provisions
        if document_type == 'contract':
            suggestions.extend([
                {
                    'type': 'protective_provision',
                    'suggestion': 'Add force majeure clause',
                    'priority': 'medium',
                    'rationale': 'Protect against unforeseeable events'
                },
                {
                    'type': 'clarification',
                    'suggestion': 'Define key terms more specifically',
                    'priority': 'medium',
                    'rationale': 'Reduce ambiguity and disputes'
                }
            ])
        
        return suggestions[:10]  # Limit to top 10 suggestions
    
    def _identify_negotiation_points(self, risk_analysis: Dict, opportunity_analysis: Dict) -> List[Dict]:
        """Identify key negotiation points"""
        negotiation_points = []
        
        # High-risk items are negotiation priorities
        high_risks = []
        for category, risks in risk_analysis.get('risk_categories', {}).items():
            high_risks.extend([risk for risk in risks if risk.get('severity') == 'high'])
        
        for risk in high_risks:
            negotiation_points.append({
                'point': f"Modify {risk['indicator']} provision",
                'type': 'risk_reduction',
                'priority': 'high',
                'strategy': 'Seek to limit exposure or add balancing protections'
            })
        
        # High-priority opportunities
        high_opps = opportunity_analysis.get('priority_opportunities', [])
        for opp in high_opps[:3]:  # Top 3 opportunities
            if opp.get('priority') == 'high':
                negotiation_points.append({
                    'point': opp.get('suggestion', opp.get('opportunity')),
                    'type': 'opportunity_capture',
                    'priority': 'medium',
                    'strategy': 'Propose addition of protective provision'
                })
        
        return negotiation_points
    
    def _generate_overall_recommendation(self, risk_analysis: Dict, opportunity_analysis: Dict) -> Dict[str, Any]:
        """Generate overall recommendation for document"""
        risk_level = risk_analysis.get('overall_risk_level', 'medium')
        total_opportunities = opportunity_analysis.get('total_opportunities_identified', 0)
        
        if risk_level == 'high':
            recommendation = 'Significant revision recommended before execution'
            action = 'negotiate_major_changes'
        elif risk_level == 'medium' and total_opportunities >= 5:
            recommendation = 'Negotiate key terms and add protective provisions'
            action = 'negotiate_improvements'
        elif risk_level == 'low' and total_opportunities < 3:
            recommendation = 'Document is generally acceptable with minor revisions'
            action = 'proceed_with_minor_changes'
        else:
            recommendation = 'Review recommended improvements and negotiate as appropriate'
            action = 'selective_negotiation'
        
        return {
            'overall_recommendation': recommendation,
            'recommended_action': action,
            'confidence_level': 'moderate',
            'next_steps': [
                'Review identified risks and opportunities with legal counsel',
                'Prepare negotiation strategy for high-priority items',
                'Consider alternative terms for high-risk provisions'
            ]
        }
    
    def _determine_attorney_review_requirement(self, risk_analysis: Dict) -> bool:
        """Determine if attorney review is required"""
        risk_level = risk_analysis.get('overall_risk_level', 'medium')
        total_risks = risk_analysis.get('total_risks_identified', 0)
        
        return risk_level == 'high' or total_risks >= 8
    
    def _classify_document_complexity(self, document_text: str) -> Dict[str, Any]:
        """Classify document complexity"""
        complexity_score = self._calculate_complexity_score(document_text)
        
        if complexity_score >= 8:
            complexity_level = 'high'
            description = 'Complex document requiring careful legal review'
        elif complexity_score >= 6:
            complexity_level = 'medium'
            description = 'Moderately complex document with standard legal provisions'
        else:
            complexity_level = 'low'
            description = 'Straightforward document with basic legal structure'
        
        return {
            'complexity_level': complexity_level,
            'complexity_score': complexity_score,
            'description': description
        }
    
    def _create_error_response(self, error_message: str, attorney_id: str = None,
                              client_id: str = None) -> Dict[str, Any]:
        """Create error response for failed document review"""
        return self._format_legal_response(
            f"Document review encountered an error: {error_message}. "
            "Please consult with qualified legal counsel for comprehensive document analysis.",
            {
                'error': True,
                'error_message': error_message,
                'document_review': None,
                'requires_manual_review': True
            },
            attorney_id,
            client_id
        )