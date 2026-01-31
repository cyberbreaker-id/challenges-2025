package app.bz.javana.api;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import javax.servlet.ServletException;
import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.json.JSONObject;

@WebServlet(urlPatterns = "/api/register")
public class RegisterApi extends HttpServlet {
  // demo in-memory users
  private static final ConcurrentHashMap<String,String> USERS = new ConcurrentHashMap<>();

  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    JSONObject j = new JSONObject(new BufferedReader(new InputStreamReader(req.getInputStream()))
        .lines().reduce("", (a,b)->a+b));
    String u = j.optString("username","");
    String p = j.optString("password","");

    resp.setContentType("application/json;charset=UTF-8");

    if (u.isEmpty() || p.isEmpty()) {
      resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
      Map<String,Object> error = new HashMap<>();
      error.put("ok", false);
      error.put("msg", "username/password required");
      resp.getWriter().write(new JSONObject(error).toString());
      return;
    }

    if (USERS.putIfAbsent(u,p) != null) {
      resp.setStatus(HttpServletResponse.SC_CONFLICT);
      Map<String,Object> error = new HashMap<>();
      error.put("ok", false);
      error.put("msg", "user exists");
      resp.getWriter().write(new JSONObject(error).toString());
      return;
    }

    resp.setStatus(HttpServletResponse.SC_OK);
    Map<String,Object> ok = new HashMap<>();
    ok.put("ok", true);
    resp.getWriter().write(new JSONObject(ok).toString());
  }

  public static boolean valid(String u, String p) {
    return p != null && p.equals(USERS.get(u));
  }
}
