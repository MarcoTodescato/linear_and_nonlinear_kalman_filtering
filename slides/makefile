
all: pdf

pdf: *.tex
	pdflatex main.tex
	pdflatex main.tex

bib: *.tex
	pdflatex main.tex
	bibtex main.aux
	pdflatex main.tex
	pdflatex main.tex

clean:
	rm -f *.bbl
	rm -f *.blg
	rm -f *.aux
	rm -f *.log
	rm -f *.out
	rm -f *.dvi
	rm -f *.synctex.gz
	rm -f *.fdb_latexmk
	rm -f *.fls
	rm -f *.nav
	rm -f *.snm
	rm -f *.toc
	rm -f *.vrb


clean_all: clean
	rm -f *.pdf

