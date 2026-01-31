package com.example.springthief;

import org.springframework.stereotype.Service;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class NoteService
{
    private final Map<Long, Note> notes = new HashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    public List<Note> getAllNotes() {
        return new ArrayList<>(notes.values());
    }
    
    public Note getNoteById(Long id) {
        return notes.get(id);
    }
    
    public Note createNote(String title, String content, String author) {
        Note note = new Note(title, content, author);
        Long id = idGenerator.getAndIncrement();
        note.setId(id);
        notes.put(id, note);
        return note;
    }
    
    public Note updateNote(Long id, String title, String content) {
        Note note = notes.get(id);
        if (note != null) {
            if (title != null) {
                note.setTitle(title);
            }
            if (content != null) {
                note.setContent(content);
            }
        }
        return note;
    }
    
    public boolean deleteNote(Long id) {
        return notes.remove(id) != null;
    }
    
    public List<Note> getNotesByAuthor(String author) {
        return notes.values().stream()
            .filter(note -> note.getAuthor().equals(author))
            .collect(ArrayList::new, (list, note) -> list.add(note), (list1, list2) -> list1.addAll(list2));
    }
}