/**
 * SECE — Unified Digital Forensics Workstation Main Application Engine
 */

let currentCaseId = null;
let currentTab = 'overview';
let activeFilterEntityType = 'ALL';

document.addEventListener('DOMContentLoaded', async () => {
  // Render user info in top-bar
  const user = getUser();
  if (user) {
    const nameEl = document.getElementById('user-display-name');
    const roleEl = document.getElementById('user-role-tag');
    if (nameEl) nameEl.textContent = user.full_name || user.username || 'Investigator';
    if (roleEl) roleEl.textContent = (user.role || 'INVESTIGATOR').toUpperCase();
  }

  // Load cases dropdown
  await loadCasesDropdown();
});

/**
 * Tab Navigation Controller
 */
function switchTab(tabName) {
  currentTab = tabName;

  // Update nav links active class
  const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
  navItems.forEach(item => item.classList.remove('active'));

  const activeNav = document.getElementById(`nav-${tabName}`);
  if (activeNav) activeNav.classList.add('active');

  // Update tab panes active class
  const panes = document.querySelectorAll('.tab-pane');
  panes.forEach(pane => pane.classList.remove('active'));

  const activePane = document.getElementById(`pane-${tabName}`);
  if (activePane) activePane.classList.add('active');

  // Refresh active tab content
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
  } else if (currentTab === 'audit') {
    loadAuditLogs(currentCaseId);
  }
}

/**
 * Case Selector Controller
 */
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
      opt.textContent = '-- No Cases Found (Create One) --';
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

    refreshActiveTab();
  } catch (err) {
    console.error('Failed to load cases:', err);
  }
}

function handleCaseSelectChange(caseId) {
  currentCaseId = caseId;
  refreshActiveTab();
}

/**
 * PANE 1: Overview Controller
 */
