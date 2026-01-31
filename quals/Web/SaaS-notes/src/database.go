package main

import (
	"log"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var db *gorm.DB

func InitDB() {
	var err error
	db, err = gorm.Open(sqlite.Open("notes.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	err = db.AutoMigrate(&User{}, &Note{})
	if err != nil {
		log.Fatal("Failed to migrate database:", err)
	}

	var count int64
	db.Model(&User{}).Count(&count)
	if count == 0 {
		normalUser := User{
			Username: "user",
			Password: "password",
			Premium:  false,
		}
		db.Create(&normalUser)
	}
}

func CloseDB() {
	sqlDB, err := db.DB()
	if err == nil {
		sqlDB.Close()
	}
}

func AuthenticateUser(loginUser *User) (*User, error) {
	var user User
	result := db.Where("username = ? AND password = ?", loginUser.Username, loginUser.Password).First(&user)
	if result.Error != nil {
		return nil, result.Error
	}
	return &user, nil
}

func RegisterUser(user *User) error {
	result := db.Create(user)
	return result.Error
}

func CreateNote(note *Note) error {
	note.Template = getDefaultHeaderPattern()
	result := db.Create(note)
	return result.Error
}

func GetUserNotes(userID uint) ([]Note, error) {
	var notes []Note
	result := db.Where("user_id = ?", userID).Find(&notes)
	return notes, result.Error
}
