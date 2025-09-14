// Legal research integration
const API_BASE_URL = 'http://localhost:5001';

export const legalAPI = {
  // Health check
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  },

  // Legal research
  async conductResearch(query, sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/legal/research`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        session_id: sessionId
      })
    });
    return response.json();
  },

  // Get research summary
  async getResearchSummary(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/legal/research/${sessionId}/summary`);
    return response.json();
  },

  // Create attorney session
  async createAttorneySession(attorneyId) {
    const response = await fetch(`${API_BASE_URL}/api/legal/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        attorney_id: attorneyId
      })
    });
    return response.json();
  },

  // Verify session
  async verifySession(sessionId) {
    const response = await fetch(`${API_BASE_URL}/api/legal/session/${sessionId}/verify`);
    return response.json();
  },

  // Get attorney history
  async getAttorneyHistory(attorneyId) {
    const response = await fetch(`${API_BASE_URL}/api/legal/attorney/${attorneyId}/history`);
    return response.json();
  }
};