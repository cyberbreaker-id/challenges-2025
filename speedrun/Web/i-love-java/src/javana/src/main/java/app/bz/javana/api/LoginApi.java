package app.bz.javana.api;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import javax.servlet.ServletException;
import java.io.*;
import java.util.HashMap;
import java.util.Map;
import org.json.JSONObject;

@WebServlet(urlPatterns = "/api/login")
public class LoginApi extends HttpServlet {
  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp)
      throws ServletException, IOException {
    
    // Parse request body into JSON
    JSONObject j = new JSONObject(new BufferedReader(new InputStreamReader(req.getInputStream()))
        .lines().reduce("", (a,b)->a+b));
    String u = j.optString("username", "");
    String p = j.optString("password", "");

    resp.setContentType("application/json;charset=UTF-8");

    if (!RegisterApi.valid(u, p)) {
      resp.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
      Map<String,Object> err = new HashMap<>();
      err.put("ok", false);
      err.put("msg", "invalid credentials");
      resp.getWriter().write(new JSONObject(err).toString());
      return;
    }

    req.getSession(true).setAttribute("user", u);

    resp.setStatus(HttpServletResponse.SC_OK);
    Map<String,Object> ok = new HashMap<>();
    ok.put("ok", true);
    ok.put("redirect", "/dashboard");
    resp.getWriter().write(new JSONObject(ok).toString());
  }
}
