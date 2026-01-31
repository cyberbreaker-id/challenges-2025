package com.example.springapp.util;

import java.util.Base64;

public class BasicAuthUtil {
    
    public static String[] parseBasicAuth(String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Basic ")) {
            return null;
        }
        
        String encodedCredentials = authHeader.substring(6);
        String decodedCredentials;
        
        try {
            byte[] decodedBytes = Base64.getDecoder().decode(encodedCredentials);
            decodedCredentials = new String(decodedBytes);
        } catch (IllegalArgumentException e) {
            return null;
        }
        
        String[] credentials = decodedCredentials.split(":", 2);
        if (credentials.length != 2) {
            return null;
        }
        
        return credentials; // [username, password]
    }
    
    public static boolean isValidBasicAuth(String authHeader) {
        return parseBasicAuth(authHeader) != null;
    }
}