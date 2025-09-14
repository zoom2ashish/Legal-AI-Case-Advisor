#!/usr/bin/env python3
"""
Legal Ethics Compliance Manager for Legal AI System
Handles professional responsibility compliance, ethical guidelines, and regulatory requirements
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class EthicsRuleCategory(Enum):
    """Categories of legal ethics rules"""
    COMPETENCE = "competence"
    CONFIDENTIALITY = "confidentiality"
    CONFLICT_OF_INTEREST = "conflict_of_interest"
    CLIENT_RELATIONSHIP = "client_relationship"
    COMMUNICATION = "communication"
    FEES_AND_BILLING = "fees_and_billing"
    ADVOCACY = "advocacy"
    PROFESSIONAL_RESPONSIBILITY = "professional_responsibility"
    TECHNOLOGY_USE = "technology_use"
    AI_DISCLOSURE = "ai_disclosure"

class ComplianceStatus(Enum):
    """Compliance status levels"""
    COMPLIANT = "compliant"
    WARNING = "warning"
    VIOLATION = "violation"
    REVIEW_REQUIRED = "review_required"
    REMEDIATION_NEEDED = "remediation_needed"

class LegalEthicsComplianceManager:
    """
    Manages legal ethics compliance for AI systems
    Ensures adherence to professional responsibility rules and regulatory requirements
    """
    
    def __init__(self):
        """Initialize legal ethics compliance system"""
        self.ethics_rules = self._load_ethics_rules()
        self.compliance_log = []
        self.violation_tracking = {}
        self.attorney_competence_records = {}
        self.ai_disclosure_requirements = self._initialize_ai_disclosure_requirements()
        
        # Compliance thresholds
        self.compliance_thresholds = {
            'technology_competence_score': 7.0,
            'ai_disclosure_compliance': 90.0,
            'privilege_protection_score': 95.0,
            'conflict_screening_accuracy': 98.0,
            'client_communication_timeliness': 85.0
        }
        
        logger.info("Legal Ethics Compliance Manager initialized successfully")
    
    def _load_ethics_rules(self) -> Dict[str, Any]:
        """Load professional responsibility and ethics rules"""
        return {
            EthicsRuleCategory.COMPETENCE.value: {
                "rule_1_1": {
                    "title": "Competent Representation",
                    "description": "Lawyer shall provide competent representation requiring legal knowledge, skill, thoroughness, and preparation",
                    "ai_requirements": [
                        "Understand AI system capabilities and limitations",
                        "Maintain competence in legal technology use",
                        "Supervise AI-generated work appropriately"
                    ]
                },
                "rule_1_1_comment_8": {
                    "title": "Technology Competence",
                    "description": "Lawyer should keep abreast of changes in technology and their benefits/risks",
                    "ai_requirements": [
                        "Understand how AI systems work",
                        "Know when AI assistance is appropriate",
                        "Maintain human oversight of AI decisions"
                    ]
                }
            },
            EthicsRuleCategory.CONFIDENTIALITY.value: {
                "rule_1_6": {
                    "title": "Confidentiality of Information",
                    "description": "Lawyer shall not reveal information relating to client representation",
                    "ai_requirements": [
                        "Ensure AI systems protect client confidentiality",
                        "Implement proper data security measures",
                        "Control AI access to privileged information"
                    ]
                }
            },
            EthicsRuleCategory.CONFLICT_OF_INTEREST.value: {
                "rule_1_7": {
                    "title": "Conflict of Interest - Current Clients",
                    "description": "Lawyer shall not represent client if representation involves concurrent conflict of interest",
                    "ai_requirements": [
                        "Use AI to screen for conflicts systematically",
                        "Maintain comprehensive conflict databases",
                        "Regular conflict checking procedures"
                    ]
                }
            },
            EthicsRuleCategory.CLIENT_RELATIONSHIP.value: {
                "rule_1_4": {
                    "title": "Communication",
                    "description": "Lawyer shall reasonably consult with client about means of representation",
                    "ai_requirements": [
                        "Disclose AI use to clients when material",
                        "Explain AI role in representation",
                        "Maintain meaningful attorney-client communication"
                    ]
                }
            },
            EthicsRuleCategory.AI_DISCLOSURE.value: {
                "ai_disclosure_rule": {
                    "title": "AI Usage Disclosure",
                    "description": "Attorney must disclose material use of AI in client representation",
                    "ai_requirements": [
                        "Disclose AI use when outcome-determinative",
                        "Explain AI limitations and attorney oversight",
                        "Document AI disclosure in client files"
                    ]
                }
            }
        }
    
    def _initialize_ai_disclosure_requirements(self) -> Dict[str, Any]:
        """Initialize AI disclosure requirements and templates"""
        return {
            "disclosure_triggers": [
                "AI generates substantive legal work product",
                "AI influences significant case strategy decisions", 
                "AI reviews confidential client documents",
                "AI assists with legal research for critical issues",
                "Client specifically asks about technology use"
            ],
            "disclosure_templates": {
                "general_ai_disclosure": """
