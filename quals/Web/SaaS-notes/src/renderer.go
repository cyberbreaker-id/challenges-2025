package main

import (
	"html/template"
	"path/filepath"
	
	"github.com/gofiber/fiber/v2"
)

var templates *template.Template

func InitTemplates() {
	var err error
	templates, err = template.ParseGlob(filepath.Join("templates", "*.html"))
	if err != nil {
		panic("Failed to load templates: " + err.Error())
	}
}

func RenderTemplate(c *fiber.Ctx, templateName string, data interface{}) error {
	c.Set("Content-Type", "text/html")
	return templates.ExecuteTemplate(c.Response().BodyWriter(), templateName, data)
}