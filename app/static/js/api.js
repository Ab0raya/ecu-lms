/**
 * ECU LMS API Service Client
 */
const API = {
  getBaseUrl() {
    const custom = localStorage.getItem('ecu_api_server');
    if (custom) return custom.replace(/\/$/, '');
    if (window.location.protocol === 'capacitor:' || window.location.protocol === 'file:' || !window.location.host) {
      return 'http://192.168.100.4:8000';
    }
    return '';
  },

  getHeaders() {
    const session = localStorage.getItem('ecu_moodle_session');
    const headers = { 'Content-Type': 'application/json' };
    if (session) {
      headers['X-Moodle-Session'] = session;
    }
    return headers;
  },

  async getMe() {
    try {
      const res = await fetch(`${this.getBaseUrl()}/api/auth/me`, { headers: this.getHeaders() });
      return await res.json();
    } catch (e) {
      console.error('Error fetching user profile', e);
      return { authenticated: false };
    }
  },

  async setSession(moodleSession, name = null) {
    const res = await fetch(`${this.getBaseUrl()}/api/auth/session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ moodle_session: moodleSession, name: name })
    });
    return await res.json();
  },

  async getCourses() {
    const res = await fetch(`${this.getBaseUrl()}/api/courses`, { headers: this.getHeaders() });
    if (!res.ok) throw new Error('Failed to load courses');
    return await res.json();
  },

  async getCourseDetail(courseId) {
    const res = await fetch(`${this.getBaseUrl()}/api/courses/${courseId}`, { headers: this.getHeaders() });
    if (!res.ok) throw new Error('Failed to load course details');
    return await res.json();
  },

  async getAssignments() {
    const res = await fetch(`${this.getBaseUrl()}/api/assignments`, { headers: this.getHeaders() });
    if (!res.ok) throw new Error('Failed to load assignments');
    return await res.json();
  },

  async getGrades(courseId) {
    const res = await fetch(`${this.getBaseUrl()}/api/grades/${courseId}`, { headers: this.getHeaders() });
    if (!res.ok) return null;
    return await res.json();
  },

  async logout() {
    await fetch(`${this.getBaseUrl()}/api/auth/logout`, { method: 'POST' });
    localStorage.removeItem('ecu_moodle_session');
  }
};
