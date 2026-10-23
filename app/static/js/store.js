/**
 * State store for ECU LMS Mobile App
 */
const Store = {
  state: {
    user: null,
    courses: [],
    assignments: [],
    selectedCourse: null,
    currentTab: 'courses',
    searchQuery: '',
    isLoading: false,
    isConnected: true
  },

  listeners: [],

  subscribe(fn) {
    this.listeners.push(fn);
  },

  notify() {
    this.listeners.forEach(fn => fn(this.state));
  },

  setState(updates) {
    this.state = { ...this.state, ...updates };
    this.notify();
  }
};
