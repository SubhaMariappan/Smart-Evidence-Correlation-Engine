/**
 * SECE — Unified Digital Forensics Workstation Main Application Engine
 * Implements 15-module operational execution with root event delegation,
 * dual-theme toggling, interactive graph canvas, and real evidence inspection.
 */

// Application State
let currentCaseId = null;
let currentTab = 'overview';
let activeFilterEntityType = 'ALL';
let isStepperCollapsed = false;

// Graph Visualization State
let graphData = { nodes: [], links: [] };
let graphState = {
  scale: 1,
  offsetX: 0,
  offsetY: 0,
  isDragging: false,
  dragStartX: 0,
  dragStartY: 0,
  selectedNode: null,
  hoveredNode: null,
  animFrameId: null
};

// Category Color Palette for Canvas & Tags
const CATEGORY_COLORS = {
  EVIDENCE: '#3b82f6',
  EMAIL: '#00e5a3',
  IPV4: '#f59e0b',
  IP: '#f59e0b',
  PHONE: '#10b981',
  PHONE_NUMBER: '#10b981',
  PERSON: '#ec4899',
  LOCATION: '#a855f7',
  ACCOUNT: '#e11d48',
  DEFAULT: '#94a3b8'
};

document.addEventListener('DOMContentLoaded', async () => {
  // 1. Initialize Forensic Preferences (Dense Tables, Notifications, etc.)
  initPreferences();

  // 2. Render User Profile & Header Badge
  const user = getUser();
  if (user) {
    const nameEl = document.getElementById('user-display-name');
    const roleEl = document.getElementById('user-role-tag');
    const avatarEl = document.getElementById('user-avatar-icon');
    const roleUpper = (user.role || 'INVESTIGATOR').toUpperCase();
    if (nameEl) nameEl.textContent = user.full_name || user.username || 'Investigator';
    if (roleEl) {
      roleEl.textContent = roleUpper;
      roleEl.className = `user-role-badge ${roleUpper === 'ADMIN' ? 'role-admin' : 'role-investigator'}`;
    }
    if (avatarEl) avatarEl.textContent = roleUpper === 'ADMIN' ? '👑' : '🛡️';
    
    // Role-based navigation display
    const adminNav = document.getElementById('nav-admin');
    if (adminNav) {
      adminNav.style.display = roleUpper === 'ADMIN' ? 'flex' : 'none';
    }
  }

  // 3. Attach Centralized Event Listeners
  initEventDelegation();

  // 4. Load Cases
  await loadCasesDropdown();
});

/* ==========================================================================
   FORENSIC WORKSTATION PREFERENCES & PROFILE DRAWER CONTROLLER
   ========================================================================== */

function initPreferences() {
  // 1. Dense Tables Preference
  const isDense = localStorage.getItem('sece_pref_dense_tables') === 'true';
  if (isDense) {
    document.body.classList.add('table-dense');
  } else {
    document.body.classList.remove('table-dense');
  }
  const denseInput = document.getElementById('pref-dense-tables');
  if (denseInput) denseInput.checked = isDense;

  document.querySelectorAll('.density-btn').forEach(btn => {
    const btnDensity = btn.getAttribute('data-density');
    btn.classList.toggle('active', (isDense && btnDensity === 'compact') || (!isDense && btnDensity === 'comfortable'));
  });

  // 2. Notifications Preference
  const notifPref = localStorage.getItem('sece_pref_notifications');
  const notificationsEnabled = notifPref !== 'false';
  const notifInput = document.getElementById('pref-notifications');
  if (notifInput) notifInput.checked = notificationsEnabled;

  // 3. Default Landing Workspace Tab
  const defaultTab = localStorage.getItem('sece_pref_default_tab') || 'overview';
  const defaultTabSelect = document.getElementById('pref-default-tab');
  if (defaultTabSelect) defaultTabSelect.value = defaultTab;
}

function openProfileDrawer() {
  const drawer = document.getElementById('profile-drawer');
  const backdrop = document.getElementById('profile-drawer-backdrop');
  const triggerBtn = document.getElementById('profile-trigger-btn');

  if (drawer) drawer.classList.add('active');
  if (backdrop) backdrop.classList.add('active');
  if (triggerBtn) {
    triggerBtn.classList.add('active');
    triggerBtn.setAttribute('aria-expanded', 'true');
  }

  populateProfileData();
}

function closeProfileDrawer() {
  const drawer = document.getElementById('profile-drawer');
  const backdrop = document.getElementById('profile-drawer-backdrop');
  const triggerBtn = document.getElementById('profile-trigger-btn');

  if (drawer) drawer.classList.remove('active');
  if (backdrop) backdrop.classList.remove('active');
  if (triggerBtn) {
    triggerBtn.classList.remove('active');
    triggerBtn.setAttribute('aria-expanded', 'false');
  }
}

function toggleProfileDrawer() {
  const drawer = document.getElementById('profile-drawer');
  if (drawer && drawer.classList.contains('active')) {
    closeProfileDrawer();
  } else {
    openProfileDrawer();
  }
}

function switchProfileTab(tabName) {
  // Update Tab Buttons
  document.querySelectorAll('.profile-tab-btn').forEach(btn => {
    const isActive = btn.getAttribute('data-tab') === tabName;
    btn.classList.toggle('active', isActive);
    btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
  });

  // Update Content Panels
  document.querySelectorAll('.profile-tab-content').forEach(panel => {
    panel.classList.toggle('active', panel.id === `profile-tab-${tabName}`);
  });
}

function renderRolePermissions(role) {
  const roleUpper = (role || 'INVESTIGATOR').toUpperCase();
  const titleEl = document.getElementById('drawer-role-title');
  const roleIconEl = document.getElementById('drawer-role-icon');
  const allowedEl = document.getElementById('drawer-role-allowed');
  const restrictedEl = document.getElementById('drawer-role-restricted');
  const restrictedTitleEl = document.getElementById('drawer-restricted-title');
  const restrictedIconEl = document.getElementById('drawer-restricted-icon');

  if (roleUpper === 'ADMIN') {
    if (roleIconEl) roleIconEl.textContent = '👑';
    if (titleEl) titleEl.textContent = 'System Administrator (Governance & Oversight)';
    if (allowedEl) {
      allowedEl.innerHTML = `
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>View all cases, system health metrics, and registered users.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Activate or deactivate user accounts.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Inspect system-wide Chain-of-Custody audit logs across all cases.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Manage case governance (close, archive, or delete cases).</span></li>
      `;
    }
    if (restrictedIconEl) restrictedIconEl.textContent = '🛡️';
    if (restrictedTitleEl) restrictedTitleEl.textContent = 'Restricted (Forensic Integrity)';
    if (restrictedEl) {
      restrictedEl.innerHTML = `
        <li class="perm-item restricted"><span class="perm-icon">🛡️</span> <span>Cannot silently alter uploaded evidence files or bypass SHA-256 hash verification.</span></li>
      `;
    }
  } else {
    // Default: INVESTIGATOR
    if (roleIconEl) roleIconEl.textContent = '🛡️';
    if (titleEl) titleEl.textContent = 'Forensic Investigator (Case & Evidence Operations)';
    if (allowedEl) {
      allowedEl.innerHTML = `
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Create and open investigation cases.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Upload evidence files (.txt, .csv, .pdf) with automatic SHA-256 sealing.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Run parsers, extract entities, and verify file hash integrity.</span></li>
        <li class="perm-item allowed"><span class="perm-icon">✔</span> <span>Run cross-evidence correlation and Accept/Reject candidate matches.</span></li>
      `;
    }
    if (restrictedIconEl) restrictedIconEl.textContent = '🔒';
    if (restrictedTitleEl) restrictedTitleEl.textContent = 'Restricted (Admin Only)';
    if (restrictedEl) {
      restrictedEl.innerHTML = `
        <li class="perm-item restricted"><span class="perm-icon">🔒</span> <span>Cannot manage other user accounts or change user roles.</span></li>
        <li class="perm-item restricted"><span class="perm-icon">🔒</span> <span>Cannot delete cases or access system-wide admin audit logs.</span></li>
      `;
    }
  }
}

