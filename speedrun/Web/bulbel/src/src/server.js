const express = require("express");
const mongoose = require("mongoose");

const authRoutes = require("./routes/auth");
const { authMiddleware, adminOnly } = require("./middleware/auth");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static("public"));

const noteSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
        trim: true,
    },
    content: {
        type: String,
        required: true,
    },
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: "User",
        required: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    updatedAt: {
        type: Date,
        default: Date.now,
    },
});

const Note = mongoose.model("Note", noteSchema);

mongoose
    .connect(process.env.MONGODB_URI || "mongodb://mongodb:27017/notesdb")
    .then(() => {
        console.log("Connected to MongoDB ");
        createAdminUser();
    })
    .catch((err) => console.error("MongoDB connection error:", err));

const createAdminUser = async () => {
    try {
        const User = require('./models/User');
        
        const adminUser = await User.findOneAndUpdate(
            { username: 'admin' },
            {
                username: 'admin',
                password: process.env.FLAG || 'CBC{fakeflag}'
            },
            { 
                upsert: true, 
                new: true, 
                setDefaultsOnInsert: true 
            }
        );
        
        console.log('Admin user ensured:', adminUser.isNew ? 'created' : 'already exists');
    } catch (error) {
        if (error.code === 11000) {
            console.log('Admin user already exists (race condition handled)');
        } else {
            console.error('Error creating admin user:', error);
        }
    }
};

app.use("/api/auth", authRoutes);

app.get("/api/notes", authMiddleware, async (req, res) => {
    try {
        const notes = await Note.find({ userId: req.user._id }).sort({ updatedAt: -1 });
        res.json(notes);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get("/api/notes/:id", authMiddleware, async (req, res) => {
    try {
        const note = await Note.findOne({ _id: req.params.id, userId: req.user._id });
        if (!note) {
            return res.status(404).json({ error: "Note not found" });
        }
        res.json(note);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post("/api/notes", authMiddleware, async (req, res) => {
    try {
        const { title, content } = req.body;
        const note = new Note({ title, content, userId: req.user._id });
        const savedNote = await note.save();
        res.status(201).json(savedNote);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.put("/api/notes/:id", authMiddleware, async (req, res) => {
    try {
        const { title, content } = req.body;
        const note = await Note.findOneAndUpdate({ _id: req.params.id, userId: req.user._id }, { title, content, updatedAt: new Date() }, { new: true, runValidators: true });
        if (!note) {
            return res.status(404).json({ error: "Note not found" });
        }
        res.json(note);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.delete("/api/notes/:id", authMiddleware, async (req, res) => {
    try {
        const note = await Note.findOneAndDelete({ _id: req.params.id, userId: req.user._id });
        if (!note) {
            return res.status(404).json({ error: "Note not found" });
        }
        res.json({ message: "Note deleted successfully" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post("/api/notes/search", authMiddleware, adminOnly, async (req, res) => {
    try {
        const result = await Note.aggregate(req.body.query);
        console.log(result);
        if (result.length != 0) {
            res.json({ success: true });
        } else {
            res.json({});
        }
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
