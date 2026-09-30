🌍 HeatML\_Machine



Global Geothermal Heat Flow Prediction using Machine Learning



HeatML\_Machine is an interactive Streamlit application for exploring machine-learning predictions of surface geothermal heat flow (SHF/GHF) at a 1° × 1° spatial resolution.



The application allows users to select a geographic region, choose a machine-learning model, visualize predicted heat flow as a high-resolution contour map, inspect model metrics, and download both the selected prediction data and the generated map.



Features



🌍 Interactive geographic region selection



🤖 Three machine-learning models:



XGBoost



Random Forest



Deep Neural Network (DNN)



🔥 Predicted Surface Heat Flow visualization



🗺️ High-resolution contour maps



🌊 Dark-blue background for areas without prediction data



🌐 Country and continent boundaries



📊 Model performance metrics displayed on the map



📥 Download predictions for the selected region as CSV



🖼️ Download the generated map as a high-resolution PNG



📏 Surface Heat Flow units shown as mW/m²



📍 Longitude and latitude are used for geographic selection and visualization only, and are not used as machine-learning input features



Machine-Learning Features



The prediction models use the following features:



Dis\_2\_hotspot

Dis\_2\_volcano

Dis\_2\_trench

Moho\_depth

LAB\_depth

Heat\_prod\_provinces





Longitude and latitude are geographic coordinates only and are not used as machine-learning input features.



Prediction Resolution



The prediction datasets have a spatial resolution of:



1° × 1°





Users can define their own geographic bounding box using:



Longitude minimum



Longitude maximum



Latitude minimum



Latitude maximum



Models



The application supports the following models:



Model	Prediction File

XGBoost	XGBoost\_GHF\_predictions\_1deg.csv

Random Forest	Random\_Forest\_GHF\_predictions\_1deg.csv

DNN	DNN\_GHF\_predictions\_1deg.csv



Prediction files are stored in:



predictions/



Model Metrics



Model performance metrics are loaded from:



models/metrics.json





The application displays the available:



R²



RMSE



metrics on the lower-left portion of the map.



Downloading Regional Data



After generating a prediction map, users can download the predictions corresponding to their selected geographic region.



The CSV download contains the available prediction cells within the selected bounding box and includes:



Model



Longitude



Latitude



Prediction values



Prediction unit



Other available prediction-file columns



The prediction unit is:



mW/m²



Downloading Maps



Users can download the generated map as a high-resolution PNG.



The map displayed inside the web application is intentionally kept compact for a better single-page layout, while the downloaded PNG is generated at 300 DPI.



Project Structure

HeatML\_Machine/

│

├── app.py

├── LICENSE.txt

├── README.md

├── requirements.txt

│

├── predictions/

│   ├── XGBoost\_GHF\_predictions\_1deg.csv

│   ├── Random\_Forest\_GHF\_predictions\_1deg.csv

│   └── DNN\_GHF\_predictions\_1deg.csv

│

└── models/

&#x20;   └── metrics.json





The repository contains the application and pre-generated prediction datasets required for visualization. Training scripts and model-training workflows are not included in this repository.



Requirements



Install the required Python packages with:



pip install -r requirements.txt





The main dependencies are:



streamlit

numpy

pandas

matplotlib

geopandas



Running the Application



From the project directory, run:



streamlit run app.py





The application will open in your web browser.



How to Use



Select the longitude and latitude boundaries of the desired region.



Select the machine-learning model.



Click Generate SHF.



Inspect the predicted surface heat-flow map.



Review the model metrics shown on the map.



Download the regional prediction data as CSV.



Download the generated map as PNG.



Scientific Reference



Mousavi, N., \& Mousavi, S. M. (2026).



Optimizing Feature Selection for Global Geothermal Heat Flow Prediction using Machine Learning.



Scientific Reports.



DOI:

https://doi.org/10.1038/s41598-026-63610-z



Citation



If you use HeatML\_Machine, the associated prediction datasets, or the methodology in academic work, please cite the related publication:



Mousavi, N., \& Mousavi, S. M. (2026).

Optimizing Feature Selection for Global Geothermal Heat Flow Prediction using Machine Learning.

Scientific Reports.



https://doi.org/10.1038/s41598-026-63610-z



License



HeatML\_Machine is distributed under the license specified in LICENSE.txt.



The prediction datasets included in this repository are provided as part of the HeatML\_Machine project. Please refer to LICENSE.txt for the applicable terms and conditions.



Acknowledgment



This application provides an interactive interface for exploring pre-generated machine-learning predictions of global geothermal heat flow.



© 2026 N Mousavi \& SM Mousavi — HeatML\_Machine

