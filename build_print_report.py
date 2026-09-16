"""Inject print-focused CSS into the nbconvert HTML report."""

from pathlib import Path


source = Path("COMP576_HW1.html")
stylesheet = Path("print_report.css")
destination = Path("COMP576_HW1_print.html")

html = source.read_text(encoding="utf-8")
css = stylesheet.read_text(encoding="utf-8")
marker = "</head>"
if marker not in html:
    raise RuntimeError("Could not find </head> in notebook HTML")

html = html.replace(marker, f"<style>\n{css}\n</style>\n{marker}", 1)
destination.write_text(html, encoding="utf-8")
print(f"Created {destination}")
