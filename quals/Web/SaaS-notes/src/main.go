package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
)

func main() {
	InitDB()
	defer CloseDB()

	InitSession()
	InitTemplates()
	app := fiber.New()

	app.Get("/", HomeHandler)
	app.Post("/login", LoginHandler)
	app.Post("/register", RegisterHandler)
	app.Get("/dashboard", DashboardHandler)
	app.Post("/notes", CreateNoteHandler)
	app.Get("/logout", LogoutHandler)

	log.Fatal(app.Listen(":3000"))
}
