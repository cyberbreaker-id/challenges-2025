package main

import (
	"time"
	"gorm.io/gorm"
)

type User struct {
	ID       uint   `json:"id" gorm:"primarykey"`
	Username string `json:"username" gorm:"unique;not null"`
	Password string `json:"password" gorm:"not null"`
	Premium  bool   `json:"-,omitempty" gorm:"default:false"`
	Notes    []Note `json:"-" gorm:"foreignKey:UserID"`
}

type Note struct {
	ID       uint           `json:"id" gorm:"primarykey"`
	UserID   uint           `json:"user_id" gorm:"not null"`
	Title    string         `json:"title" gorm:"not null"`
	Content  string         `json:"content" gorm:"not null"`
	Template string         `json:"template"`
	CreatedAt time.Time     `json:"created"`
	UpdatedAt time.Time     `json:"updated"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"`
	User     User           `json:"-" gorm:"foreignKey:UserID"`
}