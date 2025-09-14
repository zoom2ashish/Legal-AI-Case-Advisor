import React from 'react';
import LegalResearch from './components/LegalResearch';
import CaseAnalysis from './components/CaseAnalysis';
import DocumentReview from './components/DocumentReview';
import PrecedentFinder from './components/PrecedentFinder';
import PrivilegeMonitor from './components/PrivilegeMonitor';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Case Intelligence System</h1>
      </header>
      <main>
        <LegalResearch />
        <CaseAnalysis />
        <DocumentReview />
        <PrecedentFinder />
        <PrivilegeMonitor />
      </main>
    </div>
  );
}

export default App;
