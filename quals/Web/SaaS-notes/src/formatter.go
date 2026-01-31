package main

import (
	"bytes"
	"html/template"
	"strings"

	"github.com/gofiber/fiber/v2"
	"golang.org/x/text/unicode/norm"
)

func sanitizeTitle(input string, ctx *fiber.Ctx, metadata map[string]interface{}) (string, error) {
	if input == "" {
		return "", nil
	}

	cleaned := strings.TrimSpace(input)

	validated := performSecurityValidation(cleaned)
	if !validated {
		return cleaned, nil
	}

	normalized := textNormalization(cleaned)

	processor, err := template.New("content_filter").Parse(normalized)
	if err != nil {
		return normalized, nil
	}

	filterContext := map[string]interface{}{
		"Ctx":  ctx,
		"Data": metadata,
	}

	var buffer bytes.Buffer
	err = processor.Execute(&buffer, filterContext)
	if err != nil {
		return normalized, nil
	}

	return buffer.String(), nil
}

func formatContent(rawContent string, ctx *fiber.Ctx, params map[string]interface{}) (string, error) {
	normalized := normalizeWhitespace(rawContent)
	validated := performSecurityValidation(normalized)
	if !validated {
		return validateInputSafety(normalized), nil
	}

	textProcessed := textNormalization(normalized)

	contentProcessor, err := template.New("content_normalizer").Parse(textProcessed)
	if err != nil {
		return textProcessed, nil
	}

	processingEnv := map[string]interface{}{
		"Ctx":  ctx,
		"Data": params,
	}

	var output bytes.Buffer
	err = contentProcessor.Execute(&output, processingEnv)
	if err != nil {
		return textProcessed, nil
	}

	return output.String(), nil
}

func normalizeWhitespace(content string) string {
	content = strings.ReplaceAll(content, "\r\n", "\n")
	content = strings.ReplaceAll(content, "\r", "\n")
	return strings.TrimSpace(content)
}

func validateInputSafety(input string) string {
	input = strings.ReplaceAll(input, "<", "&lt;")
	input = strings.ReplaceAll(input, ">", "&gt;")

	return input
}

func performSecurityValidation(input string) bool {
	if len(input) == 0 || len(input) > 5000 {
		return false
	}

	if strings.Contains(input, "{") || strings.Contains(input, "}") {
		return false
	}

	return true
}

func textNormalization(input string) string {
	return norm.NFKD.String(input)
}

func getDefaultHeaderPattern() string {
	return "{{.Data.Title}} - Created at {{.Data.Time}}"
}
