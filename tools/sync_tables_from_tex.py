#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate markdown tables from the paper tex.

The paper .tex files are the single source of truth. For each configured table
this script locates the tex `tabular` by its \\label, converts it to a markdown
table, and writes it to docs/_static/table/<name>.md. The notebooks include
those files with a MyST directive, e.g.

    ```{include} ../_static/table/svrd_rd_decomposition.md
    ```

so the notebooks themselves are never rewritten -- only the generated .md
files change when the tex changes.

The paper is read from <repo>/paper/, which is a symlink (or copy) of the
Overleaf clone and is gitignored. Both the main text and the appendix are
parsed, because some tables (for example the non-monotonicity table) live in
the appendix.

Usage:
    python tools/sync_tables_from_tex.py                 # (re)write the .md files
    python tools/sync_tables_from_tex.py --check          # report only, exit 1 if stale
    python tools/sync_tables_from_tex.py --paper-dir DIR  # read the tex from DIR

Tables without a \\label are reached by position: `after_label` names a
\\label that precedes them (a figure label, or the \\label of the \\section
that holds them) and `skip` counts how many live table environments after
that anchor to pass over (0, the default, takes the first one). The target
must lie before the next \\section heading after the anchor, so a table that
moves out of its section stops the run instead of picking up a neighbour.

Tables with a paper number (`number`) also get the paper caption, written
as a line "Table N: ..." after the markdown table. A \\ref in a caption is
replaced by its printed number from REF_NUMBERS.

