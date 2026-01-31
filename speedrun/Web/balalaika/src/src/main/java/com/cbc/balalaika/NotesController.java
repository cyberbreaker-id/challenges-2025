package com.cbc.balalaika;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/notes")
public class NotesController {

    @Autowired
    private NoteService noteService;

    @Autowired
    private AuthorizationService authorizationService;

    private String getUserIdFromToken(String authHeader) throws UnauthorizedException {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw new UnauthorizedException();
        }
        String token = authHeader.substring(7);
        return authorizationService.getSubject(token);
    }

    @GetMapping
    public ResponseEntity<?> getUserNotes(@RequestHeader("Authorization") String authHeader) {
        try {
            String userId = getUserIdFromToken(authHeader);
            List<Note> notes = noteService.getUserNotes(userId);
            return ResponseEntity.ok(notes);
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ErrorResponse("Unauthorized"));
        }
    }

    @PostMapping
    public ResponseEntity<?> createNote(@RequestHeader("Authorization") String authHeader, 
                                      @RequestBody CreateNoteRequest request) {
        try {
            String userId = getUserIdFromToken(authHeader);
            Note note = noteService.createNote(request.getTitle(), request.getContent(), userId);
            return ResponseEntity.ok(note);
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ErrorResponse("Unauthorized"));
        }
    }

    @PutMapping("/{noteId}")
    public ResponseEntity<?> updateNote(@RequestHeader("Authorization") String authHeader,
                                      @PathVariable String noteId,
                                      @RequestBody UpdateNoteRequest request) {
        try {
            String userId = getUserIdFromToken(authHeader);
            Note note = noteService.updateNote(noteId, request.getTitle(), request.getContent(), userId);
            if (note == null) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok(note);
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ErrorResponse("Unauthorized"));
        }
    }

    @DeleteMapping("/{noteId}")
    public ResponseEntity<?> deleteNote(@RequestHeader("Authorization") String authHeader,
                                      @PathVariable String noteId) {
        try {
            String userId = getUserIdFromToken(authHeader);
            boolean deleted = noteService.deleteNote(noteId, userId);
            if (!deleted) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok().build();
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ErrorResponse("Unauthorized"));
        }
    }

    @GetMapping("/{noteId}")
    public ResponseEntity<?> getNote(@RequestHeader("Authorization") String authHeader,
                                   @PathVariable String noteId) {
        try {
            String userId = getUserIdFromToken(authHeader);
            Note note = noteService.getNote(noteId, userId);
            if (note == null) {
                return ResponseEntity.notFound().build();
            }
            return ResponseEntity.ok(note);
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(new ErrorResponse("Unauthorized"));
        }
    }

    public static class CreateNoteRequest {
        private String title;
        private String content;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
    }

    public static class UpdateNoteRequest {
        private String title;
        private String content;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
    }

    public static class ErrorResponse {
        private String error;

        public ErrorResponse(String error) {
            this.error = error;
        }

        public String getError() { return error; }
        public void setError(String error) { this.error = error; }
    }
}