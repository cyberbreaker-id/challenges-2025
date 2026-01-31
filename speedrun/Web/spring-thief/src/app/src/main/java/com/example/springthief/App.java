package com.example.springthief;

import org.springframework.web.bind.annotation.*;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import java.util.List;
import java.util.ArrayList;

@SpringBootApplication
@RestController
public class App extends SpringBootServletInitializer
{
    @Autowired
    private NoteService noteService;
    
    @Autowired
    private UserService userService;
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
         return application.sources(App.class);
    }

    public static void main(final String[] args) {
        SpringApplication.run(App.class, args);
    }
    
    
    
    
    @GetMapping("/notes")
    public ResponseEntity<List<Note>> getAllNotes(@RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        List<Note> userNotes = noteService.getNotesByAuthor(currentUser.getUsername());
        return ResponseEntity.ok(userNotes);
    }
    
    @GetMapping("/notes/{id}")
    public ResponseEntity<Note> getNoteById(@PathVariable Long id, @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        Note note = noteService.getNoteById(id);
        if (note != null && note.getAuthor().equals(currentUser.getUsername())) {
            return ResponseEntity.ok(note);
        }
        return ResponseEntity.notFound().build();
    }
    
    @PostMapping("/notes")
    public ResponseEntity<Note> createNote(@RequestParam String title, 
                                         @RequestParam String content, 
                                         @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        Note note = noteService.createNote(title, content, currentUser.getUsername());
        return ResponseEntity.ok(note);
    }
    
    @PutMapping("/notes/{id}")
    public ResponseEntity<Note> updateNote(@PathVariable Long id, 
                                          @RequestParam(required = false) String title, 
                                          @RequestParam(required = false) String content,
                                          @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        Note existingNote = noteService.getNoteById(id);
        if (existingNote == null || !existingNote.getAuthor().equals(currentUser.getUsername())) {
            return ResponseEntity.notFound().build();
        }
        
        Note note = noteService.updateNote(id, title, content);
        return ResponseEntity.ok(note);
    }
    
    @DeleteMapping("/notes/{id}")
    public ResponseEntity<Void> deleteNote(@PathVariable Long id, @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        Note existingNote = noteService.getNoteById(id);
        if (existingNote == null || !existingNote.getAuthor().equals(currentUser.getUsername())) {
            return ResponseEntity.notFound().build();
        }
        
        if (noteService.deleteNote(id)) {
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.notFound().build();
    }
    
    @GetMapping("/notes/author/{author}")
    public ResponseEntity<List<Note>> getNotesByAuthor(@PathVariable String author, @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return ResponseEntity.badRequest().build();
        }
        
        if (!author.equals(currentUser.getUsername())) {
            return ResponseEntity.badRequest().build();
        }
        
        List<Note> notes = noteService.getNotesByAuthor(author);
        return ResponseEntity.ok(notes);
    }
    
    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestParam String username, 
                                          @RequestParam String password) {
        if (userService.usernameExists(username)) {
            return ResponseEntity.badRequest().body("Username already exists");
        }
        
        User user = userService.register(username, password);
        if (user != null) {
            return ResponseEntity.ok("User registered successfully");
        }
        return ResponseEntity.badRequest().body("Registration failed");
    }

    @RequestMapping("/search")
    String searchNotes(final Note note, @RequestParam String sessionId) {
        User currentUser = userService.getCurrentUser(sessionId);
        if (currentUser == null) {
            return "Invalid session";
        }
        
        List<Note> results = noteService.getNotesByAuthor(currentUser.getUsername());
        if (note.getTitle() != null && !note.getTitle().isEmpty()) {
            results = results.stream()
                .filter(n -> n.getTitle().toLowerCase().contains(note.getTitle().toLowerCase()))
                .collect(ArrayList::new, (list, n) -> list.add(n), (list1, list2) -> list1.addAll(list2));
        }
        if (note.getContent() != null && !note.getContent().isEmpty()) {
            results = results.stream()
                .filter(n -> n.getContent().toLowerCase().contains(note.getContent().toLowerCase()))
                .collect(ArrayList::new, (list, n) -> list.add(n), (list1, list2) -> list1.addAll(list2));
        }
        
        return "Found " + results.size() + " of your notes matching: " + note.toString();
    }
    
    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestParam String username, 
                                       @RequestParam String password) {
        String sessionId = userService.login(username, password);
        if (sessionId != null) {
            return ResponseEntity.ok(sessionId);
        }
        return ResponseEntity.badRequest().body("Invalid credentials");
    }
    
    @PostMapping("/logout")
    public ResponseEntity<String> logout(@RequestParam String sessionId) {
        if (userService.logout(sessionId)) {
            return ResponseEntity.ok("Logged out successfully");
        }
        return ResponseEntity.badRequest().body("Invalid session");
    }
    
}
