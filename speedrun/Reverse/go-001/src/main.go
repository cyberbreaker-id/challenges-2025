package main

import (
	"fmt"
	"sync"
)

func goo(n uint) uint {
	if n <= 1 {
		return 1
	}

	var soup uint = 0
	var wg sync.WaitGroup
	ch := make(chan uint, n)

	for i := uint(0); i < n; i++ {
		wg.Add(1)
		go func(i uint) {
			defer wg.Done()
			left := goo(i)
			right := goo(n - i - 1)
			ch <- left * right
		}(i)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	for v := range ch {
		soup += v
	}

	return soup
}

func main() {
	a := goo(37)
	b := goo(69)

	flag := fmt.Sprintf("CBC{%016x%016x}", a, b)
	fmt.Println(flag)
}

