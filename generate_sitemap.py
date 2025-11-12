#!/usr/bin/env python3
"""
Generate sitemap.xml from list.json
Run this script whenever you add new articles to keep the sitemap up to date.
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

def generate_sitemap():
    # Read list.json
    list_path = Path(__file__).parent / 'list.json'
    with open(list_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Get current date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Create XML root
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:news', 'http://www.google.com/schemas/sitemap-news/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    urlset.set('xmlns:mobile', 'http://www.google.com/schemas/sitemap-mobile/1.0')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    urlset.set('xmlns:video', 'http://www.google.com/schemas/sitemap-video/0.1')
    
    # Add homepage
    homepage = ET.SubElement(urlset, 'url')
    ET.SubElement(homepage, 'loc').text = 'https://help.appclust.com/'
    ET.SubElement(homepage, 'lastmod').text = today
    ET.SubElement(homepage, 'changefreq').text = 'daily'
    ET.SubElement(homepage, 'priority').text = '1.0'
    
    # Add videos page
    videos_page = ET.SubElement(urlset, 'url')
    ET.SubElement(videos_page, 'loc').text = 'https://help.appclust.com/#videos'
    ET.SubElement(videos_page, 'lastmod').text = today
    ET.SubElement(videos_page, 'changefreq').text = 'weekly'
    ET.SubElement(videos_page, 'priority').text = '0.9'
    
    # Add articles (non-video items)
    for item in articles:
        if item.get('type') != 'video':
            kb_id = item.get('kb_id')
            if kb_id:
                url_elem = ET.SubElement(urlset, 'url')
                ET.SubElement(url_elem, 'loc').text = f'https://help.appclust.com/article/{kb_id}'
                ET.SubElement(url_elem, 'lastmod').text = today
                ET.SubElement(url_elem, 'changefreq').text = 'monthly'
                # Higher priority for sign in and popular articles
                priority = '0.9' if 'sign_in' in kb_id or 'how_to_add' in kb_id else '0.8'
                ET.SubElement(url_elem, 'priority').text = priority
    
    # Write to file
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space='  ')
    sitemap_path = Path(__file__).parent / 'sitemap.xml'
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Sitemap generated successfully with {len(articles)} items")
    print(f"📄 Saved to: {sitemap_path}")

if __name__ == '__main__':
    generate_sitemap()

