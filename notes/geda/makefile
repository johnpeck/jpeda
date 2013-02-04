# Makefile for geda notes

# The file to run LaTeX on (without the .tex)
MAINFILE = geda_notes

# The other LaTeX sources
LATEXSRC = $(MAINFILE).tex \
           pcb.tex \
           figs/4_40_mthole_fat.eps

#------------------------- Done with configuration ---------------------

help:
	@echo 'Makefile for the gEDA notes                                              '
	@echo '                                                                         '
	@echo 'Usage:                                                                   '
	@echo '   make edit                        Use emacs to edit the document       '
	@echo '   make preview                     Preview the document with xdvi       '
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
dvi: $(LATEXSRC)
	latex $(MAINFILE).tex

# The dvi preview target
.PHONY: preview
preview:
	xdvi $(MAINFILE).dvi &

.PHONY: edit
edit :
	emacs --geometry 120x40 \
              --visit $(MAINFILE).tex \
              --funcall visual-line-mode &





# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Making figures ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# The mounting hole figure
figs/4_40_mthole_fat.eps: figs/4_40_mthole_fat.fig
	fig2dev -L eps -m 1 $< $@


clean:
	rm -f *.aux
	rm -f figs/*.eps
	rm -f figs/*.bak


.PHONY: help clean dvi ps manual pdf comcheck spell fieldcal
