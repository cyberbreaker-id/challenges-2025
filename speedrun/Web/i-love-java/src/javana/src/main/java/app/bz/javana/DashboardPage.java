package app.bz.javana;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import javax.servlet.ServletException;
import java.io.IOException;

@WebServlet(urlPatterns = "/dashboard")
public class DashboardPage extends HttpServlet {
  @Override
  protected void doGet(HttpServletRequest req, HttpServletResponse resp)
      throws ServletException, IOException {
    if (req.getSession(false) == null || req.getSession().getAttribute("user") == null) {
      resp.sendRedirect("/login");
      return;
    }
    req.getRequestDispatcher("/WEB-INF/jsp/dashboard.jsp").forward(req, resp);
  }
}