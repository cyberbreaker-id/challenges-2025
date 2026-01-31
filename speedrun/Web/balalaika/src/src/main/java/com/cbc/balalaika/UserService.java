package com.cbc.balalaika;

import org.springframework.stereotype.Service;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class UserService {
    private final Map<String, User> users = new HashMap<>();
    private final Map<String, String> usernameToId = new HashMap<>();

    public User registerUser(String username, String password, String email) {
        if (usernameToId.containsKey(username)) {
            throw new RuntimeException("Username already exists");
        }

        String userId = UUID.randomUUID().toString();
        User user = new User(userId, username, password, email);
        
        users.put(userId, user);
        usernameToId.put(username, userId);
        
        return user;
    }

    public User authenticateUser(String username, String password) {
        String userId = usernameToId.get(username);
        if (userId == null) {
            return null;
        }

        User user = users.get(userId);
        if (user != null && user.getPassword().equals(password)) {
            return user;
        }
        
        return null;
    }

    public User findById(String userId) {
        return users.get(userId);
    }

    public User findByUsername(String username) {
        String userId = usernameToId.get(username);
        return userId != null ? users.get(userId) : null;
    }
}