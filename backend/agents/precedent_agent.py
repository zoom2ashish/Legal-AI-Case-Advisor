#!/usr/bin/env python3
"""
Precedent Mining Agent for Legal AI System
Discovers and analyzes legal precedents for case strategy development
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import time

from .base_legal_agent import BaseLegalAgent

logger = logging.getLogger(__name__)

class PrecedentMiningAgent(BaseLegalAgent):
    """
    Specialized agent for legal precedent discovery and analysis
    Handles precedent identification, analysis, and strategic application
    """
    
    def __init__(self, knowledge_store, legal_db):
        """Initialize precedent mining agent"""
        super().__init__(knowledge_store, legal_db, "precedent_mining")
        self.mining_capabilities = [
            "precedent_discovery",
            "case_similarity_analysis",
            "precedent_strength_assessment",
            "distinguishing_factor_analysis",
            "strategic_precedent_selection"
        ]
        
        # Precedent authority hierarchy
        self.authority_hierarchy = {
            'supreme_court': 10,
            'circuit_court': 8,
            'district_court': 6,
            'state_supreme': 7,
            'state_appellate': 5,
            'state_trial': 3,
            'administrative': 4
        }
    
    def discover_relevant_precedents(self, legal_issue: str, case_facts: str,
                                   jurisdiction: str = "federal", attorney_id: str = None,
                                   client_id: str = None, search_context: Dict = None) -> Dict[str, Any]:
        """
        Discover and analyze relevant legal precedents
        
        Args:
            legal_issue: Legal issue or question
            case_facts: Factual background of the case
            jurisdiction: Target jurisdiction for precedent search
            attorney_id: ID of requesting attorney
            client_id: ID of client
            search_context: Additional search context
            
        Returns:
            Dict containing comprehensive precedent analysis
        """
        start_time = time.time()
        
        try:
            # Validate attorney-client relationship
            if attorney_id and client_id:
                if not self._validate_attorney_client_relationship(attorney_id, client_id):
                    raise PermissionError("Invalid attorney-client relationship")
            
            # Create precedent search prompt
            search_prompt = self._create_precedent_search_prompt(
                legal_issue, case_facts, jurisdiction, search_context
            )
            
            # Generate AI precedent analysis
            ai_response = self._generate_legal_response(
                search_prompt,
                search_context,
                attorney_id,
                client_id
            )
            
            # Extract structured precedent data
            structured_analysis = self._extract_legal_structured_data(ai_response, "precedent_analysis")
            
            # Search for precedents in knowledge base
            precedent_search_results = self._search_precedent_database(
                legal_issue, case_facts, jurisdiction
            )
            
            # Analyze precedent relevance and strength
            precedent_analysis = self._analyze_precedent_relevance(
                precedent_search_results, legal_issue, case_facts
            )
            
            # Identify binding vs. persuasive authority
            authority_analysis = self._categorize_precedent_authority(
                precedent_search_results, jurisdiction
            )
            
            # Find similar factual patterns
            factual_similarity_analysis = self._analyze_factual_similarity(
                precedent_search_results, case_facts
            )
            
            # Identify distinguishing factors
            distinguishing_analysis = self._identify_distinguishing_factors(
                precedent_search_results, case_facts, legal_issue
            )
            
            # Assess adverse authority
            adverse_authority_analysis = self._identify_adverse_authority(
                precedent_search_results, legal_issue
            )
            
            # Generate strategic recommendations
            strategic_recommendations = self._generate_precedent_strategy(
                precedent_analysis, authority_analysis, distinguishing_analysis
            )
            
            # Compile comprehensive precedent analysis
            precedent_mining_results = {
                'legal_issue': legal_issue,
                'jurisdiction': jurisdiction,
                'ai_analysis': ai_response,
                'search_results_summary': self._summarize_search_results(precedent_search_results),
                'precedent_analysis': precedent_analysis,
                'authority_analysis': authority_analysis,
                'factual_similarity': factual_similarity_analysis,
                'distinguishing_factors': distinguishing_analysis,
                'adverse_authority': adverse_authority_analysis,
                'strategic_recommendations': strategic_recommendations,
                'precedent_timeline': self._analyze_precedent_timeline(precedent_search_results),
                'citation_network': self._build_citation_network(precedent_search_results),
                'research_confidence': structured_analysis.get('confidence_level', 6),
                'follow_up_searches': self._suggest_follow_up_searches(precedent_analysis),
                'timestamp': datetime.now().isoformat()
            }
            
            # Format final response
            formatted_response = self._format_legal_response(
                ai_response,
                {
                    'precedent_mining_results': precedent_mining_results,
                    'analysis_type': 'comprehensive_precedent_analysis',
                    'precedents_found': len(precedent_search_results.get('cases', [])),
                    'binding_precedents': len(authority_analysis.get('binding_authority', [])),
                    'strategic_value': strategic_recommendations.get('overall_strategic_value', 'moderate')
                },
                attorney_id,
                client_id
            )
            
            # Log precedent mining interaction
            processing_time = time.time() - start_time
            self._log_legal_interaction(
                attorney_id or 'unknown',
                client_id or 'unknown',
                'precedent_mining',
                {'legal_issue': legal_issue, 'jurisdiction': jurisdiction},
                formatted_response,
                processing_time
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Precedent mining failed: {str(e)}")
            return self._create_error_response(str(e), attorney_id, client_id)
    
    def _create_precedent_search_prompt(self, legal_issue: str, case_facts: str,
                                      jurisdiction: str, context: Dict = None) -> str:
        """Create specialized prompt for precedent analysis"""
        specific_instructions = f"""
You are conducting comprehensive precedent research for the following legal matter in {jurisdiction} jurisdiction:

LEGAL ISSUE: {legal_issue}

CASE FACTS: {case_facts}

Please provide thorough precedent analysis covering:

