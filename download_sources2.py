import requests
import os
import time

out_dir = "sources"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# direct PDF attempts
direct_pdfs = [
    ("https://www.nature.com/articles/s41598-025-86554-2.pdf", "29_anwar_ensemble_fault_detection_nature2025.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S2772671124004005/pdfft?md5=07f2a5243398e5753374ae0062687124&pid=1-s2.0-S2772671124004005-main.pdf", "21_ghodchar_cnn_medium_voltage.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S0957417424028124/pdfft", "22_amiri_intelligent_fault_diagnosis.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S0306261920308114/pdfft", "23_linares_generalizable_fault_detection.pdf"),
    ("https://pdfs.semanticscholar.org/611e/12632181f1cf371badb68ae15bea87ae0cfc.pdf", "08_yang_cnn_lstm_semanticscholar.pdf"),
    ("https://www.preprints.org/manuscript/202405.0265/v1/download", "03_ml_fault_detection_literature_review.pdf"),
    ("https://www.preprints.org/manuscript/202405.0265/download", "03b_ml_fault_detection_literature_review.pdf"),
]

log = []
for url, fname in direct_pdfs:
    fpath = os.path.join(out_dir, fname)
    if os.path.exists(fpath) and os.path.getsize(fpath) > 5000:
        log.append(f"SKIP {fname} already exists")
        continue
    try:
        r = requests.get(url, headers=headers, timeout=(10, 60), stream=True, allow_redirects=True)
        r.raise_for_status()
        # read first chunk to detect HTML
        first = next(r.iter_content(1024))
        is_html = b"<html" in first.lower() or b"<!doctype" in first.lower()
        if fname.endswith(".pdf") and is_html:
            log.append(f"HTML {fname} (paywall)")
            continue
        with open(fpath, "wb") as f:
            f.write(first)
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        log.append(f"OK   {fname} ({os.path.getsize(fpath)} bytes)")
    except Exception as e:
        log.append(f"ERR  {fname}: {e}")
    time.sleep(0.5)

# For open-access MDPI and Springer, try to extract pdf version from article page
html_to_parse = [
    ("https://www.mdpi.com/2227-7390/10/21/3949", "05_mdpi_disturbance_inception_time.pdf"),
    ("https://www.mdpi.com/1996-1073/18/1/145", "14_mdpi_fault_location_ann_series_compensation.pdf"),
    ("https://www.mdpi.com/1996-1073/15/18/6525", "18_kulikov_relay_protection_ml_2022.pdf"),
    ("https://www.mdpi.com/1996-1073/16/14/5563", "19_kulikov_decision_tree_faults_2023.pdf"),
    ("https://www.sba.org.br/open_journal_systems/index.php/sbai/article/view/4055", "12_cieslak_symmetrical_components_dfr.pdf"),
]

import re
for page_url, desired_pdf in html_to_parse:
    fpath = os.path.join(out_dir, desired_pdf)
    if os.path.exists(fpath) and os.path.getsize(fpath) > 5000:
        log.append(f"SKIP {desired_pdf} already exists")
        continue
    try:
        r = requests.get(page_url, headers=headers, timeout=20, allow_redirects=True)
        if r.status_code != 200:
            log.append(f"FAIL {desired_pdf} page HTTP {r.status_code}")
            continue
        # look for pdf link
        m = re.search(r'href="(/[^"]+/pdf[^"]*)"', r.text)
        if not m:
            m = re.search(r'href="([^"]+\.pdf[^"]*)"', r.text)
        if m:
            pdf_url = m.group(1)
            if pdf_url.startswith("/"):
                from urllib.parse import urljoin
                pdf_url = urljoin(page_url, pdf_url)
            r2 = requests.get(pdf_url, headers=headers, timeout=(10, 60), stream=True)
            r2.raise_for_status()
            first = next(r2.iter_content(1024))
            if b"<html" in first.lower():
                log.append(f"HTML {desired_pdf} (paywall after parse)")
                continue
            with open(fpath, "wb") as f:
                f.write(first)
                for chunk in r2.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            log.append(f"OK   {desired_pdf} ({os.path.getsize(fpath)} bytes)")
        else:
            log.append(f"NOPDF {desired_pdf} no pdf link found")
    except Exception as e:
        log.append(f"ERR  {desired_pdf}: {e}")
    time.sleep(0.5)

with open(os.path.join(out_dir, "download_log2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("Round 2 complete. See download_log2.txt")
