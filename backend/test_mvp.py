#!/usr/bin/env python3
"""
MVP Test Script for Legal AI Case Advisor
Tests the core functionality of the MVP implementation
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.sqlite_legal_manager import LegalDataManager
from utils.legal_security import AttorneyClientPrivilegeManager
from agents.mvp_research_agent import MVPResearchAgent

def test_database_connection():
    """Test database connection and basic operations"""
    print("🔍 Testing Database Connection...")
    
    try:
        db_manager = LegalDataManager("./database/legal_data.db")
        
        # Test health check
        health = db_manager.health_check()
        print(f"✅ Database health check: {health}")
        
        # Test basic search
        results = db_manager.search_case_law("Miranda", limit=3)
        print(f"✅ Case law search returned {len(results)} results")
        
        if results:
            print(f"   Sample result: {results[0]['case_name']}")
        
        db_manager.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_security_manager():
    """Test attorney-client privilege manager"""
    print("\n🔒 Testing Security Manager...")
    
    try:
        privilege_manager = AttorneyClientPrivilegeManager()
        
        # Test health check
        health = privilege_manager.health_check()
        print(f"✅ Security manager health check: {health}")
        
        # Test session creation
        session = privilege_manager.create_secure_session("att_001", "client_001")
        print(f"✅ Session created: {session['session_id'][:8]}...")
        
        # Test session verification
        verification = privilege_manager.verify_privileged_access(
            session_id=session['session_id'],
            session_token=session['session_token'],
            attorney_id="att_001",
            client_id="client_001"
        )
        print(f"✅ Session verification: {verification['authorized']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security manager test failed: {str(e)}")
        return False

def test_research_agent():
    """Test MVP research agent"""
    print("\n🤖 Testing Research Agent...")
    
    try:
        db_manager = LegalDataManager("./database/legal_data.db")
        privilege_manager = AttorneyClientPrivilegeManager()
        research_agent = MVPResearchAgent(db_manager, privilege_manager)
        
        # Test health check
        health = research_agent.health_check()
        print(f"✅ Research agent health check: {health}")
        
        # Test legal research
        result = research_agent.conduct_legal_research(
            query="Miranda rights in criminal cases",
            jurisdiction="federal",
            attorney_id="att_001",
            client_id="client_001"
        )
        
        if 'error' not in result:
            print(f"✅ Research completed in {result['processing_time_seconds']:.2f}s")
            print(f"   Total results: {result['total_results']}")
            print(f"   Confidence: {result['confidence_score']:.2f}")
            print(f"   AI Analysis type: {result['ai_analysis']['analysis_type']}")
        else:
            print(f"❌ Research failed: {result['error']}")
            return False
        
        # Test summary generation
        summary = research_agent.get_research_summary(result)
        if 'error' not in summary:
            print(f"✅ Summary generated successfully")
            print(f"   Key findings: {len(summary['key_findings'])}")
        else:
            print(f"❌ Summary generation failed: {summary['error']}")
        
        db_manager.close()
        return True
        
    except Exception as e:
        print(f"❌ Research agent test failed: {str(e)}")
        return False

def test_flask_api():
    """Test Flask API endpoints"""
    print("\n🌐 Testing Flask API...")
    
    base_url = "http://localhost:5001"
    
    try:
        # Test health check endpoint
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check endpoint working")
            print(f"   Service: {data['service']}")
            print(f"   Database: {data['components']['database']}")
            print(f"   Privilege Manager: {data['components']['privilege_manager']}")
            print(f"   Research Agent: {data['components']['research_agent']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test legal research endpoint
        research_data = {
            "query": "Miranda rights in criminal cases",
            "jurisdiction": "federal",
            "attorney_id": "att_001"
        }
        
        response = requests.post(
            f"{base_url}/api/legal-research",
            json=research_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Legal research endpoint working")
            print(f"   Results: {data['research_result']['total_results']}")
            print(f"   Processing time: {data['research_result']['processing_time_seconds']:.2f}s")
        else:
            print(f"❌ Legal research endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test database stats endpoint
        response = requests.get(f"{base_url}/api/database/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database stats endpoint working")
            stats = data['stats']
            print(f"   Case Law: {stats.get('case_law_count', 0)}")
            print(f"   Statutes: {stats.get('statutes_count', 0)}")
            print(f"   Precedents: {stats.get('precedents_count', 0)}")
        else:
            print(f"❌ Database stats endpoint failed: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Flask API at {base_url}")
        print("   Make sure the Flask app is running: python app.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

def test_database_seeding():
    """Test database seeding with sample data"""
    print("\n🌱 Testing Database Seeding...")
    
    try:
        # Import and run the seeding script
        from seed_mvp_data import main as seed_main
        seed_main()
        print("✅ Database seeding completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database seeding failed: {str(e)}")
        return False

def main():
    """Run all MVP tests"""
    print("🚀 Legal AI Case Advisor MVP - Test Suite")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Database Seeding", test_database_seeding),
        ("Database Connection", test_database_connection),
        ("Security Manager", test_security_manager),
        ("Research Agent", test_research_agent),
        ("Flask API", test_flask_api),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
        
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MVP is ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
