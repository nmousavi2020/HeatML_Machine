import os
import io
import json

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="HeatML_Machine",
    page_icon="🌍",
    layout="wide"
)


# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PREDICTION_DIR = os.path.join(
    BASE_DIR,
    "predictions"
)

METRICS_FILE = os.path.join(
    BASE_DIR,
    "models",
    "metrics.json"
)


# =====================================================
# ML FEATURES
# IMPORTANT:
# lon and lat are NOT ML FEATURES
# =====================================================

ML_FEATURES = [
    "Dis_2_hotspot",
    "Dis_2_volcano",
    "Dis_2_trench",
    "Moho_depth",
    "LAB_depth",
    "Heat_prod_provinces"
]


# =====================================================
# PREDICTION FILES
# =====================================================

PREDICTION_FILES = {
    "XGBoost": "XGBoost_GHF_predictions_1deg.csv",
    "Random Forest": "Random_Forest_GHF_predictions_1deg.csv",
    "DNN": "DNN_GHF_predictions_1deg.csv"
}


# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(120,145,85,0.25),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #142019 0%,
            #30472f 48%,
            #66784d 100%
        );

    color: #f5f1df;
}

.block-container {
    max-width: 1400px;
    padding: 0.5rem 1.5rem 0.2rem 1.5rem;
}

h1 {
    color: #f5f1df;
    font-size: 2.4rem;
    margin: 0;
}

h2, h3 {
    color: #e7d99a;
}

.subtitle {
    color: #d8d7c2;
    font-size: 0.92rem;
    margin-bottom: 0.45rem;
}

.coord-box {
    background: rgba(245, 241, 223, 0.07);
    border: 1px solid rgba(231, 217, 154, 0.18);
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 10px;
}

.selected-box {
    background: rgba(216, 202, 139, 0.14);
    border: 1px solid rgba(231, 217, 154, 0.25);
    border-radius: 10px;
    padding: 8px;
    margin-bottom: 8px;
}

.citation {
    background: linear-gradient(
        90deg,
        #d8ca8b,
        #aebd80
    );

    color: #18251b;
    padding: 9px 15px;
    border-radius: 10px;
    margin-top: 7px;
    font-size: 0.9rem;
    line-height: 1.35;
}

.citation a {
    color: #18251b;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #f0ead0;
    font-size: 1rem;
    font-weight: 500;
    padding: 6px;
}

.stButton > button {
    background: #c7b96f;
    color: #172019;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    height: 2.4rem;
}

.stButton > button:hover {
    background: #ded092;
}

[data-testid="stDownloadButton"] > button {
    background: #aebd80;
    color: #172019;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    height: 2.4rem;
}

[data-testid="stDownloadButton"] > button:hover {
    background: #d8ca8b;
}

