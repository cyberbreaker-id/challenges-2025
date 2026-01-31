package com.example.springthief;

import java.time.LocalDateTime;

class User
{
    private Long id;
    private String username;
    private String password;
    private LocalDateTime createdAt;
    private boolean isActive;
    
    public User() {
        this.createdAt = LocalDateTime.now();
        this.isActive = true;
    }
    
    public User(String username, String password) {
        this();
        this.username = username;
        this.password = password;
    }
    
    public Long getId() {
        return this.id;
    }
    
    public void setId(final Long id) {
        this.id = id;
    }
    
    public String getUsername() {
        return this.username;
    }
    
    public void setUsername(final String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return this.password;
    }
    
    public void setPassword(final String password) {
        this.password = password;
    }
    
    
    public LocalDateTime getCreatedAt() {
        return this.createdAt;
    }
    
    public boolean isActive() {
        return this.isActive;
    }
    
    public void setActive(final boolean active) {
        this.isActive = active;
    }
    
    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", createdAt=" + createdAt +
                ", isActive=" + isActive +
                '}';
    }
}