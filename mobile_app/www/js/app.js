/**
 * ECU LMS Mobile App UI Controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  initApp();
});

async function initApp() {
  setupTabs();
  setupSearch();
  setupModals();
  registerServiceWorker();

  await loadInitialData();
}

function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(err => {
      console.log('SW registration note:', err);
    });
  }
}

async function loadInitialData() {
  showLoader(true);
  try {
    const authData = await API.getMe();
    if (authData && authData.user) {
      Store.setState({ user: authData.user, isConnected: authData.authenticated });
      updateUserUI(authData.user);
    }

    const [courses, assignments] = await Promise.all([
      API.getCourses().catch(() => []),
      API.getAssignments().catch(() => [])
    ]);

    Store.setState({ courses, assignments });
    renderCourses(courses);
    renderAssignments(assignments);
    updateStats(courses, assignments);
  } catch (err) {
    showToast('Offline or connecting to server...', 'info');
  } finally {
    showLoader(false);
  }
}

/* User & Stats Rendering */
function updateUserUI(user) {
  const nameEl = document.getElementById('studentName');
  const roleEl = document.getElementById('studentRole');
  const avatarEl = document.getElementById('studentAvatar');
  const syncBtn = document.getElementById('syncStatusBtn');

  if (nameEl && user) nameEl.textContent = user.name || 'ECU Student';
  if (roleEl && user) roleEl.textContent = `${user.faculty || 'Engineering'} • ${user.role || 'Student'}`;
  if (avatarEl && user && user.avatar_url) avatarEl.src = user.avatar_url;

  const demoBanner = document.getElementById('demoNoticeBanner');
  const sessionToken = localStorage.getItem('ecu_moodle_session');
  const isRealSession = sessionToken && sessionToken !== 'demo_active_session_ecu';

  if (demoBanner) {
    demoBanner.style.display = isRealSession ? 'none' : 'flex';
  }

  if (syncBtn) {
    if (isRealSession && Store.state.isConnected) {
      syncBtn.className = 'sync-status-btn';
      syncBtn.innerHTML = '<span class="pulse-dot"></span><span>Live ECU Synced</span>';
    } else {
      syncBtn.className = 'sync-status-btn disconnected';
      syncBtn.innerHTML = '<span class="pulse-dot"></span><span>وضع تجريبي (Connect)</span>';
    }
  }
}

function updateStats(courses, assignments) {
  const courseCountEl = document.getElementById('statCoursesCount');
  const pendingCountEl = document.getElementById('statPendingCount');
  const gpaEl = document.getElementById('statGpa');

  if (courseCountEl) courseCountEl.textContent = courses.length || '0';
  if (pendingCountEl) {
    const pending = assignments.filter(a => a.status === 'pending').length;
    pendingCountEl.textContent = pending || '0';
  }
  if (gpaEl) gpaEl.textContent = '3.82';
}

/* Tab Navigation */
function setupTabs() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const tab = item.getAttribute('data-tab');
      if (!tab) return;

      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      document.querySelectorAll('.tab-view').forEach(view => view.style.display = 'none');
      const targetView = document.getElementById(`tab-${tab}`);
      if (targetView) targetView.style.display = 'block';

      Store.setState({ currentTab: tab });

      if (tab === 'grades') {
        renderGradesTab();
      } else if (tab === 'profile') {
        renderProfileTab();
      }
    });
  });
}

/* Search Filtering */
function setupSearch() {
  const searchInput = document.getElementById('courseSearchInput');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const filtered = Store.state.courses.filter(c => 
      c.name.toLowerCase().includes(query) || (c.code && c.code.toLowerCase().includes(query))
    );
    renderCourses(filtered);
  });
}