async function loadCaseOverview(caseId) {
  const titleEl = document.getElementById('overview-case-title');
  const descEl = document.getElementById('overview-case-desc');
  const statusEl = document.getElementById('overview-case-status');
  const auditBody = document.querySelector('#overview-audit-table tbody');

  if (!caseId) {
    if (titleEl) titleEl.textContent = 'No Active Case Selected';
    if (descEl) descEl.textContent = 'Please create a new case container or select an existing case from the header dropdown.';
    if (statusEl) statusEl.textContent = 'N/A';
    if (auditBody) auditBody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No active case selected.</td></tr>';
    updateMetrics(0, 0, 0, 0);
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/summary`);
    if (!res || !res.ok) return;

    const summary = await res.json();

    // Update metrics
    let totalEntities = 0;
    if (summary.entities_summary) {
      Object.values(summary.entities_summary).forEach(count => totalEntities += count);
    }

    updateMetrics(
      summary.total_evidence_files || 0,
      totalEntities,
      summary.total_relationships || 0,
      summary.pending_candidate_matches || 0
    );

    // Update case info
    if (titleEl) titleEl.textContent = summary.title ? `[${summary.case_number}] ${summary.title}` : `Case #${summary.case_number}`;
    if (descEl) descEl.textContent = summary.description || 'No description provided for this case.';
    if (statusEl) {
      statusEl.textContent = (summary.status || 'OPEN').replace('_', ' ');
      statusEl.className = `badge badge-${(summary.status || 'open').toLowerCase()}`;
    }

    // Update recent audit activity
    if (auditBody) {
      if (!summary.recent_audit_logs || summary.recent_audit_logs.length === 0) {
        auditBody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No audit entries recorded yet.</td></tr>';
      } else {
        auditBody.innerHTML = summary.recent_audit_logs.map(log => `
          <tr>
            <td><strong style="color: var(--primary);">${log.action}</strong></td>
            <td>Investigator</td>
            <td>${log.details || '-'}</td>
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

/**
 * PANE 2: Case Management Controller
 */
async function loadCasesTable() {
  const tbody = document.getElementById('cases-table-body');
  if (!tbody) return;

  try {
    const res = await authFetch('/api/v1/cases/');
    if (!res || !res.ok) return;

    const cases = await res.json();
    if (cases.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted);">No cases found. Click "Create New Case" to get started.</td></tr>';
      return;
    }

    tbody.innerHTML = cases.map(c => `
      <tr>
        <td><strong>${c.case_number}</strong></td>
        <td>${c.title}</td>
        <td><span class="badge badge-${(c.status || 'open').toLowerCase()}">${c.status.replace('_', ' ')}</span></td>
        <td>Investigator</td>
        <td>${new Date(c.created_at).toLocaleDateString()}</td>
        <td>
          ${c.id === currentCaseId 
            ? '<span class="badge badge-open">Active Case</span>'
            : `<button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="setActiveCase('${c.id}')">Select Active</button>`
          }
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load cases table:', err);
  }
}

function setActiveCase(caseId) {
  currentCaseId = caseId;
  const selectEl = document.getElementById('active-case-select');
  if (selectEl) selectEl.value = caseId;
  switchTab('overview');
}

/**
 * PANE 3: Evidence Ledger Controller
 */
async function loadEvidenceLedger(caseId) {
  const tbody = document.getElementById('evidence-table-body');
  if (!tbody) return;

  if (!caseId) {
    tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted);">No active case selected. Select or create a case first.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/evidence/`);
    if (!res || !res.ok) return;

    const evidenceList = await res.json();
    if (evidenceList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="color: var(--text-muted);">No evidence files uploaded to this case yet. Click "+ Upload Evidence File" to ingest.</td></tr>';
      return;
    }

    tbody.innerHTML = evidenceList.map(e => `
      <tr>
        <td><strong>${e.original_filename}</strong></td>
        <td><span class="badge badge-open">${e.evidence_type}</span></td>
        <td>${(e.file_size_bytes / 1024).toFixed(1)} KB</td>
        <td><code style="font-size: 0.75rem;">${e.sha256_hash ? e.sha256_hash.substring(0, 16) + '...' : '-'}</code></td>
        <td><span class="badge badge-${e.processing_status === 'EXTRACTED' || e.processing_status === 'PARSED' ? 'open' : 'closed'}">${e.processing_status}</span></td>
        <td>
          <div style="display: flex; gap: 0.35rem;">
            <button class="btn btn-secondary" style="padding: 0.2rem 0.4rem; font-size: 0.75rem;" onclick="parseEvidenceFile('${e.id}')">⚡ Parse</button>
            <button class="btn btn-primary" style="padding: 0.2rem 0.4rem; font-size: 0.75rem;" onclick="extractEntities('${e.id}')">🏷️ Extract</button>
            <button class="btn btn-secondary" style="padding: 0.2rem 0.4rem; font-size: 0.75rem;" onclick="verifyIntegrity('${e.id}')">🛡️ Verify</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load evidence ledger:', err);
  }
}

async function parseEvidenceFile(evidenceId) {
  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/parse`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      alert(`Evidence Parsed Successfully!\n\nText Preview: ${data.text_preview.substring(0, 150)}...`);
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Parsing Error: ${errData.detail || 'Failed to parse file'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

async function extractEntities(evidenceId) {
  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/extract-entities`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      alert(`Entities Extracted!\nTotal Mentions: ${data.total_mentions_extracted}\nDistinct Canonical Entities: ${data.distinct_canonical_entities}`);
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Extraction Error: ${errData.detail || 'Failed to extract entities'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

async function verifyIntegrity(evidenceId) {
  try {
    const res = await authFetch(`/api/v1/evidence/${evidenceId}/verify-integrity`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      if (data.is_valid) {
        alert(`✅ INTEGRITY VERIFIED (PASS)\nFilename: ${data.original_filename}\nSHA256 Match: ${data.calculated_sha256_hash}`);
      } else {
        alert(`❌ INTEGRITY FAILURE (TAMPER DETECTED)\nStored Hash: ${data.stored_sha256_hash}\nCalculated Hash: ${data.calculated_sha256_hash}`);
      }
    } else {
      const errData = await res.json();
      alert(`Integrity Verification Error: ${errData.detail || 'Failed to verify file'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

/**
 * PANE 4: Extracted Entities Controller
 */
async function loadEntities(caseId) {
  const container = document.getElementById('canonical-entities-container');
  const filtersDiv = document.getElementById('entity-type-filters');
  const mentionsTbody = document.getElementById('mentions-table-body');

  if (!container) return;

  if (!caseId) {
    container.innerHTML = '<p style="color: var(--text-muted);">No active case selected.</p>';
    if (mentionsTbody) mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted);">No active case selected.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/entities`);
    if (!res || !res.ok) return;

    const entities = await res.json();

    if (entities.length === 0) {
      container.innerHTML = '<p style="color: var(--text-muted);">No canonical entities discovered yet. Upload evidence files and run extraction.</p>';
      if (filtersDiv) filtersDiv.innerHTML = '';
      if (mentionsTbody) mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted);">No entity mentions extracted yet.</td></tr>';
      return;
    }

    // Build filter buttons
    const types = ['ALL', ...new Set(entities.map(e => e.entity_type))];
    if (filtersDiv) {
      filtersDiv.innerHTML = types.map(t => `
        <button class="btn ${activeFilterEntityType === t ? 'btn-primary' : 'btn-secondary'}" 
                style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" 
                onclick="filterEntitiesByType('${t}')">${t}</button>
      `).join('');
    }

    // Render entity cards
    const filteredEntities = activeFilterEntityType === 'ALL' 
      ? entities 
      : entities.filter(e => e.entity_type === activeFilterEntityType);

    container.innerHTML = filteredEntities.map(e => `
      <div class="card" style="padding: 1rem; border-left: 3px solid var(--primary);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <span class="badge badge-open">${e.entity_type}</span>
          <span style="font-size: 0.8rem; color: var(--text-muted);">${e.mention_count || 1} Mention(s)</span>
        </div>
        <div style="font-size: 1.05rem; font-weight: 600; font-family: var(--font-mono);">${e.canonical_name}</div>
      </div>
    `).join('');

    // Also fetch raw evidence mentions if available
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
      mentionsTbody.innerHTML = '<tr><td colspan="5" style="color: var(--text-muted);">No raw entity mentions extracted yet.</td></tr>';
      return;
    }

    mentionsTbody.innerHTML = allMentions.map(m => `
      <tr>
        <td><span class="badge badge-open">${m.entity_type}</span></td>
        <td><code>${m.raw_value}</code></td>
        <td><code>${m.normalized_value}</code></td>
        <td>${m.start_offset != null ? `[${m.start_offset}:${m.end_offset}]` : '-'}</td>
        <td style="font-size: 0.85rem; color: var(--text-muted);">${m.context_snippet ? '...' + m.context_snippet + '...' : '-'}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load entity mentions:', err);
  }
}

/**
 * PANE 5: Correlation Engine Controller
 */
async function loadCorrelationData(caseId) {
  const matchesTbody = document.getElementById('matches-table-body');
  const relsTbody = document.getElementById('relationships-table-body');

  if (!matchesTbody || !relsTbody) return;

  if (!caseId) {
    matchesTbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No active case selected.</td></tr>';
    relsTbody.innerHTML = '<tr><td colspan="3" style="color: var(--text-muted);">No active case selected.</td></tr>';
    return;
  }

  try {
    // Load Candidate Matches
    const resM = await authFetch(`/api/v1/cases/${caseId}/matches`);
    if (resM && resM.ok) {
      const matches = await resM.json();
      if (matches.length === 0) {
        matchesTbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No candidate matches discovered yet. Click "⚡ Run Correlation Engine" to analyze.</td></tr>';
      } else {
        matchesTbody.innerHTML = matches.map(m => `
          <tr>
            <td><strong>${m.confidence_score}</strong></td>
            <td>${m.match_rationale}</td>
            <td><span class="badge badge-${m.status === 'ACCEPTED' ? 'open' : m.status === 'REJECTED' ? 'closed' : 'in-progress'}">${m.status}</span></td>
            <td>
              <div style="display: flex; gap: 0.35rem;">
                <button class="btn btn-primary" style="padding: 0.2rem 0.4rem; font-size: 0.75rem;" onclick="updateMatchStatus('${m.id}', 'ACCEPTED')">Accept</button>
                <button class="btn btn-secondary" style="padding: 0.2rem 0.4rem; font-size: 0.75rem;" onclick="updateMatchStatus('${m.id}', 'REJECTED')">Reject</button>
              </div>
            </td>
          </tr>
        `).join('');
      }
    }

    // Load Relationships
    const resR = await authFetch(`/api/v1/cases/${caseId}/relationships`);
    if (resR && resR.ok) {
      const rels = await resR.json();
      if (rels.length === 0) {
        relsTbody.innerHTML = '<tr><td colspan="3" style="color: var(--text-muted);">No cross-evidence relationships generated yet. Click "⚡ Run Correlation Engine".</td></tr>';
      } else {
        relsTbody.innerHTML = rels.map(r => `
          <tr>
            <td><span class="badge badge-open">${r.relationship_type}</span></td>
            <td><strong>${r.confidence_score}</strong></td>
            <td>${r.rationale || '-'}</td>
          </tr>
        `).join('');
      }
    }
  } catch (err) {
    console.error('Failed to load correlation data:', err);
  }
}

async function triggerCorrelationPipeline() {
  if (!currentCaseId) {
    alert('Please select an active case container first.');
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${currentCaseId}/correlate`, { method: 'POST' });
    if (res && res.ok) {
      const data = await res.json();
      alert(`Correlation Complete!\nCandidate Matches: ${data.total_candidate_matches}\nRelationships Discovered: ${data.total_relationships}`);
      loadCorrelationData(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Correlation Error: ${errData.detail || 'Failed to run correlation pipeline'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

async function updateMatchStatus(matchId, status) {
  try {
    const res = await authFetch(`/api/v1/correlate/matches/${matchId}?match_status=${status}`, { method: 'PATCH' });
    if (res && res.ok) {
      loadCorrelationData(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Failed to update status: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

/**
 * PANE 6: Chain of Custody Audit Log Controller
 */
async function loadAuditLogs(caseId) {
  const tbody = document.getElementById('audit-full-table-body');
  if (!tbody) return;

  if (!caseId) {
    tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No active case selected.</td></tr>';
    return;
  }

  try {
    const res = await authFetch(`/api/v1/cases/${caseId}/summary`);
    if (!res || !res.ok) return;

    const summary = await res.json();
    if (!summary.recent_audit_logs || summary.recent_audit_logs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="color: var(--text-muted);">No chain of custody logs recorded for this case container.</td></tr>';
      return;
    }

    tbody.innerHTML = summary.recent_audit_logs.map(log => `
      <tr>
        <td><strong style="color: var(--primary);">${log.action}</strong></td>
        <td>Investigator</td>
        <td>${log.details || '-'}</td>
        <td>${new Date(log.timestamp).toLocaleString()}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Failed to load audit logs:', err);
  }
}

/**
 * MODAL CONTROLLERS & FORM SUBMISSIONS
 */
function openCreateCaseModal() {
  document.getElementById('modal-create-case').style.display = 'flex';
}

function closeCreateCaseModal() {
  document.getElementById('modal-create-case').style.display = 'none';
}

async function handleCreateCaseSubmit(e) {
  e.preventDefault();
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
      closeCreateCaseModal();
      currentCaseId = newCase.id;
      await loadCasesDropdown();
      switchTab('overview');
    } else {
      const errData = await res.json();
      alert(`Failed to create case: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

function openUploadEvidenceModal() {
  if (!currentCaseId) {
    alert('Please select an active case container before uploading evidence.');
    return;
  }
  document.getElementById('modal-upload-evidence').style.display = 'flex';
}

function closeUploadEvidenceModal() {
  document.getElementById('modal-upload-evidence').style.display = 'none';
}

async function handleUploadEvidenceSubmit(e) {
  e.preventDefault();
  if (!currentCaseId) return;

  const fileInput = document.getElementById('upload-file');
  const typeInput = document.getElementById('upload-type');
  const descInput = document.getElementById('upload-desc');

  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Please select a file to upload.');
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
      closeUploadEvidenceModal();
      alert('Evidence File Ingested Successfully! SHA-256 Digest Computed and Stored.');
      loadEvidenceLedger(currentCaseId);
    } else {
      const errData = await res.json();
      alert(`Upload Failed: ${errData.detail || 'Unknown error'}`);
    }
  } catch (err) {
    alert(`Upload Error: ${err.message}`);
  }
}
