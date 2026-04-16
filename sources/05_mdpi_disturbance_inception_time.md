# Fast Algorithms for Estimating the Disturbance Inception Time in Power Systems Based on Time Series of Instantaneous Values of Current and Voltage with a High Sampling Rate

**Authors:** Mihail Senyuk, Svetlana Beryozkina, Pavel Gubin, Anna Dmitrieva, Firuz Kamalov, Murodbek Safaraliev, Inga Zicmane  
**Journal:** Mathematics 2022, 10(21), 3949  
**DOI:** https://doi.org/10.3390/math10213949  
**URL:** https://www.mdpi.com/2227-7390/10/21/3949

## Abstract

The study examines the development and testing of algorithms for disturbance inception time estimation in a power system using instantaneous values of current and voltage with a high sampling rate. The algorithms were tested on both modeled and physical data. The error of signal extremum forecast, the error of signal form forecast, and the signal value at the so-called joint point provided the basis for the suggested algorithms. The method of tuning for each algorithm was described. The time delay and accuracy of the algorithms were evaluated with varying tuning parameters. The algorithms were tested on the two-machine model of a power system in Matlab/Simulink. Signals from emergency event recorders installed on real power facilities were used in testing procedures. The results of this study indicated a possible and promising application of the suggested methods in the emergency control of power systems.

## 1. Introduction

The development of modern power systems is related to the global trend toward digitalization of all primary processes: generation, distribution, and consumption of power. A considerable emphasis is given to the design and application of digital devices of protection and control based on phasor measurement units (PMU). Time-synchronized instantaneous values of voltages and currents from power system objects can be obtained using these devices. This kind of data opens completely new possibilities for using adaptive emergency control systems based on steady-state measurements.

Emergency control, which is aimed at preserving both small signal stability and transient stability, is widely used in systems with relatively long distances between generation and load, large synchronous generators, and significantly constrained transmission lines.

The major problem of transition to corrective online emergency control is to come up with adaptive and fast algorithms for the detection of disturbance inception time using instantaneous values of voltage and current.

## 2. Related Works

Methods used for disturbance detection include: Fourier transform, Gabor transform, Kalman filter, Hilbert–Huang transform, Wavelet transform, S transform, and AI-based methods.

- **Fourier transform:** Used for stationary signals; STFT finds time-frequency variations but has window width selection issues.
- **Gabor transform:** Determines frequency components over time; combined with neural networks for arcing faults.
- **Kalman filter:** Together with DWT and fuzzy logic for disturbance detection; particle swarm optimization improves accuracy.
- **HHT:** Adaptive method extracting base functions; widely used with SVM and PNN.
- **Wavelet transform (MRA):** Decomposes signal for different resolutions; vast literature on voltage surge detection, transients classification, and online implementations.
- **S transform:** Advancement of wavelet and STFT with phase correction; combined with fuzzy logic and SVM.
- **AI/Neural Networks:** SC-CNN, MC-CNN, autoencoders, transfer learning (LocIT), deep learning with PMU data achieving ~97% accuracy on synthetic models.

## 3. Description of the Algorithms of Disturbance Time Estimation Using Currents and Voltages

Three adaptive algorithms were developed based on statistical analysis:

### 3.1. Algorithm 1 (Extremum Forecast Error)
- Predicts signal extremum on training interval
- Finds difference between actual and predicted extremum
- Determines mathematical expectation and standard deviation
- Forms 3-σ corridor
- Adjustable parameters: number of extremums on learning stage and forecast extremums

### 3.2. Algorithm 2 (Signal Forecast Error)
- Uses polynomial forecast (sum of first three Fourier series elements)
- Compares forecast signal with actual one
- Forms 3-σ corridor for forecast error
- Adjustable parameters: training dataset size and prediction interval size

### 3.3. Algorithm 3 (Joint Point Derivative Difference)
- Uses second-order approximation on two sliding windows
- "Joint point" is common for both first and second-order polynomials
- Calculates difference between derivatives from two windows
- Forms 3-σ corridor
- Adjustable parameters: sizes of first and second windows

### 3.4. Comparison of Time Delays
- Algorithm 1: highest delay (~10 ms), medium accuracy
- Algorithm 2: high accuracy, ~1 ms delay
- Algorithm 3: high accuracy, ~1.5 ms delay

### 3.5. Tuning Parameters
- Algorithm 1: retrospective extremum 5 ms, forecast extremum 2 ms
- Algorithm 2: training interval 60 ms, forecast interval 1 ms
- Algorithm 3: first window 0.5 ms, second window 1.5 ms

## 4. Testing on Modeled and Physical Data

### 4.1. Modeled Signal
Two-machine model in Matlab/Simulink with three-phase fault on parallel transmission lines.

**Table 3. Results of inception time estimation for the modeled signal.**

| Parameter | Algorithm 1 | Algorithm 2 | Algorithm 3 |
|-----------|-------------|-------------|-------------|
| Estimated time, s | 1.0020 | 1.0010 | 1.0011 |
| Deviation from reference | 0.20% | 0.10% | 0.11% |

### 4.2. Physical Signal
Physical signal from emergency event recorder (10 kHz sampling). Reference value from discrete wavelet transform: 0.8342 s.

**Table 4. Results for the physical signal.**

| Parameter | Algorithm 1 | Algorithm 2 | Algorithm 3 |
|-----------|-------------|-------------|-------------|
| Estimated time, s | 0.8374 | 0.8352 | 0.8341 |
| Deviation | 0.3836% | 0.1198% | **0.0119%** |

### 4.3. Accuracy Improvement Method
Using simultaneous analysis of 6 signals (3 phase voltages + 3 line voltages + 3 phase currents + 3 line currents):

`tFault = median(tUa, tUb, tUc, tUab, tUbc, tUca, tIa, tIb, tIc)`

For Algorithm 1 with this method: deviation reduced to **0.09%**.

## 5. Comparison with Existing Methods

**Table 6. Comparison with existing methods.**

| Algorithm | Input Data | Accuracy | Delay |
|-----------|-----------|----------|-------|
| Threshold RMS voltage | 1-phase, rms | low | 40 ms |
| Waveform Envelope | 1-phase, inst. | medium | 10 ms |
| Discrete Wavelet Transform | 1-phase, inst. | high | 40 ms |
| Algorithm 1 | 1-phase, inst. | medium | 10 ms |
| Algorithm 2 | 1-phase, inst. | high | **1.0 ms** |
| Algorithm 3 | 1-phase, inst. | high | **1.5 ms** |

## 6. Conclusions

Algorithm 3 has minimal time delay and smallest deviation from reference value. The developed algorithms can be used in parallel for backup. Future work: online testing and automatic parameter selection.

---
*Note: Full article extracted from MDPI open-access HTML. Some figures and tables referenced by links.*
