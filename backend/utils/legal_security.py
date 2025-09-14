#!/usr/bin/env python3
"""
Attorney-Client Privilege Security Manager for Legal AI System
Handles privilege protection, confidentiality, and secure access controls
"""

import os
import logging
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import uuid

logger = logging.getLogger(__name__)

class AttorneyClientPrivilegeManager:
    """
    Manages attorney-client privilege protection with encryption, access controls, and audit logging
    Ensures compliance with legal ethics rules and confidentiality requirements
    """
    
    def __init__(self):
        """Initialize privilege protection systems"""
        self.master_key = self._initialize_encryption_key()
        self.cipher = Fernet(self.master_key)
        self.session_store = {}
        self.access_log = []
        
        # Privilege protection settings
        self.privilege_settings = {
            'require_attorney_verification': True,
            'require_client_consent': True,
            'encrypt_all_communications': True,
            'audit_all_access': True,
            'session_timeout_minutes': 60,
            'max_failed_attempts': 3,
            'privilege_retention_years': 10
        }
        
        logger.info("Attorney-Client Privilege Manager initialized successfully")
    
    def _initialize_encryption_key(self) -> bytes:
        """Initialize or load master encryption key"""
        try:
            # In production, load from secure key management system
            key_env = os.getenv('LEGAL_PRIVILEGE_KEY')
            if key_env:
                return base64.urlsafe_b64decode(key_env)
            else:
                # Generate new key for demo (DO NOT use in production)
                key = Fernet.generate_key()
                logger.warning("Generated new encryption key for demo - use proper key management in production")
                return key
        except Exception as e:
            logger.error(f"Failed to initialize encryption key: {str(e)}")
            raise
    
    def create_secure_session(self, attorney_id: str, client_id: str = None,
                            session_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create secure session for attorney-client communications"""
        try:
            session_id = str(uuid.uuid4())
            session_token = self._generate_session_token()
            
            # Create session data
            session_data = {
                'session_id': session_id,
                'session_token': session_token,
                'attorney_id': attorney_id,
                'client_id': client_id,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(minutes=self.privilege_settings['session_timeout_minutes'])).isoformat(),
                'privilege_level': 'full_privilege' if client_id else 'attorney_only',
                'access_count': 0,
                'last_activity': datetime.now().isoformat(),
                'context': session_context or {},
                'active': True
            }
            
            # Encrypt session data
            encrypted_session_data = self.encrypt_privileged_data(json.dumps(session_data))
            
            # Store session
            self.session_store[session_id] = {
                'token': session_token,
                'encrypted_data': encrypted_session_data,
                'attorney_id': attorney_id,
                'client_id': client_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now()
            }
            
            # Log session creation
            self._log_privilege_access(
                attorney_id=attorney_id,
                client_id=client_id,
                action='secure_session_created',
                session_id=session_id,
                details='Secure privileged session established'
            )
            
            return {
                'session_id': session_id,
                'session_token': session_token,
                'expires_at': session_data['expires_at'],
                'privilege_level': session_data['privilege_level'],
                'message': 'Secure privileged session created successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to create secure session: {str(e)}")
            raise
    
    def verify_privileged_access(self, session_id: str, session_token: str,
                                attorney_id: str, client_id: str = None) -> Dict[str, Any]:
        """Verify privileged access with attorney-client relationship validation"""
        try:
            # Check if session exists
            if session_id not in self.session_store:
                self._log_privilege_violation(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    violation_type='invalid_session',
                    details='Attempted access with invalid session ID'
                )
                return {'authorized': False, 'reason': 'Invalid session'}
            
            session_info = self.session_store[session_id]
            
            # Verify session token
            if session_info['token'] != session_token:
                self._log_privilege_violation(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    violation_type='invalid_token',
                    details='Invalid session token provided'
                )
                return {'authorized': False, 'reason': 'Invalid session token'}
            
            # Decrypt and verify session data
            decrypted_data = self.decrypt_privileged_data(session_info['encrypted_data'])
            session_data = json.loads(decrypted_data)
            
            # Check if session has expired
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                self._invalidate_session(session_id)
                return {'authorized': False, 'reason': 'Session expired'}
            
            # Verify attorney identity
            if session_data['attorney_id'] != attorney_id:
                self._log_privilege_violation(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    violation_type='attorney_mismatch',
                    details='Attorney ID does not match session'
                )
                return {'authorized': False, 'reason': 'Attorney mismatch'}
            
            # Verify client relationship if client_id provided
            if client_id and session_data.get('client_id') != client_id:
                self._log_privilege_violation(
                    attorney_id=attorney_id,
                    client_id=client_id,
                    violation_type='client_mismatch',
                    details='Client ID does not match session'
                )
                return {'authorized': False, 'reason': 'Client relationship mismatch'}
            
            # Update session activity
            self._update_session_activity(session_id)
            
            # Log successful access
            self._log_privilege_access(
                attorney_id=attorney_id,
                client_id=client_id,
                action='privileged_access_verified',
                session_id=session_id,
                details='Privileged access authorized'
            )
            
            return {
                'authorized': True,
                'session_data': session_data,
                'privilege_level': session_data['privilege_level'],
                'remaining_time_minutes': int((expires_at - datetime.now()).total_seconds() / 60)
            }
            
        except Exception as e:
            logger.error(f"Failed to verify privileged access: {str(e)}")
            self._log_privilege_violation(
                attorney_id=attorney_id,
                client_id=client_id,
                violation_type='verification_error',
                details=f'Error verifying access: {str(e)}'
            )
            return {'authorized': False, 'reason': 'Access verification failed'}
    
    def encrypt_privileged_data(self, data: str) -> str:
        """Encrypt privileged attorney-client data"""
        try:
            if isinstance(data, dict) or isinstance(data, list):
                data = json.dumps(data)
            return self.cipher.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt privileged data: {str(e)}")
            raise
    
    def decrypt_privileged_data(self, encrypted_data: str) -> str:
        """Decrypt privileged attorney-client data"""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Failed to decrypt privileged data: {str(e)}")
            raise
    
    def protect_privileged_communication(self, communication_data: Dict[str, Any],
                                       attorney_id: str, client_id: str) -> Dict[str, Any]:
        """Apply privilege protection to attorney-client communication"""
        try:
            # Generate communication ID
            communication_id = str(uuid.uuid4())
            
            # Create privilege metadata
            privilege_metadata = {
                'communication_id': communication_id,
                'attorney_id': attorney_id,
                'client_id': client_id,
                'privilege_type': 'attorney_client',
                'protection_level': 'full_privilege',
                'confidentiality_level': 'highest',
                'work_product_protection': communication_data.get('work_product', False),
                'privilege_holders': [attorney_id, client_id],
                'created_at': datetime.now().isoformat(),
                'retention_until': (datetime.now() + timedelta(days=365 * self.privilege_settings['privilege_retention_years'])).isoformat(),
                'access_restrictions': {
                    'require_attorney_authorization': True,
                    'require_client_consent': True,
                    'audit_all_access': True
                }
            }
            
            # Encrypt communication content
            encrypted_content = self.encrypt_privileged_data(communication_data.get('content', ''))
            
            # Create protected communication structure
            protected_communication = {
                'communication_id': communication_id,
                'privilege_metadata': privilege_metadata,
                'encrypted_content': encrypted_content,
                'communication_type': communication_data.get('type', 'legal_advice'),
                'timestamp': datetime.now().isoformat(),
                'integrity_hash': self._calculate_integrity_hash(encrypted_content)
            }
            
            # Log privilege protection application
            self._log_privilege_access(
                attorney_id=attorney_id,
                client_id=client_id,
                action='privilege_protection_applied',
                details=f'Communication {communication_id} protected with attorney-client privilege'
            )
            
            return protected_communication
            
        except Exception as e:
            logger.error(f"Failed to protect privileged communication: {str(e)}")
            raise
    
    def verify_privilege_waiver(self, attorney_id: str, client_id: str,
                              waiver_scope: str, waiver_authorization: Dict[str, Any]) -> Dict[str, Any]:
        """Verify and process privilege waiver"""
        try:
            waiver_id = str(uuid.uuid4())
            
            # Verify waiver authorization
            required_fields = ['client_signature', 'waiver_date', 'waiver_scope', 'attorney_approval']
            missing_fields = [field for field in required_fields if field not in waiver_authorization]
            
            if missing_fields:
                return {
                    'waiver_valid': False,
                    'reason': f'Missing required fields: {missing_fields}'
                }
            
            # Create waiver record
            waiver_record = {
                'waiver_id': waiver_id,
                'attorney_id': attorney_id,
                'client_id': client_id,
                'waiver_scope': waiver_scope,
                'waiver_date': waiver_authorization['waiver_date'],
                'client_signature': waiver_authorization['client_signature'],
                'attorney_approval': waiver_authorization['attorney_approval'],
                'waiver_limitations': waiver_authorization.get('limitations', []),
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Log privilege waiver
            self._log_privilege_access(
                attorney_id=attorney_id,
                client_id=client_id,
                action='privilege_waiver_processed',
                details=f'Privilege waiver {waiver_id} for scope: {waiver_scope}'
            )
            
            return {
                'waiver_valid': True,
                'waiver_id': waiver_id,
                'waiver_record': waiver_record,
                'message': 'Privilege waiver verified and processed'
            }
            
        except Exception as e:
            logger.error(f"Failed to verify privilege waiver: {str(e)}")
            return {'waiver_valid': False, 'reason': f'Waiver verification failed: {str(e)}'}
    
    def check_conflict_of_interest(self, attorney_id: str, new_client_id: str,
                                 matter_description: str) -> Dict[str, Any]:
        """Check for conflicts of interest in attorney-client relationships"""
        try:
            conflict_check_id = str(uuid.uuid4())
            
            # Get existing client relationships for conflict analysis
            existing_relationships = self._get_attorney_relationships(attorney_id)
            
            # Analyze potential conflicts
            conflicts_detected = []
            
            # Check for direct conflicts (same parties on different sides)
            for relationship in existing_relationships:
                if self._analyze_direct_conflict(relationship, new_client_id, matter_description):
                    conflicts_detected.append({
                        'type': 'direct_conflict',
                        'existing_client': relationship['client_id'],
                        'description': 'Direct conflict with existing client representation'
                    })
            
            # Check for business conflicts
            business_conflicts = self._analyze_business_conflicts(existing_relationships, new_client_id)
            conflicts_detected.extend(business_conflicts)
            
            # Determine if representation can proceed
            can_represent = len(conflicts_detected) == 0
            requires_waiver = False
            
            if conflicts_detected:
                # Check if conflicts can be waived
                waivable_conflicts = [c for c in conflicts_detected if c['type'] != 'direct_conflict']
                requires_waiver = len(waivable_conflicts) == len(conflicts_detected)
                can_represent = requires_waiver
            
            conflict_result = {
                'conflict_check_id': conflict_check_id,
                'attorney_id': attorney_id,
                'new_client_id': new_client_id,
                'can_represent': can_represent,
                'requires_waiver': requires_waiver,
                'conflicts_detected': conflicts_detected,
                'check_date': datetime.now().isoformat(),
                'matter_description': matter_description
            }
            
            # Log conflict check
            self._log_privilege_access(
                attorney_id=attorney_id,
                client_id=new_client_id,
                action='conflict_check_performed',
                details=f'Conflict check {conflict_check_id}: {len(conflicts_detected)} conflicts detected'
            )
            
            return conflict_result
            
        except Exception as e:
            logger.error(f"Failed to check conflicts of interest: {str(e)}")
            return {
                'can_represent': False,
                'reason': f'Conflict check failed: {str(e)}'
            }
    
    def generate_privilege_report(self, attorney_id: str, client_id: str = None,
                                start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """Generate comprehensive privilege protection report"""
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Filter access logs
            relevant_logs = []
            for log_entry in self.access_log:
                log_date = datetime.fromisoformat(log_entry['timestamp'])
                if start_date <= log_date <= end_date:
                    if attorney_id == log_entry.get('attorney_id'):
                        if not client_id or client_id == log_entry.get('client_id'):
                            relevant_logs.append(log_entry)
            
            # Analyze privilege activities
            privilege_report = {
                'report_id': str(uuid.uuid4()),
                'attorney_id': attorney_id,
                'client_id': client_id,
                'report_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'privilege_activities': {
                    'total_access_events': len(relevant_logs),
                    'privileged_communications': len([log for log in relevant_logs if 'communication' in log['action']]),
                    'session_activities': len([log for log in relevant_logs if 'session' in log['action']]),
                    'conflict_checks': len([log for log in relevant_logs if 'conflict' in log['action']]),
                    'privilege_violations': len([log for log in relevant_logs if log['event_type'] == 'violation'])
                },
                'compliance_summary': self._generate_compliance_summary(relevant_logs),
                'privilege_protection_score': self._calculate_privilege_protection_score(relevant_logs),
                'recommendations': self._generate_privilege_recommendations(relevant_logs),
                'generated_at': datetime.now().isoformat()
            }
            
            return privilege_report
            
        except Exception as e:
            logger.error(f"Failed to generate privilege report: {str(e)}")
            return {'error': f'Report generation failed: {str(e)}'}
    
    def _generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def _update_session_activity(self, session_id: str):
        """Update session last activity timestamp"""
        if session_id in self.session_store:
            self.session_store[session_id]['last_activity'] = datetime.now()
            
            # Update encrypted session data
            encrypted_data = self.session_store[session_id]['encrypted_data']
            decrypted_data = self.decrypt_privileged_data(encrypted_data)
            session_data = json.loads(decrypted_data)
            session_data['last_activity'] = datetime.now().isoformat()
            session_data['access_count'] = session_data.get('access_count', 0) + 1
            
            # Re-encrypt updated data
            self.session_store[session_id]['encrypted_data'] = self.encrypt_privileged_data(
                json.dumps(session_data)
            )
    
    def _invalidate_session(self, session_id: str):
        """Invalidate an expired or compromised session"""
        if session_id in self.session_store:
            session_info = self.session_store[session_id]
            
            # Log session invalidation
            self._log_privilege_access(
                attorney_id=session_info.get('attorney_id'),
                client_id=session_info.get('client_id'),
                action='session_invalidated',
                session_id=session_id,
                details='Session invalidated due to expiration or security concern'
            )
            
            # Remove from session store
            del self.session_store[session_id]
    
    def _calculate_integrity_hash(self, data: str) -> str:
        """Calculate integrity hash for data verification"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _log_privilege_access(self, attorney_id: str, client_id: str = None,
                            action: str = '', session_id: str = None,
                            details: str = '', **kwargs):
        """Log privilege-related access event"""
        log_entry = {
            'log_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'event_type': 'access',
            'attorney_id': attorney_id,
            'client_id': client_id,
            'session_id': session_id,
            'action': action,
            'details': details,
            'ip_address': kwargs.get('ip_address'),
            'user_agent': kwargs.get('user_agent'),
            'privilege_level': kwargs.get('privilege_level', 'standard')
        }
        
        self.access_log.append(log_entry)
        logger.info(f"Privilege access logged: {action} by attorney {attorney_id}")
    
    def _log_privilege_violation(self, attorney_id: str, client_id: str = None,
                               violation_type: str = '', details: str = '', **kwargs):
        """Log privilege violation event"""
        violation_entry = {
            'log_id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'event_type': 'violation',
            'violation_type': violation_type,
            'attorney_id': attorney_id,
            'client_id': client_id,
            'details': details,
            'ip_address': kwargs.get('ip_address'),
            'user_agent': kwargs.get('user_agent'),
            'severity': kwargs.get('severity', 'high')
        }
        
        self.access_log.append(violation_entry)
        logger.warning(f"Privilege violation logged: {violation_type} by attorney {attorney_id}")
    
    def _get_attorney_relationships(self, attorney_id: str) -> List[Dict[str, Any]]:
        """Get existing attorney-client relationships for conflict checking"""
        # This would integrate with the legal database in production
        # For now, return mock data
        return [
            {
                'client_id': 'client_001',
                'matter_type': 'corporate_law',
                'status': 'active',
                'company_name': 'TechCorp Inc.'
            },
            {
                'client_id': 'client_002', 
                'matter_type': 'employment_law',
                'status': 'active',
                'company_name': 'DataSystems LLC'
            }
        ]
    
    def _analyze_direct_conflict(self, existing_relationship: Dict[str, Any],
                               new_client_id: str, matter_description: str) -> bool:
        """Analyze for direct conflicts of interest"""
        # Simplified conflict analysis - would be more sophisticated in production
        if existing_relationship['client_id'] == new_client_id:
            return False  # Same client is not a conflict
        
        # Check for opposing party scenarios
        if 'litigation' in matter_description.lower():
            # More complex logic would analyze if clients are on opposing sides
            return False
        
        return False
    
    def _analyze_business_conflicts(self, existing_relationships: List[Dict[str, Any]],
                                  new_client_id: str) -> List[Dict[str, Any]]:
        """Analyze for business conflicts of interest"""
        business_conflicts = []
        
        # This would include sophisticated business relationship analysis
        # For now, return empty list
        return business_conflicts
    
    def _generate_compliance_summary(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate compliance summary from access logs"""
        total_events = len(logs)
        violations = len([log for log in logs if log['event_type'] == 'violation'])
        
        compliance_score = ((total_events - violations) / max(total_events, 1)) * 100
        
        return {
            'total_events': total_events,
            'violations': violations,
            'compliance_score': round(compliance_score, 2),
            'compliance_level': 'excellent' if compliance_score >= 95 else 
                              'good' if compliance_score >= 85 else
                              'needs_improvement'
        }
    
    def _calculate_privilege_protection_score(self, logs: List[Dict[str, Any]]) -> int:
        """Calculate privilege protection effectiveness score"""
        if not logs:
            return 100
        
        violations = len([log for log in logs if log['event_type'] == 'violation'])
        total_events = len(logs)
        
        protection_score = max(0, min(100, int(((total_events - violations) / total_events) * 100)))
        return protection_score
    
    def _generate_privilege_recommendations(self, logs: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations for privilege protection improvement"""
        recommendations = []
        
        violations = [log for log in logs if log['event_type'] == 'violation']
        
        if violations:
            recommendations.append(f"Review and address {len(violations)} privilege violations")
        
        if len(logs) > 100:
            recommendations.append("Consider implementing additional access monitoring")
        
        recommendations.extend([
            "Conduct regular privilege protection training",
            "Review and update conflict checking procedures",
            "Implement regular privilege protection audits"
        ])
        
        return recommendations
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_info in self.session_store.items():
            try:
                encrypted_data = session_info['encrypted_data']
                decrypted_data = self.decrypt_privileged_data(encrypted_data)
                session_data = json.loads(decrypted_data)
                
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if current_time > expires_at:
                    expired_sessions.append(session_id)
                    
            except Exception as e:
                logger.error(f"Error checking session expiration: {str(e)}")
                expired_sessions.append(session_id)  # Remove problematic sessions
        
        # Remove expired sessions
        for session_id in expired_sessions:
            self._invalidate_session(session_id)
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_privilege_status(self, attorney_id: str, client_id: str) -> Dict[str, Any]:
        """Get current privilege protection status"""
        try:
            # Count recent activities
            recent_logs = [
                log for log in self.access_log 
                if (log.get('attorney_id') == attorney_id and 
                    log.get('client_id') == client_id and
                    datetime.fromisoformat(log['timestamp']) > datetime.now() - timedelta(days=7))
            ]
            
            status = {
                'attorney_id': attorney_id,
                'client_id': client_id,
                'privilege_status': 'active',
                'recent_activities': len(recent_logs),
                'last_activity': max([log['timestamp'] for log in recent_logs]) if recent_logs else None,
                'protection_level': 'full_privilege',
                'compliance_status': 'compliant',
                'active_sessions': len([
                    session for session in self.session_store.values()
                    if session['attorney_id'] == attorney_id and session.get('client_id') == client_id
                ])
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get privilege status: {str(e)}")
            return {'error': f'Status check failed: {str(e)}'}
    
    def health_check(self) -> bool:
        """Check if privilege protection system is functioning"""
        try:
            # Test encryption/decryption
            test_data = "privilege protection test"
            encrypted = self.encrypt_privileged_data(test_data)
            decrypted = self.decrypt_privileged_data(encrypted)
            
            if decrypted != test_data:
                return False
            
            # Clean up expired sessions
            self.cleanup_expired_sessions()
            
            return True
            
        except Exception as e:
            logger.error(f"Privilege protection health check failed: {str(e)}")
            return False