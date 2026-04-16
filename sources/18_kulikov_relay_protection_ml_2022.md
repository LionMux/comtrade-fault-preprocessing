# Relay Protection and Automation Algorithms of Electrical Networks Based on Simulation and Machine Learning Methods

**Authors:** Aleksandr Kulikov, Anton Loskutov, Dmitriy Bezdushniy  
**Journal:** Energies 2022, 15(18), 6525  
**DOI:** https://doi.org/10.3390/en15186525  
**URL:** https://www.mdpi.com/1996-1073/15/18/6525

## Abstract

The tendencies and perspective directions of development of modern digital devices of relay protection and automation (RPA) are considered. One of the promising ways to develop protection and control systems is the development of fundamentally new algorithms for recognizing emergency modes. They work in accordance with the triggering rule, which is formed after processing the results of model experiments. These algorithms are able to simultaneously control a large number of features or mode parameters (current, voltage, resistance, phase, etc.). Thus, the algorithms are multidimensional. The application of classical machine learning algorithms in RPA tasks is analyzed, in particular, methods of k-nearest neighbors, logistic regression, and support vectors. The use of specialized trainable triggering elements is studied both for building new protections and for improving the sophistication of traditional types of relay protection devices.

**Keywords:** relay protection and automation (RPA); IEC 61850; machine learning; simulation; RPA algorithm; k-nearest neighbor method; logistic regression method; support vector machine

## 1. Introduction

World trends in the electric power industry determine promising areas of scientific research in relay protection. Among them:
- Development of adaptive protections
- Issues of organizing remote access and cybersecurity
- Analysis of the need to increase requirements for relay protection in distribution networks with distributed generation
- Application of simulation technologies and IEC 61850 standard

The existing tendency to increase the share of digital relay protection devices, as well as the growth of their computing power, is likely to continue. Modern RPA terminals perform protection, control, registration, oscillography, and data exchange functions.

The construction of new recognition systems requires:
1. Obtaining statistical data that fully describes normal and emergency modes
2. Identification of regularities allowing to formulate a recognition rule

The solution can be carried out with EPS simulation using the Monte Carlo method, which determines ranges, frequency distributions, and correlations between signs.

## 2. Machine Learning in the Task of Developing New Algorithms for Identifying Emergency Modes

Machine learning is a section of artificial intelligence designed to build algorithms that can learn from empirical data. Unlike statistical methods, ML methods directly analyze instances of the training sample.

Types:
- **Unsupervised learning:** discovers hidden patterns (clustering)
- **Supervised learning:** predicts unknown quantities based on feature vectors
  - Regression (continuous target)
  - Classification (discrete target)

The task of constructing trainable RPA modules based on labeled model data is a typical supervised learning classification task.

## 3. Application of Simulation in the Problem of Classifying EPS Modes

A network section with distributed generation was modeled in Matlab. The task: develop a triggering element for the RPA device at the beginning of line ω1, protecting from three-phase and phase-to-phase short circuits, with detuning from normal and self-start modes.

Simulation results showed that a significant part of emergency short-circuit currents turned out to be commensurate with normal currents due to the generator in the branch line reducing the proportion of short-circuit current. Classic current protection is ineffective due to low sensitivity.

Distance protection with a characteristic obtained by detuning from normal modes accommodated **74%** of short circuits on the line. Despite exceeding current protection results, efficiency is still insufficient.

## 4. Considered Machine Learning Methods

### 4.1. K-Nearest Neighbor Method
- Metric classification algorithm analyzing closest elements of the training sample
- Classification by majority principle among k-nearest neighbors
- Distance functions: Euclidean, Chebyshev, Manhattan
- Feature space: active and reactive components of complex resistance
- Result: **95.2%** of short circuits detected, **2.9%** false triggering probability
- With modified criterion (all k neighbors must be α): reduced false triggering at cost of sensitivity
- Maximum achieved recognition: **98.8%**

### 4.2. Logistic Regression Method
- Linear data classification finding optimal hyperplane
- Optimization minimizes objective function increasing with classification error
- Uses sigmoid function to determine probability of belonging to class α
- ROC-curve analysis: unambiguous recognition in ~60% with zero false operations; up to ~90% with 10% false triggering
- With expanded feature space (phase current, reactive power, complex resistance modulus) and rectifying space: **98%** correct classification (0.8% lower than k-NN)

### 4.3. Support Vector Machine (SVM)
- Finds hyperplane with maximum gap between classes
- For linearly inseparable samples, introduces penalty for misclassification (parameter C)
- Dual task solved via quadratic programming
- On 2D feature space (P-Z): outperformed logistic regression
- **With feature space dimension ≥ 4: error-free classification achieved**
- SVM proved superior to k-NN and logistic regression for the classification task

## 5. Improving Technical Excellence of RPA Devices through Training Modules

Example: distance protection of line ω1 with reserve for transformer T1, line ω2, and line ω3.
- Traditional DP second stage: only **42.7%** detection for transformer T1, **5.8%** for line ω2
- Proposed solution: combine independent DP stages with SVM-based faulty section selectors
- Three SVM classifiers developed: "SVM T1", "SVM ω2", "SVM ω3"

Results:
- **SVM T1:** 95% correct decisions for phase-to-phase SCs inside transformer
- **SVM ω2:** required 3D feature space (impedance + current) for error-free separation
- **SVM ω3:** error-free classification possible in 2D with linear kernel; polynomial kernel preferred for robustness

These additional triggering elements almost unmistakably identify damaged sections, increasing sensitivity in reserve zones.

## 6. Conclusions

1. Simulation-based statistical experiments for parameterizing triggering elements: distance protection characteristic based on simulation accommodated **17% more** short-circuits than the analytical method.
2. Trained multi-parameter relay protection using k-NN, logistic regression, and SVM demonstrated higher short-circuit detection than traditional current and distance protection.
3. Machine learning methods recognized **>98%** of various short circuits vs. **74%** for distance triggering — an increase of **>24%**. SVM provided error-free classification.
4. SVM-based trainable triggering elements enable error-free fault localization, allowing more efficient redundancy and increased reliability.

---
*Extracted from MDPI open-access HTML. Full article contains 20 figures and 33 references.*