/* Courses Rendering */
function renderCourses(courses) {
  const container = document.getElementById('coursesContainer');
  if (!container) return;

  if (!courses || courses.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px 10px; color: var(--text-dim);">
        <p style="font-size: 1.8rem; margin-bottom: 8px;">📚</p>
        <p style="font-weight: 600; color: var(--text-muted);">No courses found</p>
        <p style="font-size: 0.8rem; margin-top: 4px;">Sync your ECU LMS session to load active courses.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = courses.map(course => {
    return `
      <div class="course-card" onclick="openCourseDetail('${course.id}')" id="course-card-${course.id}">
        <div class="course-top">
          <span class="course-code-tag">${course.code || 'COURSE'}</span>
          <span class="course-term">${course.term || 'Spring 2026'}</span>
        </div>
        <h3 class="course-title">${escapeHtml(course.name)}</h3>
        <p class="course-instructor">
          <span>👨‍🏫</span>
          <span>${course.instructor || 'Faculty Staff'}</span>
        </p>
        <div class="progress-container">
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: ${course.progress || 0}%"></div>
          </div>
          <span class="progress-text">${course.progress || 0}%</span>
        </div>
      </div>
    `;
  }).join('');
}

/* Course Detail Sheet */
async function openCourseDetail(courseId) {
  const modal = document.getElementById('courseDetailModal');
  const titleEl = document.getElementById('detailCourseTitle');
  const bodyEl = document.getElementById('detailCourseBody');
  
  if (!modal || !bodyEl) return;

  titleEl.textContent = 'Loading Course...';
  bodyEl.innerHTML = '<div style="text-align: center; padding: 30px;"><span class="pulse-dot"></span> Loading lecture topics...</div>';
  modal.classList.add('open');

  try {
    const detail = await API.getCourseDetail(courseId);
    titleEl.textContent = detail.name || 'Course Content';

    if (!detail.sections || detail.sections.length === 0) {
      bodyEl.innerHTML = '<p style="text-align: center; color: var(--text-dim); padding: 20px;">No materials posted yet in this course.</p>';
      return;
    }

    let html = '';

    // Announcements if any
    if (detail.announcements && detail.announcements.length > 0) {
      html += `
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: var(--radius-md); padding: 12px; margin-bottom: 14px;">
          <div style="font-weight: 700; font-size: 0.85rem; color: var(--accent-amber); margin-bottom: 4px;">📢 Notice</div>
          <div style="font-size: 0.8rem; color: #fff;">${escapeHtml(detail.announcements[0].name)}</div>
        </div>
      `;
    }

    // Sections & Lectures
    html += detail.sections.map((section, sIdx) => {
      return `
        <div class="section-accordion">
          <div class="accordion-header" onclick="toggleSectionAccordion(this)">
            <span>${escapeHtml(section.title)}</span>
            <span style="font-size: 0.75rem; color: var(--text-dim);">▼</span>
          </div>
          <div class="accordion-body">
            ${section.summary ? `<p style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 6px;">${escapeHtml(section.summary)}</p>` : ''}
            ${section.items && section.items.length > 0 ? section.items.map(item => `
              <div class="resource-file-row">
                <div class="file-left">
                  <div class="file-icon-badge ${item.type === 'pdf' ? 'badge-pdf' : (item.type === 'assignment' ? 'badge-assign' : 'badge-link')}">
                    ${item.type.toUpperCase()}
                  </div>
                  <div class="file-details">
                    <div class="file-name" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>
                    <div class="file-sub">${item.file_size ? `${item.file_size} • ` : ''}${item.info || 'Course Material'}</div>
                  </div>
                </div>
                <div>
                  ${item.download_url ? `
                    <a href="${item.download_url}" class="download-icon-btn" title="Download Material">
                      ⬇
                    </a>
                  ` : `
                    <a href="${item.url}" target="_blank" class="download-icon-btn" title="Open Link">
                      ↗
                    </a>
                  `}
                </div>
              </div>
            `).join('') : '<p style="font-size: 0.75rem; color: var(--text-dim);">No items in this section.</p>'}
          </div>
        </div>
      `;
    }).join('');

    bodyEl.innerHTML = html;
  } catch (err) {
    bodyEl.innerHTML = `<p style="color: var(--accent-rose); padding: 20px;">Failed to load course details: ${escapeHtml(err.message)}</p>`;
  }
}

function toggleSectionAccordion(header) {
  const body = header.nextElementSibling;
  const arrow = header.querySelector('span:last-child');
  if (body.style.display === 'none') {
    body.style.display = 'flex';
    arrow.textContent = '▼';
  } else {
    body.style.display = 'none';
    arrow.textContent = '▶';
  }
}

/* Assignments Rendering */
function renderAssignments(assignments) {
  const container = document.getElementById('assignmentsContainer');
  if (!container) return;

  if (!assignments || assignments.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px 10px; color: var(--text-dim);">
        <p style="font-size: 1.8rem; margin-bottom: 8px;">🎉</p>
        <p style="font-weight: 600; color: var(--text-muted);">No upcoming deadlines</p>
        <p style="font-size: 0.8rem; margin-top: 4px;">You are all caught up with your submissions!</p>
      </div>
    `;
    return;
  }

  container.innerHTML = assignments.map(a => {
    const isSubmitted = a.status === 'submitted';
    return `
      <div class="assignment-card">
        <div class="assignment-top">
          <span class="assignment-course">${escapeHtml(a.course_code || a.course_name)}</span>
          <span class="status-badge ${isSubmitted ? 'status-submitted' : 'status-pending'}">
            ${isSubmitted ? 'Submitted' : 'Pending'}
          </span>
        </div>
        <h4 class="assignment-title">${escapeHtml(a.title)}</h4>
        ${a.description ? `<p class="assignment-desc">${escapeHtml(a.description)}</p>` : ''}
        <div class="assignment-bottom">
          <span class="due-countdown">
            ${isSubmitted ? `⭐ Grade: ${a.grade || 'Graded'}` : `⏰ Due: ${a.due_date}`}
          </span>
          <a href="${a.submission_url}" target="_blank" style="color: var(--primary-light); text-decoration: none; font-weight: 600;">
            ${isSubmitted ? 'Review ↗' : 'Submit ↗'}
          </a>
        </div>
      </div>
    `;
  }).join('');
}

/* Grades Tab Rendering */
async function renderGradesTab() {
  const container = document.getElementById('gradesContainer');
  if (!container) return;

  container.innerHTML = '<div style="text-align: center; padding: 30px;"><span class="pulse-dot"></span> Loading Academic Records...</div>';

  const courses = Store.state.courses;
  if (!courses || courses.length === 0) {
    container.innerHTML = '<p style="text-align: center; color: var(--text-dim); padding: 20px;">No courses available for grades.</p>';
    return;
  }

  let html = `
    <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(6, 182, 212, 0.1)); border: 1px solid var(--border-primary); border-radius: var(--radius-lg); padding: 18px; margin-bottom: 20px; text-align: center;">
      <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--primary-light); font-weight: 700; letter-spacing: 0.05em;">Cumulative GPA</div>
      <div style="font-family: var(--font-heading); font-size: 2.4rem; font-weight: 800; color: #fff; margin: 4px 0;">3.82 <span style="font-size: 1rem; color: var(--text-dim);">/ 4.0</span></div>
      <div style="font-size: 0.8rem; color: var(--accent-emerald); font-weight: 600;">Class Rank: Top 5% • Excellent Standing</div>
    </div>
  `;

  for (const c of courses.slice(0, 3)) {
    const gradeData = await API.getGrades(c.id).catch(() => null);
    if (gradeData) {
      html += `
        <div class="assignment-card" style="margin-bottom: 14px;">
          <div class="assignment-top">
            <span class="assignment-course">${escapeHtml(c.code || c.name)}</span>
            <span class="status-badge status-submitted" style="font-size: 0.8rem;">Grade: ${gradeData.letter_grade || 'A'} (${gradeData.total_grade})</span>
          </div>
          <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px;">
            ${gradeData.items.map(it => `
              <div style="display: flex; justify-content: space-between; font-size: 0.78rem; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color: var(--text-main);">${escapeHtml(it.item)}</span>
                <span style="color: var(--accent-cyan); font-weight: 600;">${it.grade}</span>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }
  }

  container.innerHTML = html;
}

/* Profile Tab Rendering */
function renderProfileTab() {
  const container = document.getElementById('profileContainer');
  if (!container) return;

  const user = Store.state.user || {};
  container.innerHTML = `
    <div style="text-align: center; padding: 20px 0;">
      <img src="${user.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid var(--primary); box-shadow: var(--shadow-glow); margin-bottom: 12px;" />
      <h3 style="font-family: var(--font-heading); font-size: 1.3rem; font-weight: 700; color: #fff;">${escapeHtml(user.name || 'Ahmed Mansour')}</h3>
      <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">${escapeHtml(user.email || 'student@ecu.edu.eg')}</p>
      <span class="badge-tag" style="margin-top: 8px; display: inline-block;">${user.role || 'Undergraduate'}</span>
    </div>

    <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 16px; margin-bottom: 18px;">
      <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-muted); margin-bottom: 12px; text-transform: uppercase;">Academic Profile</div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle); font-size: 0.85rem;">
        <span style="color: var(--text-dim);">University</span>
        <span style="color: #fff; font-weight: 600;">Egyptian Chinese University</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border-subtle); font-size: 0.85rem;">
        <span style="color: var(--text-dim);">Faculty</span>
        <span style="color: #fff; font-weight: 600;">Engineering & Technology</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.85rem;">
        <span style="color: var(--text-dim);">Academic Term</span>
        <span style="color: var(--accent-emerald); font-weight: 600;">Spring 2026 (Active)</span>
      </div>
    </div>

    <button class="btn-primary" onclick="openSyncModal()" style="margin-bottom: 10px;">
      🔄 Re-sync ECU LMS Session
    </button>
    <button class="btn-secondary" onclick="handleLogout()">
      Sign Out
    </button>
  `;
}

/* Modals Setup */
function setupModals() {
  const syncBtn = document.getElementById('syncStatusBtn');
  const syncModal = document.getElementById('syncModal');
  const courseModal = document.getElementById('courseDetailModal');

  if (syncBtn) {
    syncBtn.addEventListener('click', openSyncModal);
  }

  // Close modals on overlay click or close button
  document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('open');
    });
  });

  document.querySelectorAll('.sheet-close-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.modal-overlay');
      if (modal) modal.classList.remove('open');
    });
  });

  // Setup Sync Form submission
  const syncForm = document.getElementById('syncSessionForm');
  if (syncForm) {
    syncForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const tokenInput = document.getElementById('sessionCookieInput');
      const token = tokenInput ? tokenInput.value.trim() : '';

      if (!token) {
        showToast('Please enter your MoodleSession token', 'error');
        return;
      }

      showLoader(true);
      try {
        const res = await API.setSession(token);
        if (res.success) {
          localStorage.setItem('ecu_moodle_session', token);
          showToast('Connected to ECU LMS successfully!', 'success');
          document.getElementById('syncModal').classList.remove('open');
          await loadInitialData();
        } else {
          showToast(res.message || 'Verification failed', 'error');
        }
      } catch (err) {
        showToast('Failed to connect: ' + err.message, 'error');
      } finally {
        showLoader(false);
      }
    });
  }
}

