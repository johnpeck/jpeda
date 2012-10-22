# Makefile for geda notes



help:
	@echo 'Makefile for the gEDA notes                                              '
	@echo '                                                                         '
	@echo 'Usage:                                                                   '
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


dvi: geda_notes.dvi
.PHONY: geda_notes.dvi
geda_notes.dvi: geda_notes.tex \
                $(wildcard *.tex)
	# ------------- Running latex on the document ---------------------
	latex $<





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Making figures ~~~~~~~~~~~~~~~~~~~~~~~~~~~


clean:
	rm -f *.aux
	rm -f figs/*.eps
	rm -f figs/*.bak


.PHONY: help clean dvi ps manual pdf comcheck spell fieldcal
