import requests
import os
import time

out_dir = "sources"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

sources = [
    ("https://www.nature.com/articles/s41597-026-06587-8.pdf", "01_nature_dataset_oscillograms.pdf"),
    ("https://arxiv.org/pdf/2507.10011.pdf", "02_martinez_velasco_survey_ai_faults.pdf"),
    ("https://www.preprints.org/manuscript/202405.0265/download", "03_ml_fault_detection_literature_review.pdf"),
    ("https://arxiv.org/pdf/2302.09332.pdf", "04_li_incipient_fault_detection.pdf"),
    ("https://www.mdpi.com/2227-7390/10/21/3949/pdf", "05_mdpi_disturbance_inception_time.pdf"),
    ("https://ietresearch.onlinelibrary.wiley.com/doi/pdf/10.1049/iet-gtd.2018.6511", "06_silva_rms_voltage_disturbances.pdf"),
    ("https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1258549/pdf", "07_yang_cnn_lstm_dc_fault_diagnosis.pdf"),
    ("https://pdfs.semanticscholar.org/611e/12632181f1cf371badb68ae15bea87ae0cfc.pdf", "08_yang_cnn_lstm_semanticscholar.pdf"),
    ("https://ieeexplore.ieee.org/iel8/6287639/10820123/11224829.pdf", "09_ieee_deep_learning_fault_diagnosis.pdf"),
    ("https://pure.tudelft.nl/ws/portalfiles/portal/152461539/energies_16_04262.pdf", "10_tudelft_integrated_fault_detection_pmu.pdf"),
    ("https://overbye.engr.tamu.edu/wp-content/uploads/sites/146/2025/08/NAPS_October-2025_Warm-Start-State-Estimation-in-Power-Systems-Using-Deep-Residual-Networks-A-Comparative-Study-Against-CNN-LSTM-and-GAN.pdf", "11_mahzarnia_resnet_warm_start.pdf"),
    ("https://www.sba.org.br/open_journal_systems/index.php/sbai/article/download/4055/3583", "12_cieslak_symmetrical_components_dfr.pdf"),
    ("https://link.springer.com/content/pdf/10.1186/s42162-024-00429-w.pdf", "13_stepanova_deep_learning_relay_protection.pdf"),
    ("https://www.mdpi.com/1996-1073/18/1/145/pdf", "14_mdpi_fault_location_ann_series_compensation.pdf"),
    ("https://link.springer.com/content/pdf/10.1007/s00202-024-02818-6.pdf", "15_mondal_cnn_power_quality.pdf"),
    ("https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1132895/pdf", "16_tang_waveform_split_recognition.pdf"),
    ("https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2024.1365538/pdf", "17_gogula_hilbert_transform_hif.pdf"),
    ("https://www.mdpi.com/1996-1073/15/18/6525/pdf", "18_kulikov_relay_protection_ml_2022.pdf"),
    ("https://www.mdpi.com/1996-1073/16/14/5563/pdf", "19_kulikov_decision_tree_faults_2023.pdf"),
    ("https://link.springer.com/content/pdf/10.1007/s10462-022-10296-0.pdf", "20_shakiba_ml_survey.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S2772671124004005/pdfft", "21_ghodchar_cnn_medium_voltage.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S0957417424028124/pdfft", "22_amiri_intelligent_fault_diagnosis.pdf"),
    ("https://www.sciencedirect.com/science/article/pii/S0306261920308114/pdfft", "23_linares_generalizable_fault_detection.pdf"),
    ("https://arxiv.org/pdf/1605.09444.pdf", "24_arxiv_lssvm_fault_classification.pdf"),
    ("https://www.ijert.org/research/identification-of-power-system-faults-based-on-parks-transformation-IJERTV4IS070364.pdf", "25_ijert_parks_transformation_faults.pdf"),
    ("https://www.ijsrd.com/articles/LDRPTCP058.pdf", "26_ijsrd_fault_detection_ai.pdf"),
    # Russian / HTML sources (save as text via requests HTML fallback)
    ("https://eepir.ru/article/identifikaciya-tipa-korotkogo-zamykaniya-v-nbsp-elektricheskih-setyah-na-osnove-ansamblevyh-metodov-mashinnogo-obucheniya-i-nbsp-sinhronizirovannyh-vektornyh-izmerenij/", "27_eepir_fault_classification_sv_html.txt"),
    ("https://www.dissercat.com/content/informatsionnye-aspekty-zashchity-i-lokatsii-povrezhdenii-elektricheskoi-seti", "28_dissercat_info_aspects_fault_location_html.txt"),
]

log = []
for url, fname in sources:
    fpath = os.path.join(out_dir, fname)
    try:
        r = requests.get(url, headers=headers, timeout=45, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 500:
            # heuristic: if URL ends with pdf but we got HTML error page, skip
            if fname.endswith(".pdf") and b"<html" in r.content[:200].lower():
                # Might be paywall / redirect page
                # Save anyway but mark as possible HTML
                with open(fpath.replace(".pdf", "_html.pdf"), "wb") as f:
                    f.write(r.content)
                log.append(f"HTML {fname} (possible paywall, saved as _html.pdf) {len(r.content)} bytes")
            else:
                with open(fpath, "wb") as f:
                    f.write(r.content)
                log.append(f"OK   {fname} ({len(r.content)} bytes)")
        else:
            log.append(f"FAIL {fname} HTTP {r.status_code} size {len(r.content)}")
    except Exception as e:
        log.append(f"ERR  {fname}: {e}")
    time.sleep(0.7)

with open(os.path.join(out_dir, "download_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("Done. See sources/download_log.txt")