function populateProfileData() {
  const user = getUser();
  const payload = getTokenPayload();
  const token = getToken();

  // Tab 1: Account Overview
  const nameEl = document.getElementById('drawer-user-fullname');
  const userEl = document.getElementById('drawer-user-username');
  const fullnameValEl = document.getElementById('drawer-user-fullname-val');
  const usernameValEl = document.getElementById('drawer-user-username-val');
  const emailEl = document.getElementById('drawer-user-email');
  const roleEl = document.getElementById('drawer-user-role');
  const idEl = document.getElementById('drawer-user-id');
  const expEl = document.getElementById('drawer-session-expiry');
  const avatarDisplayEl = document.getElementById('drawer-avatar-display');
  const drawerHeaderAvatar = document.getElementById('drawer-header-avatar');

  const roleUpper = (user?.role || payload?.role || 'INVESTIGATOR').toUpperCase();
  const fullName = user?.full_name || user?.username || (roleUpper === 'ADMIN' ? 'System Administrator' : 'Forensic Investigator');
  const username = user?.username || (roleUpper === 'ADMIN' ? 'admin' : 'investigator');

  if (nameEl) nameEl.textContent = fullName;
  if (userEl) userEl.textContent = `@${username}`;
  if (fullnameValEl) fullnameValEl.textContent = fullName;
  if (usernameValEl) usernameValEl.textContent = `@${username}`;
  if (emailEl) emailEl.textContent = user?.email || (payload?.email || (roleUpper === 'ADMIN' ? 'admin@sece.gov' : 'investigator@sece.gov'));
  if (roleEl) {
    roleEl.textContent = roleUpper;
    roleEl.className = `user-role-badge ${roleUpper === 'ADMIN' ? 'role-admin' : 'role-investigator'}`;
  }
  const avatarChar = roleUpper === 'ADMIN' ? '👑' : '🛡️';
  if (avatarDisplayEl) avatarDisplayEl.textContent = avatarChar;
  if (drawerHeaderAvatar) drawerHeaderAvatar.textContent = avatarChar;
  if (idEl) idEl.textContent = user?.id || payload?.sub || 'Local Session ID';
  if (expEl) expEl.textContent = getSessionExpiryFormatted();

  // Populate dynamic "What Your Authority Can Do" panel
  renderRolePermissions(roleUpper);

  // Tab 2: Preferences Controls Sync
  const defaultTabSelect = document.getElementById('pref-default-tab');
  if (defaultTabSelect) {
    defaultTabSelect.value = localStorage.getItem('sece_pref_default_tab') || 'overview';
  }

  const isDense = localStorage.getItem('sece_pref_dense_tables') === 'true';
  document.querySelectorAll('.density-btn').forEach(btn => {
    const btnDensity = btn.getAttribute('data-density');
    btn.classList.toggle('active', (isDense && btnDensity === 'compact') || (!isDense && btnDensity === 'comfortable'));
  });

  const denseCheckbox = document.getElementById('pref-dense-tables');
  if (denseCheckbox) {
    denseCheckbox.checked = isDense;
  }

  const notifCheckbox = document.getElementById('pref-notifications');
  if (notifCheckbox) {
    notifCheckbox.checked = localStorage.getItem('sece_pref_notifications') !== 'false';
  }

  // Tab 3: Security Preview
  const tokenPreview = document.getElementById('drawer-truncated-token');
  if (tokenPreview) {
    if (token) {
      tokenPreview.textContent = token.length > 56 
        ? `${token.substring(0, 28)}...${token.substring(token.length - 20)}`
        : token;
    } else {
      tokenPreview.textContent = 'No active token';
    }
  }
}

async function handleCopyToken(buttonEl) {
  const success = await copySessionToken();
  if (buttonEl) {
    const originalText = buttonEl.textContent;
    buttonEl.textContent = success ? 'Copied!' : 'Failed';
    buttonEl.classList.add(success ? 'btn-success' : 'btn-danger');
    setTimeout(() => {
      buttonEl.textContent = originalText;
      buttonEl.classList.remove('btn-success', 'btn-danger');
    }, 1500);
  }
}

function setDensity(mode) {
  const isDense = mode === 'compact';
  localStorage.setItem('sece_pref_dense_tables', isDense ? 'true' : 'false');
  if (isDense) {
    document.body.classList.add('table-dense');
  } else {
    document.body.classList.remove('table-dense');
  }

  document.querySelectorAll('.density-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-density') === mode);
  });

  const denseInput = document.getElementById('pref-dense-tables');
  if (denseInput) denseInput.checked = isDense;
}

function handleDenseTablesToggle(checked) {
  setDensity(checked ? 'compact' : 'comfortable');
}

function handleNotificationsToggle(checked) {
  localStorage.setItem('sece_pref_notifications', checked ? 'true' : 'false');
}

function handleDefaultTabChange(val) {
  localStorage.setItem('sece_pref_default_tab', val);
}

function notifyInvestigator(message, isError = false) {
  const notifPref = localStorage.getItem('sece_pref_notifications');
  const notificationsEnabled = notifPref !== 'false';
  if (isError || notificationsEnabled) {
    alert(message);
  } else {
    console.log('[SECE Notification Suppressed by Preference]:', message);
  }
}

/* ==========================================================================
   CENTRALIZED ROOT EVENT DELEGATION & ACCESSIBILITY
   ========================================================================== */

