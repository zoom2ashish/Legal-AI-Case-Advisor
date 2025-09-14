#!/usr/bin/env python3
"""
Fix Database Schema Issues
Recreates the database with proper schema if there are column issues
"""

import os
import sys
import logging

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.sqlite_legal_manager import LegalDataManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database():
    """Fix database schema issues by recreating with proper structure"""
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'legal_data.db')
        
        # Remove existing database if it exists
        if os.path.exists(db_path):
            logger.info("Removing existing database to fix schema issues...")
            os.remove(db_path)
        
        # Create new database with proper schema
        logger.info("Creating new database with proper schema...")
        db_manager = LegalDataManager(db_path)
        
        # Test database creation
        logger.info("Testing database functionality...")
        
        # Test case law table
        test_case = {
            'case_law_id': 'test_case_001',
            'case_name': 'Test Case',
            'citation': 'Test Citation',
            'court': 'Test Court',
            'jurisdiction': 'federal',
            'decision_date': '2024-01-01',
            'judge_name': 'Test Judge',
            'legal_issues': '["Test Issue"]',
            'holding': 'Test holding',
            'key_facts': 'Test facts',
            'legal_reasoning': 'Test reasoning',
            'precedent_type': 'binding',
            'citation_count': 100,
            'relevance_keywords': '["test"]',
            'practice_areas': '["Test Law"]',
            'summary': 'Test summary'
        }
        
        db_manager.conn.execute('''
            INSERT INTO case_law 
            (case_law_id, case_name, citation, court, jurisdiction, decision_date, judge_name,
             legal_issues, holding, key_facts, legal_reasoning, precedent_type, citation_count,
             relevance_keywords, practice_areas, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_case['case_law_id'], test_case['case_name'], test_case['citation'], test_case['court'],
            test_case['jurisdiction'], test_case['decision_date'], test_case['judge_name'],
            test_case['legal_issues'], test_case['holding'], test_case['key_facts'], test_case['legal_reasoning'],
            test_case['precedent_type'], test_case['citation_count'], test_case['relevance_keywords'],
            test_case['practice_areas'], test_case['summary']
        ))
        
        # Test statutes table
        test_statute = {
            'statute_id': 'test_stat_001',
            'title': 'Test Statute',
            'citation': 'Test Citation',
            'jurisdiction': 'federal',
            'chapter': '1',
            'section': '1',
            'effective_date': '2024-01-01',
            'statute_text': 'Test statute text',
            'summary': 'Test summary',
            'keywords': '["test"]',
            'practice_areas': '["Test Law"]',
            'related_regulations': '["Test Reg"]'
        }
        
        db_manager.conn.execute('''
            INSERT INTO statutes 
            (statute_id, title, citation, jurisdiction, chapter, section, effective_date,
             statute_text, summary, keywords, practice_areas, related_regulations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_statute['statute_id'], test_statute['title'], test_statute['citation'], test_statute['jurisdiction'],
            test_statute['chapter'], test_statute['section'], test_statute['effective_date'], test_statute['statute_text'],
            test_statute['summary'], test_statute['keywords'], test_statute['practice_areas'], test_statute['related_regulations']
        ))
        
        # Test precedents table
        test_precedent = {
            'precedent_id': 'test_prec_001',
            'case_law_id': 'test_case_001',
            'legal_principle': 'Test Principle',
            'precedent_weight': 5,
            'binding_authority': 'Test Court',
            'jurisdiction': 'federal',
            'practice_area': 'Test Law',
            'fact_pattern': 'Test facts',
            'legal_standard': 'Test standard',
            'exceptions': '["Test exception"]',
            'related_precedents': '["Test precedent"]'
        }
        
        db_manager.conn.execute('''
            INSERT INTO legal_precedents 
            (precedent_id, case_law_id, legal_principle, precedent_weight, binding_authority,
             jurisdiction, practice_area, fact_pattern, legal_standard, exceptions, related_precedents)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_precedent['precedent_id'], test_precedent['case_law_id'], test_precedent['legal_principle'],
            test_precedent['precedent_weight'], test_precedent['binding_authority'], test_precedent['jurisdiction'],
            test_precedent['practice_area'], test_precedent['fact_pattern'], test_precedent['legal_standard'],
            test_precedent['exceptions'], test_precedent['related_precedents']
        ))
        
        db_manager.conn.commit()
        
        logger.info("✅ Database schema test successful!")
        logger.info("All tables created with correct column names:")
        logger.info("- case_law.practice_areas (plural)")
        logger.info("- statutes.practice_areas (plural)")
        logger.info("- legal_precedents.practice_area (singular)")
        
        # Clean up test data
        db_manager.conn.execute("DELETE FROM case_law WHERE case_law_id = 'test_case_001'")
        db_manager.conn.execute("DELETE FROM statutes WHERE statute_id = 'test_stat_001'")
        db_manager.conn.execute("DELETE FROM legal_precedents WHERE precedent_id = 'test_prec_001'")
        db_manager.conn.commit()
        
        db_manager.close()
        
        logger.info("🎉 Database fixed successfully! You can now run the seeding script.")
        
    except Exception as e:
        logger.error(f"❌ Database fix failed: {str(e)}")
        raise

if __name__ == '__main__':
    fix_database()
