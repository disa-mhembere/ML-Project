LATEX = pdflatex
SPELL = aspell
TEX = writeup
BIBTEX = bibtex

default: $(TEX).tex
	$(LATEX) $(TEX); $(BIBTEX) $(TEX); $(LATEX) $(TEX); $(LATEX) $(TEX)

view: $(TEX).tex
	$(LATEX) $(TEX); $(BIBTEX) $(TEX); $(LATEX) $(TEX); $(LATEX) $(TEX)
	open $(TEX).pdf &

clean:
	$(RM) -vf *.aux *.blg *.dvi *.log *.cb *.bbl
	$(RM) $(TEX).pdf *~

check:
	@echo "Passing the check will cause make to report Error 1."
	$(LATEX) $(TEX)  | grep -i undefined
