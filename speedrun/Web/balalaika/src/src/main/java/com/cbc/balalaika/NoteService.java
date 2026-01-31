package com.cbc.balalaika;

import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class NoteService {
    private final Map<String, Note> notes = new HashMap<>();

    public Note createNote(String title, String content, String userId) {
        String noteId = UUID.randomUUID().toString();
        Note note = new Note(noteId, title, content, userId);
        notes.put(noteId, note);
        return note;
    }

    public Note updateNote(String noteId, String title, String content, String userId) throws UnauthorizedException {
        Note note = notes.get(noteId);
        if (note == null) {
            return null;
        }
        
        if (!note.getUserId().equals(userId)) {
            throw new UnauthorizedException();
        }

        note.setTitle(title);
        note.setContent(content);
        return note;
    }

    public boolean deleteNote(String noteId, String userId) throws UnauthorizedException {
        Note note = notes.get(noteId);
        if (note == null) {
            return false;
        }
        
        if (!note.getUserId().equals(userId)) {
            throw new UnauthorizedException();
        }

        notes.remove(noteId);
        return true;
    }

    public Note getNote(String noteId, String userId) throws UnauthorizedException {
        Note note = notes.get(noteId);
        if (note == null) {
            return null;
        }
        
        if (!note.getUserId().equals(userId)) {
            throw new UnauthorizedException();
        }

        return note;
    }

    public List<Note> getUserNotes(String userId) {
        return notes.values().stream()
            .filter(note -> note.getUserId().equals(userId))
            .collect(Collectors.toList());
    }
}