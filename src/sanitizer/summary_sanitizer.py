from pylatex.utils import escape_latex

def sanitize_summary(path_markers, summary_data, ERRORS):
    return escape_latex(summary_data)