function openSyncModal() {
  const modal = document.getElementById('syncModal');
  if (modal) {
    modal.classList.add('open');
    const serverInput = document.getElementById('serverUrlInput');
    if (serverInput) {
      serverInput.value = localStorage.getItem('ecu_api_server') || '';
    }
  }
}

function saveServerUrl() {
  const serverInput = document.getElementById('serverUrlInput');
  if (!serverInput) return;
  const val = serverInput.value.trim();
  if (val) {
    localStorage.setItem('ecu_api_server', val);
    showToast('Saved Cloud URL: ' + val, 'success');
  } else {
    localStorage.removeItem('ecu_api_server');
    showToast('Reset to local/default server', 'info');
  }
  loadInitialData();
}

function copyBookmarklet() {
  const code = `javascript:(function(){const m=document.cookie.match(/MoodleSession=([^;]+)/);if(m){navigator.clipboard.writeText(m[1]).then(()=>alert('Copied ECU MoodleSession: '+m[1]));}else{alert('Please log into lms.ecu.edu.eg first!');}})();`;
  navigator.clipboard.writeText(code).then(() => {
    showToast('Bookmarklet script copied to clipboard!', 'success');
  });
}

function applyDemoSession() {
  localStorage.setItem('ecu_moodle_session', 'demo_active_session_ecu');
  showToast('Demo Mode Activated with sample ECU courses!', 'success');
  document.getElementById('syncModal').classList.remove('open');
  loadInitialData();
}

async function handleLogout() {
  await API.logout();
  showToast('Logged out', 'info');
  loadInitialData();
}

/* Helpers */
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  const icon = type === 'success' ? '✅' : (type === 'error' ? '⚠️' : 'ℹ️');
  toast.innerHTML = `<span>${icon}</span><span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function showLoader(show) {
  // subtle visual indicator if needed
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
}