[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    color: #e7dfc4 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================

st.title("🌍 HeatML_Machine")

st.markdown(
    '<div class="subtitle">'
    'Global Geothermal Heat Flow Prediction using Machine Learning'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns(
    [0.8, 2.2],
    gap="medium"
)


# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.subheader("Coordinates")

    st.markdown(
        '<div class="coord-box">',
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # LATITUDE MAX
    # -------------------------------------------------

    _, center, _ = st.columns([1, 1.4, 1])

    with center:

        lat_max = st.number_input(
            "↑ Lat Max",
            min_value=-90.0,
            max_value=90.0,
            value=50.0,
            step=0.1
        )

    # -------------------------------------------------
    # LONGITUDE
    # -------------------------------------------------

    c1, c2, c3 = st.columns(
        [1.3, 0.5, 1.3]
    )

    with c1:

        lon_min = st.number_input(
            "← Lon Min",
            min_value=-180.0,
            max_value=180.0,
            value=-10.0,
            step=0.1
        )

    with c2:

        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:24px;
                padding-top:25px;
                color:#d8ca8b;
            ">
            ↔
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        lon_max = st.number_input(
            "Lon Max →",
            min_value=-180.0,
            max_value=180.0,
            value=10.0,
            step=0.1
        )

    # -------------------------------------------------
    # LATITUDE MIN
    # -------------------------------------------------

    _, center, _ = st.columns(
        [1, 1.4, 1]
    )

    with center:

        lat_min = st.number_input(
            "↓ Lat Min",
            min_value=-90.0,
            max_value=90.0,
            value=30.0,
            step=0.1
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =================================================
    # ML MODEL
    # =================================================

    st.subheader("ML Model")

    model_type = st.selectbox(
        "Select algorithm",
        [
            "XGBoost",
            "Random Forest",
            "DNN"
        ]
    )

    st.markdown(
        f"""
        <div class="selected-box">
        <b>Selected:</b> {model_type}
        </div>
        """,
        unsafe_allow_html=True
    )

    run = st.button(
        "Generate SHF",
        use_container_width=True
    )


# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    st.subheader("Predicted Surface Heat Flow")

    if run:

        # =================================================
        # CHECK COORDINATES
        # =================================================

        if lon_min >= lon_max:

            st.error(
                "Longitude Min must be smaller than Longitude Max."
            )

            st.stop()

        if lat_min >= lat_max:

            st.error(
                "Latitude Min must be smaller than Latitude Max."
            )

            st.stop()


        # =================================================
        # LOAD PREDICTION FILE
        # =================================================

        prediction_file = os.path.join(
            PREDICTION_DIR,
            PREDICTION_FILES[model_type]
        )

        if not os.path.exists(prediction_file):

            st.error(
                f"Prediction file was not found:\n\n"
                f"{prediction_file}"
            )

            st.stop()


        try:

            df = pd.read_csv(
                prediction_file
            )

        except Exception as e:

            st.error(
                f"Could not read prediction file: {e}"
            )

            st.stop()


        # =================================================
        # FIND COORDINATE COLUMNS
        # =================================================

        lon_candidates = [
            "lon",
            "longitude",
            "Longitude",
            "LON"
        ]

        lat_candidates = [
            "lat",
            "latitude",
            "Latitude",
            "LAT"
        ]

        lon_column = next(
            (
                c for c in lon_candidates
                if c in df.columns
            ),
            None
        )

        lat_column = next(
            (
                c for c in lat_candidates
                if c in df.columns
            ),
            None
        )


        if lon_column is None or lat_column is None:

            st.error(
                "The prediction file must contain "
                "longitude and latitude columns."
            )

            st.write(
                "Available columns:",
                list(df.columns)
            )

            st.stop()


        # =================================================
        # FIND PREDICTION COLUMN
        # =================================================

        prediction_candidates = [
            "Predicted_GHF",
            "Predicted_SHF",
            "predicted_GHF",
            "predicted_SHF",
            "Prediction",
            "prediction",
            "GHF_prediction",
            "SHF_prediction",
            "GHF_pred",
            "SHF_pred",
            "Predicted",
            "predicted",
            "GHF",
            "SHF"
        ]

        prediction_column = None

        for column in prediction_candidates:

            if column in df.columns:

                prediction_column = column
                break


        # -------------------------------------------------
        # AUTOMATIC NUMERIC COLUMN DETECTION
        # -------------------------------------------------

        if prediction_column is None:

            excluded = {
                lon_column,
                lat_column,
                "FID",
                "fid"
            }

            numeric_columns = df.select_dtypes(
                include=np.number
            ).columns.tolist()

            possible = [
                c for c in numeric_columns
                if c not in excluded
            ]

            if len(possible) == 1:

                prediction_column = possible[0]


        if prediction_column is None:

            st.error(
                "Prediction column was not found in "
                f"{os.path.basename(prediction_file)}"
            )

            st.write(
                "Available columns:"
            )

            st.code(
                ", ".join(df.columns)
            )

            st.stop()


        # =================================================
        # CONVERT TO NUMERIC
        # =================================================

        df[lon_column] = pd.to_numeric(
            df[lon_column],
            errors="coerce"
        )

        df[lat_column] = pd.to_numeric(
            df[lat_column],
            errors="coerce"
        )

        df[prediction_column] = pd.to_numeric(
            df[prediction_column],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                lon_column,
                lat_column,
                prediction_column
            ]
        )


        # =================================================
        # FILTER SELECTED REGION
        # =================================================

        selected = df[
            (df[lon_column] >= lon_min) &
            (df[lon_column] <= lon_max) &
            (df[lat_column] >= lat_min) &
            (df[lat_column] <= lat_max)
        ].copy()


        if selected.empty:

            st.warning(
                "No available prediction cells were found "
                "for the selected geographic region."
            )

            st.stop()


        # =================================================
        # PREPARE DOWNLOAD DATA
        # =================================================

        download_data = selected.copy()

        preferred_columns = [
            lon_column,
            lat_column
        ]

        remaining_columns = [
            c for c in download_data.columns
            if c not in preferred_columns
        ]

        download_data = download_data[
            preferred_columns + remaining_columns
        ]

        download_data.insert(
            0,
            "Model",
            model_type
        )

        download_data["Prediction_Unit"] = "mW/m²"


        # =================================================
        # CSV DOWNLOAD
        # =================================================

        csv_data = download_data.to_csv(
            index=False
        ).encode("utf-8")


        # =================================================
        # PREPARE GRID
        # =================================================

        x_values = np.sort(
            selected[lon_column].unique()
        )

        y_values = np.sort(
            selected[lat_column].unique()
        )

        grid = selected.pivot_table(
            index=lat_column,
            columns=lon_column,
            values=prediction_column,
            aggfunc="mean"
        )

        grid = grid.reindex(
            index=y_values,
            columns=x_values
        )

        Z = grid.to_numpy(
            dtype=float
        )

        X, Y = np.meshgrid(
            x_values,
            y_values
        )


        # =================================================
        # HIGH-RESOLUTION MAP
        # =================================================

        fig, ax = plt.subplots(
            figsize=(7.5, 4.8),
            dpi=180
        )

        fig.patch.set_facecolor(
            "#071b32"
        )

        ax.set_facecolor(
            "#061a31"
        )


        # =================================================
        # CUSTOM SHF COLOR MAP
        # =================================================

        colors = [
            "#163b78",
            "#245da1",
            "#2c8bb8",
            "#51b7a5",
            "#91c95b",
            "#d5d75b",
            "#f3b44b",
            "#e96b3d",
            "#b92736"
        ]

        shf_cmap = LinearSegmentedColormap.from_list(
            "HeatML_SHF",
            colors,
            N=512
        )


        # =================================================
        # DATA RANGE
        # =================================================

        valid_values = Z[
            np.isfinite(Z)
        ]

        if len(valid_values) > 0:

            vmin = np.nanpercentile(
                valid_values,
                1
            )

            vmax = np.nanpercentile(
                valid_values,
                99
            )

            if vmin == vmax:

                vmin = np.nanmin(
                    valid_values
                )

                vmax = np.nanmax(
                    valid_values
                )

        else:

            vmin = 0
            vmax = 100


        # =================================================
        # CONTOUR
        # =================================================

        levels = np.linspace(
            vmin,
            vmax,
            80
        )

        contour = ax.contourf(
            X,
            Y,
            Z,
            levels=levels,
            cmap=shf_cmap,
            vmin=vmin,
            vmax=vmax,
            extend="both"
        )


        # =================================================
        # LAND / COUNTRY BORDERS
        # =================================================

        try:

            world = gpd.read_file(
                "https://naturalearth.s3.amazonaws.com/"
                "110m_cultural/"
                "ne_110m_admin_0_countries.zip"
            )

            world.boundary.plot(
                ax=ax,
                color="#eeeeee",
                linewidth=0.35,
                alpha=0.75
            )

        except Exception:

            pass


        # =================================================
        # AXIS
        # =================================================

        ax.set_xlim(
            lon_min,
            lon_max
        )

        ax.set_ylim(
            lat_min,
            lat_max
        )

        ax.set_xlabel(
            "Longitude",
            color="white",
            fontsize=8
        )

        ax.set_ylabel(
            "Latitude",
            color="white",
            fontsize=8
        )

        ax.tick_params(
            colors="white",
            labelsize=7
        )

        ax.grid(
            color="white",
            alpha=0.12,
            linewidth=0.35
        )


        # =================================================
        # COLORBAR
        # =================================================

        cbar = fig.colorbar(
            contour,
            ax=ax,
            pad=0.015,
            shrink=0.82
        )

        cbar.set_label(
            "Surface Heat Flow (mW/m²)",
            color="white",
            fontsize=8
        )

        cbar.ax.tick_params(
            colors="white",
            labelsize=7
        )


        # =================================================
        # TITLE
        # =================================================

        ax.set_title(
            f"{model_type} — Predicted Surface Heat Flow",
            color="white",
            fontsize=11,
            pad=6
        )


        # =================================================
        # LOAD METRICS
        # =================================================

        r2 = None
        rmse = None

        if os.path.exists(METRICS_FILE):

            try:

                with open(
                    METRICS_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:

                    metrics = json.load(f)

                model_metrics = metrics.get(
                    model_type,
                    {}
                )

                r2 = (
                    model_metrics.get("R2")
                    if "R2" in model_metrics
                    else model_metrics.get("r2")
                )

                rmse = (
                    model_metrics.get("RMSE")
                    if "RMSE" in model_metrics
                    else model_metrics.get("rmse")
                )

            except Exception:

                r2 = None
                rmse = None


        # =================================================
        # METRICS — BOTTOM LEFT
        # =================================================

        if r2 is not None and rmse is not None:

            metrics_text = (
                f"{model_type}   |   "
                f"R² = {float(r2):.4f}   |   "
                f"RMSE = {float(rmse):.4f}"
            )

            ax.text(
                0.015,
                0.025,
                metrics_text,
                transform=ax.transAxes,
                ha="left",
                va="bottom",
                fontsize=7.5,
                color="#ffffff",
                bbox=dict(
                    boxstyle="round,pad=0.4",
                    facecolor="#142019",
                    edgecolor="#d8ca8b",
                    linewidth=0.7,
                    alpha=0.92
                )
            )


        # =================================================
        # SAVE HIGH-RESOLUTION PNG
        # =================================================

        plt.tight_layout(
            pad=0.3
        )

        png_buffer = io.BytesIO()

        fig.savefig(
            png_buffer,
            format="png",
            dpi=300,
            bbox_inches="tight",
            facecolor=fig.get_facecolor()
        )

        png_buffer.seek(0)


        # =================================================
        # =================================================
        # DISPLAY SMALLER MAP
        # =================================================
        map_left, map_center, map_right = st.columns(
            [0.25, 1, 0.15]
        )

        with map_center:

            st.image(
                png_buffer,
                width=600
            )


        # =================================================
        # DOWNLOAD FILE NAMES
        # =================================================

        lon_min_name = f"{lon_min:g}".replace(
            "-",
            "m"
        )

        lon_max_name = f"{lon_max:g}".replace(
            "-",
            "m"
        )

        lat_min_name = f"{lat_min:g}".replace(
            "-",
            "m"
        )

        lat_max_name = f"{lat_max:g}".replace(
            "-",
            "m"
        )

        model_name = model_type.replace(
            " ",
            "_"
        )

        csv_filename = (
            f"HeatML_{model_name}_"
            f"lon{lon_min_name}_{lon_max_name}_"
            f"lat{lat_min_name}_{lat_max_name}.csv"
        )

        png_filename = (
            f"HeatML_{model_name}_"
            f"lon{lon_min_name}_{lon_max_name}_"
            f"lat{lat_min_name}_{lat_max_name}.png"
        )


        # =================================================
        # DOWNLOAD SELECTED REGION
        # =================================================

        st.markdown(
            "### Download Selected Region"
        )

        download_col1, download_col2 = st.columns(
            2,
            gap="medium"
        )

        with download_col1:

            st.download_button(
                label="Download Data (CSV)",
                data=csv_data,
                file_name=csv_filename,
                mime="text/csv",
                use_container_width=True
            )

        with download_col2:

            st.download_button(
                label="Download Map (PNG)",
                data=png_buffer,
                file_name=png_filename,
                mime="image/png",
                use_container_width=True
            )


        # =================================================
        # DOWNLOAD INFORMATION
        # =================================================

        st.markdown(
            f"""
            <div style="
                color:#d8d7c2;
                font-size:0.76rem;
                margin-top:4px;
                text-align:center;
            ">
            {len(selected):,} available 1° × 1° prediction cells
            in the selected region.
            </div>
            """,
            unsafe_allow_html=True
        )

        plt.close(fig)


    else:

        st.info(
            "Select the geographic region and ML model, "
            "then click Generate SHF."
        )


# =====================================================
# CITATION
# =====================================================

st.markdown("""
<div class="citation">
Mousavi, N., & Mousavi, S. M. (2026). Optimizing Feature Selection for Global Geothermal Heat Flow Prediction using Machine Learning. <em>Scientific Reports.</em>
&nbsp;&nbsp; DOI:
<a href="https://doi.org/10.1038/s41598-026-63610-z"
target="_blank">10.1038/s41598-026-63610-z</a>
</div>
""", unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
© 2026 N Mousavi & SM Mousavi — HeatML_Machine
</div>
""", unsafe_allow_html=True)
