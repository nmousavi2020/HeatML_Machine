🌍 HeatML\_Machine — Global Geothermal Heat Flow Prediction



A machine-learning application for exploring global surface geothermal heat flow (SHF/GHF) predictions at 1° × 1° spatial resolution.



Overview



HeatML\_Machine provides an interactive Streamlit interface for exploring pre-generated machine-learning predictions of global surface geothermal heat flow.



The workflow is:



Geophysical Features

&#x20;       ↓

Machine-Learning Model

&#x20;       ↓

1° × 1° Prediction Grid

&#x20;       ↓

Regional Selection

&#x20;       ↓

Heat-Flow Map

&#x20;       ↓

Model Metrics

&#x20;       ↓

CSV / PNG Download





Users can select a geographic region, choose a machine-learning model, generate a heat-flow map, inspect model performance, and download the corresponding prediction data.



Machine-Learning Models



The application provides predictions from three models:



XGBoost

Random Forest

Deep Neural Network (DNN)





Prediction files:



predictions/

├── XGBoost\_GHF\_predictions\_1deg.csv

├── Random\_Forest\_GHF\_predictions\_1deg.csv

└── DNN\_GHF\_predictions\_1deg.csv





All prediction datasets have a spatial resolution of:



1° × 1°



Machine-Learning Features



The models use six geological and geophysical features:



Dis\_2\_hotspot

Dis\_2\_volcano

Dis\_2\_trench

Moho\_depth

LAB\_depth

Heat\_prod\_provinces



Geographic Coordinates



Longitude and latitude are used for:



Geographic region selection



Prediction-cell location



Map visualization



They are not used as machine-learning input features.



Surface Heat Flow



The predicted variable is:



Surface Heat Flow (SHF/GHF)





with units of:



mW/m²





The prediction grid represents the available machine-learning estimates at 1° × 1° spatial resolution.



Areas without available prediction data are displayed with a dark-blue background on the map.



Interactive Map



Users define a geographic bounding box using:



Longitude minimum

Longitude maximum



Latitude minimum

Latitude maximum





The workflow is:



Select longitude range

&#x20;       ↓

Select latitude range

&#x20;       ↓

Select model

&#x20;       ↓

Generate SHF

&#x20;       ↓

Display prediction map





The generated map contains:



Predicted surface heat flow



High-resolution contours



Country boundaries



Continent boundaries



Model information



Model performance metrics



Model Metrics



Model performance metrics are loaded from:



models/metrics.json





The available metrics include:



R²

RMSE





These metrics are displayed on the generated map together with the corresponding model prediction.



Download Regional Data



After generating a prediction map, users can download the available prediction cells within the selected geographic bounding box.



The CSV contains:



Model

Longitude

Latitude

Prediction

Prediction Unit

Other prediction-file columns





Prediction units:



mW/m²





Only prediction cells available within the selected region are included in the download.



Download Map



The generated map can also be downloaded as a PNG image.



The interactive map is kept compact for a cleaner single-page Streamlit interface.



The downloadable figure is generated at:



300 DPI





This provides a higher-resolution version suitable for further use in reports, presentations, and scientific documentation.



Project Structure

HeatML\_Machine/

│

├── predictions/

│   ├── XGBoost\_GHF\_predictions\_1deg.csv

│   ├── Random\_Forest\_GHF\_predictions\_1deg.csv

│   └── DNN\_GHF\_predictions\_1deg.csv

│

├── models/

│   └── metrics.json

│

├── app.py

├── requirements.txt

├── README.md

└── LICENSE.txt



Requirements



Install the required dependencies:



pip install -r requirements.txt





Main dependencies:



streamlit

numpy

pandas

matplotlib

geopandas



Run



From the project root:



streamlit run app.py





The application will open in your web browser.



How to Use

1\. Select a Region



Define the desired:



Longitude minimum

Longitude maximum

Latitude minimum

Latitude maximum



2\. Select a Model



Choose:



XGBoost

Random Forest

DNN



3\. Generate the Prediction Map



Click:



Generate SHF



4\. Explore the Results



Inspect:



Predicted Surface Heat Flow

Model Metrics

Geographic Distribution



5\. Download the Results



Download:



Regional CSV

High-resolution PNG



Scientific Reference



The prediction methodology is associated with:



Mousavi, N., \& Mousavi, S. M. (2026).



Optimizing Feature Selection for Global Geothermal Heat Flow Prediction using Machine Learning.



Scientific Reports.



DOI:



https://doi.org/10.1038/s41598-026-63610-z



Citation



If you use HeatML\_Machine, the associated prediction datasets, or the methodology in academic work, please cite:



Mousavi, N., \& Mousavi, S. M. (2026).



Optimizing Feature Selection for Global Geothermal Heat Flow

Prediction using Machine Learning.



Scientific Reports.



https://doi.org/10.1038/s41598-026-63610-z



Repository Scope



This repository contains the interactive application and pre-generated prediction datasets used for visualization.



Training scripts and model-training workflows are not included.



The repository therefore focuses on:



Pre-generated Predictions

&#x20;       ↓

Interactive Exploration

&#x20;       ↓

Visualization

&#x20;       ↓

Regional Data Export



License



HeatML\_Machine is distributed under the license specified in:



LICENSE.txt





Please refer to the license file for the applicable terms and conditions.



Acknowledgment



HeatML\_Machine provides an interactive interface for exploring pre-generated machine-learning predictions of global geothermal heat flow.



© 2026 N. Mousavi \& S. M. Mousavi

