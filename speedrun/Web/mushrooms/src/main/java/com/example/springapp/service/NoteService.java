package com.example.springapp.service;

import com.example.springapp.model.Note;
import com.example.springapp.repository.NoteRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class NoteService {
    
    @Autowired
    private NoteRepository noteRepository;
    
    @Autowired
    private AuthService authService;

    public Note createNote(String title, String content, String userId) {
        if (!authService.validateUser(userId)) {
            throw new IllegalArgumentException("Invalid user");
        }
        
        Note note = new Note(null, title, content, userId);
        Note savedNote = noteRepository.save(note);
        
        return savedNote;
    }

    public List<Note> getUserNotes(String userId) {
        if (!authService.validateUser(userId)) {
            throw new IllegalArgumentException("Invalid user");
        }
        
        List<Note> notes = noteRepository.findByUserId(userId);
        return notes;
    }

    public Optional<Note> getNoteById(String noteId, String userId) {
        if (!authService.validateUser(userId)) {
            throw new IllegalArgumentException("Invalid user");
        }
        
        Optional<Note> noteOpt = noteRepository.findById(noteId);
        if (noteOpt.isEmpty()) {
            return Optional.empty();
        }
        
        Note note = noteOpt.get();
        if (!note.getUserId().equals(userId)) {
            return Optional.empty();
        }
        
        return Optional.of(note);
    }

    public Optional<Note> updateNote(String noteId, String title, String content, String userId) {
        Optional<Note> noteOpt = getNoteById(noteId, userId);
        if (noteOpt.isEmpty()) {
            return Optional.empty();
        }
        
        Note note = noteOpt.get();
        note.setTitle(title);
        note.setContent(content);
        note.setUpdatedAt(LocalDateTime.now());
        
        Note updatedNote = noteRepository.save(note);
        return Optional.of(updatedNote);
    }

    public boolean deleteNote(String noteId, String userId) {
        if (!noteRepository.existsByIdAndUserId(noteId, userId)) {
            return false;
        }
        
        noteRepository.deleteById(noteId);
        return true;
    }

    public List<Note> searchNotes(String userId, String keyword) {
        if (!authService.validateUser(userId)) {
            throw new IllegalArgumentException("Invalid user");
        }
        
        List<Note> notes = noteRepository.findByUserIdAndTitleContaining(userId, keyword);
        return notes;
    }

    public long getUserNoteCount(String userId) {
        if (!authService.validateUser(userId)) {
            throw new IllegalArgumentException("Invalid user");
        }
        return noteRepository.countByUserId(userId);
    }
}