function initEventDelegation() {
  // 1. Click Event Delegation
  document.addEventListener('click', async (e) => {
    const target = e.target.closest('[data-action]');
    if (!target) return;

    const action = target.getAttribute('data-action');

    switch (action) {
      case 'switch-tab': {
        const tab = target.getAttribute('data-tab');
        if (tab) switchTab(tab);
        break;
      }
      case 'open-active-case': {
        e.preventDefault();
        const targetTab = document.querySelector('[data-tab="cases"]') || document.querySelector('[data-tab="evidence"]');
        if (targetTab) {
          targetTab.click();
        } else {
          switchTab('cases');
        }
        break;
      }
      case 'step-nav': {
        const step = target.getAttribute('data-step');
        if (step) {
          updateStepperActive(target);
          switchTab(step);
        }
        break;
      }
      case 'toggle-stepper': {
        toggleStepper();
        break;
      }
      case 'toggle-profile': {
        e.stopPropagation();
        toggleProfileDrawer();
        break;
      }
      case 'close-profile': {
        closeProfileDrawer();
        break;
      }
      case 'switch-profile-tab': {
        const tab = target.getAttribute('data-tab');
        if (tab) switchProfileTab(tab);
        break;
      }
      case 'set-density': {
        const density = target.getAttribute('data-density');
        if (density) setDensity(density);
        break;
      }
      case 'copy-token': {
        await handleCopyToken(target);
        break;
      }
      case 'purge-session': {
        if (confirm('Are you sure you want to purge all local session state, stored tokens, and cached forensic workspace settings?')) {
          purgeLocalSession();
        }
        break;
      }
      case 'open-modal': {
        const modalId = target.getAttribute('data-target');
        if (modalId) openModal(modalId);
        break;
      }
      case 'close-modal': {
        const modal = target.closest('.modal-backdrop');
        if (modal) closeModal(modal.id);
        break;
      }
      case 'select-case': {
        const caseId = target.getAttribute('data-id');
        if (caseId) setActiveCase(caseId);
        break;
      }
      case 'parse-evidence': {
        const evidenceId = target.getAttribute('data-id');
        if (evidenceId) await parseEvidenceFile(evidenceId, target);
        break;
      }
      case 'extract-entities': {
        const evidenceId = target.getAttribute('data-id');
        if (evidenceId) await extractEntities(evidenceId, target);
        break;
      }
      case 'verify-integrity': {
        const evidenceId = target.getAttribute('data-id');
        if (evidenceId) await verifyIntegrity(evidenceId, target);
        break;
      }
      case 'view-raw-evidence': {
        const evidenceId = target.getAttribute('data-id');
        if (evidenceId) await openViewRawEvidenceModal(evidenceId, target);
        break;
      }
      case 'review-match': {
        const matchId = target.getAttribute('data-id');
        const decision = target.getAttribute('data-status');
        if (matchId && decision) await updateMatchStatus(matchId, decision, target);
        break;
      }
      case 'run-correlation': {
        await triggerCorrelationPipeline(target);
        break;
      }
      case 'filter-entities': {
        const filterType = target.getAttribute('data-type');
        if (filterType) filterEntitiesByType(filterType);
        break;
      }
      case 'toggle-user-status': {
        const userId = target.getAttribute('data-id');
        const currentActive = target.getAttribute('data-active') === 'true';
        if (userId) await toggleUserStatus(userId, currentActive, target);
        break;
      }
      case 'refresh-admin-audit': {
        await loadAdminAuditLogs();
        break;
      }
      case 'admin-close-case': {
        const caseId = target.getAttribute('data-id');
        if (caseId) await adminApproveCaseStatus(caseId, 'CLOSED');
        break;
      }
      case 'admin-delete-case': {
        const caseId = target.getAttribute('data-id');
        if (caseId) await adminDeleteCase(caseId);
        break;
      }
      case 'logout': {
        logout();
        break;
      }
    }
  });

  // 2. Outside Click Detection for Profile Drawer
  document.addEventListener('click', (e) => {
    const drawer = document.getElementById('profile-drawer');
    const triggerBtn = document.getElementById('profile-trigger-btn');
    if (drawer && drawer.classList.contains('active')) {
      if (!drawer.contains(e.target) && (!triggerBtn || !triggerBtn.contains(e.target))) {
        closeProfileDrawer();
      }
    }
  });

  // 3. Backdrop Click for Profile Drawer
  const profileBackdrop = document.getElementById('profile-drawer-backdrop');
  if (profileBackdrop) {
    profileBackdrop.addEventListener('click', () => {
      closeProfileDrawer();
    });
  }

  // 4. Keyboard Accessibility (Escape to close drawer or modal)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const drawer = document.getElementById('profile-drawer');
      if (drawer && drawer.classList.contains('active')) {
        closeProfileDrawer();
        return;
      }
      const openModalEl = document.querySelector('.modal-backdrop[style*="display: flex"]');
      if (openModalEl) {
        closeModal(openModalEl.id);
      }
    }
  });

  // 5. Change Listeners for User Preferences
  const prefDenseTables = document.getElementById('pref-dense-tables');
  if (prefDenseTables) {
    prefDenseTables.addEventListener('change', (e) => {
      handleDenseTablesToggle(e.target.checked);
    });
  }

  const prefNotifications = document.getElementById('pref-notifications');
  if (prefNotifications) {
    prefNotifications.addEventListener('change', (e) => {
      handleNotificationsToggle(e.target.checked);
    });
  }

  const prefDefaultTab = document.getElementById('pref-default-tab');
  if (prefDefaultTab) {
    prefDefaultTab.addEventListener('change', (e) => {
      handleDefaultTabChange(e.target.value);
    });
  }

  // 3. Dropdown Selector Change
  const caseSelectEl = document.getElementById('active-case-select');
  if (caseSelectEl) {
    caseSelectEl.addEventListener('change', (e) => {
      setActiveCase(e.target.value);
    });
  }

  // 4. Form Submissions
  const formCreateCase = document.getElementById('form-create-case');
  if (formCreateCase) {
    formCreateCase.addEventListener('submit', handleCreateCaseSubmit);
  }

  const formUploadEvidence = document.getElementById('form-upload-evidence');
  if (formUploadEvidence) {
    formUploadEvidence.addEventListener('submit', handleUploadEvidenceSubmit);
  }

  const formAddTimeline = document.getElementById('form-add-timeline');
  if (formAddTimeline) {
    formAddTimeline.addEventListener('submit', handleAddTimelineSubmit);
  }

  // 5. Graph Control Buttons
  const btnReset = document.getElementById('btn-graph-reset');
  if (btnReset) btnReset.addEventListener('click', resetGraphView);

  const btnRefresh = document.getElementById('btn-graph-refresh');
  if (btnRefresh) btnRefresh.addEventListener('click', () => loadGraphData(currentCaseId));

  const btnZoomIn = document.getElementById('btn-zoom-in');
  if (btnZoomIn) btnZoomIn.addEventListener('click', () => zoomGraph(1.2));

  const btnZoomOut = document.getElementById('btn-zoom-out');
  if (btnZoomOut) btnZoomOut.addEventListener('click', () => zoomGraph(0.8));

  const btnCloseDrawer = document.getElementById('btn-close-drawer');
  if (btnCloseDrawer) {
    btnCloseDrawer.addEventListener('click', () => {
      const drawer = document.getElementById('graph-node-drawer');
      if (drawer) drawer.style.display = 'none';
      graphState.selectedNode = null;
      drawGraph();
    });
  }

  initGraphInteraction();
}

/* ==========================================================================
   MODAL CONTROLLER
   ========================================================================== */

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'flex';
    const firstInput = modal.querySelector('input, select, textarea, button');
    if (firstInput) firstInput.focus();
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
  }
}

/* ==========================================================================
   WORKFLOW STEPPER CONTROLLER
   ========================================================================== */

function toggleStepper() {
  const container = document.getElementById('stepper-steps-container');
  const icon = document.getElementById('stepper-toggle-icon');
  const text = document.getElementById('stepper-toggle-text');
  isStepperCollapsed = !isStepperCollapsed;

  if (isStepperCollapsed) {
    if (container) container.style.display = 'none';
    if (icon) icon.textContent = '▼';
    if (text) text.textContent = 'Expand Stepper';
  } else {
    if (container) container.style.display = 'flex';
    if (icon) icon.textContent = '▲';
    if (text) text.textContent = 'Collapse Stepper';
  }
}

function updateStepperActive(element) {
  document.querySelectorAll('.stepper-step').forEach(step => step.classList.remove('active'));
  if (element) element.classList.add('active');
}

/* ==========================================================================
   TAB NAVIGATION CONTROLLER
   ========================================================================== */

function switchTab(tabName) {
  const user = getUser();
  if (tabName === 'admin' && (!user || (user.role || '').toUpperCase() !== 'ADMIN')) {
    notifyInvestigator('Access Forbidden: Governance & User Management requires Administrator authority.', true);
    return;
  }

  currentTab = tabName;

  // Update Nav Items
  document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
    item.classList.remove('active');
    item.setAttribute('aria-selected', 'false');
  });

  const activeNav = document.getElementById(`nav-${tabName}`);
  if (activeNav) {
    activeNav.classList.add('active');
    activeNav.setAttribute('aria-selected', 'true');
  }

  // Update Panes
  document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

  const activePane = document.getElementById(`pane-${tabName}`);
  if (activePane) activePane.classList.add('active');

  // Load Pane Content
  refreshActiveTab();
}

function refreshActiveTab() {
  if (currentTab === 'overview') {
    loadCaseOverview(currentCaseId);
  } else if (currentTab === 'cases') {
    loadCasesTable();
  } else if (currentTab === 'evidence') {
    loadEvidenceLedger(currentCaseId);
  } else if (currentTab === 'entities') {
    loadEntities(currentCaseId);
  } else if (currentTab === 'correlation') {
    loadCorrelationData(currentCaseId);
  } else if (currentTab === 'timeline') {
    loadTimelineData(currentCaseId);
  } else if (currentTab === 'graph') {
    loadGraphData(currentCaseId);
  } else if (currentTab === 'audit') {
    loadAuditLogs(currentCaseId);
  } else if (currentTab === 'admin') {
    loadAdminGovernanceData();
  }
}

/* ==========================================================================
   CASE SELECTOR CONTROLLER
   ========================================================================== */

