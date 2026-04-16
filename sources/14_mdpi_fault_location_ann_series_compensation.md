# A Practical Approach for Fault Location in Transmission Lines with Series Compensation Using Artificial Neural Networks: Results with Field Data

**Authors:** Simone Aparecida Rocha, Thiago Gomes de Mattos, Eduardo Gonzaga da Silveira  
**Journal:** Energies 2025, 18(1), 145  
**DOI:** https://doi.org/10.3390/en18010145  
**URL:** https://www.mdpi.com/1996-1073/18/1/145

## Abstract

This paper presents a new method for fault location in transmission lines with series compensation, using data from voltage and current measurements at both terminals, applied to artificial neural networks. To determine the fault location, we present the proposal of using current phasors, obtained from the oscillography recorded during the short circuit, as the input to the neural network for training. However, the method does not rely on the internal voltage values of the sources or their respective equivalent Thevenin impedances to generate training files for the neural network in a transient simulator. The source data are not known exactly at the time of the short circuit in the transmission line, leading to greater errors when neural networks are applied to real electrical systems of utility companies, which reduces the dependency on electrical network parameters. Low errors are obtained in both simulated and real fault cases, demonstrating its effectiveness and practical applicability.

**Keywords:** transmission lines; series compensation; artificial neural networks; fault location; field oscillographs

## 1. Introduction

Overhead transmission lines are vulnerable to defects. Determining the location of the fault is critically important as it avoids the need for a complete inspection of the transmission line, enabling quicker restoration of power supply.

Artificial neural networks (ANNs) enable pattern recognition for fault location. Since the early 2000s, various authors have researched fault location using ANNs. Only Aggarwall's study presents results for real fault location cases, highlighting limitations in generalization of ANNs: low errors in simulated cases but poor performance on real-field oscillographs. The main cause is the difficulty in ensuring training data effectively represent real electrical systems.

This paper proposes a new methodology independent of the parameters of the sources connected to the transmission line terminals, enabling reduced errors.

## 2. Protection of Capacitor Banks with MOV

Capacitor banks connected in series use metal oxide varistors (MOV) to limit overvoltage. During a fault, the MOV enters conduction, diverting current. After fault elimination, operating conditions are restored.

## 3. Steps of the Process

The algorithm flowchart:
1. Read voltage and current data from both terminals in **COMTRADE** format
2. Identify fault instant (divide into pre-fault and fault periods)
3. Low-pass filtering (2nd-order Butterworth, fc=100 Hz)
4. Data interpolation to 16 points per cycle
5. Least squares method to estimate fundamental phasors
6. Fault classification
7. Fault location using ANN

## 4. Fault Dynamics in a Compensated Line

Illustrated on a 211 km, 500 kV, 70% compensated line in Brazil. Field data from actual AG fault shown with oscillograms from both terminals and MOV conduction periods.

## 5. Proposed Algorithm

Main characteristics:
- (a) Elimination of Thevenin equivalent voltage and impedance values from ATP training
- (b) Individualization: for each fault occurrence, network training is performed specifically

The sources are adjusted using phasors estimated from the COMTRADE file of the fault input. Pre-fault source impedances are **not required**.

### 5.1. Fault Circuit Representation

ATP model assembled from voltage phasors of the fault period. Training files generated for each fault occurrence.

**Table 2. Training patterns variables.**
- Fault locations: every 2.5% of line (39 points)
- Phase-ground Rf: 0–42 Ω (15 values) → 585 scenarios
- Phase-phase/3-phase Rf: 0–5 Ω (7 values) → 273 scenarios

**Table 3. Validation patterns variables.**
- Fault locations: every 7% (14 points)
- Various fault resistances

### 5.2. Neural Network Structure

- Feedforward structure, backpropagation, Levenberg–Marquardt
- Hyperbolic tangent activation
- Hidden layers: 12 and 8 neurons
- Output: 1 neuron (fault location)
- Inputs based on current phasor modules:
  - Phase-ground: 2 inputs
  - Phase-phase-ground/phase-phase: 4 inputs
  - Three-phase: 6 inputs

## 6. Results Obtained

### 6.1. Real Signals — Lines Without Series Compensation

Nine real fault cases from Brazilian power system.

**Table 5. Errors for real short-circuit cases (lines without series compensation).**

| Line | Fault | Inspection (km) | Cause | Ref. [39] Error (%) | **Proposed Method Error (%)** |
|------|-------|-----------------|-------|---------------------|-------------------------------|
| 1 | AG | 60.0 | AD | 12.41 | **0.38** |
| 1 | BG | 54.0 | — | 31.40 | **2.29** |
| 2 | AG | 30.0 | Fire | 12.70 | **2.96** |
| 3 | AG | 55.0 | Fire | 4.90 | **0.19** |
| 3 | CG | 76.0 | — | 8.90 | **0.06** |
| 3 | CG | 317.0 | AD | 3.30 | **0.10** |
| 4 | ABG | 16.0 | AD | — | **1.44** |

**Average error:** Ref. [39] = 12.27%, **Proposed = 1.14%**

### 6.2. Simulated Signals — Series-Compensated Lines

256 km, 345 kV line with 35% and 70% compensation. Errors for simulated cases: **0.01% to 0.63%**.

### 6.3. Real Signals — Series-Compensated Lines

211 km line, 70% compensation (Sobradinho–S. J. Piauí):

| Fault | Location (km) | Inspection (km) | Error (%) |
|-------|---------------|-------------------|-----------|
| AG | 5.7 | 7.0 | **0.62** |
| BCG | 129.38 | 132.32 | **1.39** |

## 7. Conclusions

The method eliminates source parameter dependency, significantly improving reliability. Processing time: approximately 5 minutes on a 2.78 GHz/8 GB RAM computer in MATLAB. Code available at: https://github.com/Eduardo-Gonzaga-CEFET/Fault_Locator

---
*Full article extracted from MDPI open-access HTML.*
