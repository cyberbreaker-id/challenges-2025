package main

import (
	"bufio"
	"bytes"
	"io"
	"log"
	"net/http"
	"net/url"
	"path"
	"regexp"
	"strings"

	limits "github.com/gin-contrib/size"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
)

var isAlphaNum = regexp.MustCompile(`^[a-zA-Z0-9-_]+$`).MatchString

const (
	ReverseServerAddr = "0.0.0.0:4142"
)

type Auth struct {
	Username string `form:"username" binding:"required"`
	Password string `form:"password" binding:"required"`
	Action   string `form:"action" binding:"required"`
}

type ActionNotes struct {
	Title    string `form:"title" binding:"required"`
	Content  string `form:"content" binding:"required"`
	Username string `form:"username"`
}

type ActionDebug struct {
	YamlContent string `form:"yaml_content" binding:"required"`
}

func validation(c *gin.Context) {
	req := c.Request
	bodyBytes, err := io.ReadAll(req.Body)
	req.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
	if err != nil {
		log.Printf("error reading request body: %v", err)
		c.String(http.StatusInternalServerError, "error")
		return
	}

	reqPath := path.Clean(req.URL.Path)
	req.URL.Path = reqPath
	
	if strings.Contains(reqPath, "..") {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid path"})
		c.Abort()
		return
	}

	switch {
	case reqPath == "/api/user/login":
		var form Auth
		if err := c.ShouldBindWith(&form, binding.Form); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			c.Abort()
			return
		}
		if !isAlphaNum(form.Username) {
			c.JSON(http.StatusBadRequest, gin.H{"error": "username contains illegal characters"})
			c.Abort()
			return
		}

		if form.Action != "user_login" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Login as Admin is disabled"})
			c.Abort()
			return
		}
		break
	case reqPath == "/api/user/register":
		var form Auth
		if err := c.ShouldBind(&form); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			c.Abort()
			return
		}

		if !isAlphaNum(form.Username) {
			c.JSON(http.StatusBadRequest, gin.H{"error": "username contains illegal characters"})
			c.Abort()
			return
		}

		if form.Action != "user_register" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Registration as Admin is disabled"})
			c.Abort()
			return
		}
		break
	case reqPath == "/api/notes":
		var form ActionNotes
		if err := c.ShouldBind(&form); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			c.Abort()
			return
		}
		break
	case reqPath == "/api/debug":
		var form ActionDebug
		if err := c.ShouldBind(&form); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			c.Abort()
			return
		}

		if !isAlphaNum(form.YamlContent) {
			c.JSON(http.StatusBadRequest, gin.H{"error": "contains illegal characters"})
			c.Abort()
			return
		}

		break
	case strings.HasPrefix(reqPath, "/api/notes"):
		break
	}
	req.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

	c.Next()
}

func reverseHandler(c *gin.Context) {

	req := c.Request
	proxy, err := url.Parse("http://paper-backend:8000")
	if err != nil {
		log.Printf("error parsing addr: %v", err)
		c.String(http.StatusInternalServerError, "error")
		return
	}
	req.URL.Scheme = proxy.Scheme
	req.URL.Host = proxy.Host

	if req.Body != nil {
		bodyBytes, err := io.ReadAll(req.Body)
		if err != nil {
			log.Printf("error reading request body: %v", err)
			c.String(http.StatusInternalServerError, "error")
			return
		}
		req.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
	}

	transport := http.DefaultTransport
	resp, err := transport.RoundTrip(req)
	if err != nil {
		log.Printf("error in roundtrip: %v", err)
		c.String(http.StatusInternalServerError, "error")
		return
	}
	defer resp.Body.Close()

	for k, vv := range resp.Header {
		for _, v := range vv {
			c.Header(k, v)
		}
	}

	bufio.NewReader(resp.Body).WriteTo(c.Writer)
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	r.Use(limits.RequestSizeLimiter(1024 * 1024))
	r.GET("/*path", validation, reverseHandler)
	r.POST("/*path", validation, reverseHandler)
	r.PUT("/*path", validation, reverseHandler)
	r.DELETE("/*path", validation, reverseHandler)

	if err := r.Run(ReverseServerAddr); err != nil {
		log.Printf("Error: %v", err)
	}
}
