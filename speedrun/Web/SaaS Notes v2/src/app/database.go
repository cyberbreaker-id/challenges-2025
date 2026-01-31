package main

import (
	"log"
	"math/rand"
	"os"

	"golang.org/x/crypto/bcrypt"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func initDB() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("file::memory:"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	err = db.Migrator().DropTable(&User{}, &Note{})
	if err != nil {
		log.Println("Warning: Failed to drop tables (might not exist):", err)
	}

	err = db.AutoMigrate(&User{}, &Note{})
	if err != nil {
		log.Fatal("Failed to migrate database:", err)
	}

	createDefaultAdmin(db)

	return db
}

const letterBytes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func RandStringBytes(n int) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = letterBytes[rand.Intn(len(letterBytes))]
	}
	return string(b)
}

func createDefaultAdmin(db *gorm.DB) {
	var count int64
	db.Model(&User{}).Count(&count)

	if count == 0 {
		// Read flag.txt content and then delete it
		content, err := os.ReadFile("./flag.txt")
		if err != nil {
			log.Println("Failed to read flag.txt:", err)
		} else {
			err = os.Remove("./flag.txt")
			if err != nil {
				log.Println("Failed to delete flag.txt:", err)
			}
		}

		randomPassword := RandStringBytes(64)

		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(randomPassword), bcrypt.DefaultCost)
		if err != nil {
			log.Fatal("Failed to hash admin password:", err)
		}

		admin := User{
			Username: "admin",
			Email:    "admin@example.com",
			Password: string(hashedPassword),
		}

		result := db.Create(&admin)
		if result.Error != nil {
			log.Fatal("Failed to create admin user:", result.Error)
		}

		defaultNote := Note{
			Title:   "Welcome to Notes App",
			Content: string(content),
			UserID:  admin.ID,
		}

		result = db.Create(&defaultNote)
		if result.Error != nil {
			log.Fatal("Failed to create default note:", result.Error)
		}

		log.Println("Default admin user created:")
		log.Println("Username: admin")
		log.Println("Password:", randomPassword)
		log.Println("Flag: ", string(content))
	}
}
