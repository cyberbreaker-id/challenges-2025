package com.cbc.balalaika;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MainController {

    @GetMapping("/")
    public ResponseEntity<String> index() {
        return ResponseEntity.ok("Balalaika Notes App - Use /auth/register or /auth/login to get started");
    }

    @Autowired
    private AuthorizationService authorizationService;

    @GetMapping("/admin")
    public ResponseEntity<String> admin(@RequestHeader(value = "Authorization", required = false) String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Unauthorized");
        }

        try {
            String token = authHeader.substring(7);
            String userId = authorizationService.getSubject(token);
            
            if (!"admin".equals(userId)) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body("Admin access required");
            }
            
            return ResponseEntity.ok(System.getenv("FLAG"));
        } catch (UnauthorizedException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Invalid token");
        }
    }
}