1. PRECEDENT IDENTIFICATION:
   - Identify directly relevant case precedents
   - Find cases with similar legal issues
   - Locate cases with comparable factual patterns
   - Include proper legal citations in Bluebook format

2. AUTHORITY ANALYSIS:
   - Distinguish binding vs. persuasive authority
   - Assess hierarchical precedential value
   - Consider jurisdictional authority levels
   - Note any supreme court guidance

3. FACTUAL SIMILARITY ASSESSMENT:
   - Compare factual patterns with precedents
   - Identify key factual similarities
   - Note significant factual distinctions
   - Assess analogical strength

4. LEGAL REASONING ANALYSIS:
   - Extract key legal principles from precedents
   - Analyze judicial reasoning and rationale
   - Identify applicable legal standards
   - Note any evolution in legal doctrine

5. DISTINGUISHING FACTOR IDENTIFICATION:
   - Identify factors that distinguish cases
   - Assess impact of distinguishing factors
   - Determine if distinctions are material
   - Consider argument strategies for distinctions

6. ADVERSE AUTHORITY ASSESSMENT:
   - Identify potentially adverse precedents
   - Assess strength of adverse authority
   - Develop strategies to distinguish adverse cases
   - Consider limitations of adverse holdings

7. STRATEGIC PRECEDENT RECOMMENDATIONS:
   - Recommend strongest precedents to cite
   - Suggest argument hierarchy and structure
   - Identify precedents to emphasize or minimize
   - Recommend additional research areas

8. PRECEDENT EVOLUTION ANALYSIS:
   - Track development of legal doctrine over time
   - Identify any shifts in judicial interpretation
   - Note recent trends in case law
   - Assess stability of precedential foundation

