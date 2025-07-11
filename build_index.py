### updates index.html every time i push new data
#!/usr/bin/env python3
import pathlib, datetime, html, sys

DATA_DIR = pathlib.Path("data")
links = "\n".join(
    f'    <li><a href="data/{p.name}">{p.stem}</a></li>'
    for p in sorted(DATA_DIR.glob("*.html"))
)

template = f"""<!DOCTYPE html>
<html lang="en">
<meta charset="utf-8">
<title>DBS Peripheral Phys Figures</title>
<body>
  <h1>Interactive Figures</h1>
  <ul>
{links}
  </ul>
  <footer><small>Last updated {datetime.date.today()}</small></footer>
</body>
</html>"""

pathlib.Path("index.html").write_text(template, encoding="utf-8")
print("index.html rebuilt with", len(links.splitlines()), "entries.")
