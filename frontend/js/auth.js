const API = 'http://localhost:8000';


function showRegister() {
  document.getElementById('login-form').style.display = 'none';
  document.getElementById('register-form').style.display = 'block';
}


function showLogin() {
  document.getElementById('register-form').style.display = 'none';
  document.getElementById('login-form').style.display = 'block';
}


async function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  const body = new URLSearchParams({ username, password });
  const res = await fetch(`${API}/api/users/login`, {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });
  if (res.ok) {
    const data = await res.json();
    localStorage.setItem('token', data.access_token);
    window.location.href = 'quotes.html';
  } else {
    document.getElementById('auth-error').textContent = 'Invalid username or password.';
  }
}


async function register() {
  const username = document.getElementById('reg-username').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const res = await fetch(`${API}/api/users/register`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  if (res.ok) {
    alert('Account created! Please log in.');
    showLogin();
  } else {
    const err = await res.json();
    document.getElementById('auth-error').textContent = err.detail || 'Registration failed.';
  }
}
