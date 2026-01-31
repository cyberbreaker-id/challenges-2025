package com.example.springapp.config;

import com.example.springapp.model.Note;
import com.example.springapp.model.User;
import com.example.springapp.service.AuthService;
import com.example.springapp.service.NoteService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {
    
    @Autowired
    private AuthService authService;
    
    @Autowired
    private NoteService noteService;

    @Override
    public void run(String... args) throws Exception {
        initializeAdminData();
    }

    private void initializeAdminData() {
        try {
            User adminUser = authService.register("admin", System.getenv("ADMIN_PASSWORD"));
            System.out.println("Admin user created with ID: " + adminUser.getId());
            
            Note note1 = noteService.createNote(
                "Flag", 
                System.getenv("FLAG"), 
                adminUser.getId()
            );
            System.out.println("Admin note created: " + note1.getId());
            
            
        } catch (IllegalArgumentException e) {
            System.out.println("Admin user already exists, skipping initialization.");
        } catch (Exception e) {
            System.err.println("Error during admin initialization: " + e.getMessage());
        }
    }
}