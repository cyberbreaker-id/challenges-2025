package main

import (
	"crypto/rand"
	"encoding/hex"
	"sync"
	"time"
)

type TempNote struct {
	ID       string    `json:"id"`
	UserID   uint      `json:"user_id"`
	Title    string    `json:"title"`
	Content  string    `json:"content"`
	Template string    `json:"template"`
	Created  time.Time `json:"created"`
	Expires  time.Time `json:"expires"`
}

type TempNoteStorage struct {
	notes map[string]*TempNote
	mutex sync.RWMutex
}

var tempStorage *TempNoteStorage

func InitTempStorage() {
	tempStorage = &TempNoteStorage{
		notes: make(map[string]*TempNote),
		mutex: sync.RWMutex{},
	}
	
	go tempStorage.cleanupExpired()
}

func (ts *TempNoteStorage) generateID() string {
	bytes := make([]byte, 16)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

func (ts *TempNoteStorage) CreateTempNote(userID uint, title, content string) (*TempNote, error) {
	ts.mutex.Lock()
	defer ts.mutex.Unlock()
	
	note := &TempNote{
		ID:       ts.generateID(),
		UserID:   userID,
		Title:    title,
		Content:  content,
		Template: getDefaultHeaderPattern(),
		Created:  time.Now(),
		Expires:  time.Now().Add(1 * time.Hour),
	}
	
	ts.notes[note.ID] = note
	return note, nil
}

func (ts *TempNoteStorage) GetTempNote(id string) (*TempNote, bool) {
	ts.mutex.RLock()
	defer ts.mutex.RUnlock()
	
	note, exists := ts.notes[id]
	if !exists || time.Now().After(note.Expires) {
		return nil, false
	}
	
	return note, true
}

func (ts *TempNoteStorage) GetUserTempNotes(userID uint) []*TempNote {
	ts.mutex.RLock()
	defer ts.mutex.RUnlock()
	
	var userNotes []*TempNote
	now := time.Now()
	
	for _, note := range ts.notes {
		if note.UserID == userID && now.Before(note.Expires) {
			userNotes = append(userNotes, note)
		}
	}
	
	return userNotes
}

func (ts *TempNoteStorage) DeleteTempNote(id string, userID uint) bool {
	ts.mutex.Lock()
	defer ts.mutex.Unlock()
	
	note, exists := ts.notes[id]
	if !exists || note.UserID != userID {
		return false
	}
	
	delete(ts.notes, id)
	return true
}

func (ts *TempNoteStorage) cleanupExpired() {
	ticker := time.NewTicker(10 * time.Minute)
	defer ticker.Stop()
	
	for range ticker.C {
		ts.mutex.Lock()
		now := time.Now()
		
		for id, note := range ts.notes {
			if now.After(note.Expires) {
				delete(ts.notes, id)
			}
		}
		ts.mutex.Unlock()
	}
}