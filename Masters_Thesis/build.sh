#!/bin/bash
# =============================================================
# build.sh — Compile and preview a LaTeX thesis
# =============================================================
#
# USAGE:
#   From the Masters_Thesis directory:
#     ./build.sh           <- compile main.tex and open the PDF
#     ./build.sh clean     <- delete all build artifacts
#
# FIRST TIME SETUP:
#   Make this script executable (only need to do this once):
#     chmod +x build.sh
#
# REQUIREMENTS:
#   - pdflatex and bibtex must be installed (comes with MacTeX)
#     Install MacTeX: https://www.tug.org/mactex/
#   - 'open' is a built-in macOS command, no install needed
#
# HOW IT WORKS:
#   LaTeX needs to be compiled multiple times to resolve all
#   cross-references and bibliography entries:
#     1. pdflatex  <- first pass, builds .aux files
#     2. bibtex    <- reads .aux, resolves citations from .bib
#     3. pdflatex  <- second pass, writes resolved references
#     4. pdflatex  <- third pass, finalises all page numbers
#   Then 'open' launches the PDF in your default viewer (Preview).
#
# OUTPUT:
#   main.pdf is created in the same directory as main.tex
#   Build logs are written to build.log
# =============================================================

# --- Config --------------------------------------------------
TEX_FILE="main"          # name of your .tex file without extension
BUILD_LOG="build.log"    # all compiler output goes here
# -------------------------------------------------------------

# Colour codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # no colour

# --- Clean mode ----------------------------------------------
if [ "$1" = "clean" ]; then
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    rm -f "$TEX_FILE".aux \
          "$TEX_FILE".bbl \
          "$TEX_FILE".blg \
          "$TEX_FILE".log \
          "$TEX_FILE".out \
          "$TEX_FILE".toc \
          "$BUILD_LOG"
    echo -e "${GREEN}Done. PDF kept.${NC}"
    exit 0
fi

# --- Check that the .tex file exists -------------------------
if [ ! -f "$TEX_FILE.tex" ]; then
    echo -e "${RED}Error: $TEX_FILE.tex not found.${NC}"
    echo "Run this script from the Masters_Thesis directory."
    exit 1
fi

# --- Compile -------------------------------------------------
echo -e "${YELLOW}Step 1/4: pdflatex (first pass)...${NC}"
pdflatex -interaction=nonstopmode "$TEX_FILE.tex" >> "$BUILD_LOG" 2>&1

echo -e "${YELLOW}Step 2/4: bibtex (resolve citations)...${NC}"
bibtex "$TEX_FILE" >> "$BUILD_LOG" 2>&1

echo -e "${YELLOW}Step 3/4: pdflatex (second pass)...${NC}"
pdflatex -interaction=nonstopmode "$TEX_FILE.tex" >> "$BUILD_LOG" 2>&1

echo -e "${YELLOW}Step 4/4: pdflatex (final pass)...${NC}"
pdflatex -interaction=nonstopmode "$TEX_FILE.tex" >> "$BUILD_LOG" 2>&1

# --- Check for errors ----------------------------------------
# pdflatex exits with 0 even on some errors, so we grep the log
if grep -q "^!" "$TEX_FILE.log" 2>/dev/null; then
    echo ""
    echo -e "${RED}Build failed. Errors found:${NC}"
    # Print only the error lines for quick diagnosis
    grep -A 2 "^!" "$TEX_FILE.log"
    echo ""
    echo "Full output is in $BUILD_LOG"
    exit 1
fi

# --- Check PDF was actually produced -------------------------
if [ ! -f "$TEX_FILE.pdf" ]; then
    echo -e "${RED}Build failed. No PDF produced. Check $BUILD_LOG for details.${NC}"
    exit 1
fi

# --- Success -------------------------------------------------
echo ""
echo -e "${GREEN}Build successful -> $TEX_FILE.pdf${NC}"
echo ""

# Open the PDF in Preview (macOS)
# If the PDF is already open, Preview will reload it automatically
open "$TEX_FILE.pdf"
