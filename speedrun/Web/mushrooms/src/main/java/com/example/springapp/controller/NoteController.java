package com.example.springapp.controller;

import com.example.springapp.model.Note;
import com.example.springapp.service.NoteService;
import com.example.springapp.service.AuthService;
import com.example.springapp.util.BasicAuthUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/notes")
public class NoteController {
    
    @Autowired
    private NoteService noteService;
    
    @Autowired
    private AuthService authService;

    @PostMapping
    public ResponseEntity<Map<String, Object>> createNote(@RequestHeader("Authorization") String authHeader, @RequestBody CreateNoteRequest request) {
        Map<String, Object> response = new HashMap<>();
        
        try {
            if (request.getTitle() == null || request.getContent() == null || request.getUserId() == null) {
                response.put("success", false);
                response.put("message", "Title, content, and userId are required");
                return ResponseEntity.badRequest().body(response);
            }
            
            String userId = validateBasicAuth(authHeader);
            if (userId == null) {
                response.put("success", false);
                response.put("message", "Unauthorized");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
            
            if (!userId.equals(request.getUserId())) {
                response.put("success", false);
                response.put("message", "Unauthorized - User ID mismatch");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
            
            Note note = noteService.createNote(request.getTitle(), request.getContent(), request.getUserId());
            
            response.put("success", true);
            response.put("message", "Note created successfully");
            response.put("note", convertNoteToMap(note));
            
            return ResponseEntity.ok(response);
            
        } catch (IllegalArgumentException e) {
            response.put("success", false);
            response.put("message", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", "Internal server error");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }

    @GetMapping("/{noteId}/user/{userId}")
    public ResponseEntity<Map<String, Object>> getNote(@RequestHeader("Authorization") String authHeader, @PathVariable String noteId, @PathVariable String userId) {
        Map<String, Object> response = new HashMap<>();
        
        try {
            String authenticatedUserId = validateBasicAuth(authHeader);
            if (authenticatedUserId == null || !authenticatedUserId.equals(userId)) {
                response.put("success", false);
                response.put("message", "Unauthorized");
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
            }
            
            Optional<Note> noteOpt = noteService.getNoteById(noteId, userId);
            
            if (noteOpt.isPresent()) {
                response.put("success", true);
                response.put("note", convertNoteToMap(noteOpt.get()));
                return ResponseEntity.ok(response);
            } else {
                response.put("success", false);
                response.put("message", "Note not found or access denied");
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
            }
            
        } catch (IllegalArgumentException e) {
            response.put("success", false);
            response.put("message", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", "Internal server error");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }

    private String validateBasicAuth(String authHeader) {
        String[] credentials = BasicAuthUtil.parseBasicAuth(authHeader);
        if (credentials == null) {
            return null;
        }
        
        String username = credentials[0];
        String password = credentials[1];
        
        return authService.login(username, password)
                .map(user -> user.getId())
                .orElse(null);
    }

    private Map<String, Object> convertNoteToMap(Note note) {
        Map<String, Object> noteMap = new HashMap<>();
        noteMap.put("id", note.getId());
        noteMap.put("title", note.getTitle());
        noteMap.put("content", note.getContent());
        noteMap.put("userId", note.getUserId());
        noteMap.put("createdAt", note.getCreatedAt().toString());
        noteMap.put("updatedAt", note.getUpdatedAt().toString());
        return noteMap;
    }

    public static class CreateNoteRequest {
        private String title;
        private String content;
        private String userId;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
    }

    public static class UpdateNoteRequest {
        private String title;
        private String content;
        private String userId;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
    }
}