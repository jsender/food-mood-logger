# Minimal makefile for python setup
# 
# Quick guide:
#	make clean		- will delete build.log, venv/, dist/ and build/
#
#	make build		- will create dist/{packagename}.tar.gz with setup.py necessary to install the package
#
#	make venv		- will create python's virtual environment under VENVDIR (default venv)
#       			and make `activate' file, which can be sourced `source activate' or `.
#   		    	activate' to activate the virtual environment
#
#	make check		- https://docs.python.org/3.7/distutils/apiref.html#module-distutils.command.check
#
#	make install 	- will attempt to install the package via `python $(SETUP) install' command. Take care,
#					for this reason venv command was made.
#
#	make venv LOGMESSAGES=y - will turn logging on, after running the command build.log will be generated

PYTHON		?= python
SETUP		?= setup.py
SETUPOPTS	?=
BUILDDIR	?= build
DISTDIR		?= dist
VENVDIR		?= venv
BUILDLOG	?= build.log
LOG			= ([ $(BUILDLOG) ] && sed s/^/[`date +%Y.%m.%d-%H:%M`]\($(BUILDER)\)\ / >> $(BUILDLOG) || cat)

FREEZEEXCLUDE = -e 'pkg-resources'
REQUIREMENTS  = venv-requirements.txt

# $1 - question to end with [y/N]:
# $2 - command to run
define prompt
	@while [ -z "$$CONTINUE" ]; do read -r -p "$(1) [y/N]: " CONTINUE; done; case "$$CONTINUE" in [yY]) $(2);; esac
endef

.PHONY: help compileall freeze clean build build_py install install_lib sdist bdist bdist_rpm bdist_wininst check upload register index dist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean         to clean up temporary files from 'build' and 'venv' directory"
	@echo "  compileall    to compile all .py files and put them into build/cpl directory"
	@echo "  freeze        to generate new venv-requirements.txt based on current environment"
	@echo "  venv          to create a venv with necessary tools"
	@echo "  build         to build everything needed to install"
	@echo "  build_py      to "build" pure Python modules (copy to build directory)"
	@echo "  install  	   to install everything from build directory"
	@echo "  install_lib   to install all Python modules (extensions and pure Python)"
	@echo "  wheel         to create default dist packages used for index downloads"
	@echo "  sdist         to create a source distribution (tarball, zip file, etc.)"
	@echo "  bdist         to create a built (binary) distribution"
	@echo "  bdist_dumb    to create a "dumb" built distribution"
	@echo "  bdist_rpm     to create an RPM distribution"
	@echo "  bdist_wininst to create an executable installer for MS Windows"
	@echo "  check         to perform some checks on the package"
	@echo "  register      to register the distribution with the Python package index"
	@echo "  index         to create index file and link required setup files"

build_cmd:
	$(PYTHON) $(SETUP) $(COMMAND) $(SETUPOPTS) | $(LOG)
	@echo

build: COMMAND = build
build: build_cmd

build_py: COMMAND = build_py
build_py: build_cmd

install: COMMAND = install
install: build_cmd

install_lib: COMMAND = install_lib
install_lib: build_cmd

sdist: COMMAND = sdist
sdist: build_cmd
	@echo "Library archive is available under dist/ directory"

bdist: COMMAND = bdist
bdist: build_cmd
	@echo "Library archive is available under dist/ directory"

bdist_dumb: COMMAND = bdist_dumb
bdist_dumb: build_cmd
	@echo "Library archive is available under dist/ directory"

bdist_rpm: COMMAND = bdist_rpm
bdist_rpm: build_cmd
	@echo "Library archive is available under dist/ directory"

bdist_wininst: COMMAND = bdist_wininst
bdist_wininst: build_cmd
	@echo "Library archive is available under dist/ directory"

wheel: COMMAND = bdist_wheel
wheel: build_cmd

check: COMMAND = check
check: build_cmd

register: COMMAND = register
register: build_cmd

dist:
	-rm -rf $(DISTDIR)
	-mkdir -p $(DISTDIR) $(DISTDIR)/index

	make wheel

	make build
	
	make build_py

index:
	@echo TODO

clean: COMMAND = clean
clean: build_cmd
	@-rm -rf $(BUILDDIR) *.egg-info activate dist build.log
	$(call prompt,Remove venv ($(VENVDIR))?,rm -rf $(VENVDIR))

freeze:
	# https://github.com/pypa/pip/issues/4022
	$(VENVDIR)/bin/pip freeze --all | grep -v $(FREEZEEXCLUDE) > $(REQUIREMENTS)

venv:
	$(PYTHON) -m venv $(VENVDIR) | $(LOG)
	$(VENVDIR)/bin/python3 -m pip install -U pip setuptools wheel | $(LOG)
	$(VENVDIR)/bin/python3 -m pip install -r $(REQUIREMENTS) | $(LOG)
	@echo "The venv has been created in the $(VENVDIR) directory"