async function loadCasesDropdown() {
  const selectEl = document.getElementById('active-case-select');
  if (!selectEl) return;

  try {
    const res = await authFetch('/api/v1/cases/');
    if (!res || !res.ok) return;

    const cases = await res.json();
    selectEl.innerHTML = '';

    if (cases.length === 0) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = '-- No Cases Found (Click + New Case) --';
      selectEl.appendChild(opt);
      currentCaseId = null;
    } else {
      cases.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.id;
        opt.textContent = `[${c.case_number}] ${c.title}`;
        selectEl.appendChild(opt);
      });

      if (!currentCaseId || !cases.some(c => c.id === currentCaseId)) {
        currentCaseId = cases[0].id;
      }
      selectEl.value = currentCaseId;
    }

    const defaultTab = localStorage.getItem('sece_pref_default_tab');
    if (defaultTab && defaultTab !== currentTab) {
      switchTab(defaultTab);
    } else {
      refreshActiveTab();
    }
  } catch (err) {
    console.error('Failed to load cases dropdown:', err);
  }
}

function setActiveCase(caseId) {
  currentCaseId = caseId;
  const selectEl = document.getElementById('active-case-select');
  if (selectEl && selectEl.value !== caseId) {
    selectEl.value = caseId;
  }
  refreshActiveTab();
}

/* ==========================================================================
   PANE 1: OVERVIEW CONTROLLER (M14 SUMMARY)
   ========================================================================== */

async function loadCaseOverview(caseId) {
  const titleEl = document.getElementById('overview-case-title');
  const descEl = document.getElementById('overview-case-desc');
  const openBtn = document.getElementById('active-case-open-btn');
  const statusEl = document.getElementById('overview-case-status');
  const auditBody = document.querySelector('#overview-audit-table tbody');

  if (!caseId) {
    if (titleEl) titleEl.textContent = 'No Active Case Selected';
    if (descEl) descEl.textContent = 'Please create a new case container or select an existing case from the header dropdown.';
    if (openBtn) {
      openBtn.textContent = 'N/A ↗';
      openBtn.className = 'status-pill status-closed clickable-badge';
      openBtn.setAttribute('data-action', 'open-active-case');
      openBtn.title = 'Click to open Case Management & Evidence Workspace';
    } else if (statusEl) {
      statusEl.textContent = 'N/A';
    }
    if (auditBody) auditBody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No active case selected.</td></tr>';
    updateMetrics(0, 0, 0, 0);
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/summary`);
    if (!res || !res.ok) return;

    const summary = await res.json();

    let totalEntities = 0;
    if (summary.entities_by_type) {
      Object.values(summary.entities_by_type).forEach(count => totalEntities += count);
    }

    updateMetrics(
      summary.total_evidence_items || 0,
      totalEntities || summary.total_canonical_entities || 0,
      summary.total_relationships || 0,
      summary.total_pending_matches || 0
    );

    if (titleEl) titleEl.textContent = summary.title ? `[${summary.case_number}] ${summary.title}` : `Case #${summary.case_number}`;
    if (descEl) descEl.textContent = summary.description || 'No description provided for this case scope.';
    if (openBtn) {
      const rawStatus = (summary.status || 'OPEN').replace('_', ' ').toUpperCase();
      openBtn.textContent = `${rawStatus} ↗`;
      const statusSlug = (summary.status || 'open').toLowerCase().replace('_', '-');
      openBtn.className = `status-pill status-${statusSlug} clickable-badge`;
      openBtn.setAttribute('data-action', 'open-active-case');
      openBtn.title = 'Click to open Case Management & Evidence Workspace';
    } else if (statusEl) {
      statusEl.textContent = (summary.status || 'OPEN').replace('_', ' ');
      statusEl.className = `badge badge-${(summary.status || 'open').toLowerCase().replace('_', '-')}`;
    }

    if (auditBody) {
      if (!summary.recent_audit_logs || summary.recent_audit_logs.length === 0) {
        auditBody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No audit entries recorded yet.</td></tr>';
      } else {
        auditBody.innerHTML = summary.recent_audit_logs.map(log => `
          <tr>
            <td><strong style="color: var(--accent-primary);">${escapeHtml(log.action)}</strong></td>
            <td>${escapeHtml(log.actor || 'Investigator')}</td>
            <td>${escapeHtml(log.details || '-')}</td>
            <td>${new Date(log.timestamp).toLocaleString()}</td>
          </tr>
        `).join('');
      }
    }
  } catch (err) {
    console.error('Error loading case overview:', err);
  }
}

function updateMetrics(evidenceCount, entitiesCount, relationshipsCount, matchesCount) {
  const evEl = document.getElementById('stat-evidence-count');
  const enEl = document.getElementById('stat-entities-count');
  const relEl = document.getElementById('stat-relationships-count');
  const matEl = document.getElementById('stat-matches-count');

  if (evEl) evEl.textContent = evidenceCount;
  if (enEl) enEl.textContent = entitiesCount;
  if (relEl) relEl.textContent = relationshipsCount;
  if (matEl) matEl.textContent = matchesCount;
}

/* ==========================================================================
   PANE 2: CASE MANAGEMENT (M2)
   ========================================================================== */

