package ctf.spel;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
public class Api {
  @Autowired JdbcTemplate db;

  private record LoginReq(String username, String password) {}
  private record NoteReq(String title) {}
  private record NoteResp(String id) {}

  private static final String SESS_USER = "user";
  private static final String SESS_WS = "workspace";

  @GetMapping("/health")
  public String health() { return "ok"; }

  @GetMapping("/users/search")
  public List<String> sqli(@RequestParam String name) {
    String sql = "SELECT username FROM users WHERE username = '" + name + "'";
    return db.query(sql, (rs, i) -> rs.getString(1));
  }

  @PostMapping("/login")
  public ResponseEntity<?> login(@RequestBody LoginReq req, HttpServletRequest http) {
    try {
      String pw = db.queryForObject("SELECT password FROM users WHERE username = ?", String.class, req.username());
      if (!Objects.equals(pw, req.password())) return ResponseEntity.status(401).body("invalid");
    } catch (EmptyResultDataAccessException e) {
      return ResponseEntity.status(401).body("invalid");
    }
    HttpSession old = http.getSession(false);
    if (old != null) old.invalidate();
    HttpSession s = http.getSession(true);
    s.setAttribute(SESS_USER, req.username());
    s.setAttribute(SESS_WS, UUID.randomUUID().toString());
    return ResponseEntity.ok(Map.of("user", req.username(), "workspace", s.getAttribute(SESS_WS)));
  }

  @GetMapping("/me")
  public ResponseEntity<?> me(HttpSession s) {
    String u = (String) s.getAttribute(SESS_USER);
    String ws = (String) s.getAttribute(SESS_WS);
    if (u == null) return ResponseEntity.status(401).body("unauth");
    return ResponseEntity.ok(Map.of("user", u, "workspace", ws));
  }

  @PostMapping("/notes")
  public ResponseEntity<?> create(@RequestBody NoteReq req, HttpSession s) {
    String u = (String) s.getAttribute(SESS_USER);
    String ws = (String) s.getAttribute(SESS_WS);
    if (u == null || ws == null) return ResponseEntity.status(401).body("unauth");
    if (req == null || req.title() == null || req.title().length() > 1500) return ResponseEntity.badRequest().body("bad");
    String id = UUID.randomUUID().toString();
    db.update("INSERT INTO notes(id,workspace,title) VALUES (?,?,?)", id, ws, req.title());
    return ResponseEntity.ok(new NoteResp(id));
  }

  @GetMapping("/notes")
  public ResponseEntity<?> list(HttpSession s) {
    String u = (String) s.getAttribute(SESS_USER);
    String ws = (String) s.getAttribute(SESS_WS);
    if (u == null || ws == null) return ResponseEntity.status(401).body("unauth");
    List<Map<String,Object>> ids = db.queryForList("SELECT id FROM notes WHERE workspace = ?", ws);
    return ResponseEntity.ok(ids);
  }

  private final ExpressionParser spel = new SpelExpressionParser();

  @GetMapping("/notes/{id}")
  public ResponseEntity<Void> view(@PathVariable String id, HttpSession s, HttpServletRequest req) {
    String u = (String) s.getAttribute(SESS_USER);
    String ws = (String) s.getAttribute(SESS_WS);
    if (u == null || ws == null) return ResponseEntity.status(401).build();
    List<Map<String,Object>> rows = db.queryForList("SELECT title FROM notes WHERE id = ? AND workspace = ?", id, ws);
    if (rows.isEmpty()) return ResponseEntity.notFound().build();
    String exprStr = Objects.toString(rows.get(0).get("title"), "");
    try {
      var ctx = new StandardEvaluationContext();
      ctx.setVariable("session", s);
      ctx.setVariable("req", req);
      Expression expr = spel.parseExpression(exprStr);
      expr.getValue(ctx);
    } catch (Exception ignored) {}
    return ResponseEntity.noContent().build();
  }
}
