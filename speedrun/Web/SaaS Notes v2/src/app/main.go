package main

import (
	"log"
	"net/http"
	"strings"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	initJWTSecret()
	db := initDB()
	noteHandler := NewNoteHandler(db)
	authHandler := NewAuthHandler(db)

	http.HandleFunc("/api/register", authHandler.Register)
	http.HandleFunc("/api/login", authHandler.Login)

	http.HandleFunc("/api/notes", JWTMiddleware(func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "GET":
			if r.URL.Query().Get("id") != "" {
				noteHandler.GetNote(w, r)
			} else {
				noteHandler.GetNotes(w, r)
			}
		case "POST":
			noteHandler.CreateNote(w, r)
		case "PUT":
			noteHandler.UpdateNote(w, r)
		case "DELETE":
			noteHandler.DeleteNote(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	}))

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" {
			http.ServeFile(w, r, "./static/index.html")
		} else {
			http.NotFound(w, r)
		}
	})

	prefix := "static"
	http.HandleFunc("/static/", func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.RequestURI(), "/"+prefix)
		if path == r.URL.RequestURI() {
			http.NotFound(w, r)
			return
		}
		http.ServeFile(w, r, "./static"+path)
	})

	log.Println("Server starting on :3001")
	log.Fatal(http.ListenAndServe(":3001", nil))
}
