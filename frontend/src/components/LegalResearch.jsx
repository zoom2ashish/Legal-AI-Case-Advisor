import React, { useState, useEffect } from 'react';
import './LegalResearch.css';

const LegalResearch = () => {
  const [query, setQuery] = useState('');
  const [jurisdiction, setJurisdiction] = useState('federal');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [session, setSession] = useState(null);
  const [attorneyId, setAttorneyId] = useState('att_001'); // Default for demo

  // Initialize attorney session on component mount
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/attorney/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attorney_id: attorneyId
        }),
      });

      const data = await response.json();
      if (data.success) {
        setSession(data.session);
      }
    } catch (err) {
      console.error('Failed to initialize session:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:5001/api/legal-research', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          jurisdiction: jurisdiction,
          attorney_id: attorneyId,
          session_id: session?.session_id,
          session_token: session?.session_token
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        setResults(data.research_result);
      } else {
        setError(data.error || 'Research failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatCitation = (citation) => {
    return citation || 'No citation available';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Date unknown';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="legal-research">
      <div className="research-header">
        <h1>⚖️ Legal AI Research</h1>
        <p>Powered by AI for comprehensive legal analysis</p>
      </div>

      <form onSubmit={handleSearch} className="research-form">
        <div className="search-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your legal research query (e.g., 'Miranda rights in criminal cases')"
            className="search-input"
            disabled={loading}
          />
          <select
            value={jurisdiction}
            onChange={(e) => setJurisdiction(e.target.value)}
            className="jurisdiction-select"
            disabled={loading}
          >
            <option value="federal">Federal</option>
            <option value="california">California</option>
            <option value="new_york">New York</option>
            <option value="texas">Texas</option>
          </select>
          <button 
            type="submit" 
            className="search-button"
            disabled={loading || !query.trim()}
          >
            {loading ? 'Researching...' : 'Search'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          <h3>❌ Error</h3>
          <p>{error}</p>
        </div>
      )}

      {results && (
        <div className="research-results">
          <div className="results-header">
            <h2>Research Results</h2>
            <div className="results-summary">
              <span className="total-results">
                {results.total_results} results found
              </span>
              <span className="confidence-score">
                Confidence: {Math.round(results.confidence_score * 100)}%
              </span>
              <span className="processing-time">
                Processed in {results.processing_time_seconds?.toFixed(2)}s
              </span>
            </div>
          </div>

          {/* AI Analysis */}
          {results.ai_analysis && (
            <div className="ai-analysis">
              <h3>🤖 AI Legal Analysis</h3>
              <div className="analysis-type">
                Analysis Type: {results.ai_analysis.analysis_type === 'ai_generated' ? 'AI Generated' : 'Database Only'}
              </div>
              
              {results.ai_analysis.key_legal_principles && (
                <div className="analysis-section">
                  <h4>Key Legal Principles</h4>
                  <ul>
                    {results.ai_analysis.key_legal_principles.map((principle, index) => (
                      <li key={index}>{principle}</li>
                    ))}
                  </ul>
                </div>
              )}

              {results.ai_analysis.strategic_recommendations && (
                <div className="analysis-section">
                  <h4>Strategic Recommendations</h4>
                  <ul>
                    {results.ai_analysis.strategic_recommendations.map((recommendation, index) => (
                      <li key={index}>{recommendation}</li>
                    ))}
                  </ul>
                </div>
              )}

              {results.ai_analysis.risk_assessment && (
                <div className="analysis-section">
                  <h4>Risk Assessment</h4>
                  <p>{results.ai_analysis.risk_assessment}</p>
                </div>
              )}

              {/* Disclaimers */}
              {results.ai_analysis.disclaimers && (
                <div className="disclaimers">
                  <h4>⚠️ Important Disclaimers</h4>
                  <ul>
                    {results.ai_analysis.disclaimers.map((disclaimer, index) => (
                      <li key={index}>{disclaimer}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Case Law Results */}
          {results.case_law_results && results.case_law_results.length > 0 && (
            <div className="case-law-results">
              <h3>📚 Case Law</h3>
              {results.case_law_results.map((case_law, index) => (
                <div key={index} className="case-card">
                  <div className="case-header">
                    <h4>{case_law.case_name}</h4>
                    <span className="citation">{formatCitation(case_law.citation)}</span>
                  </div>
                  <div className="case-details">
                    <p><strong>Court:</strong> {case_law.court}</p>
                    <p><strong>Date:</strong> {formatDate(case_law.decision_date)}</p>
                    <p><strong>Judge:</strong> {case_law.judge_name}</p>
                    {case_law.citation_count && (
                      <p><strong>Citations:</strong> {case_law.citation_count}</p>
                    )}
                  </div>
                  {case_law.holding && (
                    <div className="case-holding">
                      <strong>Holding:</strong> {case_law.holding}
                    </div>
                  )}
                  {case_law.summary && (
                    <div className="case-summary">
                      <strong>Summary:</strong> {case_law.summary}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Statute Results */}
          {results.statute_results && results.statute_results.length > 0 && (
            <div className="statute-results">
              <h3>📖 Statutes</h3>
              {results.statute_results.map((statute, index) => (
                <div key={index} className="statute-card">
                  <div className="statute-header">
                    <h4>{statute.title}</h4>
                    <span className="citation">{formatCitation(statute.citation)}</span>
                  </div>
                  <div className="statute-details">
                    <p><strong>Jurisdiction:</strong> {statute.jurisdiction}</p>
                    <p><strong>Effective Date:</strong> {formatDate(statute.effective_date)}</p>
                  </div>
                  {statute.summary && (
                    <div className="statute-summary">
                      <strong>Summary:</strong> {statute.summary}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Precedent Results */}
          {results.precedent_results && results.precedent_results.length > 0 && (
            <div className="precedent-results">
              <h3>⚖️ Legal Precedents</h3>
              {results.precedent_results.map((precedent, index) => (
                <div key={index} className="precedent-card">
                  <div className="precedent-header">
                    <h4>{precedent.legal_principle}</h4>
                    <span className="precedent-weight">
                      Weight: {precedent.precedent_weight}/10
                    </span>
                  </div>
                  <div className="precedent-details">
                    <p><strong>Authority:</strong> {precedent.binding_authority}</p>
                    <p><strong>Jurisdiction:</strong> {precedent.jurisdiction}</p>
                    <p><strong>Practice Area:</strong> {precedent.practice_area}</p>
                  </div>
                  {precedent.legal_standard && (
                    <div className="precedent-standard">
                      <strong>Legal Standard:</strong> {precedent.legal_standard}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LegalResearch;
