# An Automated Methodology for Events Classification in Power Plants Based on DFR Data and Symmetrical Components

**Authors:** Dionatan A. G. Cieslak, Heitor J. Tessaro, Miguel Moreto  
**Conference:** Simpósio Brasileiro de Automação Inteligente - SBAI 2023  
**DOI:** https://doi.org/10.20906/SBAI-SBSE-2023/4055  
**URL:** https://www.sba.org.br/open_journal_systems/index.php/sbai/article/view/4055

## Abstract

Digital Fault Recorders (DFR) are valuable devices for power system monitoring since they allow the analysis of electrical quantities and information from the protection system. This paper presents two automated methodologies for event classification in power plants based on the phasor records, thus the same methodologies can be applied to PMU data. Besides the classification of the power units' operational states, the methodologies can also diagnose the causes of forced shutdowns of units based on the analysis of the symmetrical components. The process of fault classification aims to identify distinct events, such as single, double or three-line faults. The paper presents a comparison between pros and cons of the use of a specialist approach, based on fuzzy logic, and a generalist approach, based on convolutional neural networks. The methodologies are tested and evaluated with simulated data, and the validation is performed using real disturbance records. The results demonstrate the feasibility and effectiveness of the proposed methods. The convolutional network approach presented better performance with simulated data, while the fuzzy based approach managed to maintain its accuracy when used to classify real records.

**Keywords:** Digital Fault Recorder, Fault Classification, Fuzzy Logic, Machine Learning, Symmetrical Components

## Key Points

- **Data Source:** Digital Fault Recorder (DFR) phasor records (also applicable to PMU data)
- **Two Approaches Compared:**
  1. **Fuzzy Logic (Specialist approach)** — rule-based expert system using symmetrical components
  2. **Convolutional Neural Network (Generalist approach)** — deep learning for automatic feature extraction
- **Classification Goals:**
  - Operational states of power units
  - Causes of forced shutdowns
  - Fault types: single-line, double-line, three-line faults
- **Validation:** Simulated data + real disturbance records
- **Results:**
  - **CNN** performed better on simulated data
  - **Fuzzy logic** maintained accuracy better on real records

## Relevance to Current Project

This work directly supports the use of symmetrical components (Fortescue transformation) for fault classification and validates both classical (fuzzy logic) and modern (CNN) approaches for processing DFR/COMTRADE-type oscillographic data.

---
*Note: Full PDF was not available via automated download. This summary was compiled from the article abstract and metadata.*
