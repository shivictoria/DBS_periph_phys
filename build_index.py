#!/usr/bin/env python3
"""
Auto-generate hierarchical index pages.

* Home page lists every first-level folder in ./data  (e.g. Cat_A, Cat_B …)
* Each category gets its own index.html that lists the Plotly *.html files
  inside that folder (no recursion beyond one level for clarity).

Run via GitHub Actions on every push that touches data/.
"""

from pathlib import Path
import datetime as dt
import html
import sys

DATA_DIR = Path("data")           # root for all categories
TODAY    = dt.date.today()


def write_file(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    print("wrote", path)


def get_shared_styles():
    """Return the shared CSS styles for all index pages"""
    return """
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
        background-color: #f8f9fa;
      }
      .container {
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      }
      h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 15px;
        margin-bottom: 30px;
        font-size: 2em;
      }
      h2 {
        color: #34495e;
        margin-top: 30px;
        margin-bottom: 20px;
        border-left: 4px solid #3498db;
        padding-left: 15px;
      }
      .intro {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 20px 0;
      }
      .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 30px 0;
      }
      .category-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }
      .category-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
      }
      .category-card h3 {
        color: #2c3e50;
        margin-top: 0;
        margin-bottom: 15px;
      }
      .category-card p {
        color: #6c757d;
        margin-bottom: 15px;
        font-size: 0.9em;
      }
      .category-card a {
        color: #3498db;
        text-decoration: none;
        font-weight: 500;
      }
      .category-card a:hover {
        text-decoration: underline;
      }
      .figure-list {
        list-style: none;
        padding: 0;
        margin: 20px 0;
      }
      .figure-list li {
        background: #f8f9fa;
        margin: 10px 0;
        padding: 15px 20px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        transition: background-color 0.2s ease;
      }
      .figure-list li:hover {
        background: #e9ecef;
      }
      .figure-list a {
        color: #2c3e50;
        text-decoration: none;
        font-weight: 500;
        display: block;
      }
      .figure-list a:hover {
        color: #3498db;
      }
      .back-link {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        text-align: center;
      }
      .back-link a {
        color: #7f8c8d;
        text-decoration: none;
        font-size: 0.9em;
      }
      .back-link a:hover {
        text-decoration: underline;
      }
      .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        text-align: center;
        color: #6c757d;
        font-size: 0.8em;
      }
    </style>
    """


def get_category_descriptions():
    """Return descriptions for each category"""
    return {
        "bp_nk_sync": "Biopac, NK (iEEG) and behavioural data synchronisation process to align data streams.",
        "emp_vs_bp": "Comparative analysis between Empatica wearable sensors and Bioac laboratory measurements for physiological monitoring validation."
    }


def make_homepage(categories):
    descriptions = get_category_descriptions()
    
    cards = []
    for cat in categories:
        desc = descriptions.get(cat.name, "Interactive data visualisations and analysis results.")
        cards.append(f"""
        <div class="category-card">
          <h3>{html.escape(cat.name)}</h3>
          <p>{desc}</p>
          <a href="{DATA_DIR.name}/{cat.name}/">Explore →</a>
        </div>""")
    
    category_grid = "\n".join(cards)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DBS Peripheral Phys – Interactive Data Visualisations</title>
{get_shared_styles()}
</head>
<body>
<div class="container">
  <h1>DBS Peripheral Physiology</h1>
  
  <div class="intro">
    <p>Multimodal data collection and visualisation of peripheral physiological data during deep brain stimulation monitoring research.</p>
  </div>

  <h2>Projects</h2>
  <div class="category-grid">
{category_grid}
  </div>

  <div class="footer">
    <small>Last updated {TODAY}</small>
  </div>
</div>
</body>
</html>"""


def make_category_page(cat: Path, html_files):
    descriptions = get_category_descriptions()
    category_desc = descriptions.get(cat.name, "Interactive figures and analysis results.")
    
    # Filter out the index.html from the list and create special entries for story pages
    filtered_files = [f for f in html_files if f.name != "index.html"]
    
    fig_links = []
    for p in filtered_files:
        title = p.stem
        # Special handling for story pages
        if "_sync_story" in p.name:
            title = title.replace("_sync_story", " - Synchronization Story")
        elif "_timeline_" in p.name:
            title = title.replace("_timeline_", " Timeline - ").replace("presync", "Pre-sync").replace("postsync", "Post-sync")
        
        fig_links.append(f'    <li><a href="{html.escape(p.name)}">{html.escape(title)}</a></li>')
    
    fig_list = "\n".join(fig_links) if fig_links else "    <li><em>No figures available yet</em></li>"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(cat.name)} – DBS Peripheral Phys</title>
{get_shared_styles()}
</head>
<body>
<div class="container">
  <h1>{html.escape(cat.name)}</h1>
  
  <div class="intro">
    <p>{category_desc}</p>
  </div>

  <h2>Available Figures</h2>
  <ul class="figure-list">
{fig_list}
  </ul>

  <div class="back-link">
    <a href="../../index.html">← Back to Categories</a>
  </div>

  <div class="footer">
    <small>Last updated {TODAY}</small>
  </div>
</div>
</body>
</html>"""


def main():
    if not DATA_DIR.is_dir():
        sys.exit("❌  data/ folder not found")

    categories = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])

    # --- build category pages ------------------------------------------------
    for cat in categories:
        html_files = sorted(cat.glob("*.html"))
        cat_page   = make_category_page(cat, html_files)
        write_file(cat / "index.html", cat_page)

    # --- build home page -----------------------------------------------------
    homepage = make_homepage(categories)
    write_file(Path("index.html"), homepage)

    print(f"✔️  Rebuilt root index + {len(categories)} category pages")


if __name__ == "__main__":
    main()