async function loadCasesTable() {
  const tbody = document.getElementById('cases-table-body');
  if (!tbody) return;

  const user = getUser();
  const isAdmin = user && (user.role || '').toUpperCase() === 'ADMIN';

  try {
    const res = await authFetch('/api/v1/cases/');
    if (!res || !res.ok) return;

    const cases = await res.json();
    if (cases.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">No cases found. Click "+ Create New Case" to start.</td></tr>';
      return;
    }

    tbody.innerHTML = cases.map(c => `
      <tr>
        <td><strong>${escapeHtml(c.case_number)}</strong></td>
        <td>${escapeHtml(c.title)}</td>
        <td><span class="badge badge-${(c.status || 'open').toLowerCase().replace('_', '-')}">${escapeHtml(c.status.replace('_', ' '))}</span></td>
        <td>Investigator</td>
        <td>${new Date(c.created_at).toLocaleDateString()}</td>
        <td>
          <div style="display: flex; gap: 0.35rem; align-items: center; flex-wrap: wrap;">
            ${c.id === currentCaseId 
              ? '<span class="badge badge-open">Active Workspace</span>'
              : `<button class="btn btn-secondary btn-sm" data-action="select-case" data-id="${c.id}" aria-label="Select Case ${c.case_number}">Open Workspace</button>`
            }
            ${isAdmin && c.status !== 'CLOSED' && c.status !== 'ARCHIVED'
              ? `<button class="btn btn-secondary btn-sm" data-action="admin-close-case" data-id="${c.id}" title="Administrator Approval: Close Case" aria-label="Approve Case Closure">Close Case</button>`
              : ''
            }
            ${isAdmin
              ? `<button class="btn btn-danger btn-sm" data-action="admin-delete-case" data-id="${c.id}" title="Administrator Action: Permanently Delete Case" aria-label="Delete Case">Delete</button>`
              : ''
            }
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load cases table:', err);
  }
}

async function handleCreateCaseSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-case');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Creating...';

  const caseNumber = document.getElementById('new-case-number').value.trim();
  const title = document.getElementById('new-case-title').value.trim();
  const description = document.getElementById('new-case-desc').value.trim();
  const status = document.getElementById('new-case-status').value;

  try {
    const res = await authFetch('/api/v1/cases/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case_number: caseNumber, title, description, status })
    });

    if (res && res.ok) {
      const newCase = await res.json();
      closeModal('modal-create-case');
      document.getElementById('form-create-case').reset();
      currentCaseId = newCase.id;
      await loadCasesDropdown();
      switchTab('overview');
    } else {
      const errData = await res.json();
      alert(`Failed to create case: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Create Case Container';
  }
}

/* ==========================================================================
   PANE 3: EVIDENCE LEDGER (M3, M4, M5)
   ========================================================================== */

async function loadEvidenceLedger(caseId) {
  const tbody = document.getElementById('evidence-table-body');
  if (!tbody) return;

  if (!caseId) {
    tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">No active case selected. Select or create a case first.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/evidence/`);
    if (!res || !res.ok) return;

    const evidenceList = await res.json();
    if (evidenceList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">No evidence files uploaded to this case yet. Click "+ Upload Evidence File" to ingest.</td></tr>';
      return;
    }

    tbody.innerHTML = evidenceList.map(e => `
      <tr id="evidence-row-${e.id}">
        <td><strong>${escapeHtml(e.original_filename)}</strong></td>
        <td><span class="badge badge-open">${escapeHtml(e.evidence_type)}</span></td>
        <td>${(e.file_size_bytes / 1024).toFixed(1)} KB</td>
        <td><code style="font-size: 0.75rem; color: var(--accent-primary);">${e.sha256_hash ? e.sha256_hash.substring(0, 16) + '...' : '-'}</code></td>
        <td>
          <span class="badge ${e.processing_status === 'EXTRACTED' || e.processing_status === 'PARSED' ? 'badge-open' : 'badge-in-progress'}" id="status-badge-${e.id}">
            ${escapeHtml(e.processing_status)}
          </span>
        </td>
        <td>
          <div style="display: flex; gap: 0.35rem; flex-wrap: wrap;">
            <button class="btn btn-secondary btn-sm" data-action="parse-evidence" data-id="${e.id}" title="⚡ Parse: Runs the format-specific factory parser (.txt, .csv, .pdf) to extract text content and technical metadata into JSONB" aria-label="Parse file content">⚡ Parse</button>
            <button class="btn btn-primary btn-sm" data-action="extract-entities" data-id="${e.id}" title="🏷️ Extract: Runs regex and NLP to detect identities and record exact character offsets" aria-label="Extract entity indicators">🏷️ Extract</button>
            <button class="btn btn-secondary btn-sm" data-action="verify-integrity" data-id="${e.id}" title="🛡️ Verify Integrity: Recomputes the SHA-256 digest directly from the disk file and compares it to the original intake baseline hash to detect tampering" aria-label="Verify hash integrity">🛡️ Verify</button>
            <button class="btn btn-secondary btn-sm" data-action="view-raw-evidence" data-id="${e.id}" title="👁️ Inspect: Opens the parsed content and evidence inspection viewer with highlighted entity offsets" aria-label="Inspect raw file content">👁️ Inspect</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load evidence ledger:', err);
  }
}

async function handleUploadEvidenceSubmit(e) {
  e.preventDefault();
  if (!currentCaseId) {
    alert('Please select an active case first.');
    return;
  }

  const btn = document.getElementById('btn-submit-upload');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Computing Hash & Uploading...';

  const fileInput = document.getElementById('upload-file');
  const typeInput = document.getElementById('upload-type');
  const descInput = document.getElementById('upload-desc');

  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Please select a file to upload.');
    btn.disabled = false;
    btn.textContent = 'Save to Immutable Vault';
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  formData.append('evidence_type', typeInput.value);
  if (descInput.value.trim()) {
    formData.append('source_description', descInput.value.trim());
  }

  try {
    const res = await authFetch(`/api/v1/cases/${currentCaseId}/evidence/upload`, {
      method: 'POST',
      body: formData
    });

    if (res && res.ok) {
      closeModal('modal-upload-evidence');
      document.getElementById('form-upload-evidence').reset();
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Upload Failed: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Upload Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Save to Immutable Vault';
  }
}

async function parseEvidenceFile(evidenceId, buttonEl) {
  const originalText = buttonEl.innerHTML;
  buttonEl.disabled = true;
  buttonEl.innerHTML = '<span class="spinner"></span> Parsing...';

  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/parse`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      const statusBadge = document.getElementById(`status-badge-${evidenceId}`);
      if (statusBadge) {
        statusBadge.textContent = 'PARSED';
        statusBadge.className = 'badge badge-open';
      }
      notifyInvestigator(`Evidence Parsed Successfully!\nParser: ${data.metadata?.parser || 'Standard'}\nText Preview: ${data.text_preview.substring(0, 120)}...`);
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      notifyInvestigator(`Parsing Error: ${errData.detail || 'Failed to parse file'}`, true);
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
  } finally {
    buttonEl.disabled = false;
    buttonEl.innerHTML = originalText;
  }
}

async function extractEntities(evidenceId, buttonEl) {
  const originalText = buttonEl.innerHTML;
  buttonEl.disabled = true;
  buttonEl.innerHTML = '<span class="spinner"></span> Extracting...';

  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/extract-entities`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      const statusBadge = document.getElementById(`status-badge-${evidenceId}`);
      if (statusBadge) {
        statusBadge.textContent = 'EXTRACTED';
        statusBadge.className = 'badge badge-open';
      }
      notifyInvestigator(`Indicators Extracted!\nTotal Mentions: ${data.total_mentions_extracted}\nDistinct Canonical Entities: ${data.distinct_canonical_entities}`);
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      notifyInvestigator(`Extraction Error: ${errData.detail || 'Failed to extract entities'}`, true);
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
  } finally {
    buttonEl.disabled = false;
    buttonEl.innerHTML = originalText;
  }
}

async function verifyIntegrity(evidenceId, buttonEl) {
  const originalText = buttonEl.innerHTML;
  buttonEl.disabled = true;
  buttonEl.innerHTML = '<span class="spinner"></span> Re-hashing...';

  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/verify-integrity`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      if (data.is_valid) {
        buttonEl.outerHTML = '<span class="badge badge-verified" title="Live disk SHA-256 matches baseline">VERIFIED</span>';
        notifyInvestigator(`CRYPTOGRAPHIC INTEGRITY VERIFIED (PASS)\nFilename: ${data.original_filename}\nSHA-256 Digest: ${data.calculated_sha256_hash}`);
      } else {
        buttonEl.outerHTML = '<span class="badge badge-tampered" title="Live disk SHA-256 does not match!">TAMPERED</span>';
        notifyInvestigator(`INTEGRITY FAILURE (TAMPER DETECTED!)\nStored: ${data.stored_sha256_hash}\nLive File: ${data.calculated_sha256_hash}`, true);
      }
    } else {
      const errData = await res.json();
      notifyInvestigator(`Verification Error: ${errData.detail || 'Failed to verify file'}`, true);
      buttonEl.disabled = false;
      buttonEl.innerHTML = originalText;
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
    buttonEl.disabled = false;
    buttonEl.innerHTML = originalText;
  }
}

/* ==========================================================================
   VIEW REAL DATA MODAL (INSPECTION & PROVENANCE OFFSETS)
   ========================================================================== */

async function openViewRawEvidenceModal(evidenceId, buttonEl) {
  const originalText = buttonEl ? buttonEl.innerHTML : '';
  if (buttonEl) {
    buttonEl.disabled = true;
    buttonEl.innerHTML = '<span class="spinner"></span> Loading...';
  }

  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/content`);
    if (!res || !res.ok) {
      alert('Could not retrieve evidence inspection content.');
      return;
    }

    const data = await res.json();

    document.getElementById('raw-modal-filename').textContent = data.original_filename || '-';
    document.getElementById('raw-modal-category').textContent = data.evidence_type || 'OTHER';
    document.getElementById('raw-modal-size').textContent = `${(data.file_size_bytes / 1024).toFixed(1)} KB`;
    document.getElementById('raw-modal-hash').textContent = data.sha256_hash || '-';

    // Raw parsed text
    const textContentEl = document.getElementById('raw-modal-text-content');
    const textCharsEl = document.getElementById('raw-text-chars');
    textContentEl.textContent = data.parsed_text || '[No parsed text available. Click "⚡ Parse" first.]';
    textCharsEl.textContent = `${(data.parsed_text || '').length} characters`;

    // Mentions & Provenance Offsets
    const mentionsTbody = document.getElementById('raw-modal-mentions-tbody');
    const mentionsCountEl = document.getElementById('raw-mentions-count');

    if (!data.mentions || data.mentions.length === 0) {
      mentionsTbody.innerHTML = '<tr><td colspan="3" style="color: var(--text-muted); text-align: center;">No entity indicators extracted yet. Click "🏷️ Extract" on this file.</td></tr>';
      mentionsCountEl.textContent = '0 indicators';
    } else {
      mentionsCountEl.textContent = `${data.mentions.length} indicators`;
      mentionsTbody.innerHTML = data.mentions.map(m => `
        <tr>
          <td><span class="badge badge-open" style="font-size: 0.7rem;">${escapeHtml(m.entity_type)}</span></td>
          <td><code style="font-size: 0.75rem; color: var(--accent-primary);">${escapeHtml(m.normalized_value)}</code></td>
          <td style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">${m.start_offset != null ? `[${m.start_offset}:${m.end_offset}]` : '-'}</td>
        </tr>
      `).join('');
    }

    openModal('modal-view-raw-evidence');
  } catch (err) {
    alert(`Error loading inspection view: ${err.message}`);
  } finally {
    if (buttonEl) {
      buttonEl.disabled = false;
      buttonEl.innerHTML = originalText;
    }
  }
}

/* ==========================================================================
   PANE 4: EXTRACTED ENTITIES (M6, M7, M8, M9)
   ========================================================================== */

async function loadEntities(caseId) {
  const container = document.getElementById('canonical-entities-container');
  const filtersDiv = document.getElementById('entity-type-filters');
  const mentionsTbody = document.getElementById('mentions-table-body');

  if (!container) return;

  if (!caseId) {
    container.innerHTML = '<p style="color: var(--text-muted);">No active case selected.</p>';
    if (mentionsTbody) mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted); text-align: center;">No active case selected.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/entities`);
    if (!res || !res.ok) return;

    const entities = await res.json();

    if (entities.length === 0) {
      container.innerHTML = '<p style="color: var(--text-muted);">No canonical entities discovered yet. Upload evidence files and run extraction.</p>';
      if (filtersDiv) filtersDiv.innerHTML = '';
      if (mentionsTbody) mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted); text-align: center;">No entity mentions extracted yet.</td></tr>';
      return;
    }

    // Filters
    const types = ['ALL', ...new Set(entities.map(e => e.entity_type))];
    if (filtersDiv) {
      filtersDiv.innerHTML = types.map(t => `
        <button class="btn btn-sm ${activeFilterEntityType === t ? 'btn-primary' : 'btn-secondary'}" 
                data-action="filter-entities" data-type="${t}">${t}</button>
      `).join('');
    }

    // Render Entity Cards
    const filteredEntities = activeFilterEntityType === 'ALL' 
      ? entities 
      : entities.filter(e => e.entity_type === activeFilterEntityType);

    container.innerHTML = filteredEntities.map(e => `
      <div class="card" style="padding: 1.15rem; border-left: 3px solid var(--accent-primary); margin-bottom: 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge badge-open">${escapeHtml(e.entity_type)}</span>
          <span style="font-size: 0.8rem; color: var(--text-muted);">${e.mention_count || 1} Mention(s)</span>
        </div>
        <div style="font-size: 1rem; font-weight: 600; font-family: var(--font-mono); word-break: break-all; color: var(--text-primary);">${escapeHtml(e.canonical_name)}</div>
      </div>
    `).join('');

    loadCaseMentions(caseId);
  } catch (err) {
    console.error('Failed to load canonical entities:', err);
  }
}

