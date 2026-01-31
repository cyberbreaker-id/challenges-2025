class NotesApp {
    constructor() {
        this.token = localStorage.getItem('token');
        this.currentUser = null;
        this.editingNoteId = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        
        if (this.token) {
            this.showApp();
            this.loadNotes();
        } else {
            this.showAuth();
        }
    }

    setupEventListeners() {
        document.getElementById('login').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('register').addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('show-register').addEventListener('click', (e) => this.showRegisterForm(e));
        document.getElementById('show-login').addEventListener('click', (e) => this.showLoginForm(e));
        document.getElementById('logout').addEventListener('click', () => this.logout());
        document.getElementById('note-form').addEventListener('submit', (e) => this.handleNoteSubmit(e));
        document.getElementById('cancel-btn').addEventListener('click', () => this.cancelEdit());
    }

    async makeRequest(url, options = {}) {
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(this.token && { 'Authorization': `Bearer ${this.token}` })
            },
            ...options
        };

        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showError(message) {
        const errorEl = document.getElementById('error-message');
        errorEl.textContent = message;
        errorEl.style.display = 'block';
        setTimeout(() => errorEl.style.display = 'none', 5000);
    }

    showAuth() {
        document.getElementById('auth-container').style.display = 'block';
        document.getElementById('app-container').style.display = 'none';
    }

    showApp() {
        document.getElementById('auth-container').style.display = 'none';
        document.getElementById('app-container').style.display = 'block';
        
        if (this.currentUser) {
            document.getElementById('user-info').textContent = `Welcome, ${this.currentUser.username}`;
        }
    }

    showRegisterForm(e) {
        e.preventDefault();
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('register-form').style.display = 'block';
    }

    showLoginForm(e) {
        e.preventDefault();
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
    }

    async handleLogin(e) {
        e.preventDefault();
        
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            this.showLoading();
            const data = await this.makeRequest('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });

            this.token = data.token;
            this.currentUser = data.user;
            localStorage.setItem('token', this.token);
            
            this.showApp();
            this.loadNotes();
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;

        try {
            this.showLoading();
            const data = await this.makeRequest('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });

            this.token = data.token;
            this.currentUser = data.user;
            localStorage.setItem('token', this.token);
            
            this.showApp();
            this.loadNotes();
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    logout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('token');
        this.showAuth();
        this.clearForms();
    }

    clearForms() {
        document.getElementById('login').reset();
        document.getElementById('register').reset();
        document.getElementById('note-form').reset();
        this.cancelEdit();
    }

    async loadNotes() {
        try {
            this.showLoading();
            const notes = await this.makeRequest('/api/notes');
            this.renderNotes(notes);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    renderNotes(notes) {
        const container = document.getElementById('notes-container');
        
        if (notes.length === 0) {
            container.innerHTML = '<div class="empty-state">No notes yet. Create your first note!</div>';
            return;
        }

        container.innerHTML = notes.map(note => `
            <div class="note-item" data-id="${note._id}">
                <div class="note-header">
                    <div class="note-title">${this.escapeHtml(note.title)}</div>
                    <div class="note-actions">
                        <button class="edit-btn" onclick="app.editNote('${note._id}')">Edit</button>
                        <button class="delete-btn" onclick="app.deleteNote('${note._id}')">Delete</button>
                    </div>
                </div>
                <div class="note-content">${this.escapeHtml(note.content)}</div>
                <div class="note-meta">
                    Created: ${new Date(note.createdAt).toLocaleDateString()}
                    ${note.updatedAt !== note.createdAt ? `| Updated: ${new Date(note.updatedAt).toLocaleDateString()}` : ''}
                </div>
            </div>
        `).join('');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async handleNoteSubmit(e) {
        e.preventDefault();
        
        const title = document.getElementById('note-title').value;
        const content = document.getElementById('note-content').value;

        try {
            this.showLoading();
            
            if (this.editingNoteId) {
                await this.makeRequest(`/api/notes/${this.editingNoteId}`, {
                    method: 'PUT',
                    body: JSON.stringify({ title, content })
                });
            } else {
                await this.makeRequest('/api/notes', {
                    method: 'POST',
                    body: JSON.stringify({ title, content })
                });
            }

            document.getElementById('note-form').reset();
            this.cancelEdit();
            this.loadNotes();
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    async editNote(noteId) {
        try {
            this.showLoading();
            const note = await this.makeRequest(`/api/notes/${noteId}`);
            
            document.getElementById('note-title').value = note.title;
            document.getElementById('note-content').value = note.content;
            document.getElementById('form-title').textContent = 'Edit Note';
            document.getElementById('save-btn').textContent = 'Update Note';
            document.getElementById('cancel-btn').style.display = 'inline-block';
            
            this.editingNoteId = noteId;
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    cancelEdit() {
        this.editingNoteId = null;
        document.getElementById('form-title').textContent = 'Add New Note';
        document.getElementById('save-btn').textContent = 'Save Note';
        document.getElementById('cancel-btn').style.display = 'none';
        document.getElementById('note-form').reset();
    }

    async deleteNote(noteId) {
        if (!confirm('Are you sure you want to delete this note?')) {
            return;
        }

        try {
            this.showLoading();
            await this.makeRequest(`/api/notes/${noteId}`, {
                method: 'DELETE'
            });
            this.loadNotes();
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }
}

const app = new NotesApp();