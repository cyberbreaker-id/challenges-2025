package main

import (
	"fmt"
	"sync"
)

var (
	memo = map[uint]uint{}
	mu   sync.Mutex
)

func goo(n uint) uint {
	// Check cache
	mu.Lock()
	if val, ok := memo[n]; ok {
		mu.Unlock()
		return val
	}
	mu.Unlock()

	// Base case
	if n <= 1 {
		mu.Lock()
		memo[n] = 1
		mu.Unlock()
		return 1
	}

	var soup uint = 0
	for i := uint(0); i < n; i++ {
		soup += goo(i) * goo(n-i-1)
	}

	// Store in cache
	mu.Lock()
	memo[n] = soup
	mu.Unlock()

	return soup
}

func main() {
	a := goo(37)
	b := goo(69)

	flag := fmt.Sprintf("CBC{%016x%016x}", a, b)
	fmt.Println(flag)
}