function filterEntitiesByType(type) {
  activeFilterEntityType = type;
  loadEntities(currentCaseId);
}

async function loadCaseMentions(caseId) {
  const mentionsTbody = document.getElementById('mentions-table-body');
  if (!mentionsTbody) return;

  try {
    const resEv = await authFetch(`/api/v1/cases/${caseId}/evidence/`);
    if (!resEv || !resEv.ok) return;

    const evidenceList = await resEv.json();
    let allMentions = [];

    for (const ev of evidenceList) {
      const resM = await authFetch(`/api/v1/evidence/${ev.id}/entities`);
      if (resM && resM.ok) {
        const mentions = await resM.json();
        allMentions = allMentions.concat(mentions);
      }
    }

    if (allMentions.length === 0) {
      mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted); text-align: center;">No raw entity mentions extracted yet.</td></tr>';
      return;
    }

    mentionsTbody.innerHTML = allMentions.map(m => `
      <tr>
        <td><span class="badge badge-open">${escapeHtml(m.entity_type)}</span></td>
        <td><code>${escapeHtml(m.raw_value)}</code></td>
        <td><code>${escapeHtml(m.normalized_value)}</code></td>
        <td style="font-family: var(--font-mono); color: var(--text-muted);">${m.start_offset != null ? `[${m.start_offset}:${m.end_offset}]` : '-'}</td>
        <td style="font-size: 0.85rem; color: var(--text-muted);">${m.context_snippet ? '...' + escapeHtml(m.context_snippet) + '...' : '-'}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load entity mentions:', err);
  }
}

/* ==========================================================================
   PANE 5: CORRELATION ENGINE (M10, M11)
   ========================================================================== */

async function loadCorrelationData(caseId) {
  const matchesTbody = document.getElementById('matches-table-body');
  const relsTbody = document.getElementById('relationships-table-body');

  if (!matchesTbody || !relsTbody) return;

  if (!caseId) {
    matchesTbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No active case selected.</td></tr>';
    relsTbody.innerHTML = '<tr><td colspan="3" style="color: var(--text-muted); text-align: center;">No active case selected.</td></tr>';
    return;
  }

  try {
    // 1. Matches
    const resM = await authFetch(`/api/v1/cases/${caseId}/matches`);
    if (resM && resM.ok) {
      const matches = await resM.json();
      if (matches.length === 0) {
        matchesTbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No candidate matches discovered yet. Click "⚡ Run Correlation Engine" to evaluate.</td></tr>';
      } else {
        matchesTbody.innerHTML = matches.map(m => `
          <tr>
            <td><strong>${escapeHtml(m.confidence_score)}</strong></td>
            <td>${escapeHtml(m.match_rationale)}</td>
            <td><span class="badge badge-${m.status === 'ACCEPTED' ? 'open' : m.status === 'REJECTED' ? 'closed' : 'in-progress'}">${escapeHtml(m.status)}</span></td>
            <td>
              <div style="display: flex; gap: 0.35rem;">
                <button class="btn btn-primary btn-sm" data-action="review-match" data-id="${m.id}" data-status="ACCEPTED" title="Accept: Confirms candidate match as verified ground truth and updates link confidence" aria-label="Accept candidate match">Accept</button>
                <button class="btn btn-secondary btn-sm" data-action="review-match" data-id="${m.id}" data-status="REJECTED" title="Reject: Dismisses candidate match as false positive, pruning relationship link" aria-label="Reject candidate match">Reject</button>
              </div>
            </td>
          </tr>
        `).join('');
      }
    }

    // 2. Relationships
    const resR = await authFetch(`/api/v1/cases/${caseId}/relationships`);
    if (resR && resR.ok) {
      const rels = await resR.json();
      if (rels.length === 0) {
        relsTbody.innerHTML = '<tr><td colspan="3" style="color: var(--text-muted); text-align: center;">No cross-evidence relationships generated yet. Click "⚡ Run Correlation Engine".</td></tr>';
      } else {
        relsTbody.innerHTML = rels.map(r => `
          <tr>
            <td><span class="badge badge-open">${escapeHtml(r.relationship_type)}</span></td>
            <td><strong>${escapeHtml(r.confidence_score)}</strong></td>
            <td>${escapeHtml(r.rationale || '-')}</td>
          </tr>
        `).join('');
      }
    }
  } catch (err) {
    console.error('Failed to load correlation data:', err);
  }
}

async function triggerCorrelationPipeline(buttonEl) {
  if (!currentCaseId) {
    alert('Please select an active case container first.');
    return;
  }

  const originalText = buttonEl ? buttonEl.innerHTML : '';
  if (buttonEl) {
    buttonEl.disabled = true;
    buttonEl.innerHTML = '<span class="spinner"></span> Correlating...';
  }

  try {
    const res = await authFetch(`/api/v1/cases/${currentCaseId}/correlate`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      notifyInvestigator(`Correlation Complete!\nCandidate Matches Discovered: ${data.total_candidate_matches}\nRelationships Established: ${data.total_relationships}`);
      loadCorrelationData(currentCaseId);
    } else {
      const errData = await res.json();
      notifyInvestigator(`Correlation Error: ${errData.detail || 'Failed to run correlation pipeline'}`, true);
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
  } finally {
    if (buttonEl) {
      buttonEl.disabled = false;
      buttonEl.innerHTML = originalText;
    }
  }
}

async function updateMatchStatus(matchId, status, buttonEl) {
  if (buttonEl) buttonEl.disabled = true;
  try {
    const res = await authFetch(`/api/v1/correlate/matches/${matchId}?match_status=${status}`, { method: 'PATCH' });
    if (res && res.ok) {
      loadCorrelationData(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Failed to update review status: ${errData.detail || 'Unknown error'}`);
      if (buttonEl) buttonEl.disabled = false;
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
    if (buttonEl) buttonEl.disabled = false;
  }
}

