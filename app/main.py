"""
African Climate Trends Dashboard
10 Academy - Week 0 Challenge
COP32 Evidence-Backed Analysis
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="🌍 African Climate Dashboard | COP32",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TITLE & HEADER
# ============================================================
st.title("🌍 African Climate Trends Dashboard")
st.markdown("### COP32 Evidence-Backed Analysis | 2015-2026")
st.caption("10 Academy - Artificial Intelligence Mastery | Week 0 Challenge")

# Key metrics row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Countries Analyzed", "5", "Ethiopia, Kenya, Sudan, Tanzania, Nigeria")
col2.metric("Data Source", "NASA POWER", "MERRA-2 Reanalysis")
col3.metric("Time Period", "2015-2026", "~4,100 days/country")
col4.metric("Variables", "10", "Temp, Precip, Humidity, Wind")
col5.metric("Insights", "Negotiation-Grade", "COP32 Ready")

st.markdown("---")

# ============================================================
# DATA LOADING (CACHED)
# ============================================================
@st.cache_data(ttl=3600)
def load_all_data():
    """Load and combine all cleaned country datasets."""
    countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
    country_names = {
        'ethiopia': 'Ethiopia', 'kenya': 'Kenya', 'sudan': 'Sudan',
        'tanzania': 'Tanzania', 'nigeria': 'Nigeria'
    }
    dfs = []
    for country in countries:
        try:
            df = pd.read_csv(f'data/{country}_clean.csv')
            df['Date'] = pd.to_datetime(df['Date'])
            df['Country'] = country_names.get(country, country.capitalize())
            dfs.append(df)
        except FileNotFoundError:
            st.warning(f"Data file for {country} not found. Skipping.")
    
    if not dfs:
        st.error("No data files found. Please ensure cleaned CSV files are in the 'data/' directory.")
        st.stop()
    
    return pd.concat(dfs, ignore_index=True)

# Load data with spinner
with st.spinner("🔄 Loading climate data from NASA POWER (MERRA-2)..."):
    all_data = load_all_data()
    st.success(f"✅ Loaded {len(all_data):,} observations across {all_data['Country'].nunique()} countries")

# ============================================================
# SIDEBAR - FILTERS
# ============================================================
st.sidebar.header("🎛️ Dashboard Controls")
st.sidebar.markdown("---")

# Country multi-select
st.sidebar.subheader("📍 Countries")
all_countries = sorted(all_data['Country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select countries to display:",
    options=all_countries,
    default=['Ethiopia', 'Kenya', 'Sudan'],
    help="Choose one or more countries to compare"
)

if not selected_countries:
    st.sidebar.warning("⚠️ Please select at least one country.")
    st.stop()

# Year range slider
st.sidebar.subheader("📅 Time Period")
min_year = int(all_data['Year'].min())
max_year = int(all_data['Year'].max())
year_range = st.sidebar.slider(
    "Select year range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    help="Drag the handles to filter by year"
)

# Variable selector
st.sidebar.subheader("📊 Climate Variable")
variable_options = {
    'T2M': '🌡️ Temperature (°C)',
    'T2M_MAX': '🔴 Max Temperature (°C)',
    'T2M_MIN': '🔵 Min Temperature (°C)',
    'T2M_RANGE': '📐 Daily Temperature Range (°C)',
    'PRECTOTCORR': '🌧️ Precipitation (mm/day)',
    'RH2M': '💧 Relative Humidity (%)',
    'WS2M': '💨 Wind Speed (m/s)',
    'PS': '🔵 Atmospheric Pressure (kPa)',
    'QV2M': '💦 Specific Humidity (g/kg)'
}
selected_variable = st.sidebar.selectbox(
    "Select climate variable:",
    options=list(variable_options.keys()),
    format_func=lambda x: variable_options[x],
    help="Choose which climate variable to visualize"
)

# About section
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 About")
st.sidebar.info(
    "This dashboard analyzes climate data from five African nations to support "
    "Ethiopia's COP32 hosting preparations. Data sourced from NASA POWER (MERRA-2)."
)
st.sidebar.markdown("### 👤 Author")
st.sidebar.markdown("**Meron Teklehaymanot Gebru**")
st.sidebar.caption("10 Academy AI Mastery | Week 0")

# ============================================================
# FILTER DATA
# ============================================================
filtered_data = all_data[
    (all_data['Country'].isin(selected_countries)) &
    (all_data['Year'].between(year_range[0], year_range[1]))
]

# Show data summary in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Data Summary")
st.sidebar.write(f"**Observations:** {len(filtered_data):,}")
st.sidebar.write(f"**Countries:** {len(selected_countries)}")
if len(filtered_data) > 0:
    st.sidebar.write(f"**Date Range:** {filtered_data['Date'].min().strftime('%b %Y')} – {filtered_data['Date'].max().strftime('%b %Y')}")

# ============================================================
# MAIN DASHBOARD TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Time Series",
    "📊 Distributions",
    "📋 Summary Statistics",
    "🔥 Extreme Events",
    "📖 Key Findings"
])

# ============================================================
# TAB 1: TIME SERIES
# ============================================================
with tab1:
    st.subheader(f"Monthly {variable_options[selected_variable]} Trend")
    st.caption(f"Showing data for: {', '.join(selected_countries)} | {year_range[0]} – {year_range[1]}")
    
    # Calculate monthly averages
    monthly = filtered_data.groupby(['Country', 'Year', 'Month'])[selected_variable].mean().reset_index()
    monthly['Date'] = pd.to_datetime(monthly[['Year', 'Month']].assign(Day=1))
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Color map for countries
    country_colors = {
        'Ethiopia': '#2E86AB', 'Kenya': '#A23B72', 'Sudan': '#F18F01',
        'Tanzania': '#C73E1D', 'Nigeria': '#3B1F2B'
    }
    
    for country in selected_countries:
        data = monthly[monthly['Country'] == country]
        color = country_colors.get(country, '#333333')
        ax.plot(data['Date'], data[selected_variable], label=country, linewidth=1.5, color=color)
    
    ax.set_title(
        f'Monthly {variable_options[selected_variable]} ({year_range[0]}–{year_range[1]})',
        fontsize=14, fontweight='bold'
    )
    ax.set_ylabel(variable_options[selected_variable], fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend(loc='upper right', frameon=True, fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)
    plt.close()
    
    # Trend summary
    st.markdown("---")
    st.markdown("#### 📝 Trend Observations")
    
    # Calculate trend for each country
    for country in selected_countries:
        country_data = monthly[monthly['Country'] == country].dropna(subset=[selected_variable])
        if len(country_data) > 12:
            from scipy import stats
            x = np.arange(len(country_data))
            y = country_data[selected_variable].values
            if len(y) > 1:
                slope, _, r_value, _, _ = stats.linregress(x, y)
                direction = "⬆️ warming" if slope > 0 else "⬇️ cooling"
                st.write(f"**{country}:** {direction} trend ({slope:.4f} per month, R²={r_value**2:.3f})")

# ============================================================
# TAB 2: DISTRIBUTIONS
# ============================================================
with tab2:
    st.subheader("Distribution Analysis")
    st.caption(f"Showing data for: {', '.join(selected_countries)} | {year_range[0]} – {year_range[1]}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {variable_options[selected_variable]} Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        for country in selected_countries:
            data = filtered_data[filtered_data['Country'] == country][selected_variable].dropna()
            color = country_colors.get(country, '#333333')
            ax.hist(data, bins=40, alpha=0.5, label=country, color=color, edgecolor='white')
        
        ax.set_xlabel(variable_options[selected_variable], fontsize=11)
        ax.set_ylabel('Frequency', fontsize=11)
        ax.legend(fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("#### 🌧️ Precipitation Distribution (Boxplot)")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        precip_data = filtered_data[filtered_data['Country'].isin(selected_countries)]
        sns.boxplot(
            x='Country', y='PRECTOTCORR', data=precip_data,
            order=selected_countries, palette=country_colors, width=0.5
        )
        ax.set_ylabel('Precipitation (mm/day)', fontsize=11)
        ax.set_xlabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
        plt.close()
    
    # Correlation heatmap
    st.markdown("---")
    st.markdown("#### 🔗 Correlation Analysis")
    
    if len(selected_countries) >= 1:
        selected_country = st.selectbox("Select country for correlation heatmap:", selected_countries)
        country_data = filtered_data[filtered_data['Country'] == selected_country]
        
        numeric_cols = ['T2M', 'T2M_MAX', 'T2M_MIN', 'T2M_RANGE', 'PRECTOTCORR',
                        'RH2M', 'WS2M', 'WS2M_MAX', 'PS', 'QV2M']
        corr = country_data[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    linewidths=0.5, ax=ax, vmin=-1, vmax=1)
        ax.set_title(f'{selected_country}: Correlation Matrix', fontsize=14, fontweight='bold')
        st.pyplot(fig)
        plt.close()

# ============================================================
# TAB 3: SUMMARY STATISTICS
# ============================================================
with tab3:
    st.subheader("📋 Summary Statistics")
    st.caption(f"Showing data for: {', '.join(selected_countries)} | {year_range[0]} – {year_range[1]}")
    
    # Summary table
    st.markdown(f"#### {variable_options[selected_variable]} - Statistical Summary")
    summary = filtered_data.groupby('Country')[selected_variable].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)
    summary.columns = ['Observations', 'Mean', 'Median', 'Std Dev', 'Minimum', 'Maximum']
    st.dataframe(summary, use_container_width=True)
    
    # Temperature comparison across all countries
    st.markdown("---")
    st.markdown("#### 🌡️ Temperature Comparison (All Selected Countries)")
    
    temp_cols = st.columns(3)
    metrics_to_show = [
        ('T2M', 'Mean Temp'),
        ('T2M_MAX', 'Max Temp'),
        ('T2M_MIN', 'Min Temp')
    ]
    
    for i, (col, label) in enumerate(metrics_to_show):
        with temp_cols[i]:
            st.markdown(f"**{label}**")
            for country in selected_countries:
                val = filtered_data[filtered_data['Country'] == country][col].mean()
                st.metric(country, f"{val:.1f}°C")
    
    # Precipitation summary
    st.markdown("---")
    st.markdown("#### 🌧️ Precipitation Summary")
    precip_summary = filtered_data.groupby('Country')['PRECTOTCORR'].agg([
        'mean', 'max'
    ]).round(2)
    precip_summary.columns = ['Mean (mm/day)', 'Max (mm/day)']
    precip_summary['Rainy Days %'] = filtered_data.groupby('Country')['PRECTOTCORR'].apply(
        lambda x: (x > 0).mean() * 100
    ).round(1)
    st.dataframe(precip_summary, use_container_width=True)

# ============================================================
# TAB 4: EXTREME EVENTS
# ============================================================
with tab4:
    st.subheader("🔥 Extreme Events Analysis")
    st.caption(f"Showing data for: {', '.join(selected_countries)} | {year_range[0]} – {year_range[1]}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Extreme Heat Days (T2M_MAX > 35°C)")
        heat_data = filtered_data[filtered_data['T2M_MAX'] > 35].groupby('Country').size()
        heat_data = heat_data.reindex(selected_countries, fill_value=0)
        
        if heat_data.sum() > 0:
            fig, ax = plt.subplots(figsize=(8, 5))
            colors_list = [country_colors.get(c, '#999') for c in heat_data.index]
            bars = ax.bar(heat_data.index, heat_data.values, color=colors_list, edgecolor='white')
            ax.set_ylabel('Number of Days', fontsize=11)
            ax.set_title('Total Days with T2M_MAX Exceeding 35°C', fontsize=13, fontweight='bold')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add value labels
            for bar, val in zip(bars, heat_data.values):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                            str(val), ha='center', fontsize=11, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        else:
            st.info("No extreme heat days (T2M_MAX > 35°C) found for selected countries.")
    
    with col2:
        st.markdown("#### 🏜️ Dry Days Analysis")
        dry_data = filtered_data.groupby('Country')['PRECTOTCORR'].apply(
            lambda x: (x == 0).sum()
        ).reindex(selected_countries, fill_value=0)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_list = [country_colors.get(c, '#999') for c in dry_data.index]
        bars = ax.barh(dry_data.index, dry_data.values, color=colors_list, edgecolor='white')
        ax.set_xlabel('Number of Days with Zero Precipitation', fontsize=11)
        ax.set_title('Total Dry Days (Precipitation = 0 mm)', fontsize=13, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar, val in zip(bars, dry_data.values):
            ax.text(val + 5, bar.get_y() + bar.get_height()/2,
                    f"{val} ({(val/len(filtered_data[filtered_data['Country']==bar.get_label()])*100):.0f}%)",
                    va='center', fontsize=10)
        
        st.pyplot(fig)
        plt.close()
    
    # Yearly heat days trend
    st.markdown("---")
    st.markdown("#### 📈 Yearly Extreme Heat Trend")
    
    if 'Sudan' in selected_countries or 'Nigeria' in selected_countries:
        heat_yearly = filtered_data[filtered_data['T2M_MAX'] > 35].groupby(
            ['Country', 'Year']).size().unstack(fill_value=0)
        
        if not heat_yearly.empty:
            fig, ax = plt.subplots(figsize=(14, 5))
            heat_yearly.T.plot(ax=ax, marker='o', linewidth=2, markersize=6)
            ax.set_title('Extreme Heat Days per Year (T2M_MAX > 35°C)', fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Days', fontsize=12)
            ax.set_xlabel('Year', fontsize=12)
            ax.legend(title='Country', fontsize=10)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
            plt.close()
    else:
        st.info("Selected countries have minimal extreme heat events.")

# ============================================================
# TAB 5: KEY FINDINGS
# ============================================================
with tab5:
    st.subheader("📖 Key Findings & COP32 Insights")
    
    st.markdown("""
    ### 🔑 Five Key Climate Insights
    
    **1. Elevation-Temperature Gradient**
    Temperature decreases by approximately 0.65°C for every 100 meters of elevation gain.
    Ethiopia (2,355m, 16.1°C) and Kenya (1,795m, 20.4°C) are naturally cooler than
    Sudan (400m, 28.8°C) and the coastal nations.
    
    **2. Sudan's Extreme Heat Crisis**
    Sudan experiences extreme heat on 66% of all days (T2M_MAX > 35°C), with 27% 
    exceeding 40°C. This demands urgent adaptation finance for cooling infrastructure 
    and heat early warning systems.
    
    **3. Coastal Megacity Flood Risk**
    Lagos (Nigeria) recorded 166.10 mm maximum daily rainfall and Dar es Salaam 
    (Tanzania) recorded 122.65 mm. Combined with sea-level rise, these cities face 
    compound flood risks requiring major infrastructure investment.
    
    **4. Ethiopia's Highland Vulnerability**
    Ethiopia's narrow temperature range (10.0-21.5°C, std=1.9°C) supports specialized 
    agriculture. Even small warming could push conditions outside optimal growing 
    ranges, threatening food security for 80+ million people.
    
    **5. Water Insecurity Across All Countries**
    Precipitation patterns vary dramatically: from Sudan's 0.64 mm/day (73% dry days) 
    to Tanzania's 3.74 mm/day (95% rain days). Regional water management cooperation 
    is essential for climate adaptation.
    
    ---
    
    ### 🎯 COP32 Recommendations
    
    | Priority | Country | Action Needed |
    |----------|---------|---------------|
    | 1 | Sudan | Heat adaptation finance, cooling centers |
    | 2 | Nigeria | Urban flood defense, drainage systems |
    | 3 | Tanzania | Coastal resilience, early warning systems |
    | 4 | Kenya | Water storage, soil moisture conservation |
    | 5 | Ethiopia | Climate-smart highland agriculture |
    
    ---
    
    ### 📚 References
    
    - NASA POWER Data: https://power.larc.nasa.gov/
    - WMO State of the Climate in Africa 2024
    - IPCC Sixth Assessment Report - Africa Chapter
    - COP32 Ethiopia - UNFCCC: https://unfccc.int/
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "<p><strong>Data Source:</strong> NASA POWER (MERRA-2 Reanalysis) | "
    "<strong>Period:</strong> January 2015 – March 2026 | "
    "<strong>Resolution:</strong> Daily observations at capital city coordinates</p>"
    "<p><strong>Analysis:</strong> 10 Academy AI Mastery Program – Week 0 Challenge | "
    "<strong>Author:</strong> Meron Teklehaymanot Gebru</p>"
    "<p><em>Built with Streamlit • Evidence-backed insights for COP32 negotiations</em></p>"
    "</div>",
    unsafe_allow_html=True
)