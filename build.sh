#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Building mitigation_book  $(date)"
start=$(date +%s)

# Activate the legacy Jupyter Book environment when conda is available.
# Create it with:
#   conda create -n jb015 python=3.10 -y
#   conda activate jb015
#   python -m pip install -r docs/requirements.txt
if [ "${CONDA_DEFAULT_ENV:-}" != "jb015" ] && command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  if conda env list | awk '{print $1}' | grep -qx "jb015"; then
    conda activate jb015
  fi
fi

# On Mercury, fall back to the shared venv in /project/lhansen
# (source /project/lhansen/jupyterbook.sh does the same by hand).
if ! command -v jupyter-book >/dev/null 2>&1 && [ -f /project/lhansen/jupyterbook.sh ]; then
  source /project/lhansen/jupyterbook.sh
fi

jb_cmd="jupyter-book"
if command -v jb >/dev/null 2>&1; then
  jb_cmd="jb"
fi

version="$("$jb_cmd" --version | awk 'NR == 1 {print $NF}')"
case "$version" in
  0.*) ;;
  *)
    echo "Expected legacy jupyter-book 0.x, found: $version" >&2
    echo "Create and activate jb015, then install docs/requirements.txt." >&2
    exit 1
    ;;
esac

# Regenerate docs/_static/table/*.md from the paper tex when it is present.
# paper/ is a symlink (or copy) of the Overleaf clone holding mitigation_main.tex
# and mitigation_appendix.tex. It lives outside docs/ (so Sphinx never publishes
# it) and is gitignored; without it, fall back to the committed generated tables
# so the book still builds.
if [ -f paper/mitigation_main.tex ] && [ -f paper/mitigation_appendix.tex ]; then
  echo "Syncing tables from paper tex"
  python tools/sync_tables_from_tex.py
else
  echo "Paper tex not found; using committed generated tables."
fi

(
  cd docs
  "$jb_cmd" clean .
  "$jb_cmd" build . --all
)
touch docs/_build/html/.nojekyll

end=$(date +%s)
printf "Elapsed: %02d min %02d sec\n" $(( (end-start)/60 )) $(( (end-start)%60 ))
