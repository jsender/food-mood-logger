# Minimal makefile for Sphinx documentation
#
# Quick guide:
#	make clean		- will delete build.log venv/ and build/
#
#	make html		- will create build/html with html page containing the documentation
#
#	make latex		- will create build/latex with latex files ready to be built
#
#	make check		- https://docs.python.org/3.7/distutils/apiref.html#module-distutils.command.check
#
#	make install 	- will attempt to install the package via `python $(SETUP) install' command. Take care,
#					for this reason venv command was made.
#
#	make build LOGMESSAGES=y - will turn logging on, after running the command build.log will be generated


# Estimated packages to install for dist build:
# texinfo

# Oneliner for building html and latex->pdf:
# make clean; make html; make latex; cd build/latex/; make all-pdf; cd - > /dev/null

SPHINXOPTS	?= -W -T -E
SPHINXBUILD	?= sphinx-build
PROJECTNAME	?= ContinaPythonLibrary
SOURCEDIR	?= source
BUILDDIR	?= build
DISTDIR		?= dist
PYTHON		?= python3.7
VENVDIR		?= venv37
BUILDLOG	?= build.log
LOG			= ([ $(BUILDLOG) ] && sed s/^/[`date +%Y.%m.%d-%H:%M`]\($(BUILDER)\)\ / >> $(BUILDLOG) || cat)
word=
DISTVERSION = $(subst $(word) $(word),.,$(wordlist 1, 2, $(subst ., ,$(shell cat ../cpl/VERSION))))

ALLSPHINXOPTS = -b $(BUILDER) $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/$(BUILDER)

FREEZEEXCLUDE ?= -e 'pkg-resources'
REQUIREMENTS  ?= venv-requirements.txt

# $1 - question to end with [y/N]:
# $2 - command to run
define prompt
	@while [ -z "$$CONTINUE" ]; do read -r -p "$(1) [y/N]: " CONTINUE; done; case "$$CONTINUE" in [yY]) $(2);; esac
endef

.PHONY: help clean venv html htmlview htmlhelp latex text texinfo epub changes \
	linkcheck coverage doctest dist build

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean      to remove build files"
	@echo "  freeze     to generate new venv-requirements.txt based on current environment"
	@echo "  venv       to create a venv with necessary tools"
	@echo "  html       to make standalone HTML files"
	@echo "  htmlview   to open the index page built by the html target in your browser"
	@echo "  htmlhelp   to make HTML files and a HTMLhelp project"
	@echo "  latex      to make LaTeX files"
	@echo "  text       to make plain text files"
	@echo "  texinfo    to make Texinfo file"
	@echo "  epub       to make EPUB files"
	@echo "  changes    to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  coverage   to check documentation coverage for library and C API"
	@echo "  doctest    to run doctests in the documentation"
	@echo "  dist       to make documentation dististribution build

build:
	$(SPHINXBUILD) $(ALLSPHINXOPTS) | $(LOG)
	@echo

html: BUILDER = html
	SPHINXOPTS += -A switchers=1
html: build 
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/$(BUILDER)"

htmlhelp: BUILDER = htmlhelp
htmlhelp: build
	@echo "Build finished. You can now run HTML Help Workshop with the" \
		  "$(BUILDDIR)/$(BUILDER)/pydoc.hhp project file."

latex: BUILDER = latex
latex: build
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/$(BUILDER)."
	@echo "Run \`make all-pdf' in that directory to run these through (pdf)"\
			"latex."

text: BUILDER = text
text: build
	@echo "Build finished; the text files are in $(BUILDDIR)/$(BUILDER)."

texinfo: BUILDER = texinfo
texinfo: build
	@echo "Build finished; the python.texi file is in $(BUILDDIR)/$(BUILDER)."
	@echo "Run \`make info' in that directory to run it through makeinfo."

epub: BUILDER = epub
epub: SPHINXOPTS = -T -E  # epub builder has problems with mimetypes, excluding -W flag
epub: build
	@echo "Build finished; the epub files are in $(BUILDDIR)/$(BUILDER)."

manpage: BUILDER = man
manpage: build
	@echo "[WARNING] manpage build is implemented only because it will be"\
			"implemented in the future. Do *NOT* rely on quality of the"\
			"documents generated with this method"
	@echo "Build finished; manpages are in $(BUILDDIR)/$(BUILDER)."

