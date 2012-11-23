# Makefile for geda notes

# The file to run LaTeX on
MAINFILE = geda_notes.tex

# The other LaTeX sources
LATEXSRC = $(MAINFILE) \
           pcb.tex

#------------------------- Done with configuration ---------------------

help:
	@echo 'Makefile for the gEDA notes                                              '
	@echo '                                                                         '
	@echo 'Usage:                                                                   '
	@echo '   make edit                        Use emacs to edit the document       '
	@echo '   make dvi                         (re)generate the dvi file            '
	@echo '   make ps                          (re)generate the postscript output   '
	@echo '   make pdf                         (re)generate the pdf output          '
	@echo '                                                                         '

pdf: geda_notes.pdf
geda_notes.pdf: geda_notes.ps
	ps2pdf $<

ps: geda_notes.ps
geda_notes.ps: geda_notes.dvi
	dvips -t letter $<


.PHONY : dvi
dvi : geda_notes.dvi
geda_notes.dvi: geda_notes.tex \
                $(wildcard *.tex)
	# ------------- Running latex on the document ---------------------
	latex $<

.PHONY: edit
edit :
	emacs --geometry 120x40 \
              --visit $(MAINFILE) \
              --funcall visual-line-mode &





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Making figures ~~~~~~~~~~~~~~~~~~~~~~~~~~~


clean:
	rm -f *.aux
	rm -f figs/*.eps
	rm -f figs/*.bak


.PHONY: help clean dvi ps manual pdf comcheck spell fieldcal
