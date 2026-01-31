package com.example.springapp.repository;

import com.example.springapp.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class UserRepository {
    
    private final Map<String, User> users = new ConcurrentHashMap<>();
    private final Map<String, String> usernameToId = new ConcurrentHashMap<>();
    private int nextUserId = 1;

    public User save(User user) {
        if (user.getId() == null) {
            user.setId(String.valueOf(nextUserId++));
        }
        users.put(user.getId(), user);
        usernameToId.put(user.getUsername().toLowerCase(), user.getId());
        return user;
    }

    public Optional<User> findById(String id) {
        return Optional.ofNullable(users.get(id));
    }

    public Optional<User> findByUsername(String username) {
        String id = usernameToId.get(username.toLowerCase());
        return id != null ? Optional.ofNullable(users.get(id)) : Optional.empty();
    }

    public boolean existsByUsername(String username) {
        return usernameToId.containsKey(username.toLowerCase());
    }

    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }

    public void deleteById(String id) {
        User user = users.remove(id);
        if (user != null) {
            usernameToId.remove(user.getUsername().toLowerCase());
        }
    }

    public long count() {
        return users.size();
    }
}