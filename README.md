# Toward Automated Celestial Navigation with Deep Learning
**UC Berkeley MIDS W251**
**Travis Metz and Greg Tozzi**

##  <a id="Contents">Contents
[1.0 Introduction](#Introduction)
[2.0 System Overview](#System_Overview)
[3.0 The Model](#Model)



## <a id="Introduction">1.0 Introduction

### 1.1 A _Very_ Brief Overview of Marine Navigation
Navigation, along with seamanship and collision avoidance, is one of the mariner's fundamental skills.  Celestial methods were once the cornerstone of maritime and aeronautical navigation, but they have been almost entirely supplanted by electronic means -- first by terrestrially-based systems like OMEGA [[1]](#1) and LORAN [[2]](#2), then by satellite-based systems like GPS [[3]](#3), and then by mixed systems like differential GPS (DGPS) [[4]](#4).   Unfortunately, electronic navigation is fragile both to budgetary pressure and to malicious acts [[5]](#5)[[6]](#6).  Building and maintaining proficiency in celestial navigation is difficult, however, and a skilled navigator is still only able to fix a vessel's position a few times daily, weather permitting.

In current practice, marine celestial navigation requires:

- A clear view of the horizon.  The navigator measures angles of elevation with a sextant using the horizon as a baseline.
- A clear view of celestial bodies.  Two bodies are required to fix the vessel's position, but three are typically used in practice.  Repeated observations of the sun can be combined to provided what is referred to as a _running fix_ of a vessel's position.
- An accurate clock.  Without a clock, a navigator can only compute the vessel's latitude.
- A _dead reckoning_ plot on which the navigator estimates the ship's track.
- For manual computation, a number of volumes containing published tables.

Automated celestial navigation for aircraft was solved in the 

### 1.2 Intent of this Project
We want to explore the possibility of applying deep learning to the task of automating celestial  navigation.  We entered this project wanting to answer the following questions:

- Can arbitrary images of the sky be used to fix a vessel's position?

*[Return to contents](#Contents)*

## <a id="System_Overview">2.0 System Overview

### 2.1 Use Case
We envision mariners using our system as a back-up to other forms of navigation, primarily for open-ocean navigation outside of five nautical miles from chartered hazards.  A navigator would depart on their voyage with a set of models suited for the vessel's track much in the same way as a navigator today loads relevant charts either from removable storage or the internet prior to departing on a voyage.  The system takes nothing more than the image returned from the edge device's installed camera and time from an accurate clock as input.  It returns both raw position output and an industry standard NMEA output suitable for integration with an electronic charting package.  A navigator with internet access at sea can load additional models from the cloud as needed to account for adjustments to the planned voyage.

### 2.2 Assumptions
We made a number of engineering assumptions to make the problem tractable as a term project.

- We are simulating images that would be taken at sea with synthetic images.  We hope eventually to conduct an operational test of the system.  We assume, then, that the installed camera on the operational system can replicate the resolution and overall quality of our synthetic images.
- We assume the notional vessel on which the system would be installed is fitted with a three-axis gyrocompass to allow images to be captured at a fixed azimuth and elevation.  The requirements of the stabilization system can be inferred by perturbing the synthetic images to simulate stabilization error.

### 2.3 Components
Our system consists of a cloud component and an edge component.  An image generator creates batches of synthetic images, names them using a descriptive scheme that allows easy indexing by location and time, and stores the models in object storage buckets indexed by location and time.  The model trainer pulls from these buckets to create models specific to a bounded geographic area at a given with certain time bounds.  These models are stored in object storage.  The edge device -- in this case a Jetson TX2 -- captures an image of the sky and the time at which the image was taken.  The inference engine performs a forward pass of the model, returning the vessel's predicted location both as raw output and as a NMEA string.

```mermaid
graph TB
subgraph Cloud
A[Image Generator] --> B(Image Storage - S3)
A --By location/time--> C(Image Storage - S3)
A --> D(Image Storage - S3)
C -- Pull as needed --> F[Model Trainer]
D --> F
B --> F
F --> G(Model Zoo)
end
subgraph Model Training
subgraph Edge
H[Image Capture]--> I[Inference Engine]
I --> J[Raw Output]
end
G --> I
J -- NMEA String --> K[Navigation Package]
```




*[Return to contents](#Contents)*

## <a id="Model">3.0 The Model
Our model is a relatively simple CNN tuned to provide reasonably accurate predictions over a given waterspace and 


### 3.1 Model Architecture
Our goal was to explore architectures that could learn a vessel's position from an arbitrary image of the sky with the azimuth and elevation fixed and the time known.  We explored both DNNs and CNNs but settled on the latter because CNNs are compact relatively to deep dense networks.

Our network has two inputs.  The image input ingests pictures of the sky  the time input ingests the UTC time at which the image was taken.  The images are run through a series of convolutional and max pooling layers.  The results are concatenated with the normalized time and the resulting vector is put through dropout regularization, a dense hidden layer, and the regression head.  The head consists of two neurons, one each for normalized latitude and normalized longitude.  Latitude and longitude are normalized over the test area with the latitude of the southernmost bound mapping to 0 and the latitude of the northernmost bound mapping to 1.  Longitude is mapped similarly.  The output layer uses sigmoid activation to bound the output in the spatial domain of `([0,1], [0,1])`.


### 3.2 Introducing the Haversine Loss Function
We naturally want our loss function to minimize the navigational error returned by the model.  We initially used mean squared error across latitude and longitude as our loss function, but we found that convergence was slow and that the model frequently failed to converge to reasonable values.  There is, of course a nonlinear relationship between latitude and longitude.  Whereas a degree of latitude is consistently 60 nautical miles anywhere on the globe, lines of longitude converge at the poles.  Using mean squared error, then, results in inconsistent results in terms of the model's error in distance.  To correct this, we implemented a new loss function in TensorFlow based on the haversine formula which gives the great circle distance between two points defined by latitude and longitude [[8]](#8). 

Minimizing the haversine loss minimizes the error between predicted and actual locations, and the negative gradient of the haversine loss gives the direction of steepest descent in terms of the predicted latitude and longitude.

### 3.3 Generating Images
We relied on synthetic images generated from the open source astronomy program _Stellarium_.  Stellarium can generated high-quality images of the sky for arbitrary geographic positions, times, azimuths (the heading of the virtual camera in true degrees), altitudes (the angular elevation of the virtual camera), camera field of view, and observer elevations.  Stellarium uses a JavaScript-based scripting language system to automate sequences of observations.  We wrote Python code to automate script generation based on a YAML input file.

*[Return to contents](#Contents)*

## 4.0 Experimental Results

### 4.1 Test Area
We bounded the test area both spatially and temporally in order to keep the problem tractable.  our test area exists from TODO

## References

<a id="1">[1]</a> J. Kasper and C. Hutchinson, "The Omega navigation system--An overview," in  _IEEE Communications Society Magazine_, vol. 16, no. 3, pp. 23-35, May 1978, doi: 10.1109/MCOM.1978.1089729.

<a id="2">[2]</a> W. J. Thrall, "Loran-C, an Overview," in _Proc. 13th Annu. Precise Time Planning Meet_., p. 449, 1976. and _Time Interval Applications and Planning Meet_., NASA Conf. Publ. 2220, p. 121, 1981

<a id="3">[3]</a> G. Beutler, W. Gurtner, M. Rothacher, U. Wild and E. Frei, "Relative Static Positioning with the Global Positioning System:  Basic Technical Considerations," in _Global Positioning System:  An Overview_., International Association of Geodesy Symposia 102, ch. 1, 1990.

 <a id="4">[4]</a> E. G. Blackwell, "Overview of Differential GPS Methods" in _Navigation_, 32: 114-125, 1985. doi:[10.1002/j.2161-4296.1985.tb00895.x](https://doi.org/10.1002/j.2161-4296.1985.tb00895.x)

 <a id="5">[5]</a> U. S. Coast Guard Navigation Center, "Special Notice Regarding LORAN Closure", [https://www.navcen.uscg.gov/?pageName=loranMain](https://www.navcen.uscg.gov/?pageName=loranMain).

 <a id="6">[6]</a> T. Hitchens, "SASC Wants Alternative GPS By 2023," 29 June 2020, [breakingdefense.com/2020/06/sasc-wants-alternative-gps-by-2023/](breakingdefense.com/2020/06/sasc-wants-alternative-gps-by-2023/.).

 <a id="7">[7]</a> M. Garvin, "Future of Celestial Navigation and the Ocean-Going Military Navigator," [OTS Master's Level Projects & Papers. 41](https://digitalcommons.odu.edu/ots_masters_projects/41), 2010.

 <a id="8">[8]</a> C. N. Alam, K. Manaf, A. R. Atmadja and D. K. Aurum, "Implementation of haversine formula for counting event visitor in the radius based on Android application," _2016 4th International Conference on Cyber and IT Service Management_, Bandung, 2016, pp. 1-6, doi: [10.1109/CITSM.2016.7577575]([https://ieeexplore.ieee.org/abstract/document/7577575](https://ieeexplore.ieee.org/abstract/document/7577575)).

 <a id="9">[9]</a> "NMEA 0183 INSTALLATION AND OPERATING GUIDELINES," retrieved from [https://www.navcen.uscg.gov/pdf/gmdss/taskforce/nmea_7.pdf](https://www.navcen.uscg.gov/pdf/gmdss/taskforce/nmea_7.pdf)

*[Return to contents](#Contents)*