changes: BUILDER = changes
changes: build
	@echo "The overview file is in $(BUILDDIR)/$(BUILDER)."

linkcheck: BUILDER = linkcheck
linkcheck:
	@$(MAKE) build BUILDER=$(BUILDER) || { \
	echo "Link check complete; look for any errors in the above output" \
	     "or in $(BUILDDIR)/$(BUILDER)/output.txt"; \
	false; }

coverage: BUILDER = coverage
coverage: build
	@echo "Coverage finished; see c.txt and python.txt in $(BUILDDIR)/$(BUILDER)"

htmlview: html
	$(PYTHON) -c "import webbrowser; webbrowser.open('$(BUILDDIR)/html/index.html')"

dist:
	rm -rf $(DISTDIR)
	mkdir -p $(DISTDIR)

	# archive the HTML
	make html
	cp -pPR $(BUILDDIR)/html $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-html
	tar -C $(DISTDIR) -cf $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-html.tar $(PROJECTNAME)-$(DISTVERSION)-docs-html
	bzip2 -9 -k $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-html.tar
	(cd $(DISTDIR); zip -q -r -9 $(PROJECTNAME)-$(DISTVERSION)-docs-html.zip $(PROJECTNAME)-$(DISTVERSION)-docs-html)
	rm -r $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-html
	rm $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-html.tar

	# archive the text build
	make text
	cp -pPR $(BUILDDIR)/text $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-text
	tar -C $(DISTDIR) -cf $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-text.tar $(PROJECTNAME)-$(DISTVERSION)-docs-text
	bzip2 -9 -k $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-text.tar
	(cd $(DISTDIR); zip -q -r -9 $(PROJECTNAME)-$(DISTVERSION)-docs-text.zip $(PROJECTNAME)-$(DISTVERSION)-docs-text)
	rm -r $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-text
	rm $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-text.tar

	# archive the latex (as pdf)
	rm -rf $(BUILDDIR)/latex
	make latex
	-sed -i 's/makeindex/makeindex -q/' $(BUILDDIR)/latex/Makefile
	(cd $(BUILDDIR)/latex; make clean && make all-pdf && make FMT=pdf zip bz2)
	cp $(BUILDDIR)/latex/docs-pdf.zip $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-pdf.zip
	cp $(BUILDDIR)/latex/docs-pdf.tar.bz2 $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-pdf.tar.bz2

	# copy the epub build
	rm -rf $(BUILDDIR)/epub
	make epub
	cp -pPR $(BUILDDIR)/epub/$(PROJECTNAME).epub $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs.epub

	# archive the texinfo build
	rm -rf $(BUILDDIR)/texinfo
	make texinfo
	make info --directory=$(BUILDDIR)/texinfo
	cp -pPR $(BUILDDIR)/texinfo $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-texinfo
	tar -C $(DISTDIR) -cf $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-texinfo.tar $(PROJECTNAME)-$(DISTVERSION)-docs-texinfo
	bzip2 -9 -k $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-texinfo.tar
	(cd $(DISTDIR); zip -q -r -9 $(PROJECTNAME)-$(DISTVERSION)-docs-texinfo.zip $(PROJECTNAME)-$(DISTVERSION)-docs-texinfo)
	rm -r $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-texinfo
	rm $(DISTDIR)/$(PROJECTNAME)-$(DISTVERSION)-docs-texinfo.tar

clean:
	@-rm -rf $(BUILDDIR) $(DISTDIR) build.log
	$(call prompt,Remove venv ($(VENVDIR))?,rm -rf $(VENVDIR))

freeze:
	# https://github.com/pypa/pip/issues/4022
	$(VENVDIR)/bin/pip freeze | grep -v $(FREEZEEXCLUDE) > $(REQUIREMENTS)

LATESTWHEEL=ls -At ../setup/dist/wheel/ | head -n 1
update-venv:
	$(VENVDIR)/bin/python3 -m pip install -U ../setup/dist/wheel/`$(LATESTWHEEL)` | $(LOG)

venv:
	$(PYTHON) -m venv $(VENVDIR) | $(LOG)
	$(VENVDIR)/bin/python3 -m pip install -U pip setuptools wheel | $(LOG)
	$(VENVDIR)/bin/python3 -m pip install -r $(REQUIREMENTS) | $(LOG)
	@echo "The venv has been created in the $(VENVDIR) directory"
