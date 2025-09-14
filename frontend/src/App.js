import React, { useState } from 'react';
import LegalResearch from './components/LegalResearch';
import ClientPortal from './components/ClientPortal';
import CaseAnalysis from './components/CaseAnalysis';
import DocumentReview from './components/DocumentReview';
import PrecedentFinder from './components/PrecedentFinder';
import PrivilegeMonitor from './components/PrivilegeMonitor';
import './App.css';

function App() {
  const [activeView, setActiveView] = useState('research');
  const [userRole, setUserRole] = useState('attorney'); // 'attorney' or 'client'

  const handleRoleSwitch = (role) => {
    setUserRole(role);
    setActiveView(role === 'attorney' ? 'research' : 'overview');
  };

  const renderContent = () => {
    switch (activeView) {
      case 'research':
        return <LegalResearch />;
      case 'client':
        return <ClientPortal />;
      case 'cases':
        return <CaseAnalysis />;
      case 'documents':
        return <DocumentReview />;
      case 'precedents':
        return <PrecedentFinder />;
      case 'privilege':
        return <PrivilegeMonitor />;
      default:
        return <LegalResearch />;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="header-title">
            <h1>⚖️ Legal AI Case Advisor</h1>
            <p>AI-Powered Legal Research and Case Analysis</p>
          </div>
          
          <div className="role-selector">
            <button 
              className={`role-button ${userRole === 'attorney' ? 'active' : ''}`}
              onClick={() => handleRoleSwitch('attorney')}
            >
              👨‍💼 Attorney
            </button>
            <button 
              className={`role-button ${userRole === 'client' ? 'active' : ''}`}
              onClick={() => handleRoleSwitch('client')}
            >
              👤 Client
            </button>
          </div>
        </div>
      </header>

      {userRole === 'attorney' && (
        <nav className="App-nav">
          <button 
            className={`nav-button ${activeView === 'research' ? 'active' : ''}`}
            onClick={() => setActiveView('research')}
          >
            🔍 Legal Research
          </button>
          <button 
            className={`nav-button ${activeView === 'cases' ? 'active' : ''}`}
            onClick={() => setActiveView('cases')}
          >
            📊 Case Analysis
          </button>
          <button 
            className={`nav-button ${activeView === 'documents' ? 'active' : ''}`}
            onClick={() => setActiveView('documents')}
          >
            📄 Document Review
          </button>
          <button 
            className={`nav-button ${activeView === 'precedents' ? 'active' : ''}`}
            onClick={() => setActiveView('precedents')}
          >
            ⚖️ Precedent Finder
          </button>
          <button 
            className={`nav-button ${activeView === 'privilege' ? 'active' : ''}`}
            onClick={() => setActiveView('privilege')}
          >
            🔒 Privilege Monitor
          </button>
        </nav>
      )}

      <main className="App-main">
        {renderContent()}
      </main>

      <footer className="App-footer">
        <div className="footer-content">
          <p>&copy; 2024 Legal AI Case Advisor MVP. All rights reserved.</p>
          <div className="footer-disclaimer">
            <small>
              ⚠️ This system is for demonstration purposes. All legal research should be reviewed by qualified attorneys. 
              AI-generated content does not constitute legal advice.
            </small>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
