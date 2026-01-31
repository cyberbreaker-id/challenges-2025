package com.example.springapp.repository;

import com.example.springapp.model.Note;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Repository
public class NoteRepository {
    
    private final Map<String, Note> notes = new ConcurrentHashMap<>();
    private final Map<String, Set<String>> userNotes = new ConcurrentHashMap<>();
    private int nextNoteId = 1;

    public Note save(Note note) {
        if (note.getId() == null) {
            note.setId(String.valueOf(nextNoteId++));
        }
        notes.put(note.getId(), note);
        
        userNotes.computeIfAbsent(note.getUserId(), k -> ConcurrentHashMap.newKeySet()).add(note.getId());
        
        return note;
    }

    public Optional<Note> findById(String id) {
        return Optional.ofNullable(notes.get(id));
    }

    public List<Note> findByUserId(String userId) {
        Set<String> noteIds = userNotes.get(userId);
        if (noteIds == null) {
            return new ArrayList<>();
        }
        
        return noteIds.stream()
                .map(notes::get)
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
    }

    public List<Note> findByUserIdAndTitleContaining(String userId, String titleKeyword) {
        return findByUserId(userId).stream()
                .filter(note -> note.getTitle().toLowerCase().contains(titleKeyword.toLowerCase()))
                .collect(Collectors.toList());
    }

    public List<Note> findAll() {
        return new ArrayList<>(notes.values());
    }

    public void deleteById(String id) {
        Note note = notes.remove(id);
        if (note != null) {
            Set<String> noteIds = userNotes.get(note.getUserId());
            if (noteIds != null) {
                noteIds.remove(id);
                if (noteIds.isEmpty()) {
                    userNotes.remove(note.getUserId());
                }
            }
        }
    }

    public void deleteByUserId(String userId) {
        Set<String> noteIds = userNotes.remove(userId);
        if (noteIds != null) {
            noteIds.forEach(notes::remove);
        }
    }

    public boolean existsByIdAndUserId(String id, String userId) {
        Note note = notes.get(id);
        return note != null && userId.equals(note.getUserId());
    }

    public long count() {
        return notes.size();
    }

    public long countByUserId(String userId) {
        Set<String> noteIds = userNotes.get(userId);
        return noteIds != null ? noteIds.size() : 0;
    }
}