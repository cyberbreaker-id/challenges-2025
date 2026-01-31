package ctf.spel;

import org.springframework.stereotype.Component;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.beans.factory.annotation.Autowired;

import java.security.SecureRandom;
import java.math.BigInteger;

@Component
public class Bootstrap implements CommandLineRunner {
  @Autowired JdbcTemplate db;
  private static String rnd(int bits){ return new BigInteger(bits, new SecureRandom()).toString(32); }
  @Override public void run(String... args){
    Integer c = db.queryForObject("SELECT COUNT(*) FROM users", Integer.class);
    if (c == null || c == 0){
      db.update("INSERT INTO users(username,password) VALUES (?,?)", "admin", rnd(80));
      db.update("INSERT INTO users(username,password) VALUES (?,?)", "alice", rnd(70));
      db.update("INSERT INTO users(username,password) VALUES (?,?)", "bob",   rnd(70));
    }
  }
}
