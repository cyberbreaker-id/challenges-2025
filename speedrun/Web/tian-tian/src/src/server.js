const express = require("express");

const authRoutes = require("./routes/auth");
const { authMiddleware, adminOnly } = require("./middleware/auth");
const crypto = require('crypto');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static("public"));

let nextNoteId = 1;
const notes = [];

class Note {
    constructor({ title, content, userId }) {
        this._id = nextNoteId++;
        this.title = title?.trim();
        this.content = content;
        this.userId = parseInt(userId);
        this.createdAt = new Date();
        this.updatedAt = new Date();
        
        if (!this.title || !this.content || !this.userId) {
            throw new Error('Title, content, and userId are required');
        }
    }

    static find({ userId }) {
        return notes
            .filter(n => n.userId == parseInt(userId))
            .sort((a, b) => b.updatedAt - a.updatedAt);
    }

    static findOne({ _id, userId }) {
        return notes.find(n => n._id == parseInt(_id) && n.userId == parseInt(userId)) || null;
    }

    static findOneAndUpdate({ _id, userId }, updates, options = {}) {
        const note = notes.find(n => n._id == parseInt(_id) && n.userId == parseInt(userId));
        if (!note) return null;
        
        Object.assign(note, updates);
        note.updatedAt = new Date();
        return note;
    }

    static findOneAndDelete({ _id, userId }) {
        const noteIndex = notes.findIndex(n => n._id == parseInt(_id) && n.userId == parseInt(userId));
        if (noteIndex === -1) return null;
        
        const note = notes[noteIndex];
        notes.splice(noteIndex, 1);
        return note;
    }

    static aggregate(query) {
        return notes;
    }

    save() {
        notes.push(this);
        return this;
    }
}


const createAdminUser = () => {
    try {
        const User = require('./models/User');
        const existingAdmin = User.findOne({ username: 'admin' });
        
        if (!existingAdmin) {
            const adminUser = new User({
                username: 'admin',
                password: crypto.randomBytes(64).toString('hex')
            });
            
            adminUser.save();
            console.log('Admin user created successfully');

            new Note({ title:"FLAG", content: process.env.FLAG || "CBC{fakeflag}", userId: adminUser._id }).save();
        } else {
            console.log('Admin user already exists');
        }
    } catch (error) {
        console.error('Error creating admin user:', error);
    }
};
createAdminUser();

app.use("/api/auth", authRoutes);

app.get("/api/notes", authMiddleware, (req, res) => {
    try {
        const notes = Note.find({ userId: req.user._id });
        res.json(notes);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get("/api/notes/:id", authMiddleware, (req, res) => {
    try {
        const note = Note.findOne({ _id: req.params.id, userId: req.user._id });
        if (!note) {
            return res.status(404).json({ error: "Note not found" });
        }
        res.json(note);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post("/api/notes", authMiddleware, (req, res) => {
    try {
        const { title, content } = req.body;
        const note = new Note({ title, content, userId: req.user._id });
        const savedNote = note.save();
        res.status(201).json(savedNote);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.put("/api/notes/:id", authMiddleware, (req, res) => {
    try {
        const { title, content } = req.body;
        const note = Note.findOneAndUpdate({ _id: req.params.id, userId: req.user._id }, { title, content, updatedAt: new Date() });
        if (!note) {
            return res.status(404).json({ error: "Note not found" });
        }
        res.json(note);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.get("/api/admin", authMiddleware, adminOnly, (req, res) => {
    try {
        
        res.json(notes);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get("/health", (req, res) => {
    res.json({ status: "OK", timestamp: new Date().toISOString() });
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});
