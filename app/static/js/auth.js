/**
 * SECE Authentication Guard & Helper Utilities
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
  removeToken();
  window.location.href = '/login';
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