DISCLOSURE OF ARTIFICIAL INTELLIGENCE USE

This firm uses artificial intelligence (AI) technology to assist with certain aspects of legal representation, including research, document review, and case analysis. Please be aware that:

1. AI Technology Role: AI assists our attorneys but does not replace professional legal judgment
2. Attorney Supervision: All AI-generated work is reviewed and supervised by qualified attorneys
3. Quality Control: We maintain quality control procedures for AI-assisted work
4. Confidentiality: AI systems are configured to protect client confidentiality and attorney-client privilege
5. Limitations: AI has limitations and may not capture all relevant legal nuances
6. Human Oversight: Final legal decisions and strategy remain under attorney control

If you have questions about our use of AI technology, please contact us.
""",
                "document_review_disclosure": """
AI DOCUMENT REVIEW DISCLOSURE

We use AI technology to assist with document review in your matter. The AI system helps identify relevant documents and key information, but all conclusions and legal analysis are performed by our attorneys.
""",
                "legal_research_disclosure": """
AI LEGAL RESEARCH DISCLOSURE

Our legal research for your matter includes AI-assisted case law and statute searches. All research results are verified by our attorneys before being relied upon in your representation.
"""
            }
        }
    
    def assess_technology_competence(self, attorney_id: str, 
                                   competence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess attorney's technology competence under Rule 1.1"""
        try:
            competence_assessment = {
                'assessment_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'assessment_date': datetime.now().isoformat(),
                'competence_areas': {},
                'overall_score': 0.0,
                'compliance_status': ComplianceStatus.COMPLIANT.value,
                'recommendations': []
            }
            
            # Assess different competence areas
            competence_areas = {
                'ai_understanding': competence_data.get('ai_knowledge_score', 5),
                'technology_proficiency': competence_data.get('tech_proficiency_score', 5),
                'ethical_ai_use': competence_data.get('ethics_knowledge_score', 5),
                'supervision_capability': competence_data.get('supervision_score', 5),
                'risk_assessment': competence_data.get('risk_assessment_score', 5)
            }
            
            # Calculate scores and identify issues
            total_score = 0
            for area, score in competence_areas.items():
                competence_assessment['competence_areas'][area] = {
                    'score': score,
                    'threshold': self.compliance_thresholds['technology_competence_score'],
                    'compliant': score >= self.compliance_thresholds['technology_competence_score']
                }
                total_score += score
                
                if score < self.compliance_thresholds['technology_competence_score']:
                    competence_assessment['recommendations'].append(
                        f"Improve competence in {area.replace('_', ' ')}"
                    )
            
            # Calculate overall score and compliance status
            competence_assessment['overall_score'] = total_score / len(competence_areas)
            
            if competence_assessment['overall_score'] < 5.0:
                competence_assessment['compliance_status'] = ComplianceStatus.VIOLATION.value
            elif competence_assessment['overall_score'] < 7.0:
                competence_assessment['compliance_status'] = ComplianceStatus.WARNING.value
            
            # Store competence record
            self.attorney_competence_records[attorney_id] = competence_assessment
            
            # Log compliance assessment
            self._log_compliance_event(
                attorney_id=attorney_id,
                rule_category=EthicsRuleCategory.COMPETENCE.value,
                event_type='competence_assessment',
                compliance_status=competence_assessment['compliance_status'],
                details=f"Technology competence assessed: {competence_assessment['overall_score']:.1f}/10"
            )
            
            return competence_assessment
            
        except Exception as e:
            logger.error(f"Failed to assess technology competence: {str(e)}")
            return {'error': f'Competence assessment failed: {str(e)}'}
    
    def check_ai_disclosure_compliance(self, attorney_id: str, client_id: str,
                                     ai_usage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance with AI disclosure requirements"""
        try:
            disclosure_check = {
                'check_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'client_id': client_id,
                'check_date': datetime.now().isoformat(),
                'ai_usage_summary': ai_usage_data,
                'disclosure_required': False,
                'disclosure_provided': False,
                'compliance_status': ComplianceStatus.COMPLIANT.value,
                'recommendations': []
            }
            
            # Check if disclosure is required
            disclosure_triggers = self.ai_disclosure_requirements['disclosure_triggers']
            triggered_requirements = []
            
            for trigger in disclosure_triggers:
                if self._check_disclosure_trigger(trigger, ai_usage_data):
                    triggered_requirements.append(trigger)
            
            disclosure_check['triggered_requirements'] = triggered_requirements
            disclosure_check['disclosure_required'] = len(triggered_requirements) > 0
            
            # Check if disclosure was provided
            disclosure_check['disclosure_provided'] = ai_usage_data.get('disclosure_provided', False)
            
            # Determine compliance status
            if disclosure_check['disclosure_required'] and not disclosure_check['disclosure_provided']:
                disclosure_check['compliance_status'] = ComplianceStatus.VIOLATION.value
                disclosure_check['recommendations'].append("Provide AI disclosure to client immediately")
            elif disclosure_check['disclosure_required'] and disclosure_check['disclosure_provided']:
                disclosure_check['compliance_status'] = ComplianceStatus.COMPLIANT.value
            
            # Generate disclosure template if needed
            if disclosure_check['disclosure_required'] and not disclosure_check['disclosure_provided']:
                disclosure_check['suggested_disclosure'] = self._generate_disclosure_template(
                    triggered_requirements, ai_usage_data
                )
            
            # Log compliance check
            self._log_compliance_event(
                attorney_id=attorney_id,
                client_id=client_id,
                rule_category=EthicsRuleCategory.AI_DISCLOSURE.value,
                event_type='ai_disclosure_check',
                compliance_status=disclosure_check['compliance_status'],
                details=f"AI disclosure check: {len(triggered_requirements)} triggers, disclosure {'provided' if disclosure_check['disclosure_provided'] else 'not provided'}"
            )
            
            return disclosure_check
            
        except Exception as e:
            logger.error(f"Failed to check AI disclosure compliance: {str(e)}")
            return {'error': f'AI disclosure check failed: {str(e)}'}
    
    def monitor_client_communication_compliance(self, attorney_id: str, client_id: str,
                                              communication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor compliance with client communication requirements"""
        try:
            communication_check = {
                'check_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'client_id': client_id,
                'check_date': datetime.now().isoformat(),
                'communication_analysis': {},
                'compliance_status': ComplianceStatus.COMPLIANT.value,
                'issues_identified': [],
                'recommendations': []
            }
            
            # Analyze communication timeliness
            response_times = communication_data.get('response_times', [])
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                communication_check['communication_analysis']['average_response_hours'] = avg_response_time
                
                if avg_response_time > 48:  # More than 2 days
                    communication_check['issues_identified'].append('Slow response times')
                    communication_check['compliance_status'] = ComplianceStatus.WARNING.value
            
            # Check for adequate AI disclosure in communications
            ai_mentioned = communication_data.get('ai_mentioned_in_communications', False)
            ai_used = communication_data.get('ai_assistance_used', False)
            
            if ai_used and not ai_mentioned:
                communication_check['issues_identified'].append('AI use not disclosed in relevant communications')
                communication_check['compliance_status'] = ComplianceStatus.VIOLATION.value
                communication_check['recommendations'].append('Disclose AI use in client communications when material')
            
            # Check for meaningful consultation
            consultation_frequency = communication_data.get('consultation_frequency', 'unknown')
            if consultation_frequency == 'rare':
                communication_check['issues_identified'].append('Insufficient client consultation')
                communication_check['compliance_status'] = ComplianceStatus.WARNING.value
                communication_check['recommendations'].append('Increase frequency of client consultation and updates')
            
            # Log compliance monitoring
            self._log_compliance_event(
                attorney_id=attorney_id,
                client_id=client_id,
                rule_category=EthicsRuleCategory.COMMUNICATION.value,
                event_type='communication_compliance_check',
                compliance_status=communication_check['compliance_status'],
                details=f"Communication compliance: {len(communication_check['issues_identified'])} issues identified"
            )
            
            return communication_check
            
        except Exception as e:
            logger.error(f"Failed to monitor communication compliance: {str(e)}")
            return {'error': f'Communication compliance check failed: {str(e)}'}
    
    def validate_conflict_screening_procedures(self, attorney_id: str,
                                             screening_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate conflict of interest screening procedures"""
        try:
            screening_validation = {
                'validation_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'validation_date': datetime.now().isoformat(),
                'screening_analysis': {},
                'compliance_status': ComplianceStatus.COMPLIANT.value,
                'procedural_issues': [],
                'recommendations': []
            }
            
            # Check screening frequency
            screening_frequency = screening_data.get('screening_frequency', 'unknown')
            if screening_frequency in ['rarely', 'never']:
                screening_validation['procedural_issues'].append('Inadequate conflict screening frequency')
                screening_validation['compliance_status'] = ComplianceStatus.VIOLATION.value
            
            # Check screening comprehensiveness
            screening_scope = screening_data.get('screening_scope', [])
            required_scope = ['current_clients', 'former_clients', 'third_party_interests', 'business_relationships']
            missing_scope = [item for item in required_scope if item not in screening_scope]
            
            if missing_scope:
                screening_validation['procedural_issues'].append(f'Incomplete screening scope: missing {missing_scope}')
                screening_validation['compliance_status'] = ComplianceStatus.WARNING.value
            
            # Check AI assistance in conflict screening
            ai_assisted_screening = screening_data.get('ai_assisted', False)
            if ai_assisted_screening:
                ai_supervision = screening_data.get('ai_supervision_level', 'none')
                if ai_supervision == 'none':
                    screening_validation['procedural_issues'].append('AI conflict screening lacks human supervision')
                    screening_validation['compliance_status'] = ComplianceStatus.VIOLATION.value
            
            # Generate recommendations
            if screening_validation['procedural_issues']:
                screening_validation['recommendations'].extend([
                    'Implement systematic conflict screening procedures',
                    'Ensure comprehensive scope of conflict checking',
                    'Maintain proper supervision of AI-assisted screening'
                ])
            
            # Log validation
            self._log_compliance_event(
                attorney_id=attorney_id,
                rule_category=EthicsRuleCategory.CONFLICT_OF_INTEREST.value,
                event_type='conflict_screening_validation',
                compliance_status=screening_validation['compliance_status'],
                details=f"Conflict screening validation: {len(screening_validation['procedural_issues'])} issues found"
            )
            
            return screening_validation
            
        except Exception as e:
            logger.error(f"Failed to validate conflict screening: {str(e)}")
            return {'error': f'Conflict screening validation failed: {str(e)}'}
    
    def assess_billing_practices_compliance(self, attorney_id: str, client_id: str,
                                          billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance with fee and billing ethics rules"""
        try:
            billing_assessment = {
                'assessment_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'client_id': client_id,
                'assessment_date': datetime.now().isoformat(),
                'billing_analysis': {},
                'compliance_status': ComplianceStatus.COMPLIANT.value,
                'billing_issues': [],
                'recommendations': []
            }
            
            # Check AI-related billing transparency
            ai_work_percentage = billing_data.get('ai_assisted_work_percentage', 0)
            ai_billing_disclosed = billing_data.get('ai_billing_disclosed', False)
            
            if ai_work_percentage > 20 and not ai_billing_disclosed:
                billing_assessment['billing_issues'].append('AI assistance in billable work not disclosed')
                billing_assessment['compliance_status'] = ComplianceStatus.WARNING.value
            
            # Check for appropriate billing rates for AI-assisted work
            ai_billing_rate_adjusted = billing_data.get('ai_rate_adjusted', False)
            if ai_work_percentage > 30 and not ai_billing_rate_adjusted:
                billing_assessment['billing_issues'].append('Billing rates not adjusted for AI assistance')
                billing_assessment['compliance_status'] = ComplianceStatus.WARNING.value
                billing_assessment['recommendations'].append('Consider rate adjustment for AI-assisted work')
            
            # Check fee reasonableness
            fee_reasonableness_score = billing_data.get('fee_reasonableness_score', 5)
            if fee_reasonableness_score < 6:
                billing_assessment['billing_issues'].append('Questionable fee reasonableness')
                billing_assessment['compliance_status'] = ComplianceStatus.REVIEW_REQUIRED.value
            
            # Check billing description adequacy
            billing_description_quality = billing_data.get('description_quality_score', 5)
            if billing_description_quality < 6:
                billing_assessment['billing_issues'].append('Inadequate billing descriptions')
                billing_assessment['recommendations'].append('Improve detail and clarity in billing descriptions')
            
            # Log assessment
            self._log_compliance_event(
                attorney_id=attorney_id,
                client_id=client_id,
                rule_category=EthicsRuleCategory.FEES_AND_BILLING.value,
                event_type='billing_compliance_assessment',
                compliance_status=billing_assessment['compliance_status'],
                details=f"Billing assessment: {len(billing_assessment['billing_issues'])} issues identified"
            )
            
            return billing_assessment
            
        except Exception as e:
            logger.error(f"Failed to assess billing compliance: {str(e)}")
            return {'error': f'Billing compliance assessment failed: {str(e)}'}
    
    def generate_comprehensive_compliance_report(self, attorney_id: str,
                                               reporting_period_days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive ethics compliance report"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=reporting_period_days)
            
            # Filter compliance logs for the reporting period
            relevant_logs = [
                log for log in self.compliance_log
                if (log.get('attorney_id') == attorney_id and
                    start_date <= datetime.fromisoformat(log['timestamp']) <= end_date)
            ]
            
            # Analyze compliance by category
            compliance_by_category = {}
            for category in EthicsRuleCategory:
                category_logs = [log for log in relevant_logs if log['rule_category'] == category.value]
                compliance_by_category[category.value] = {
                    'total_events': len(category_logs),
                    'violations': len([log for log in category_logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value]),
                    'warnings': len([log for log in category_logs if log['compliance_status'] == ComplianceStatus.WARNING.value]),
                    'compliance_rate': self._calculate_category_compliance_rate(category_logs)
                }
            
            # Calculate overall compliance scores
            overall_compliance = self._calculate_overall_compliance_score(relevant_logs)
            
            # Generate recommendations
            recommendations = self._generate_compliance_recommendations(compliance_by_category, relevant_logs)
            
            compliance_report = {
                'report_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'reporting_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': reporting_period_days
                },
                'overall_compliance': overall_compliance,
                'compliance_by_category': compliance_by_category,
                'key_findings': self._extract_key_findings(relevant_logs),
                'recommendations': recommendations,
                'action_items': self._prioritize_action_items(compliance_by_category),
                'generated_at': datetime.now().isoformat()
            }
            
            return compliance_report
            
        except Exception as e:
            logger.error(f"Failed to generate compliance report: {str(e)}")
            return {'error': f'Compliance report generation failed: {str(e)}'}
    
    def _check_disclosure_trigger(self, trigger: str, ai_usage_data: Dict[str, Any]) -> bool:
        """Check if specific disclosure trigger applies"""
        trigger_checks = {
            "AI generates substantive legal work product": ai_usage_data.get('substantive_work_generated', False),
            "AI influences significant case strategy decisions": ai_usage_data.get('strategy_influence', False),
            "AI reviews confidential client documents": ai_usage_data.get('document_review', False),
            "AI assists with legal research for critical issues": ai_usage_data.get('critical_research', False),
            "Client specifically asks about technology use": ai_usage_data.get('client_inquiry_about_ai', False)
        }
        
        return trigger_checks.get(trigger, False)
    
    def _generate_disclosure_template(self, triggered_requirements: List[str],
                                    ai_usage_data: Dict[str, Any]) -> str:
        """Generate appropriate disclosure template based on AI usage"""
        base_disclosure = self.ai_disclosure_requirements['disclosure_templates']['general_ai_disclosure']
        
        specific_disclosures = []
        
        if any('document' in req.lower() for req in triggered_requirements):
            specific_disclosures.append(
                self.ai_disclosure_requirements['disclosure_templates']['document_review_disclosure']
            )
        
        if any('research' in req.lower() for req in triggered_requirements):
            specific_disclosures.append(
                self.ai_disclosure_requirements['disclosure_templates']['legal_research_disclosure']
            )
        
        if specific_disclosures:
            return base_disclosure + "\n\nSPECIFIC AI USE IN YOUR MATTER:\n" + "\n".join(specific_disclosures)
        else:
            return base_disclosure
    
    def _calculate_category_compliance_rate(self, category_logs: List[Dict[str, Any]]) -> float:
        """Calculate compliance rate for a specific category"""
        if not category_logs:
            return 100.0
        
        compliant_events = len([
            log for log in category_logs 
            if log['compliance_status'] == ComplianceStatus.COMPLIANT.value
        ])
        
        return (compliant_events / len(category_logs)) * 100
    
    def _calculate_overall_compliance_score(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall compliance score"""
        if not logs:
            return {
                'overall_score': 100.0,
                'compliance_level': 'excellent',
                'total_events': 0,
                'violations': 0,
                'warnings': 0
            }
        
        violations = len([log for log in logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value])
        warnings = len([log for log in logs if log['compliance_status'] == ComplianceStatus.WARNING.value])
        compliant = len([log for log in logs if log['compliance_status'] == ComplianceStatus.COMPLIANT.value])
        
        # Weighted scoring: violations more serious than warnings
        weighted_score = (compliant + (warnings * 0.5)) / len(logs) * 100
        
        compliance_level = 'excellent' if weighted_score >= 90 else \
                          'good' if weighted_score >= 75 else \
                          'needs_improvement' if weighted_score >= 50 else \
                          'poor'
        
        return {
            'overall_score': round(weighted_score, 2),
            'compliance_level': compliance_level,
            'total_events': len(logs),
            'violations': violations,
            'warnings': warnings,
            'compliant': compliant
        }
    
    def _generate_compliance_recommendations(self, compliance_by_category: Dict[str, Any],
                                           logs: List[Dict[str, Any]]) -> List[str]:
        """Generate compliance improvement recommendations"""
        recommendations = []
        
        # Category-specific recommendations
        for category, stats in compliance_by_category.items():
            if stats['compliance_rate'] < 80:
                category_name = category.replace('_', ' ').title()
                recommendations.append(f"Improve compliance in {category_name} (current rate: {stats['compliance_rate']:.1f}%)")
        
        # General recommendations
        total_violations = sum([len([log for log in logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value])])
        if total_violations > 0:
            recommendations.append(f"Address {total_violations} compliance violations immediately")
        
        # Technology-specific recommendations
        ai_logs = [log for log in logs if 'ai' in log.get('details', '').lower()]
        if ai_logs:
            recommendations.append("Review AI usage procedures and disclosure practices")
        
        return recommendations
    
    def _extract_key_findings(self, logs: List[Dict[str, Any]]) -> List[str]:
        """Extract key findings from compliance logs"""
        findings = []
        
        # Most common issues
        violation_types = {}
        for log in logs:
            if log['compliance_status'] in [ComplianceStatus.VIOLATION.value, ComplianceStatus.WARNING.value]:
                event_type = log.get('event_type', 'unknown')
                violation_types[event_type] = violation_types.get(event_type, 0) + 1
        
        if violation_types:
            most_common = max(violation_types.items(), key=lambda x: x[1])
            findings.append(f"Most common compliance issue: {most_common[0]} ({most_common[1]} occurrences)")
        
        # AI-related findings
        ai_related_logs = [log for log in logs if 'ai' in log.get('details', '').lower()]
        if ai_related_logs:
            findings.append(f"AI-related compliance events: {len(ai_related_logs)}")
        
        return findings
    
    def _prioritize_action_items(self, compliance_by_category: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize action items based on compliance analysis"""
        action_items = []
        
        for category, stats in compliance_by_category.items():
            if stats['violations'] > 0:
                action_items.append({
                    'priority': 'high',
                    'category': category,
                    'action': f"Address {stats['violations']} violations in {category.replace('_', ' ')}",
                    'impact': 'critical'
                })
            elif stats['warnings'] > 0:
                action_items.append({
                    'priority': 'medium',
                    'category': category,
                    'action': f"Review {stats['warnings']} warnings in {category.replace('_', ' ')}",
                    'impact': 'moderate'
                })
        
        # Sort by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        action_items.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        
        return action_items
    
    def _log_compliance_event(self, rule_category: str, event_type: str,
                            compliance_status: str, attorney_id: str = None,
                            client_id: str = None, details: str = '', **kwargs):
        """Log ethics compliance event"""
        log_entry = {
            'log_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'attorney_id': attorney_id,
            'client_id': client_id,
            'rule_category': rule_category,
            'event_type': event_type,
            'compliance_status': compliance_status,
            'details': details,
            'metadata': kwargs
        }
        
        self.compliance_log.append(log_entry)
        
        # Track violations for escalation
        if compliance_status == ComplianceStatus.VIOLATION.value:
            if attorney_id not in self.violation_tracking:
                self.violation_tracking[attorney_id] = []
            self.violation_tracking[attorney_id].append(log_entry)
        
        logger.info(f"Ethics compliance event logged: {event_type} - {compliance_status}")
    
    def get_compliance_dashboard_data(self, attorney_id: str = None) -> Dict[str, Any]:
        """Get compliance dashboard data"""
        try:
            # Filter logs by attorney if specified
            relevant_logs = self.compliance_log
            if attorney_id:
                relevant_logs = [log for log in self.compliance_log if log.get('attorney_id') == attorney_id]
            
            # Recent compliance trends (last 7 days)
            recent_date = datetime.now() - timedelta(days=7)
            recent_logs = [
                log for log in relevant_logs
                if datetime.fromisoformat(log['timestamp']) > recent_date
            ]
            
            dashboard_data = {
                'overall_metrics': {
                    'total_compliance_events': len(relevant_logs),
                    'recent_events': len(recent_logs),
                    'active_violations': len([log for log in recent_logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value]),
                    'warnings_issued': len([log for log in recent_logs if log['compliance_status'] == ComplianceStatus.WARNING.value])
                },
                'compliance_by_category': self._get_category_breakdown(recent_logs),
                'trending_issues': self._identify_trending_issues(recent_logs),
                'attorney_specific_data': self.attorney_competence_records.get(attorney_id, {}) if attorney_id else {},
                'recommendations': self._get_dashboard_recommendations(recent_logs),
                'last_updated': datetime.now().isoformat()
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Failed to get compliance dashboard data: {str(e)}")
            return {'error': f'Dashboard data retrieval failed: {str(e)}'}
    
    def _get_category_breakdown(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get compliance breakdown by category"""
        category_breakdown = {}
        
        for category in EthicsRuleCategory:
            category_logs = [log for log in logs if log['rule_category'] == category.value]
            category_breakdown[category.value] = {
                'total': len(category_logs),
                'violations': len([log for log in category_logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value]),
                'warnings': len([log for log in category_logs if log['compliance_status'] == ComplianceStatus.WARNING.value]),
                'compliant': len([log for log in category_logs if log['compliance_status'] == ComplianceStatus.COMPLIANT.value])
            }
        
        return category_breakdown
    
    def _identify_trending_issues(self, logs: List[Dict[str, Any]]) -> List[str]:
        """Identify trending compliance issues"""
        issue_counts = {}
        
        for log in logs:
            if log['compliance_status'] in [ComplianceStatus.VIOLATION.value, ComplianceStatus.WARNING.value]:
                category = log['rule_category']
                issue_counts[category] = issue_counts.get(category, 0) + 1
        
        # Sort by frequency and return top issues
        trending = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{category.replace('_', ' ').title()}: {count} issues" for category, count in trending[:3]]
    
    def _get_dashboard_recommendations(self, logs: List[Dict[str, Any]]) -> List[str]:
        """Get dashboard-specific recommendations"""
        recommendations = []
        
        violation_count = len([log for log in logs if log['compliance_status'] == ComplianceStatus.VIOLATION.value])
        if violation_count > 0:
            recommendations.append(f"Immediate attention required: {violation_count} compliance violations")
        
        ai_related = len([log for log in logs if 'ai' in log.get('details', '').lower()])
        if ai_related > 5:
            recommendations.append("Consider AI ethics training and procedure review")
        
        recommendations.append("Regular compliance monitoring recommended")
        
        return recommendations
    
    def health_check(self) -> bool:
        """Check if ethics compliance system is functioning"""
        try:
            # Test logging functionality
            test_log = {
                'log_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'test': True
            }
            
            # Test ethics rules loading
            if not self.ethics_rules:
                return False
            
            # Test AI disclosure requirements
            if not self.ai_disclosure_requirements:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Ethics compliance health check failed: {str(e)}")
            return False

    # Additional methods needed by the main app
    def get_ethics_dashboard_data(self, attorney_id: str) -> Dict[str, Any]:
        """Get ethics dashboard data for a specific attorney"""
        return self.get_compliance_dashboard_data(attorney_id)
    
    def get_legal_system_metrics(self) -> Dict[str, Any]:
        """Get system-wide legal ethics metrics"""
        return self.get_compliance_dashboard_data()  # Return overall system metrics

# Create alias for the class name used in main app
LegalEthicsMonitoring = LegalEthicsComplianceManager