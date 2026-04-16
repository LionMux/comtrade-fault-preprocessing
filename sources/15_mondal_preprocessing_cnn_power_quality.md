# A novel amalgamation of pre-processing technique and CNN model for accurate classification of power quality disturbances

**Authors:** Prity Soni, Pankaj Mishra, Debasmita Mondal  
**Journal:** Electrical Engineering, Volume 107, pages 5187–5206 (2025)  
**DOI:** https://doi.org/10.1007/s00202-024-02818-6  
**URL:** https://link.springer.com/article/10.1007/s00202-024-02818-6

## Abstract

This work presents an innovative framework that combines the recurrence plots (RP) method with ResNet-50 (a convolutional neural network) to autonomously extract relevant features for classifying multiple power quality disturbances for a power signal using the support vector machine. The ResNet-50 is employed to extract the most discriminated features from the two-dimensional images obtained from 1-D signals using the RP method. The work investigates synthetic power quality disturbances, including nine single disturbances, eight double disturbances, and seven triple disturbances. The validation is conducted on the Standard IEEE 5-bus system under diverse fault scenarios. The statistical stability is assessed using the Sign test and the Wilcoxon test.

**Keywords:** Power quality disturbances; Signal processing; Image processing; Feature extraction; Deep learning; Classification

## Methodology

- **Pre-processing:** Recurrence Plots (RP) transform 1-D power signals into 2-D images
- **Feature Extraction:** ResNet-50 CNN extracts discriminated features from RP images
- **Classification:** Support Vector Machine (SVM) classifier on extracted features
- **Dataset:** Synthetic disturbances — 9 single, 8 double, 7 triple disturbances
- **Validation:** Standard IEEE 5-bus system under diverse fault scenarios
- **Statistical Tests:** Sign test and Wilcoxon test for result reliability

## Key Findings

- The proposed RP + ResNet-50 + SVM framework achieved superior performance compared to other advanced CNN models and pre-processing techniques
- Effective for complex/multi-disturbance classification scenarios
- Demonstrates the value of converting time-series power quality data into image representations for deep learning analysis

## Data Availability

No datasets were generated or analysed during the current study.

## References (Selected)

- IEEE Std 1159–1995 (Power Quality Monitoring)
- Samanta et al. (2022) — EEMD + optimized ELM for PQ events
- Eristi & Eristi (2022) — Deep learning for PQ disturbance classification
- Dawood & Babulal (2023) — Red deer optimized RNN for PQ classification
- Tang et al. (2020) — Optimized S-transform + kernel SVM
- Rodriguez et al. (2021) — HHT + LSTM for PQ disturbances
- He et al. (2016) — Deep residual learning for image recognition (ResNet)
- Todeschini et al. (2022) — Image-based deep transfer learning for PQ disturbances

---
*Note: Full text is behind Springer paywall. This file contains the abstract, methodology summary, and key findings extracted from the article preview.*
