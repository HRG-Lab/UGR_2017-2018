# Recipe for making the thesis document. Type 'make' to build it.
# If you want to change the name of the .tex file from 'thesis.tex' to
# 'something.tex', you need to change 'thesis' to 'something' here as well.

OBJ    := thesis   # The name of your document.
LATEX  := pdflatex # The name of your latex command.
BIBTEX := bibtex   # The name of your bibtex command.

document:
	$(LATEX)  $(OBJ)
	$(BIBTEX) $(OBJ)
	$(LATEX)  $(OBJ)
	$(LATEX)  $(OBJ)

# Cleanup of temporary files. Type 'make clean' to remove temporaries.

TEMPS := *.aux *.bbl *.blg *.dvi *.log *.pdf *.ps *.lof *.lot *.toc *.fls
clean:
	@echo Cleaning temporary files.
	@rm -f $(TEMPS) $(addprefix ./data/, $(TEMPS))