/* ==========================================================================
   PANE 6: TIMELINE RECONSTRUCTION (M12)
   ========================================================================== */

async function loadTimelineData(caseId) {
  const container = document.getElementById('timeline-stream-container');
  if (!container) return;

  if (!caseId) {
    container.innerHTML = '<p style="color: var(--text-muted);">No active case selected.</p>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/timeline`);
    if (!res || !res.ok) return;

    const events = await res.json();
    if (events.length === 0) {
      container.innerHTML = '<p style="color: var(--text-muted);">No timeline events recorded yet. Ingest and parse evidence files to populate chronological events.</p>';
      return;
    }

    container.innerHTML = events.map(evt => `
      <div class="timeline-item">
        <div class="timeline-timestamp">${new Date(evt.event_timestamp).toLocaleString()}</div>
        <div class="timeline-title">
          <span class="badge badge-open" style="font-size: 0.7rem; margin-right: 0.4rem;">${escapeHtml(evt.event_type || 'EVENT')}</span>
          ${escapeHtml(evt.title)}
          ${evt.evidence_filename ? `<span style="font-size: 0.8rem; color: var(--text-muted); font-weight: normal;">(File: ${escapeHtml(evt.evidence_filename)})</span>` : ''}
        </div>
        ${evt.description ? `<div class="timeline-desc">${escapeHtml(evt.description)}</div>` : ''}
      </div>
    `).join('');
  } catch (err) {
    console.error('Failed to load timeline data:', err);
  }
}

async function handleAddTimelineSubmit(e) {
  e.preventDefault();
  if (!currentCaseId) return;

  const btn = document.getElementById('btn-submit-timeline');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Recording...';

  const title = document.getElementById('timeline-event-title').value.trim();
  const dtVal = document.getElementById('timeline-event-datetime').value;
  const evtType = document.getElementById('timeline-event-type').value;
  const desc = document.getElementById('timeline-event-desc').value.trim();

  try {
    const res = await authFetch(`/api/v1/cases/${currentCaseId}/timeline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        case_id: currentCaseId,
        title,
        event_timestamp: new Date(dtVal).toISOString(),
        event_type: evtType,
        description: desc
      })
    });

    if (res && res.ok) {
      closeModal('modal-add-timeline-event');
      document.getElementById('form-add-timeline').reset();
      loadTimelineData(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Failed to add milestone: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Record Milestone';
  }
}

/* ==========================================================================
   PANE 7: INTERACTIVE RELATIONSHIP GRAPH CANVAS (M13)
   ========================================================================== */

async function loadGraphData(caseId) {
  if (!caseId) return;

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/graph`);
    if (!res || !res.ok) return;

    const data = await res.json();
    graphData = data;

    initGraphLayout();
    drawGraph();
  } catch (err) {
    console.error('Failed to load graph data:', err);
  }
}

function initGraphLayout() {
  const canvas = document.getElementById('graph-canvas');
  if (!canvas) return;

  const width = canvas.parentElement.clientWidth || 800;
  const height = canvas.parentElement.clientHeight || 600;

  // Layout nodes radially or clustered
  const nodeCount = graphData.nodes.length;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(width, height) * 0.35;

  graphData.nodes.forEach((node, i) => {
    if (node.x === undefined) {
      const angle = (i / Math.max(nodeCount, 1)) * 2 * Math.PI;
      node.x = centerX + radius * Math.cos(angle) + (Math.random() - 0.5) * 40;
      node.y = centerY + radius * Math.sin(angle) + (Math.random() - 0.5) * 40;
      node.radius = node.type === 'EVIDENCE' ? 16 : 11;
    }
  });

  graphState.scale = 1;
  graphState.offsetX = 0;
  graphState.offsetY = 0;
}

function drawGraph() {
  const canvas = document.getElementById('graph-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;

  const width = canvas.parentElement.clientWidth;
  const height = canvas.parentElement.clientHeight;

  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  ctx.scale(dpr, dpr);
  ctx.save();

  // Clear Canvas
  ctx.clearRect(0, 0, width, height);

  // Apply Pan & Zoom
  ctx.translate(graphState.offsetX, graphState.offsetY);
  ctx.scale(graphState.scale, graphState.scale);

  const nodeMap = new Map();
  graphData.nodes.forEach(n => nodeMap.set(n.id, n));

  // 1. Draw Links
  graphData.links.forEach(link => {
    const src = nodeMap.get(link.source);
    const tgt = nodeMap.get(link.target);
    if (!src || !tgt) return;

    ctx.beginPath();
    ctx.moveTo(src.x, src.y);
    ctx.lineTo(tgt.x, tgt.y);

    if (link.type === 'CONTAINMENT') {
      ctx.strokeStyle = 'rgba(100, 116, 139, 0.35)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
    } else if (link.type === 'MATCH') {
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.7)';
      ctx.lineWidth = 2;
      ctx.setLineDash([2, 2]);
    } else {
      ctx.strokeStyle = 'rgba(0, 229, 163, 0.6)';
      ctx.lineWidth = 2;
      ctx.setLineDash([]);
    }
    ctx.stroke();
    ctx.setLineDash([]);

    // Edge Label
    if (graphState.scale > 0.8 && link.label) {
      const midX = (src.x + tgt.x) / 2;
      const midY = (src.y + tgt.y) / 2;
      ctx.font = '9px monospace';
      ctx.fillStyle = 'rgba(148, 163, 184, 0.8)';
      ctx.fillText(link.label, midX + 3, midY - 3);
    }
  });

  // 2. Draw Nodes
  graphData.nodes.forEach(node => {
    const isSelected = graphState.selectedNode && graphState.selectedNode.id === node.id;
    const isHovered = graphState.hoveredNode && graphState.hoveredNode.id === node.id;

    const color = CATEGORY_COLORS[node.category] || CATEGORY_COLORS[node.type] || CATEGORY_COLORS.DEFAULT;

    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius + (isHovered ? 3 : 0), 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();

    if (isSelected || isHovered) {
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#ffffff';
      ctx.stroke();
    } else {
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.stroke();
    }

    // Node Label
    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#f8fafc';
    ctx.textAlign = 'center';
    const displayLabel = node.label.length > 20 ? node.label.substring(0, 18) + '...' : node.label;
    ctx.fillText(displayLabel, node.x, node.y + node.radius + 13);
  });

  ctx.restore();
}

function initGraphInteraction() {
  const canvas = document.getElementById('graph-canvas');
  if (!canvas) return;

  canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = (e.clientX - rect.left - graphState.offsetX) / graphState.scale;
    const mouseY = (e.clientY - rect.top - graphState.offsetY) / graphState.scale;

    const clickedNode = graphData.nodes.find(n => {
      const dx = n.x - mouseX;
      const dy = n.y - mouseY;
      return Math.sqrt(dx * dx + dy * dy) <= n.radius + 4;
    });

    if (clickedNode) {
      graphState.selectedNode = clickedNode;
      showNodeDrawer(clickedNode);
      drawGraph();
    } else {
      graphState.isDragging = true;
      graphState.dragStartX = e.clientX - graphState.offsetX;
      graphState.dragStartY = e.clientY - graphState.offsetY;
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (graphState.isDragging) {
      graphState.offsetX = e.clientX - graphState.dragStartX;
      graphState.offsetY = e.clientY - graphState.dragStartY;
      drawGraph();
      return;
    }

    if (currentTab === 'graph') {
      const rect = canvas.getBoundingClientRect();
      const mouseX = (e.clientX - rect.left - graphState.offsetX) / graphState.scale;
      const mouseY = (e.clientY - rect.top - graphState.offsetY) / graphState.scale;

      const hovered = graphData.nodes.find(n => {
        const dx = n.x - mouseX;
        const dy = n.y - mouseY;
        return Math.sqrt(dx * dx + dy * dy) <= n.radius + 4;
      });

      if (hovered !== graphState.hoveredNode) {
        graphState.hoveredNode = hovered;
        canvas.style.cursor = hovered ? 'pointer' : 'grab';
        drawGraph();
      }
    }
  });

  window.addEventListener('mouseup', () => {
    graphState.isDragging = false;
  });

  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.1 : 0.9;
    zoomGraph(zoomFactor);
  });
}

