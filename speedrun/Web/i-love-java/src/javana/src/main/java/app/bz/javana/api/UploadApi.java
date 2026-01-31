package app.bz.javana.api;

import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import javax.servlet.ServletException;
import java.io.*;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONObject;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

@MultipartConfig
@WebServlet(urlPatterns = "/api/upload")
public class UploadApi extends HttpServlet {
  @Override
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
    resp.setContentType("application/json;charset=UTF-8");

    if (req.getSession(false) == null || req.getSession().getAttribute("user") == null) {
      resp.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
      Map<String, Object> error = new HashMap<>();
      error.put("ok", false);
      error.put("msg", "not logged in");
      resp.getWriter().write(new JSONObject(error).toString());
      return;
    }

    Part p = req.getPart("invoiceFile");
    if (p == null || p.getSize() == 0) {
      resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
      Map<String, Object> error = new HashMap<>();
      error.put("ok", false);
      error.put("msg", "file required");
      resp.getWriter().write(new JSONObject(error).toString());
      return;
    }

    String xml = new String(p.getInputStream().readAllBytes());

    try {
      DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
      dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
      dbf.setFeature("http://xml.org/sax/features/external-general-entities", true);
      dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", true);
      dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", true);
      dbf.setXIncludeAware(true);
      dbf.setExpandEntityReferences(true);

      DocumentBuilder db = dbf.newDocumentBuilder();
      Document doc = db.parse(new InputSource(new StringReader(xml)));

      String content = doc.getDocumentElement().getTextContent();

      Map<String, Object> ok = new HashMap<>();
      ok.put("ok", true);
      ok.put("message", "Processed");
      // ok.put("preview", content);

      resp.setStatus(HttpServletResponse.SC_OK);
      resp.getWriter().write(new JSONObject(ok).toString());

    } catch (Exception ex) {
      resp.setStatus(HttpServletResponse.SC_BAD_REQUEST);
      Map<String, Object> error = new HashMap<>();
      error.put("ok", false);
      error.put("msg", ex.getMessage());
      resp.getWriter().write(new JSONObject(error).toString());
    }
  }
}
