/**
 * SECE Authentication Guard & Helper Utilities
 * Exclusively locked to Crimson SOC Forensic Workstation
 */

function getToken() {
  return localStorage.getItem('sece_token');
}

function setToken(token) {
  localStorage.setItem('sece_token', token);
}

function removeToken() {
  localStorage.removeItem('sece_token');
  localStorage.removeItem('sece_user');
}

function getUser() {
  const userStr = localStorage.getItem('sece_user');
  try {
    return userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    return null;
  }
}

function setUser(userObj) {
  localStorage.setItem('sece_user', JSON.stringify(userObj));
}

function logout() {
  localStorage.clear();
  window.location.href = '/login';
}

function purgeLocalSession() {
  localStorage.clear();
  window.location.href = '/login';
}

function getTokenPayload() {
  const token = getToken();
  if (!token) return null;
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

function getSessionExpiryFormatted() {
  const payload = getTokenPayload();
  if (!payload || !payload.exp) return 'Unknown';
  
  const expDate = new Date(payload.exp * 1000);
  const now = new Date();
  const diffMs = expDate.getTime() - now.getTime();

  if (diffMs <= 0) {
    return 'Expired';
  }

  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

  if (hours > 0) {
    return `${hours}h ${minutes}m remaining`;
  }
  return `${minutes}m remaining`;
}

async function copySessionToken() {
  const token = getToken();
  if (!token) return false;
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(token);
      return true;
    } else {
      const textarea = document.createElement('textarea');
      textarea.value = token;
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      return true;
    }
  } catch (err) {
    return false;
  }
}

async function authFetch(url, options = {}) {
  const token = getToken();
  if (!token && !url.includes('/auth/login') && !url.includes('/auth/register')) {
    window.location.href = '/login';
    return;
  }

  options.headers = options.headers || {};
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, options);

  if (response.status === 401) {
    removeToken();
    window.location.href = '/login';
    return;
  }

  return response;
}
