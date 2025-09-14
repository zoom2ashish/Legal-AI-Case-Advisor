import React, { useState, useEffect } from 'react';
import './ClientPortal.css';

const ClientPortal = () => {
  const [clientId] = useState('client_001'); // Default for demo
  const [session, setSession] = useState(null);
  const [caseSummaries, setCaseSummaries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // Initialize client session on component mount
  useEffect(() => {
    initializeSession();
    loadCaseSummaries();
  }, []);

  const initializeSession = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/attorney/session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attorney_id: 'att_001', // Default attorney for demo
          client_id: clientId
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

  const loadCaseSummaries = async () => {
    setLoading(true);
    try {
      // Mock case summaries for demo
      const mockSummaries = [
        {
          id: 'summary_001',
          case_title: 'Miranda Rights Case',
          status: 'Active',
          last_update: '2024-01-15',
          summary: 'Your case involves Miranda rights violations during police interrogation. The court has ruled that evidence obtained without proper Miranda warnings may be inadmissible.',
          next_steps: 'We are preparing a motion to suppress evidence obtained in violation of your Miranda rights.',
          attorney_notes: 'Strong case based on recent Supreme Court precedent.'
        },
        {
          id: 'summary_002',
          case_title: 'Employment Discrimination',
          status: 'Review',
          last_update: '2024-01-10',
          summary: 'Your employment discrimination case is under review. We have gathered evidence of discriminatory practices and are preparing for mediation.',
          next_steps: 'Mediation scheduled for February 15th. Please review the evidence package.',
          attorney_notes: 'Good documentation of discrimination patterns.'
        }
      ];
      setCaseSummaries(mockSummaries);
    } catch (err) {
      setError('Failed to load case summaries');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'active': return '#28a745';
      case 'review': return '#ffc107';
      case 'completed': return '#17a2b8';
      default: return '#6c757d';
    }
  };

  return (
    <div className="client-portal">
      <div className="portal-header">
        <h1>👤 Client Portal</h1>
        <p>Access your case information and communicate with your attorney</p>
      </div>

      <div className="portal-nav">
        <button 
          className={`nav-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`nav-button ${activeTab === 'cases' ? 'active' : ''}`}
          onClick={() => setActiveTab('cases')}
        >
          📁 Cases
        </button>
        <button 
          className={`nav-button ${activeTab === 'documents' ? 'active' : ''}`}
          onClick={() => setActiveTab('documents')}
        >
          📄 Documents
        </button>
        <button 
          className={`nav-button ${activeTab === 'contact' ? 'active' : ''}`}
          onClick={() => setActiveTab('contact')}
        >
          💬 Contact Attorney
        </button>
      </div>

      {error && (
        <div className="error-message">
          <h3>❌ Error</h3>
          <p>{error}</p>
        </div>
      )}

      <div className="portal-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="welcome-section">
              <h2>Welcome to Your Client Portal</h2>
              <p>Here you can access information about your legal cases, review case summaries, and communicate with your attorney.</p>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">📁</div>
                <div className="stat-number">{caseSummaries.length}</div>
                <div className="stat-label">Active Cases</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">⚖️</div>
                <div className="stat-number">2</div>
                <div className="stat-label">In Progress</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📅</div>
                <div className="stat-number">15</div>
                <div className="stat-label">Days Since Last Update</div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">✅</div>
                <div className="stat-number">100%</div>
                <div className="stat-label">Confidentiality Protected</div>
              </div>
            </div>

            <div className="recent-activity">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                {caseSummaries.slice(0, 3).map((summary) => (
                  <div key={summary.id} className="activity-item">
                    <div className="activity-icon">📋</div>
                    <div className="activity-content">
                      <h4>{summary.case_title}</h4>
                      <p>Updated {formatDate(summary.last_update)}</p>
                    </div>
                    <div className="activity-status">
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(summary.status) }}
                      >
                        {summary.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'cases' && (
          <div className="cases-tab">
            <h2>Your Cases</h2>
            {loading ? (
              <div className="loading">Loading cases...</div>
            ) : (
              <div className="cases-grid">
                {caseSummaries.map((summary) => (
                  <div key={summary.id} className="case-card">
                    <div className="case-header">
                      <h3>{summary.case_title}</h3>
                      <span 
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(summary.status) }}
                      >
                        {summary.status}
                      </span>
                    </div>
                    <div className="case-summary">
                      <p><strong>Case Summary:</strong></p>
                      <p>{summary.summary}</p>
                    </div>
                    <div className="case-next-steps">
                      <p><strong>Next Steps:</strong></p>
                      <p>{summary.next_steps}</p>
                    </div>
                    <div className="case-footer">
                      <span className="last-update">
                        Last updated: {formatDate(summary.last_update)}
                      </span>
                    </div>
                    <div className="disclaimer">
                      <small>
                        ⚠️ This summary is for informational purposes only and does not constitute legal advice. 
                        Please consult with your attorney for specific legal guidance.
                      </small>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="documents-tab">
            <h2>Document Center</h2>
            <div className="document-upload">
              <h3>Upload Documents</h3>
              <div className="upload-area">
                <input type="file" multiple accept=".pdf,.doc,.docx" />
                <p>Drag and drop files here or click to browse</p>
                <small>Supported formats: PDF, DOC, DOCX</small>
              </div>
            </div>

            <div className="document-list">
              <h3>Your Documents</h3>
              <div className="document-grid">
                <div className="document-item">
                  <div className="doc-icon">📄</div>
                  <div className="doc-info">
                    <h4>Case Evidence Package</h4>
                    <p>Uploaded: January 10, 2024</p>
                    <p>Status: Under Review</p>
                  </div>
                  <div className="doc-actions">
                    <button className="btn-secondary">Download</button>
                    <button className="btn-secondary">View</button>
                  </div>
                </div>
                <div className="document-item">
                  <div className="doc-icon">📋</div>
                  <div className="doc-info">
                    <h4>Mediation Agreement</h4>
                    <p>Uploaded: January 5, 2024</p>
                    <p>Status: Approved</p>
                  </div>
                  <div className="doc-actions">
                    <button className="btn-secondary">Download</button>
                    <button className="btn-secondary">View</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'contact' && (
          <div className="contact-tab">
            <h2>Contact Your Attorney</h2>
            <div className="contact-info">
              <div className="contact-card">
                <h3>📞 Contact Information</h3>
                <div className="contact-details">
                  <p><strong>Attorney:</strong> John Smith</p>
                  <p><strong>Firm:</strong> Smith & Associates</p>
                  <p><strong>Phone:</strong> (555) 123-4567</p>
                  <p><strong>Email:</strong> john.smith@smithlaw.com</p>
                </div>
              </div>
            </div>

            <div className="message-form">
              <h3>Send Message</h3>
              <form>
                <div className="form-group">
                  <label htmlFor="subject">Subject</label>
                  <input type="text" id="subject" placeholder="Brief subject line" />
                </div>
                <div className="form-group">
                  <label htmlFor="message">Message</label>
                  <textarea 
                    id="message" 
                    rows="6" 
                    placeholder="Type your message here. All communications are protected by attorney-client privilege."
                  ></textarea>
                </div>
                <div className="form-group">
                  <label>
                    <input type="checkbox" />
                    This is urgent and requires immediate attention
                  </label>
                </div>
                <button type="submit" className="btn-primary">
                  Send Secure Message
                </button>
              </form>
              <div className="security-notice">
                <p>🔒 All communications are encrypted and protected by attorney-client privilege.</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientPortal;
