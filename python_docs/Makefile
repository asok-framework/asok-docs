# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= $(shell [ -f ./venv/bin/sphinx-build ] && echo ./venv/bin/sphinx-build || echo sphinx-build)
SOURCEDIR     = .
BUILDDIR      = _build
PORT          ?= 8000

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

run:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"
	@echo "🚀 Serving python_docs documentation at http://127.0.0.1:$(PORT)"
	@python3 -m http.server $(PORT) --directory "$(BUILDDIR)/html"

pdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex"
	@cd "$(BUILDDIR)/latex" && xelatex -interaction=nonstopmode asokframework.tex > /dev/null
	@echo "📄 PDF generated successfully: $(BUILDDIR)/latex/asokframework.pdf"

.PHONY: help Makefile run pdf

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


