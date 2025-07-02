import re
import csv

# Fields to extract
TARGET_FIELDS     = ['PMID', 'TI', 'AB', 'JT']
MULTILINE_FIELDS  = ['AB', 'TI']

def parse_pubmed_entries(text):
    # Split whenever a new PMID- line appears at the start of a line
    entries = re.split(r'(?m)^(?=PMID\s*-\s*)', text.strip())
    parsed = []

    for entry in entries:
        record = {k: '' for k in TARGET_FIELDS}
        current = None

        for line in entry.split('\n'):
            # Try to match KEY  -  value (allowing spaces around dash)
            m = re.match(r'^([A-Z]{2,4})\s*-\s*(.*)$', line)
            if m:
                key, val = m.groups()
                if key in TARGET_FIELDS:
                    current = key
                    # start or overwrite
                    record[key] = val.strip()
                else:
                    current = None
            else:
                # continuation of last multiline field
                if current in MULTILINE_FIELDS:
                    record[current] += ' ' + line.strip()

        parsed.append(record)
    return parsed

def convert_to_csv(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    rows = parse_pubmed_entries(txt)

    with open(output_path, 'w', newline='', encoding='utf-8') as fout:
        w = csv.DictWriter(fout, fieldnames=TARGET_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"✅ Wrote {len(rows)} records to {output_path}")

# === Run it ===
convert_to_csv('pubmed.txt', 'pubmed_output.csv')
