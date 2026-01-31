all: generate-dist run-solver clean

generate-dist:
	sage src/challenge.sage > src/output.txt
	cp -r src/ dist/
	sed -i 's/CBC{[^}]*}/CBC{******** redacted ********}/g' dist/challenge.sage

run-solver:
	cd solver && sage solver.sage

clean:
	find . -type f -name "*.sage.py" -delete