Provide specific recommendations for precedent utilization.
Include proper legal citations and case summaries.
Note any circuit splits or conflicting authorities.
Assess overall strength of precedential support.
"""
        
        if context:
            specific_instructions += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"
        
        return self._create_legal_system_prompt(specific_instructions)
    
    def _search_precedent_database(self, legal_issue: str, case_facts: str,
                                 jurisdiction: str) -> Dict[str, List]:
        """Search legal knowledge base for relevant precedents"""
        try:
            # Search by legal issue
            issue_based_cases = self.knowledge_store.search_cases_by_issue(
                legal_issue, jurisdiction, limit=20
            )
            
            # Search by factual similarity
            fact_based_cases = self.knowledge_store.search_cases_by_facts(
                case_facts, jurisdiction, limit=15
            )
            
            # Search for related legal principles
            principle_based_cases = self.knowledge_store.search_by_legal_principle(
                legal_issue, jurisdiction, limit=10
            )
            
            # Search citation networks
            cited_cases = self.knowledge_store.search_citation_network(
                issue_based_cases, limit=10
            )
            
            # Combine and deduplicate results
            all_cases = self._deduplicate_cases(
                issue_based_cases + fact_based_cases + principle_based_cases + cited_cases
            )
            
            return {
                'cases': all_cases,
                'issue_based_results': issue_based_cases,
                'fact_based_results': fact_based_cases,
                'principle_based_results': principle_based_cases,
                'citation_network_results': cited_cases,
                'total_unique_cases': len(all_cases)
            }
            
        except Exception as e:
            logger.error(f"Failed to search precedent database: {str(e)}")
            return {'cases': [], 'total_unique_cases': 0}
    
    def _deduplicate_cases(self, case_list: List[Dict]) -> List[Dict]:
        """Remove duplicate cases from search results"""
        seen_cases = set()
        unique_cases = []
        
        for case in case_list:
            case_id = case.get('case_id') or case.get('citation', '')
            if case_id and case_id not in seen_cases:
                seen_cases.add(case_id)
                unique_cases.append(case)
        
        return unique_cases
    
    def _analyze_precedent_relevance(self, search_results: Dict, legal_issue: str,
                                   case_facts: str) -> Dict[str, Any]:
        """Analyze relevance of found precedents"""
        cases = search_results.get('cases', [])
        
        if not cases:
            return {'relevance_analysis': 'No precedents found', 'relevant_cases': []}
        
        relevance_analysis = []
        
        for case in cases:
            relevance_score = self._calculate_precedent_relevance(case, legal_issue, case_facts)
            case_analysis = {
                'case': case,
                'relevance_score': relevance_score,
                'relevance_factors': self._identify_relevance_factors(case, legal_issue, case_facts),
                'strategic_value': self._assess_strategic_value(case, relevance_score),
                'citation_strength': self._assess_citation_strength(case)
            }
            relevance_analysis.append(case_analysis)
        
        # Sort by relevance score
        relevance_analysis.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'total_cases_analyzed': len(cases),
            'highly_relevant_cases': [case for case in relevance_analysis if case['relevance_score'] >= 8],
            'moderately_relevant_cases': [case for case in relevance_analysis if 5 <= case['relevance_score'] < 8],
            'marginally_relevant_cases': [case for case in relevance_analysis if case['relevance_score'] < 5],
            'top_precedents': relevance_analysis[:10],  # Top 10 most relevant
            'overall_precedent_strength': self._calculate_overall_precedent_strength(relevance_analysis)
        }
    
    def _calculate_precedent_relevance(self, case: Dict, legal_issue: str, case_facts: str) -> float:
        """Calculate relevance score for a precedent"""
        base_score = 5.0
        
        # Legal issue similarity (40% weight)
        issue_similarity = self._calculate_issue_similarity(case, legal_issue)
        base_score += issue_similarity * 0.4 * 4  # Max 1.6 points
        
        # Factual similarity (30% weight)
        fact_similarity = self._calculate_factual_similarity(case, case_facts)
        base_score += fact_similarity * 0.3 * 4  # Max 1.2 points
        
        # Precedential authority (20% weight)
        authority_weight = self._get_authority_weight(case)
        base_score += (authority_weight / 10) * 0.2 * 4  # Max 0.8 points
        
        # Recency factor (10% weight)
        recency_factor = self._calculate_recency_factor(case)
        base_score += recency_factor * 0.1 * 4  # Max 0.4 points
        
        return min(10.0, max(1.0, round(base_score, 1)))
    
    def _calculate_issue_similarity(self, case: Dict, legal_issue: str) -> float:
        """Calculate similarity between case issue and target issue"""
        case_issues = case.get('legal_issues', []) + [case.get('issue', '')]
        case_issues_text = ' '.join(str(issue) for issue in case_issues if issue).lower()
        legal_issue_lower = legal_issue.lower()
        
        # Simple keyword matching (could be enhanced with NLP)
        issue_keywords = legal_issue_lower.split()
        matches = sum(1 for keyword in issue_keywords if keyword in case_issues_text)
        
        similarity = matches / len(issue_keywords) if issue_keywords else 0
        return min(1.0, similarity)
    
    def _calculate_factual_similarity(self, case: Dict, case_facts: str) -> float:
        """Calculate factual similarity between cases"""
        case_facts_text = (case.get('facts', '') + ' ' + case.get('summary', '')).lower()
        target_facts_lower = case_facts.lower()
        
        # Extract key factual concepts
        fact_concepts = ['contract', 'breach', 'damages', 'negligence', 'liability', 'employment']
        
        case_concepts = [concept for concept in fact_concepts if concept in case_facts_text]
        target_concepts = [concept for concept in fact_concepts if concept in target_facts_lower]
        
        if not target_concepts:
            return 0.5  # Neutral if no clear factual concepts
        
        common_concepts = set(case_concepts) & set(target_concepts)
        similarity = len(common_concepts) / len(target_concepts)
        
        return min(1.0, similarity)
    
    def _get_authority_weight(self, case: Dict) -> int:
        """Get authority weight for the case"""
        court_level = case.get('court_level', 'unknown').lower()
        
        for authority_type, weight in self.authority_hierarchy.items():
            if authority_type.replace('_', ' ') in court_level:
                return weight
        
        return 5  # Default weight for unknown courts
    
    def _calculate_recency_factor(self, case: Dict) -> float:
        """Calculate recency factor for the case"""
        try:
            case_year = case.get('decision_year') or case.get('year')
            if not case_year:
                return 0.5  # Neutral if no date available
            
            current_year = datetime.now().year
            years_old = current_year - int(case_year)
            
            if years_old <= 5:
                return 1.0  # Recent cases get full weight
            elif years_old <= 15:
                return 0.8  # Moderately old cases
            elif years_old <= 30:
                return 0.6  # Older cases
            else:
                return 0.4  # Very old cases
        
        except (ValueError, TypeError):
            return 0.5  # Default if year parsing fails
    
    def _identify_relevance_factors(self, case: Dict, legal_issue: str, case_facts: str) -> Dict[str, Any]:
        """Identify factors contributing to case relevance"""
        factors = {
            'legal_issue_match': self._calculate_issue_similarity(case, legal_issue) > 0.7,
            'factual_similarity': self._calculate_factual_similarity(case, case_facts) > 0.6,
            'high_authority': self._get_authority_weight(case) >= 8,
            'recent_decision': self._calculate_recency_factor(case) >= 0.8,
            'frequently_cited': case.get('citation_count', 0) > 50,
            'same_jurisdiction': case.get('jurisdiction', '').lower() in case_facts.lower()
        }
        
        return factors
    
    def _assess_strategic_value(self, case: Dict, relevance_score: float) -> str:
        """Assess strategic value of precedent"""
        if relevance_score >= 8:
            return 'high_strategic_value'
        elif relevance_score >= 6:
            return 'moderate_strategic_value'
        elif relevance_score >= 4:
            return 'limited_strategic_value'
        else:
            return 'minimal_strategic_value'
    
    def _assess_citation_strength(self, case: Dict) -> Dict[str, Any]:
        """Assess citation strength of the precedent"""
        citation_count = case.get('citation_count', 0)
        authority_weight = self._get_authority_weight(case)
        
        if citation_count > 100 and authority_weight >= 8:
            strength = 'very_strong'
        elif citation_count > 50 or authority_weight >= 7:
            strength = 'strong'
        elif citation_count > 20 or authority_weight >= 5:
            strength = 'moderate'
        else:
            strength = 'weak'
        
        return {
            'citation_strength': strength,
            'citation_count': citation_count,
            'authority_weight': authority_weight,
            'analysis': f"Citation strength: {strength} (cited {citation_count} times, authority weight {authority_weight})"
        }
    
    def _categorize_precedent_authority(self, search_results: Dict, jurisdiction: str) -> Dict[str, Any]:
        """Categorize precedents by authority level"""
        cases = search_results.get('cases', [])
        
        authority_categories = {
            'binding_authority': [],
            'persuasive_authority': [],
            'same_jurisdiction': [],
            'other_jurisdictions': [],
            'supreme_court_cases': [],
            'circuit_court_cases': [],
            'district_court_cases': []
        }
        
        for case in cases:
            case_jurisdiction = case.get('jurisdiction', '').lower()
            court_level = case.get('court_level', '').lower()
            
            # Categorize by binding vs. persuasive
            if jurisdiction.lower() in case_jurisdiction:
                authority_categories['binding_authority'].append(case)
                authority_categories['same_jurisdiction'].append(case)
            else:
                authority_categories['persuasive_authority'].append(case)
                authority_categories['other_jurisdictions'].append(case)
            
            # Categorize by court level
            if 'supreme' in court_level:
                authority_categories['supreme_court_cases'].append(case)
            elif 'circuit' in court_level or 'appellate' in court_level:
                authority_categories['circuit_court_cases'].append(case)
            elif 'district' in court_level or 'trial' in court_level:
                authority_categories['district_court_cases'].append(case)
        
        return {
            'authority_categories': authority_categories,
            'authority_summary': self._summarize_authority_analysis(authority_categories),
            'binding_precedent_strength': self._assess_binding_precedent_strength(authority_categories['binding_authority']),
            'persuasive_precedent_value': self._assess_persuasive_precedent_value(authority_categories['persuasive_authority'])
        }
    
    def _summarize_authority_analysis(self, authority_categories: Dict) -> Dict[str, int]:
        """Summarize authority analysis"""
        return {
            'binding_cases': len(authority_categories['binding_authority']),
            'persuasive_cases': len(authority_categories['persuasive_authority']),
            'supreme_court_cases': len(authority_categories['supreme_court_cases']),
            'circuit_court_cases': len(authority_categories['circuit_court_cases']),
            'district_court_cases': len(authority_categories['district_court_cases']),
            'same_jurisdiction_cases': len(authority_categories['same_jurisdiction']),
            'other_jurisdiction_cases': len(authority_categories['other_jurisdictions'])
        }
    
    def _assess_binding_precedent_strength(self, binding_cases: List[Dict]) -> Dict[str, Any]:
        """Assess strength of binding precedents"""
        if not binding_cases:
            return {'strength': 'none', 'analysis': 'No binding precedents found'}
        
        high_authority_cases = [case for case in binding_cases if self._get_authority_weight(case) >= 8]
        recent_cases = [case for case in binding_cases if self._calculate_recency_factor(case) >= 0.8]
        
        if len(high_authority_cases) >= 2:
            strength = 'very_strong'
        elif len(high_authority_cases) >= 1 or len(recent_cases) >= 2:
            strength = 'strong'
        elif len(binding_cases) >= 3:
            strength = 'moderate'
        else:
            strength = 'weak'
        
        return {
            'strength': strength,
            'total_binding_cases': len(binding_cases),
            'high_authority_cases': len(high_authority_cases),
            'recent_cases': len(recent_cases),
            'analysis': f"Binding precedent strength: {strength} ({len(binding_cases)} cases)"
        }
    
    def _assess_persuasive_precedent_value(self, persuasive_cases: List[Dict]) -> Dict[str, Any]:
        """Assess value of persuasive precedents"""
        if not persuasive_cases:
            return {'value': 'none', 'analysis': 'No persuasive precedents found'}
        
        high_value_cases = [case for case in persuasive_cases if self._get_authority_weight(case) >= 8]
        well_reasoned_cases = [case for case in persuasive_cases if case.get('citation_count', 0) > 50]
        
        if len(high_value_cases) >= 3:
            value = 'high'
        elif len(high_value_cases) >= 1 or len(well_reasoned_cases) >= 3:
            value = 'moderate'
        else:
            value = 'limited'
        
        return {
            'value': value,
            'total_persuasive_cases': len(persuasive_cases),
            'high_value_cases': len(high_value_cases),
            'well_reasoned_cases': len(well_reasoned_cases),
            'analysis': f"Persuasive precedent value: {value} ({len(persuasive_cases)} cases)"
        }
    
    def _analyze_factual_similarity(self, search_results: Dict, case_facts: str) -> Dict[str, Any]:
        """Analyze factual similarity with precedents"""
        cases = search_results.get('cases', [])
        
        similarity_analysis = []
        
        for case in cases:
            similarity_score = self._calculate_factual_similarity(case, case_facts)
            factual_analysis = {
                'case': case,
                'similarity_score': similarity_score,
                'similar_factors': self._identify_similar_factual_factors(case, case_facts),
                'distinguishing_factors': self._identify_case_distinguishing_factors(case, case_facts),
                'analogical_strength': self._assess_analogical_strength(case, case_facts, similarity_score)
            }
            similarity_analysis.append(factual_analysis)
        
        # Sort by similarity score
        similarity_analysis.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return {
            'total_cases_analyzed': len(cases),
            'highly_similar_cases': [case for case in similarity_analysis if case['similarity_score'] >= 0.8],
            'moderately_similar_cases': [case for case in similarity_analysis if 0.5 <= case['similarity_score'] < 0.8],
            'dissimilar_cases': [case for case in similarity_analysis if case['similarity_score'] < 0.5],
            'top_analogous_cases': similarity_analysis[:5],  # Top 5 most similar
            'analogical_argument_strength': self._assess_overall_analogical_strength(similarity_analysis)
        }
    
    def _identify_similar_factual_factors(self, case: Dict, case_facts: str) -> List[str]:
        """Identify similar factual factors between cases"""
        case_facts_lower = case_facts.lower()
        precedent_facts = (case.get('facts', '') + ' ' + case.get('summary', '')).lower()
        
        factual_elements = [
            'contract terms', 'breach', 'damages', 'performance', 'notice',
            'employment relationship', 'termination', 'discrimination',
            'negligence', 'duty of care', 'causation', 'injury',
            'property rights', 'ownership', 'possession', 'transfer'
        ]
        
        similar_factors = []
        for element in factual_elements:
            if element in case_facts_lower and element in precedent_facts:
                similar_factors.append(element)
        
        return similar_factors
    
    def _identify_case_distinguishing_factors(self, case: Dict, case_facts: str) -> List[str]:
        """Identify factors that distinguish the cases"""
        # This would be more sophisticated in production
        distinguishing_factors = []
        
        case_year = case.get('decision_year', 0)
        current_year = datetime.now().year
        
        if current_year - case_year > 20:
            distinguishing_factors.append("Significant time difference - legal landscape may have evolved")
        
        case_jurisdiction = case.get('jurisdiction', '')
        if 'state' in case_jurisdiction.lower() and 'federal' in case_facts.lower():
            distinguishing_factors.append("Different jurisdictional context (state vs. federal)")
        
        return distinguishing_factors
    
    def _assess_analogical_strength(self, case: Dict, case_facts: str, similarity_score: float) -> str:
        """Assess analogical argument strength"""
        if similarity_score >= 0.8:
            return 'very_strong_analogy'
        elif similarity_score >= 0.6:
            return 'strong_analogy'
        elif similarity_score >= 0.4:
            return 'moderate_analogy'
        else:
            return 'weak_analogy'
    
    def _assess_overall_analogical_strength(self, similarity_analysis: List[Dict]) -> str:
        """Assess overall analogical argument strength"""
        if not similarity_analysis:
            return 'no_analogical_support'
        
        strong_analogies = [case for case in similarity_analysis if case['similarity_score'] >= 0.7]
        moderate_analogies = [case for case in similarity_analysis if 0.5 <= case['similarity_score'] < 0.7]
        
        if len(strong_analogies) >= 3:
            return 'very_strong_analogical_support'
        elif len(strong_analogies) >= 1:
            return 'strong_analogical_support'
        elif len(moderate_analogies) >= 3:
            return 'moderate_analogical_support'
        else:
            return 'limited_analogical_support'
    
    def _identify_distinguishing_factors(self, search_results: Dict, case_facts: str,
                                       legal_issue: str) -> Dict[str, Any]:
        """Identify distinguishing factors for precedents"""
        cases = search_results.get('cases', [])
        
        distinguishing_analysis = []
        
        for case in cases:
            distinguishing_factors = self._analyze_case_distinctions(case, case_facts, legal_issue)
            distinguishing_analysis.append({
                'case': case,
                'distinguishing_factors': distinguishing_factors,
                'distinction_impact': self._assess_distinction_impact(distinguishing_factors),
                'argument_strategies': self._suggest_distinguishing_strategies(distinguishing_factors)
            })
        
        return {
            'cases_with_distinctions': distinguishing_analysis,
            'common_distinguishing_factors': self._identify_common_distinctions(distinguishing_analysis),
            'material_distinctions': self._identify_material_distinctions(distinguishing_analysis),
            'distinguishing_strategy_recommendations': self._recommend_distinguishing_strategies(distinguishing_analysis)
        }
    
    def _analyze_case_distinctions(self, case: Dict, case_facts: str, legal_issue: str) -> List[Dict]:
        """Analyze distinctions between precedent and current case"""
        distinctions = []
        
        # Factual distinctions
        case_facts_lower = case_facts.lower()
        precedent_facts = (case.get('facts', '') + ' ' + case.get('summary', '')).lower()
        
        # Key factual elements to compare
        factual_elements = {
            'contract_written': 'written contract',
            'contract_oral': 'oral agreement',
            'employee_at_will': 'at-will employment',
            'employee_contract': 'employment contract',
            'individual_plaintiff': 'individual plaintiff',
            'class_action': 'class action'
        }
        
        for element_key, element_text in factual_elements.items():
            current_has = element_text in case_facts_lower
            precedent_has = element_text in precedent_facts
            
            if current_has != precedent_has:
                distinctions.append({
                    'type': 'factual',
                    'factor': element_text,
                    'current_case': current_has,
                    'precedent_case': precedent_has,
                    'materiality': 'material' if element_text in ['written contract', 'employment contract'] else 'potentially_material'
                })
        
        # Jurisdictional distinctions
        case_jurisdiction = case.get('jurisdiction', '')
        if 'state' in case_jurisdiction.lower() and 'federal' in case_facts.lower():
            distinctions.append({
                'type': 'jurisdictional',
                'factor': 'different_jurisdiction',
                'current_case': 'federal',
                'precedent_case': 'state',
                'materiality': 'material'
            })
        
        # Temporal distinctions
        case_year = case.get('decision_year', datetime.now().year)
        years_difference = datetime.now().year - case_year
        
        if years_difference > 15:
            distinctions.append({
                'type': 'temporal',
                'factor': 'significant_time_difference',
                'current_case': datetime.now().year,
                'precedent_case': case_year,
                'materiality': 'potentially_material'
            })
        
        return distinctions
    
    def _assess_distinction_impact(self, distinguishing_factors: List[Dict]) -> str:
        """Assess impact of distinguishing factors"""
        if not distinguishing_factors:
            return 'no_material_distinctions'
        
        material_distinctions = [factor for factor in distinguishing_factors 
                               if factor.get('materiality') == 'material']
        
        if len(material_distinctions) >= 2:
            return 'highly_distinguishable'
        elif len(material_distinctions) == 1:
            return 'materially_distinguishable'
        elif len(distinguishing_factors) >= 3:
            return 'potentially_distinguishable'
        else:
            return 'minimally_distinguishable'
    
    def _suggest_distinguishing_strategies(self, distinguishing_factors: List[Dict]) -> List[str]:
        """Suggest strategies for distinguishing precedents"""
        strategies = []
        
        for factor in distinguishing_factors:
            if factor['type'] == 'factual':
                strategies.append(f"Emphasize factual distinction: {factor['factor']}")
            elif factor['type'] == 'jurisdictional':
                strategies.append(f"Argue jurisdictional difference affects legal standard")
            elif factor['type'] == 'temporal':
                strategies.append(f"Argue legal doctrine has evolved since precedent")
        
        return strategies
    
    def _identify_common_distinctions(self, distinguishing_analysis: List[Dict]) -> List[str]:
        """Identify common distinguishing factors across cases"""
        distinction_counts = {}
        
        for case_analysis in distinguishing_analysis:
            for factor in case_analysis['distinguishing_factors']:
                factor_key = factor['factor']
                distinction_counts[factor_key] = distinction_counts.get(factor_key, 0) + 1
        
        common_distinctions = [factor for factor, count in distinction_counts.items() 
                             if count >= 2]
        
        return common_distinctions
    
    def _identify_material_distinctions(self, distinguishing_analysis: List[Dict]) -> List[Dict]:
        """Identify material distinctions requiring attention"""
        material_distinctions = []
        
        for case_analysis in distinguishing_analysis:
            case_material_distinctions = [factor for factor in case_analysis['distinguishing_factors']
                                        if factor.get('materiality') == 'material']
            if case_material_distinctions:
                material_distinctions.append({
                    'case': case_analysis['case'],
                    'material_factors': case_material_distinctions,
                    'impact': case_analysis['distinction_impact']
                })
        
        return material_distinctions
    
    def _recommend_distinguishing_strategies(self, distinguishing_analysis: List[Dict]) -> List[str]:
        """Recommend overall distinguishing strategies"""
        strategies = [
            "Prepare comprehensive factual distinction analysis",
            "Research jurisdictional differences in legal standards",
            "Identify evolution in legal doctrine since precedent decisions",
            "Develop argument hierarchy prioritizing material distinctions"
        ]
        
        return strategies
    
    def _identify_adverse_authority(self, search_results: Dict, legal_issue: str) -> Dict[str, Any]:
        """Identify potentially adverse authority"""
        cases = search_results.get('cases', [])
        
        adverse_cases = []
        
        for case in cases:
            adverse_indicators = self._check_adverse_indicators(case, legal_issue)
            if adverse_indicators['is_adverse']:
                adverse_cases.append({
                    'case': case,
                    'adverse_factors': adverse_indicators['factors'],
                    'adverse_severity': adverse_indicators['severity'],
                    'mitigation_strategies': self._suggest_adverse_mitigation(case, adverse_indicators)
                })
        
        return {
            'adverse_cases_identified': len(adverse_cases),
            'adverse_cases': adverse_cases,
            'high_risk_adverse_cases': [case for case in adverse_cases if case['adverse_severity'] == 'high'],
            'adverse_authority_strategy': self._develop_adverse_authority_strategy(adverse_cases),
            'adverse_mitigation_priority': self._prioritize_adverse_mitigation(adverse_cases)
        }
    
    def _check_adverse_indicators(self, case: Dict, legal_issue: str) -> Dict[str, Any]:
        """Check if case presents adverse authority"""
        # This would be more sophisticated in production
        case_holding = case.get('holding', '').lower()
        case_outcome = case.get('outcome', '').lower()
        legal_issue_lower = legal_issue.lower()
        
        adverse_factors = []
        
        # Check for opposing holdings
        if any(term in case_holding for term in ['rejected', 'denied', 'dismissed', 'failed']):
            adverse_factors.append('adverse_holding')
        
        # Check for unfavorable outcomes
        if any(term in case_outcome for term in ['defendant', 'dismissed', 'summary judgment']):
            adverse_factors.append('unfavorable_outcome')
        
        # Assess severity
        if len(adverse_factors) >= 2:
            severity = 'high'
        elif len(adverse_factors) == 1:
            severity = 'medium'
        else:
            severity = 'low'
        
        return {
            'is_adverse': len(adverse_factors) > 0,
            'factors': adverse_factors,
            'severity': severity
        }
    
    def _suggest_adverse_mitigation(self, case: Dict, adverse_indicators: Dict) -> List[str]:
        """Suggest strategies to mitigate adverse authority"""
        mitigation_strategies = []
        
        for factor in adverse_indicators['factors']:
            if factor == 'adverse_holding':
                mitigation_strategies.append("Distinguish factual circumstances from adverse case")
            elif factor == 'unfavorable_outcome':
                mitigation_strategies.append("Analyze procedural posture differences")
        
        mitigation_strategies.extend([
            "Identify limiting language in adverse opinion",
            "Research subsequent treatment of adverse case",
            "Develop policy arguments against adverse holding"
        ])
        
        return mitigation_strategies
    
    def _develop_adverse_authority_strategy(self, adverse_cases: List[Dict]) -> Dict[str, Any]:
        """Develop strategy for handling adverse authority"""
        if not adverse_cases:
            return {'strategy': 'no_adverse_authority', 'actions': []}
        
        high_risk_count = len([case for case in adverse_cases if case['adverse_severity'] == 'high'])
        
        if high_risk_count >= 2:
            strategy = 'comprehensive_distinguishing_required'
            actions = [
                "Prepare detailed factual and legal distinctions",
                "Research policy arguments against adverse holdings",
                "Consider alternative legal theories"
            ]
        elif high_risk_count == 1:
            strategy = 'targeted_distinguishing'
            actions = [
                "Focus on distinguishing high-risk adverse case",
                "Prepare backup arguments",
                "Research limiting interpretations"
            ]
        else:
            strategy = 'minimal_distinguishing'
            actions = [
                "Address adverse authority briefly",
                "Focus on positive precedents"
            ]
        
        return {'strategy': strategy, 'actions': actions}
    
    def _prioritize_adverse_mitigation(self, adverse_cases: List[Dict]) -> List[Dict]:
        """Prioritize adverse authority mitigation efforts"""
        # Sort by severity and authority weight
        prioritized_cases = sorted(adverse_cases, 
                                 key=lambda x: (
                                     {'high': 3, 'medium': 2, 'low': 1}[x['adverse_severity']],
                                     self._get_authority_weight(x['case'])
                                 ), reverse=True)
        
        return prioritized_cases[:5]  # Top 5 priority adverse cases
    
    def _generate_precedent_strategy(self, precedent_analysis: Dict, authority_analysis: Dict,
                                   distinguishing_analysis: Dict) -> Dict[str, Any]:
        """Generate overall precedent strategy"""
        binding_precedents = len(authority_analysis.get('authority_categories', {}).get('binding_authority', []))
        top_precedents = precedent_analysis.get('top_precedents', [])
        
        # Determine overall strategic approach
        if binding_precedents >= 3 and len(top_precedents) >= 5:
            strategic_approach = 'precedent_heavy_strategy'
        elif binding_precedents >= 1 or len(top_precedents) >= 3:
            strategic_approach = 'balanced_precedent_strategy'
        else:
            strategic_approach = 'limited_precedent_strategy'
        
        strategic_recommendations = {
            'overall_approach': strategic_approach,
            'primary_precedents': self._select_primary_precedents(top_precedents),
            'supporting_precedents': self._select_supporting_precedents(top_precedents),
            'precedent_hierarchy': self._establish_precedent_hierarchy(authority_analysis),
            'argument_structure': self._recommend_argument_structure(strategic_approach, top_precedents),
            'research_gaps': self._identify_research_gaps(precedent_analysis, authority_analysis),
            'overall_strategic_value': self._assess_overall_strategic_value(precedent_analysis, authority_analysis)
        }
        
        return strategic_recommendations
    
    def _select_primary_precedents(self, top_precedents: List[Dict]) -> List[Dict]:
        """Select primary precedents for argument"""
        # Select top 3 most relevant precedents with high strategic value
        primary_candidates = [case for case in top_precedents 
                            if case.get('strategic_value') in ['high_strategic_value', 'moderate_strategic_value']]
        
        return primary_candidates[:3]
    
    def _select_supporting_precedents(self, top_precedents: List[Dict]) -> List[Dict]:
        """Select supporting precedents"""
        # Select additional precedents for supporting arguments
        supporting_candidates = [case for case in top_precedents[3:] 
                               if case.get('relevance_score', 0) >= 5]
        
        return supporting_candidates[:5]
    
    def _establish_precedent_hierarchy(self, authority_analysis: Dict) -> List[str]:
        """Establish precedent hierarchy for argument structure"""
        authority_categories = authority_analysis.get('authority_categories', {})
        
        hierarchy = []
        
        if authority_categories.get('supreme_court_cases'):
            hierarchy.append("Supreme Court precedents (highest authority)")
        
        if authority_categories.get('binding_authority'):
            hierarchy.append("Binding circuit/state precedents")
        
        if authority_categories.get('circuit_court_cases'):
            hierarchy.append("Circuit court precedents")
        
        if authority_categories.get('persuasive_authority'):
            hierarchy.append("Persuasive authority from other jurisdictions")
        
        if authority_categories.get('district_court_cases'):
            hierarchy.append("District court precedents")
        
        return hierarchy
    
    def _recommend_argument_structure(self, strategic_approach: str, top_precedents: List[Dict]) -> List[str]:
        """Recommend argument structure based on precedent strength"""
        if strategic_approach == 'precedent_heavy_strategy':
            structure = [
                "Lead with strongest binding precedent",
                "Support with additional binding authority",
                "Reinforce with persuasive precedents",
                "Distinguish adverse authority",
                "Conclude with policy arguments"
            ]
        elif strategic_approach == 'balanced_precedent_strategy':
            structure = [
                "Establish legal framework with available precedents",
                "Apply precedents to case facts",
                "Address distinguishing factors",
                "Support with policy and practical considerations"
            ]
        else:
            structure = [
                "Acknowledge limited precedent authority",
                "Focus on legal principles and policy arguments",
                "Use available precedents for analogy",
                "Emphasize factual uniqueness if beneficial"
            ]
        
        return structure
    
    def _identify_research_gaps(self, precedent_analysis: Dict, authority_analysis: Dict) -> List[str]:
        """Identify gaps in precedent research"""
        gaps = []
        
        binding_cases = len(authority_analysis.get('authority_categories', {}).get('binding_authority', []))
        if binding_cases < 2:
            gaps.append("Search for additional binding precedents in jurisdiction")
        
        total_cases = precedent_analysis.get('total_cases_analyzed', 0)
        if total_cases < 10:
            gaps.append("Expand precedent search with alternative keywords")
        
        gaps.extend([
            "Research recent law review articles on the topic",
            "Check for pending appeals that might affect precedent landscape",
            "Review practice guides for additional case citations"
        ])
        
        return gaps
    
    def _assess_overall_strategic_value(self, precedent_analysis: Dict, authority_analysis: Dict) -> str:
        """Assess overall strategic value of precedent research"""
        highly_relevant = len(precedent_analysis.get('highly_relevant_cases', []))
        binding_precedents = len(authority_analysis.get('authority_categories', {}).get('binding_authority', []))
        
        if highly_relevant >= 3 and binding_precedents >= 2:
            return 'very_high'
        elif highly_relevant >= 2 or binding_precedents >= 1:
            return 'high'
        elif highly_relevant >= 1 or binding_precedents >= 0:
            return 'moderate'
        else:
            return 'limited'
    
    def _calculate_overall_precedent_strength(self, relevance_analysis: List[Dict]) -> str:
        """Calculate overall precedent strength"""
        if not relevance_analysis:
            return 'no_precedent_support'
        
        high_relevance_cases = [case for case in relevance_analysis if case['relevance_score'] >= 8]
        moderate_relevance_cases = [case for case in relevance_analysis if 6 <= case['relevance_score'] < 8]
        
        if len(high_relevance_cases) >= 3:
            return 'very_strong_precedent_support'
        elif len(high_relevance_cases) >= 1:
            return 'strong_precedent_support'
        elif len(moderate_relevance_cases) >= 3:
            return 'moderate_precedent_support'
        else:
            return 'limited_precedent_support'
    
    def _analyze_precedent_timeline(self, search_results: Dict) -> Dict[str, Any]:
        """Analyze timeline of precedent development"""
        cases = search_results.get('cases', [])
        
        if not cases:
            return {'timeline_analysis': 'No cases available for timeline analysis'}
        
        # Extract years and sort cases
        cases_with_years = []
        for case in cases:
            year = case.get('decision_year') or case.get('year')
            if year:
                try:
                    cases_with_years.append({'case': case, 'year': int(year)})
                except ValueError:
                    continue
        
        cases_with_years.sort(key=lambda x: x['year'])
        
        if not cases_with_years:
            return {'timeline_analysis': 'No date information available for timeline analysis'}
        
        # Analyze timeline patterns
        timeline_analysis = {
            'earliest_case': cases_with_years[0],
            'latest_case': cases_with_years[-1],
            'time_span_years': cases_with_years[-1]['year'] - cases_with_years[0]['year'],
            'cases_by_decade': self._group_cases_by_decade(cases_with_years),
            'doctrine_evolution': self._analyze_doctrine_evolution(cases_with_years),
            'recent_trends': self._identify_recent_trends(cases_with_years)
        }
        
        return timeline_analysis
    
    def _group_cases_by_decade(self, cases_with_years: List[Dict]) -> Dict[str, int]:
        """Group cases by decade"""
        decade_counts = {}
        
        for case_data in cases_with_years:
            decade = (case_data['year'] // 10) * 10
            decade_key = f"{decade}s"
            decade_counts[decade_key] = decade_counts.get(decade_key, 0) + 1
        
        return decade_counts
    
    def _analyze_doctrine_evolution(self, cases_with_years: List[Dict]) -> List[str]:
        """Analyze evolution of legal doctrine"""
        if len(cases_with_years) < 2:
            return ["Insufficient cases for doctrine evolution analysis"]
        
        evolution_observations = []
        
        # Simple analysis - could be more sophisticated
        earliest_year = cases_with_years[0]['year']
        latest_year = cases_with_years[-1]['year']
        
        if latest_year - earliest_year > 20:
            evolution_observations.append("Long-term doctrine development spanning multiple decades")
        
        recent_cases = [case for case in cases_with_years if case['year'] >= datetime.now().year - 10]
        if len(recent_cases) > len(cases_with_years) // 2:
            evolution_observations.append("Significant recent judicial activity in this area")
        
        return evolution_observations
    
    def _identify_recent_trends(self, cases_with_years: List[Dict]) -> List[str]:
        """Identify recent trends in precedent development"""
        current_year = datetime.now().year
        recent_cases = [case for case in cases_with_years if case['year'] >= current_year - 5]
        
        trends = []
        
        if len(recent_cases) >= 3:
            trends.append("High judicial activity in recent years")
        elif len(recent_cases) >= 1:
            trends.append("Some recent judicial development")
        else:
            trends.append("Limited recent judicial activity")
        
        return trends
    
    def _build_citation_network(self, search_results: Dict) -> Dict[str, Any]:
        """Build citation network analysis"""
        cases = search_results.get('cases', [])
        
        citation_network = {
            'total_cases': len(cases),
            'highly_cited_cases': [case for case in cases if case.get('citation_count', 0) > 100],
            'moderately_cited_cases': [case for case in cases if 20 <= case.get('citation_count', 0) <= 100],
            'citation_statistics': self._calculate_citation_statistics(cases),
            'citation_relationships': self._identify_citation_relationships(cases)
        }
        
        return citation_network
    
    def _calculate_citation_statistics(self, cases: List[Dict]) -> Dict[str, Any]:
        """Calculate citation statistics"""
        citation_counts = [case.get('citation_count', 0) for case in cases]
        
        if not citation_counts:
            return {'statistics': 'No citation data available'}
        
        return {
            'total_citations': sum(citation_counts),
            'average_citations': round(sum(citation_counts) / len(citation_counts), 1),
            'max_citations': max(citation_counts),
            'min_citations': min(citation_counts),
            'cases_with_citation_data': len([c for c in citation_counts if c > 0])
        }
    
    def _identify_citation_relationships(self, cases: List[Dict]) -> List[str]:
        """Identify citation relationships between cases"""
        # This would be more sophisticated in production
        relationships = []
        
        highly_cited = [case for case in cases if case.get('citation_count', 0) > 100]
        if highly_cited:
            relationships.append(f"Found {len(highly_cited)} highly-cited foundational cases")
        
        relationships.append("Citation network analysis requires detailed case citation data")
        
        return relationships
    
    def _suggest_follow_up_searches(self, precedent_analysis: Dict) -> List[str]:
        """Suggest follow-up precedent searches"""
        suggestions = []
        
        total_relevant = len(precedent_analysis.get('highly_relevant_cases', []))
        if total_relevant < 3:
            suggestions.append("Expand search with broader keywords to find more relevant precedents")
        
        suggestions.extend([
            "Search for law review articles citing the most relevant precedents",
            "Check for recent cases citing the primary precedents",
            "Research administrative guidance or regulatory interpretations",
            "Search for similar cases in related practice areas"
        ])
        
        return suggestions
    
    def _summarize_search_results(self, search_results: Dict) -> Dict[str, Any]:
        """Summarize precedent search results"""
        return {
            'total_cases_found': search_results.get('total_unique_cases', 0),
            'issue_based_results': len(search_results.get('issue_based_results', [])),
            'fact_based_results': len(search_results.get('fact_based_results', [])),
            'principle_based_results': len(search_results.get('principle_based_results', [])),
            'citation_network_results': len(search_results.get('citation_network_results', [])),
            'search_effectiveness': self._assess_search_effectiveness(search_results)
        }
    
    def _assess_search_effectiveness(self, search_results: Dict) -> str:
        """Assess effectiveness of precedent search"""
        total_cases = search_results.get('total_unique_cases', 0)
        
        if total_cases >= 15:
            return 'highly_effective'
        elif total_cases >= 8:
            return 'moderately_effective'
        elif total_cases >= 3:
            return 'minimally_effective'
        else:
            return 'limited_effectiveness'
    
    def _create_error_response(self, error_message: str, attorney_id: str = None,
                              client_id: str = None) -> Dict[str, Any]:
        """Create error response for failed precedent mining"""
        return self._format_legal_response(
            f"Precedent mining encountered an error: {error_message}. "
            "Please consult with qualified legal counsel for comprehensive precedent research.",
            {
                'error': True,
                'error_message': error_message,
                'precedent_mining_results': None,
                'requires_manual_research': True
            },
            attorney_id,
            client_id
        )