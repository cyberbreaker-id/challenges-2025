let token = localStorage.getItem('token');
let currentUser = localStorage.getItem('username');

function showLogin() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
}

function showRegister() {
    document.getElementById('login-form').classList.add('hidden');
    document.getElementById('register-form').classList.remove('hidden');
}

function showApp() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    document.getElementById('current-user').textContent = currentUser;
}

function showAuth() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('app').classList.add('hidden');
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.token;
            currentUser = data.user.username;
            localStorage.setItem('token', token);
            localStorage.setItem('username', currentUser);
            showApp();
            loadNotes();
        } else {
            alert('Login failed');
        }
    } catch (error) {
        alert('Login error: ' + error.message);
    }
}

async function register() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.token;
            currentUser = data.user.username;
            localStorage.setItem('token', token);
            localStorage.setItem('username', currentUser);
            showApp();
            loadNotes();
        } else {
            alert('Registration failed');
        }
    } catch (error) {
        alert('Registration error: ' + error.message);
    }
}

function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    showAuth();
}

async function loadNotes() {
    if (!token) return;
    
    try {
        const response = await fetch('/api/notes', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            const notes = await response.json();
            const notesDiv = document.getElementById('notes');
            notesDiv.innerHTML = '';
            notes.forEach(note => {
                const noteDiv = document.createElement('div');
                noteDiv.className = 'note';
                noteDiv.innerHTML = `
                    <h3>${note.title}</h3>
                    <p>${note.content}</p>
                    <button onclick="deleteNote(${note.id})">Delete</button>
                `;
                notesDiv.appendChild(noteDiv);
            });
        } else if (response.status === 401) {
            logout();
        }
    } catch (error) {
        console.error('Error loading notes:', error);
    }
}

async function createNote() {
    if (!token) return;
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    try {
        const response = await fetch('/api/notes', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title, content })
        });
        
        if (response.ok) {
            document.getElementById('title').value = '';
            document.getElementById('content').value = '';
            loadNotes();
        } else if (response.status === 401) {
            logout();
        }
    } catch (error) {
        console.error('Error creating note:', error);
    }
}

async function deleteNote(id) {
    if (!token) return;
    
    try {
        const response = await fetch(`/api/notes?id=${id}`, { 
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.ok) {
            loadNotes();
        } else if (response.status === 401) {
            logout();
        }
    } catch (error) {
        console.error('Error deleting note:', error);
    }
}

if (token && currentUser) {
    showApp();
    loadNotes();
} else {
    showAuth();
}