Failure is loud: a \\label matching 0 or >1 *live* table environments, an
anchor label that is missing or repeated, a positional target outside its
section, an out-of-range tabular index, a panel without exactly one tabular
and one caption, or a caption \\ref missing from REF_NUMBERS aborts with a
non-zero exit and writes nothing, so a broken parse can never publish bad
numbers.
"""
import os
import re
import sys
import difflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER_DIR = os.path.join(REPO, "paper")
TEX_FILES = ["mitigation_main.tex", "mitigation_appendix.tex"]
OUTDIR = os.path.join(REPO, "docs", "_static", "table")

# ---- configuration --------------------------------------------------------
# Tables to generate. Per table:
#   label         \label{...} of the table environment (searched verbatim)
#   after_label   used instead of label for an unlabeled table: the \label of
#                 something that precedes it (figure or \section)
#   skip          with after_label, the number of live table environments
#                 after the anchor to pass over (default 0, the first one)
#   tabular       0-based index of the tabular inside the table environment
#   panels        optional True for a table built from subtable panels: every
#                 subtable gives one markdown table, preceded by a bold line
#                 with the panel letter and the panel's own \caption or
#                 \subcaption, "(a) ...", as the paper prints it (tabular is
#                 then not used)
#   header_rows   number of leading tex rows that form the header (skipped when
#                 header_override is set, otherwise parsed; 1 or 2 supported)
#   header_join   optional format for a two-row header cell, with {g} the group
#                 cell (first row) and {s} the sub cell (second row). Default
#                 "{g} <br> ({s})". A cell with only one of the two non-empty
#                 shows that one alone
#   header_override  optional list of markdown header cells emitted verbatim,
#                 used when the notebook header differs from the tex header
#                 (only the data values are then taken from the tex)
#   row_map       optional {first-cell -> replacement} rewrites, matched on the
#                 cleaned first cell of each data row
#   align         optional "left" or "right" for every column, or a list with
#                 one markdown rule ("---", "---:") per column. Default is
#                 left first column, right-aligned data columns
#   number        optional paper table number. When set, the tex caption is
#                 appended as "Table <number>: <caption>"
#   out           output filename under docs/_static/table/
TABLES = [
    {   # paper Table 1
        "label": "tab:uncertainty_decompose_RD",
        "tabular": 0,
        "header_rows": 2,
        "number": 1,
        "out": "svrd_rd_decomposition.md",
    },
    {   # paper Table 2
        "label": "tab:uncertainty_decomopose_Temp",  # sic: label typo in tex
        "tabular": 0,
        "header_rows": 2,
        "number": 2,
        "out": "scgw_emissions_decomposition.md",
    },
    {   # paper Table 3, drift distortions
        "label": "h_values_initial",
        "tabular": 0,
        "header_rows": 1,
        "number": 3,
        "out": "drift_distortions.md",
    },
    {
        # paper Table 4, pre-event values and post-event medians at the two
        # Figure 7 states. The two-row tex header is flattened explicitly.
        "label": "tab:quantile_damage",
        "tabular": 0,
        "header_rows": 2,
        "header_override": ["$\\xi_m$",
                            "emissions (GtC) <br> pre-event",
                            "emissions (GtC) <br> post-event",
                            "R&D investment / output <br> pre-event",
                            "R&D investment / output <br> post-event"],
        "number": 4,
        "out": "table4_quantile_damage.md",
    },
    {
        # paper Table 6, flow decomposition for the one-jump specification.
        # The tex two-row header ("R&D"/"capital" over "investment"/
        # "investment") stacks the words of one label, so the header is given
        # explicitly with the words joined by a space.
        "label": "tab:only_tech_jump",
        "tabular": 0,
        "header_rows": 2,
        "header_override": ["$\\xi_m$", "flow i", "flow ii", "flow iii",
                            "sum", "R&D investment", "capital investment"],
        "align": "right",
        "number": 6,
        "out": "flow_decomposition_one_jump.md",
    },
    {   # paper Table 21 (appendix), SVRD against xi_m, xi_m across columns
        "label": "table:nonmonotone",
        "tabular": 0,
        "header_rows": 1,
        "number": 21,
        "out": "svrd_nonmonotone.md",
    },
    {
        # paper Table 5, two panels: by jump type and by state variable
        "label": "tab:tech_flow_terms_split",
        "panels": True,
        "header_rows": 2,
        "header_join": "{g} <br> {s}",
        "number": 5,
        "out": "table5_tech_flow_terms_split.md",
    },
    {   # paper Table 7
        "label": "table:two_jump",
        "tabular": 0,
        "header_rows": 2,
        "header_join": "{g} <br> {s}",
        "number": 7,
        "out": "table7_two_jump.md",
    },
    {   # paper Table 24
        "label": "tab:hyper_params1",
        "tabular": 0,
        "header_rows": 1,
        "number": 24,
        "out": "table24_discretization.md",
    },
    {   # paper Table 25
        "label": "tab:hyper_params2",
        "tabular": 0,
        "header_rows": 1,
        "number": 25,
        "out": "table25_convergence.md",
    },
    {   # paper Table 26
        "label": "tab:residuals",
        "tabular": 0,
        "header_rows": 1,
        "number": 26,
        "out": "table26_residuals.md",
    },
    {   # paper Table 27
        "label": "tab:grids",
        "tabular": 0,
        "header_rows": 2,
        "header_join": "{g} <br> {s}",
        "number": 27,
        "out": "table27_grids.md",
    },
    {   # paper Table 28, panels coarse and fine grid
        "label": "tab:grid_refine",
        "panels": True,
        "header_rows": 1,
        "number": 28,
        "out": "table28_grid_refinement.md",
    },
    {   # paper Table 29, panels technology jump only and full model
        "label": "tab:indirect_direct_comp",
        "panels": True,
        "header_rows": 1,
        "align": ["---", "---"] + ["---:"] * 4,
        "number": 29,
        "out": "table29_indirect_direct.md",
    },
    {   # paper Table 30, a text table
        "label": "tab:summary",
        "tabular": 0,
        "header_rows": 1,
        "align": "left",
        "number": 30,
        "out": "table30_discrepancy.md",
    },
    {
        # paper Table 32 (appendix, no label), the table right after the
        # two-state figure. Same layout as Table 4 plus two state panels.
        "after_label": "fig:before_after_two_states",
        "tabular": 0,
        "header_rows": 2,
        "header_join": "{g} <br> {s}",
        "number": 32,
        "out": "table32_two_states.md",
    },
    # Online Appendix M (no labels): the three IES tables, in section order
    {"after_label": "onlineapp:rho_sensitivity", "skip": 0, "tabular": 0,
     "header_rows": 1, "number": 35, "out": "table35_ies_xi_inf.md"},
    {"after_label": "onlineapp:rho_sensitivity", "skip": 1, "tabular": 0,
     "header_rows": 1, "number": 36, "out": "table36_ies_xi_01.md"},
    {"after_label": "onlineapp:rho_sensitivity", "skip": 2, "tabular": 0,
     "header_rows": 1, "number": 37, "out": "table37_ies_xi_005.md"},
    # Online Appendix N (no labels): the three (phi_0, psi_0, chi) tables. The
    # two-row tex header stacks words of one label, so the rows are joined
    # with a space.
    {"after_label": "onlineapp:phi0_psi0_chi_sensitivity", "skip": 0,
     "tabular": 0, "header_rows": 2, "header_join": "{g} {s}",
     "number": 38, "out": "table38_phi0_psi0_chi_xi_inf.md"},
    {"after_label": "onlineapp:phi0_psi0_chi_sensitivity", "skip": 1,
     "tabular": 0, "header_rows": 2, "header_join": "{g} {s}",
     "number": 39, "out": "table39_phi0_psi0_chi_xi_01.md"},
    {"after_label": "onlineapp:phi0_psi0_chi_sensitivity", "skip": 2,
     "tabular": 0, "header_rows": 2, "header_join": "{g} {s}",
     "number": 40, "out": "table40_phi0_psi0_chi_xi_005.md"},
]

# Printed numbers for the \ref targets that occur in the captions above, as
# they appear in the compiled paper. A caption \ref missing here aborts.
REF_NUMBERS = {
    "sec:marginal": "8",
    "tab:coarse_comp": "28a",
    "tab:fine_comp": "28b",
    "tab:techonly": "29a",
    "tab:full_terminal": "29b",
}


def die(msg):
    sys.stderr.write("ABORT: %s\n" % msg)
    sys.exit(2)


# ---- tex hygiene ----------------------------------------------------------
def strip_comments(tex):
    """Remove \\begin{comment} blocks and % line comments (keeping \\%)."""
    tex = re.sub(r"\\begin\{comment\}.*?\\end\{comment\}", "", tex, flags=re.S)
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.splitlines())


def load_tex(paper_dir):
    chunks = []
    for name in TEX_FILES:
        path = os.path.join(paper_dir, name)
        if not os.path.exists(path):
            die("paper tex not found at %s" % path)
        chunks.append(strip_comments(open(path, encoding="utf-8").read()))
    return "\n".join(chunks)


def find_table_env(tex, cfg):
    envs = re.findall(r"\\begin\{table\}.*?\\end\{table\}", tex, flags=re.S)
    if "label" in cfg:
        label = cfg["label"]
        hits = [e for e in envs if ("\\label{%s}" % label) in e]
        if len(hits) != 1:
            die("label %s matched %d live table environments (expected exactly 1)"
                % (label, len(hits)))
        return hits[0]
    # unlabeled table: pass over `skip` table environments that follow the
    # anchor label and take the next one, which must sit before the next
    # \section heading
    key = "\\label{%s}" % cfg["after_label"]
    if tex.count(key) != 1:
        die("anchor label %s found %d times (expected exactly 1)"
            % (cfg["after_label"], tex.count(key)))
    rest = tex[tex.find(key):]
    skip = cfg.get("skip", 0)
    hits = list(re.finditer(r"\\begin\{table\}.*?\\end\{table\}", rest, flags=re.S))
    if skip >= len(hits):
        die("no table environment number %d after %s" % (skip, cfg["after_label"]))
    sec = re.search(r"\\section\*?\{", rest)
    if sec and hits[skip].start() > sec.start():
        die("table number %d after %s lies past the next \\section"
            % (skip, cfg["after_label"]))
    return hits[skip].group(0)


def get_tabular(env, idx, name):
    tabs = re.findall(r"\\begin\{tabular\}.*?\\end\{tabular\}", env, flags=re.S)
    if idx >= len(tabs):
        die("tabular index %d out of range for %s (found %d)"
            % (idx, name, len(tabs)))
    return tabs[idx]


# ---- cell-level cleanups --------------------------------------------------
def split_cells(row):
    """Split a tabular row on unescaped & (so R\\&D stays one cell)."""
    return [c.strip() for c in re.split(r"(?<!\\)&", row)]


def lead_zero(s):
    """.0063 -> 0.0063 and -.184 -> -0.184, without touching 3.16."""
    return re.sub(r"(?<![\d.\w])(-?)\.(\d)", r"\g<1>0.\g<2>", s)


def brace_end(s, i):
    """Index just past the group closing the { that opens before index i."""
    depth = 1
    while i < len(s) and depth:
        depth += {"{": 1, "}": -1}.get(s[i], 0)
        i += 1
    if depth:
        die("unbalanced braces in tex near: %s" % s[:80])
    return i


def brace_arg(s, cmd):
    """Return the brace-balanced argument of each \\cmd{...} in s."""
    out = []
    for m in re.finditer(r"\\%s\{" % cmd, s):
        out.append(s[m.end():brace_end(s, m.end()) - 1])
    return out


def map_text(s, fn):
    """Apply fn to the parts of s outside $...$ math, leaving math as is."""
    parts = re.split(r"(?<!\\)(\$[^$]*\$)", s)
    return "".join(p if p.startswith("$") else fn(p) for p in parts)


def trim_math(s):
    """"$ \\infty$" -> "$\\infty$" and "$ .1$" -> "$.1$"."""
    return re.sub(r"(?<!\\)\$([^$]*)\$", lambda m: "$%s$" % m.group(1).strip(), s)


def text_markup(s):
    """Tex text markup outside math to plain characters."""
    s = s.replace(r"\%", "%")
    s = s.replace("``", "\u201c").replace("''", "\u201d")
    s = s.replace("--", "\u2013").replace("~", " ")
    return s


def unwrap_shortstack(s):
    """Replace \\shortstack[opt]{a\\\\b} by "a b" (brace-balanced, so math with
    braces inside the stack is preserved). A line ending in a hyphen is joined
    without a space, so "false-\\\\transient" gives "false-transient"."""
    while True:
        m = re.search(r"\\shortstack(?:\[[^\]]*\])?\{", s)
        if not m:
            return s
        i, depth = m.end(), 1
        while i < len(s) and depth:
            depth += {"{": 1, "}": -1}.get(s[i], 0)
            i += 1
        inner = s[m.end():i - 1]
        inner = re.sub(r"-\s*\\\\", "-", inner)
        inner = inner.replace("\\\\", " ")
        s = s[:m.start()] + " ".join(inner.split()) + s[i:]


def clean(s):
    s = re.sub(r"\\hspace\{[^}]*\}", "", s)
    s = unwrap_shortstack(s)
    s = " ".join(s.split())  # a cell may span several source lines
    s = s.replace(r"\!", "")
    s = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", s)
    # \% only outside math: inside $...$ MathJax needs it escaped
    s = map_text(s, text_markup).replace(r"\&", "&")
    s = trim_math(s)
    s = lead_zero(s)
    return s.strip()


def multicol(cell):
    m = re.match(r"\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}$", cell.strip(), flags=re.S)
    return (int(m.group(1)), m.group(2)) if m else None


def expand_row(cells):
    out = []
    for c in cells:
        mc = multicol(c)
        out.extend([mc[1]] * mc[0] if mc else [c])
    return out


# ---- tabular -> markdown --------------------------------------------------
def build_header(rows, cfg):
    """Return the list of markdown header cells for this table."""
    if cfg.get("header_override"):
        return list(cfg["header_override"])

    header = [expand_row(split_cells(r)) for r in rows[:cfg["header_rows"]]]
    if cfg["header_rows"] == 1:
        return [clean(c) for c in header[0]]
    if cfg["header_rows"] == 2:
        # two-row header: a group row (with \multicolumn spans) over a sub row;
        # combine per column with header_join, default "group <br> (sub)".
        group, sub = header[0], header[1]
        join = cfg.get("header_join", "{g} <br> ({s})")
        head = []
        for i in range(len(sub)):
            g = clean(group[i]) if i < len(group) else ""
            s = clean(sub[i])
            head.append(join.format(g=g, s=s) if g and s else (g or s))
        return head
    die("unsupported header_rows=%d for %s (set header_override)"
        % (cfg["header_rows"], cfg.get("label", cfg.get("after_label"))))


def parse_rows(tab):
    """Return the tabular's content rows (rule/hline rows dropped)."""
    # the column spec may nest braces, e.g. >{\raggedright}p{4.5cm}
    start = len("\\begin{tabular}{")
    body = tab[brace_end(tab, start):tab.rindex("\\end{tabular}")]
    body = unwrap_shortstack(body)  # stacked headers contain \\ inside braces
    rows = []
    for r in body.split(r"\\"):
        r = re.sub(r"\\(?:top|mid|bottom)rule|\\hline|\\addlinespace", "", r)
        r = re.sub(r"\\cmidrule(\(lr\))?\{[^}]*\}", "", r).strip()
        if r:
            rows.append(r)
    return rows


def alignment(ncol, mode):
    if isinstance(mode, list):
        if len(mode) != ncol:
            die("align lists %d columns, table has %d" % (len(mode), ncol))
        return list(mode)
    if mode == "left":
        return ["---"] * ncol
    if mode == "right":
        return ["---:"] * ncol
    return ["---"] + ["---:"] * (ncol - 1)  # default: label left, data right


def tabular_to_md(tab, cfg):
    rows = parse_rows(tab)
    head = build_header(rows, cfg)
    data = [split_cells(r) for r in rows[cfg["header_rows"]:]]

    ncol = len(head)
    row_map = cfg.get("row_map", {})
    rule = alignment(ncol, cfg.get("align"))

    lines = ["| " + " | ".join(head) + " |",
             "|" + "|".join(rule) + "|"]
    for cells in data:
        if len(cells) == 1 and multicol(cells[0]):
            # a panel label spanning the whole row, e.g. "baseline median state"
            cells = ["*%s*" % clean(multicol(cells[0])[1])] + [""] * (ncol - 1)
        else:
            cells = [clean(c) for c in cells]
        if cells and cells[0] in row_map:
            cells[0] = row_map[cells[0]]
        if len(cells) != ncol:
            die("row with %d cells under a %d column header: %s"
                % (len(cells), ncol, " & ".join(cells)))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


# ---- panels and captions --------------------------------------------------
SUBENV = r"\\begin\{(subtable|subfigure)\}.*?\\end\{\1\}"


def one_caption(text, name):
    """The single \\caption or \\subcaption argument in text."""
    caps = brace_arg(text, "caption") + brace_arg(text, "subcaption")
    if len(caps) != 1:
        die("%s has %d captions (expected exactly 1)" % (name, len(caps)))
    return caps[0]


def caption_to_md(cap, name):
    """Tex caption text to one markdown line, math kept as $...$."""
    cap = re.sub(r"\\label\{[^}]*\}", "", cap)
    cap = re.sub(r"(\\protect)?\\footnotemark(\[[^]]*\])?", "", cap)

    def ref(m):
        if m.group(1) not in REF_NUMBERS:
            die("caption of %s refers to %s, which is not in REF_NUMBERS"
                % (name, m.group(1)))
        return REF_NUMBERS[m.group(1)]
    cap = re.sub(r"\\ref\s*\{([^}]*)\}", ref, cap)
    cap = re.sub(r"\\(?:emph|textit)\{([^}]*)\}", r"*\1*", cap)
    cap = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", cap)
    cap = map_text(" ".join(cap.split()), text_markup).replace(r"\&", "&")
    return cap.strip()


def panels(env, name):
    """[(title, tabular)] for each subtable panel of a table environment."""
    out = []
    for m in re.finditer(SUBENV, env, flags=re.S):
        sub = m.group(0)
        tabs = re.findall(r"\\begin\{tabular\}.*?\\end\{tabular\}", sub, flags=re.S)
        if len(tabs) != 1:
            die("a panel of %s has %d tabulars (expected exactly 1)"
                % (name, len(tabs)))
        title = caption_to_md(one_caption(sub, name), name).rstrip(".")
        out.append((title, tabs[0]))
    if len(out) < 2:
        die("%s is configured with panels but has %d subtables" % (name, len(out)))
    return out


# ---- driver ---------------------------------------------------------------
def generate(paper_dir):
    tex = load_tex(paper_dir)
    out = {}
    for cfg in TABLES:
        name = cfg.get("label", cfg.get("after_label"))
        env = find_table_env(tex, cfg)
        if cfg.get("panels"):
            # the paper prints subtable captions as "(a) ...", "(b) ..."
            md = "\n".join("**(%s) %s**\n\n%s" % (letter, title, tabular_to_md(tab, cfg))
                           for letter, (title, tab) in zip("abcdefgh", panels(env, name)))
        else:
            md = tabular_to_md(get_tabular(env, cfg["tabular"], name), cfg)
        if "number" in cfg:
            # the table's own caption, outside any subtable panel
            cap = one_caption(re.sub(SUBENV, "", env, flags=re.S), name)
            md += "\nTable %d: %s\n" % (cfg["number"], caption_to_md(cap, name))
        out[cfg["out"]] = md
    return out


def main():
    args = sys.argv[1:]
    check = "--check" in args
    paper_dir = PAPER_DIR
    if "--paper-dir" in args:
        paper_dir = args[args.index("--paper-dir") + 1]

    generated = generate(paper_dir)
    stale = False
    for name, md in generated.items():
        path = os.path.join(OUTDIR, name)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current == md:
            sys.stdout.write("[up-to-date] %s\n" % name)
            continue
        stale = True
        if check:
            sys.stdout.write("[STALE] %s\n" % name)
            for line in difflib.unified_diff(
                    (current or "").splitlines(), md.splitlines(),
                    lineterm="", n=0):
                sys.stdout.write("    " + line + "\n")
        else:
            if not os.path.isdir(OUTDIR):
                os.makedirs(OUTDIR)
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            sys.stdout.write("[written] %s\n" % name)

    if check and stale:
        sys.stdout.write("\nGenerated tables are out of date. "
                         "Run: python tools/sync_tables_from_tex.py\n")
        sys.exit(1)
    sys.stdout.write("\nDone.\n")


if __name__ == "__main__":
    main()
