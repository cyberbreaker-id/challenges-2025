package com.cbc.balalaika;

import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.JwtParser;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.security.KeyPair;
import java.util.Base64;
import java.util.Date;

@Service
public class AuthorizationService {


    final static Logger logger = LoggerFactory.getLogger(AuthorizationService.class);

    private final KeyPair keyPair;
    private final JwtParser jwtVerifier;


    public AuthorizationService() {
        this.keyPair = Keys.keyPairFor(SignatureAlgorithm.ES256);
        this.jwtVerifier = Jwts.parserBuilder().setSigningKey(keyPair.getPublic()).build();
    }

    private boolean isValidJWT(String jwt) {
        try {
            jwtVerifier.parseClaimsJws(jwt);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }

    public String getClaim(String jwt, String claim) throws UnauthorizedException {
        if (!isValidJWT(jwt)) {
            throw new UnauthorizedException();
        }
        return this.jwtVerifier.parseClaimsJws(jwt).getBody().get(claim, String.class);
    }

    public String getSubject(String jwt) throws UnauthorizedException {
        return getClaim(jwt, "sub");
    }

    public String generateToken(String userId) {
        return Jwts.builder()
            .setSubject(userId)
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + 86400000))
            .signWith(keyPair.getPrivate())
            .compact();
    }
}