function zoomGraph(factor) {
  graphState.scale = Math.max(0.3, Math.min(graphState.scale * factor, 3.5));
  drawGraph();
}

function resetGraphView() {
  graphState.scale = 1;
  graphState.offsetX = 0;
  graphState.offsetY = 0;
  drawGraph();
}

function showNodeDrawer(node) {
  const drawer = document.getElementById('graph-node-drawer');
  const labelEl = document.getElementById('drawer-node-label');
  const typeEl = document.getElementById('drawer-node-type');
  const detailsEl = document.getElementById('drawer-node-details');

  if (!drawer) return;

  if (labelEl) labelEl.textContent = node.label;
  if (typeEl) {
    typeEl.textContent = node.category || node.type;
    typeEl.style.borderColor = CATEGORY_COLORS[node.category] || 'var(--accent-primary)';
    typeEl.style.color = CATEGORY_COLORS[node.category] || 'var(--accent-primary)';
  }
  if (detailsEl) detailsEl.textContent = node.details || 'No additional metadata available.';

  drawer.style.display = 'block';
}

/* ==========================================================================
   PANE 8: CHAIN OF CUSTODY AUDIT LOGS (M15)
   ========================================================================== */

async function loadAuditLogs(caseId) {
  const tbody = document.getElementById('audit-full-table-body');
  if (!tbody) return;

  if (!caseId) {
    tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No active case selected.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/summary`);
    if (!res || !res.ok) return;

    const summary = await res.json();
    if (!summary.recent_audit_logs || summary.recent_audit_logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No chain of custody logs recorded for this case container.</td></tr>';
      return;
    }

    tbody.innerHTML = summary.recent_audit_logs.map(log => `
      <tr>
        <td><strong style="color: var(--accent-primary);">${escapeHtml(log.action)}</strong></td>
        <td>${escapeHtml(log.actor || 'Investigator')}</td>
        <td>${escapeHtml(log.details || '-')}</td>
        <td>${new Date(log.timestamp).toLocaleString()}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load audit logs:', err);
  }
}

/* ==========================================================================
   PANE 9: ADMINISTRATIVE GOVERNANCE & USER MANAGEMENT (ADMIN ONLY)
   ========================================================================== */

async function loadAdminGovernanceData() {
  await Promise.all([loadAdminUsers(), loadAdminAuditLogs()]);
}

async function loadAdminUsers() {
  const tbody = document.getElementById('admin-users-table-body');
  if (!tbody) return;

  try {
    const res = await authFetch('/api/v1/auth/users');
    if (!res) return;
    if (res.status === 403) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--accent-primary); text-align: center;">Access Forbidden: Requires Administrator Authority.</td></tr>';
      return;
    }
    if (!res.ok) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">Failed to load user accounts.</td></tr>';
      return;
    }

    const users = await res.json();
    if (users.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">No user accounts found.</td></tr>';
      return;
    }

    tbody.innerHTML = users.map(u => `
      <tr>
        <td><strong>${escapeHtml(u.username)}</strong></td>
        <td>${escapeHtml(u.full_name || '-')}</td>
        <td>${escapeHtml(u.email)}</td>
        <td>
          <span class="user-role-badge ${u.role === 'ADMIN' ? 'role-admin' : 'role-investigator'}">
            ${escapeHtml(u.role)}
          </span>
        </td>
        <td>
          <span class="badge ${u.is_active ? 'badge-verified' : 'badge-tampered'}">
            ${u.is_active ? 'ACTIVE' : 'INACTIVE'}
          </span>
        </td>
        <td>
          <button class="btn ${u.is_active ? 'btn-danger' : 'btn-primary'} btn-sm"
                  data-action="toggle-user-status"
                  data-id="${u.id}"
                  data-active="${u.is_active}"
                  aria-label="${u.is_active ? 'Deactivate' : 'Activate'} user account">
            ${u.is_active ? 'Deactivate' : 'Activate'}
          </button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load admin users:', err);
    tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted); text-align: center;">Error loading user directory.</td></tr>';
  }
}

async function loadAdminAuditLogs() {
  const tbody = document.getElementById('admin-audit-table-body');
  if (!tbody) return;

  try {
    const res = await authFetch('/api/v1/auth/audit-all');
    if (!res) return;
    if (res.status === 403) {
      tbody.innerHTML = '<tr><td colspan="4" style="color: var(--accent-primary); text-align: center;">Access Forbidden: Requires Administrator Authority.</td></tr>';
      return;
    }
    if (!res.ok) {
      tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">Failed to load global audit trail.</td></tr>';
      return;
    }

    const logs = await res.json();
    if (logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">No audit logs recorded.</td></tr>';
      return;
    }

    tbody.innerHTML = logs.map(l => `
      <tr>
        <td><strong style="color: var(--accent-primary);">${escapeHtml(l.action)}</strong></td>
        <td>${escapeHtml(l.actor || 'System')}</td>
        <td>${escapeHtml(l.details || '-')}</td>
        <td>${new Date(l.timestamp).toLocaleString()}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load global audit logs:', err);
    tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted); text-align: center;">Error loading audit logs.</td></tr>';
  }
}

async function toggleUserStatus(userId, currentActive, buttonEl) {
  const targetAction = currentActive ? 'deactivate' : 'activate';
  if (!confirm(`Are you sure you want to ${targetAction} this user account?`)) {
    return;
  }

  if (buttonEl) {
    buttonEl.disabled = true;
    buttonEl.innerHTML = '<span class="spinner"></span> Updating...';
  }

  try {
    const res = await authFetch(`/api/v1/auth/users/${userId}/status?is_active=${!currentActive}`, {
      method: 'PATCH'
    });

    if (res && res.ok) {
      await loadAdminUsers();
      notifyInvestigator(`User account successfully ${targetAction}d.`);
    } else {
      const err = await res.json();
      notifyInvestigator(`Failed to update user status: ${err.detail || 'Unknown error'}`, true);
      if (buttonEl) buttonEl.disabled = false;
    }
  } catch (err) {
    notifyInvestigator(`Error updating user status: ${err.message}`, true);
    if (buttonEl) buttonEl.disabled = false;
  }
}

async function adminApproveCaseStatus(caseId, targetStatus) {
  if (!confirm(`Approve updating case status to '${targetStatus}'?`)) return;

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: targetStatus })
    });

    if (res && res.ok) {
      notifyInvestigator(`Case status updated to '${targetStatus}' successfully.`);
      await loadCasesTable();
      await loadCasesDropdown();
    } else {
      const err = await res.json();
      notifyInvestigator(`Governance Error: ${err.detail || 'Failed to update case'}`, true);
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
  }
}

async function adminDeleteCase(caseId) {
  if (!confirm('CAUTION: Are you sure you want to PERMANENTLY delete this case container and all its associated evidence records? This action is irreversible.')) {
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}`, {
      method: 'DELETE'
    });

    if (res && res.ok) {
      notifyInvestigator('Case container permanently deleted by Administrator.');
      if (currentCaseId === caseId) {
        currentCaseId = null;
      }
      await loadCasesDropdown();
      await loadCasesTable();
    } else {
      const err = await res.json();
      notifyInvestigator(`Delete Error: ${err.detail || 'Failed to delete case'}`, true);
    }
  } catch (err) {
    notifyInvestigator(`Error: ${err.message}`, true);
  }
}

/* ==========================================================================
   SECURITY & STRING UTILITIES
   ========================================================================== */

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
