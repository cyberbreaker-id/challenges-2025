package com.example.springthief;

import org.springframework.stereotype.Service;
import java.util.*;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class UserService
{
    private final Map<Long, User> users = new HashMap<>();
    private final Map<String, User> usersByUsername = new HashMap<>();
    private final Map<String, String> activeSessions = new HashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);
    
    public User register(String username, String password) {
        if (usersByUsername.containsKey(username)) {
            return null;
        }
        
        User user = new User(username, password);
        Long id = idGenerator.getAndIncrement();
        user.setId(id);
        
        users.put(id, user);
        usersByUsername.put(username, user);
        
        return user;
    }
    
    public String login(String username, String password) {
        User user = usersByUsername.get(username);
        if (user != null && user.getPassword().equals(password) && user.isActive()) {
            String sessionId = UUID.randomUUID().toString();
            activeSessions.put(sessionId, username);
            return sessionId;
        }
        return null;
    }
    
    public boolean logout(String sessionId) {
        return activeSessions.remove(sessionId) != null;
    }
    
    public User getCurrentUser(String sessionId) {
        String username = activeSessions.get(sessionId);
        if (username != null) {
            return usersByUsername.get(username);
        }
        return null;
    }
    
    public boolean isValidSession(String sessionId) {
        return activeSessions.containsKey(sessionId);
    }
    
    public User getUserByUsername(String username) {
        return usersByUsername.get(username);
    }
    
    
    public boolean usernameExists(String username) {
        return usersByUsername.containsKey(username);
    }
}