package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/session"
)

var store *session.Store

func InitSession() {
	store = session.New()
}

func HomeHandler(c *fiber.Ctx) error {
	return RenderTemplate(c, "home.html", nil)
}

func LoginHandler(c *fiber.Ctx) error {
	var loginUser User
	if err := c.BodyParser(&loginUser); err != nil {
		return c.Status(400).SendString("Invalid JSON")
	}

	user, err := AuthenticateUser(&loginUser)
	if err != nil {
		return c.Status(401).SendString("Invalid credentials")
	}

	sess, err := store.Get(c)
	if err != nil {
		return c.Status(500).SendString("Session error")
	}

	sess.Set("user_id", user.ID)
	sess.Set("premium", user.Premium)
	sess.Save()

	return c.Redirect("/dashboard")
}

func DashboardHandler(c *fiber.Ctx) error {
	sess, err := store.Get(c)
	if err != nil {
		return c.Redirect("/")
	}

	userID := sess.Get("user_id")
	if userID == nil {
		return c.Redirect("/")
	}

	notes, err := GetUserNotes(userID.(uint))
	if err != nil {
		return c.Status(500).SendString("Error fetching notes")
	}


	type NoteDisplay struct {
		Note
		ProcessedTitle   string
		ProcessedContent string
	}


	var displayNotes []NoteDisplay
	for _, note := range notes {
		cleanTitle, _ := sanitizeTitle(note.Template, c, map[string]interface{}{
			"Title": note.Title,
			"Time":  note.CreatedAt.Format("2006-01-02 15:04:05"),
		})

		safeContent, _ := formatContent(note.Content, c, map[string]interface{}{
			"Title": note.Title,
			"Time":  note.CreatedAt.Format("2006-01-02 15:04:05"),
			"User":  userID,
		})

		displayNotes = append(displayNotes, NoteDisplay{
			Note:             note,
			ProcessedTitle:   cleanTitle,
			ProcessedContent: safeContent,
		})
	}


	isPremium := sess.Get("premium")
	data := map[string]interface{}{
		"Notes":     displayNotes,
		"IsPremium": isPremium != nil && isPremium.(bool),
	}

	return RenderTemplate(c, "dashboard.html", data)
}

func CreateNoteHandler(c *fiber.Ctx) error {
	sess, err := store.Get(c)
	if err != nil {
		return c.Status(401).SendString("Not authenticated")
	}

	userID := sess.Get("user_id")
	isPremium := sess.Get("premium")

	if userID == nil {
		return c.Status(401).SendString("Not authenticated")
	}

	if isPremium == nil || !isPremium.(bool) {
		return c.Status(403).SendString("Premium subscription required to create notes")
	}

	title := c.FormValue("title")
	content := c.FormValue("content")

	note := Note{
		UserID:  userID.(uint),
		Title:   title,
		Content: content,
	}

	err = CreateNote(&note)
	if err != nil {
		return c.Status(500).SendString("Error creating note")
	}

	return c.Redirect("/dashboard")
}

func RegisterHandler(c *fiber.Ctx) error {
	var registerUser User
	if err := c.BodyParser(&registerUser); err != nil {
		return c.Status(400).SendString("Invalid JSON")
	}

	if registerUser.Username == "" || registerUser.Password == "" {
		return c.Status(400).SendString("Username and password required")
	}

	err := RegisterUser(&registerUser)
	if err != nil {
		return c.Status(400).SendString("Username already exists or registration failed")
	}

	return RenderTemplate(c, "register_success.html", nil)
}


func LogoutHandler(c *fiber.Ctx) error {
	sess, err := store.Get(c)
	if err == nil {
		sess.Destroy()
	}
	return c.Redirect("/")
}