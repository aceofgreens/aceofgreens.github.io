"""
Minimal zero-dependency XML sitemap generator for Pelican.
Generates <OUTPUT_PATH>/sitemap.xml containing the homepage, published articles,
published pages, and tags page (excluding drafts and hidden pages such as 404).
"""

import os
from xml.sax.saxutils import escape

from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator

_collected_entries = []


def _format_date(dt):
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d")


def _build_url(siteurl, path):
    base = (siteurl or "").rstrip("/")
    rel = (path or "").lstrip("/")
    if not rel:
        return f"{base}/"
    return f"{base}/{rel}"


def collect_urls(generators):
    global _collected_entries
    entries = []
    latest_date = None
    settings = None

    for generator in generators:
        settings = generator.settings
        siteurl = settings.get("SITEURL", "")

        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                lastmod = getattr(article, "modified", None) or getattr(article, "date", None)
                if lastmod and (latest_date is None or lastmod > latest_date):
                    latest_date = lastmod
                entries.append({
                    "loc": _build_url(siteurl, article.url),
                    "lastmod": _format_date(lastmod),
                    "priority": "0.8",
                })
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                lastmod = getattr(page, "modified", None) or getattr(page, "date", None)
                entries.append({
                    "loc": _build_url(siteurl, page.url),
                    "lastmod": _format_date(lastmod),
                    "priority": "0.6",
                    "slug": getattr(page, "slug", ""),
                })

    if settings is None:
        _collected_entries = []
        return

    siteurl = settings.get("SITEURL", "")
    latest_str = _format_date(latest_date)

    # Set lastmod for index-like pages (e.g., posts.html) to latest article date
    for entry in entries:
        if entry.pop("slug", "") == "posts" and not entry["lastmod"]:
            entry["lastmod"] = latest_str

    result = [{
        "loc": _build_url(siteurl, ""),
        "lastmod": latest_str,
        "changefreq": "weekly",
        "priority": "1.0",
    }]

    tags_save_as = settings.get("TAGS_SAVE_AS", "")
    if tags_save_as:
        result.append({
            "loc": _build_url(siteurl, tags_save_as),
            "lastmod": latest_str,
            "priority": "0.5",
        })

    result.extend(entries)
    _collected_entries = result


def write_sitemap(pelican_obj):
    if not _collected_entries:
        return

    output_path = pelican_obj.settings.get("OUTPUT_PATH", "output")
    os.makedirs(output_path, exist_ok=True)
    sitemap_path = os.path.join(output_path, "sitemap.xml")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in _collected_entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(entry['loc'])}</loc>")
        if entry.get("lastmod"):
            lines.append(f"    <lastmod>{escape(entry['lastmod'])}</lastmod>")
        if entry.get("changefreq"):
            lines.append(f"    <changefreq>{escape(entry['changefreq'])}</changefreq>")
        if entry.get("priority"):
            lines.append(f"    <priority>{escape(entry['priority'])}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def register():
    signals.all_generators_finalized.connect(collect_urls)
    signals.finalized.connect(write_sitemap)
