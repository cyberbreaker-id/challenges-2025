package app.bgz.javanagreeter;

import freemarker.cache.StringTemplateLoader;
import freemarker.template.Configuration;
import freemarker.template.Template;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.io.StringWriter;
import java.util.HashMap;
import java.util.Map;

@Controller
public class HelloController {

    @GetMapping("/hello")
    @ResponseBody
    public Map<String, Object> helloUnsafe(@RequestParam String name) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        StringTemplateLoader loader = new StringTemplateLoader();

        loader.putTemplate("userTpl", "Hello, " + name + "!");
        cfg.setTemplateLoader(loader);

        Template template = cfg.getTemplate("userTpl");
        StringWriter out = new StringWriter();
        template.process(new HashMap<>(), out);

        Map<String, Object> resp = new HashMap<>();
        resp.put("ok", true);
        resp.put("result", out.toString());
        return resp;
    }
}

