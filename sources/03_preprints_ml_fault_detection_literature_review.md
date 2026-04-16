# Machine Learning Advances in Transmission Line Fault Detection: A Literature Review

**Authors:** Judy Lhyn Sarmiento, Jam Cyrex Delfino, Edwin R. Arboleda  
**Preprint:** Preprints.org 2024, DOI: 10.20944/preprints202405.0265  
**URL:** https://www.preprints.org/manuscript/202405.0265

## Abstract

Fault detection in transmission lines plays a role in maintaining the dependability and steadiness of power networks. Traditional methods often struggle to handle the diverse nature of real world fault situations. Machine learning (ML) algorithms offer a data centered approach that can adjust and learn from datasets potentially overcoming the limitations of traditional approaches. This document presents a review of progress in using ML for detecting faults in transmission lines. We explore how ML algorithms have evolved in fault detection, including techniques like neural networks, recurrent neural networks featuring Long Short Term Memory and convolutional neural networks. We discuss the obstacles and prospects linked to putting ML based fault detection systems into practice such as challenges with data quality, model interpretability and integration with existing grid monitoring systems.

**Keywords:** transmission line fault detection; machine learning; neural networks; fault scenarios

## Introduction

Transmission line fault detection is crucial for reliability and stability of electrical power systems. With increasing complexity of modern power grids, traditional methods face significant challenges in accuracy, speed, and adaptability. Machine learning offers the potential to automatically learn complex patterns from data, enabling more accurate and efficient detection.

Studies have demonstrated effectiveness of various ML approaches: ANNs, SVMs, decision trees, ensemble methods. Li et al. utilized deep learning for fault detection achieving high accuracy even with noise. Wong et al. proposed a hybrid CNN+LSTM model showing significant improvements over traditional methods.

## Materials and Methods

Comprehensive search of IEEE Xplore, ScienceDirect, Elsevier, and Google Scholar for studies published between 2020 and 2024. Keywords: "machine learning," "transmission line," "fault detection." A total of **25 studies** were finally included.

## Results

### Fault Types Identified
- LG (line-to-ground)
- LL (line-to-line)
- LLG (double line-to-ground)
- LLLG (triple line-to-ground)
- High impedance faults
- Short-circuit faults

### Machine Learning Algorithms Used

| Authors | Year | Fault | Method |
|---------|------|-------|--------|
| Aker et al. | 2020 | LG, LL, LLG, LLLG | Bayesian NN, MLP |
| Anand et al. | 2020 | LG, LL, LLG, LLL | Empirical mode decomposition |
| Belagoune et al. | 2021 | High Impedance | LSTM |
| Fahim et al. | 2020 | Short Circuit | Self-attention CNN (SAT-CNN) |
| Fahim et al. | 2021 | Short Circuit | Capsule network with sparse filtering (CNSF) |
| Ferreira et al. | 2020 | Short Circuit | Feedforward NN |
| Haq et al. | 2020 | Three-Phase | Db4 wavelet |
| Liang et al. | 2020 | Short Circuit | R-CNN |
| Liu et al. | 2021 | Insulator Faults | R-CNN |
| Rafique et al. | 2021 | LG, LL, LLG, LLL | RNN |
| Teimourzadeh et al. | 2020 | Single-phase ground | CNN |
| Tong et al. | 2020 | Short Circuit, 3-phase | IEEE 39 bus system |
| Wang et al. | 2020 | Three-Phase | WRC-SDT (Wavelet+Clarke+Stockwell+DT) |
| Wong et al. | 2021 | Short Circuit | CNN |
| Zhang et al. | 2021 | Internal/External Fault | Stationary wavelet transform (SWT) |
| Zheng et al. | 2021 | Short Circuit | R-CNN |

### Performance Metrics

Common metrics: accuracy, precision, recall, F1-score.
- Aker et al. reported high accuracy for BNN and MLP fault classification
- Fahim et al. demonstrated superior performance of self-attention CNNs for short-circuit faults

## Discussion

### Comparison with Traditional Methods
- **LSTM networks** (Belagoune et al.) showed effectiveness for high impedance faults compared to conventional methods
- **CNN + SWT** (Zhang et al.) outperformed traditional signal processing techniques
- ML models demonstrated robustness to different operating conditions, noise levels, and fault types
- Generalization to unseen data contributes to real-world applicability

### Limitations and Challenges
- Availability of labeled training data
- Interpretability of complex models
- Integration into existing grid monitoring systems
- Computational resources and infrastructure compatibility for real-time deployment

## Conclusion

Machine learning has transformative impact on transmission line fault detection, paving the way for more efficient and reliable power grid management. Continued research and innovation hold promise for advancing fault detection capabilities, ultimately contributing to sustainable and resilient operation of power systems.

---
*Extracted from Preprints.org open-access manuscript.*
