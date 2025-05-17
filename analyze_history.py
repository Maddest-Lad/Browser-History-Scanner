import argparse
import sqlite3
import logging
import json
import csv
from pathlib import Path

def analyze_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    result = {}

    try:
        # Total entries
        cursor.execute("SELECT COUNT(*) FROM unified_history")
        result["total_entries"] = cursor.fetchone()[0]

        # Per-browser stats
        cursor.execute("SELECT browser, COUNT(*) FROM unified_history GROUP BY browser")
        result["browser_stats"] = [{"browser": b, "count": c} for b, c in cursor.fetchall()]

        # Top 5 most visited sites
        cursor.execute("SELECT url, title, visit_count FROM unified_history ORDER BY visit_count DESC LIMIT 5")
        result["top_sites"] = [
            {"url": url, "title": title, "visit_count": visit_count}
            for url, title, visit_count in cursor.fetchall()
        ]

        # Top 5 most frequent domains
        cursor.execute("""
            SELECT domain, subdomain, visit_count 
            FROM domain_stats 
            ORDER BY visit_count DESC 
            LIMIT 5
        """)
        result["top_domains"] = [
            {"domain": domain, "subdomain": subdomain, "visit_count": count}
            for domain, subdomain, count in cursor.fetchall()
        ]
    finally:
        conn.close()
    return result

def write_csv(data, out_path):
    with open(out_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write summary stats
        writer.writerow(["total_entries", data["total_entries"]])
        writer.writerow([])
        writer.writerow(["browser", "count"])
        for stat in data["browser_stats"]:
            writer.writerow([stat["browser"], stat["count"]])
        writer.writerow([])
        writer.writerow(["Top 5 Most Visited Sites"])
        writer.writerow(["url", "title", "visit_count"])
        for site in data["top_sites"]:
            writer.writerow([site["url"], site["title"], site["visit_count"]])
        writer.writerow([])
        writer.writerow(["Top 5 Most Frequent Domains"])
        writer.writerow(["domain", "subdomain", "visit_count"])
        for dom in data["top_domains"]:
            writer.writerow([dom["domain"], dom["subdomain"] or "", dom["visit_count"]])

def write_json(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze unified browser history database and output stats.")
    parser.add_argument('--in', dest="in_db", default="aggregate_history.db", help='Input unified history database (default: aggregate_history.db)')
    parser.add_argument('--out', dest="out_file", default="history.csv", help='Output file (.csv or .json) (default: history.csv)')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    data = analyze_db(args.in_db)
    out_path = Path(args.out_file)
    if out_path.suffix.lower() == ".csv":
        write_csv(data, out_path)
        logging.info(f"Analysis written to {out_path} (CSV format)")
    elif out_path.suffix.lower() == ".json":
        write_json(data, out_path)
        logging.info(f"Analysis written to {out_path} (JSON format)")
    else:
        raise ValueError("Output file must have .csv or .json extension")