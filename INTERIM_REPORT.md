# Interim Report - Week 0 Climate Challenge

## Task 1: Environment & CI/CD Setup 

### Completed:
- Python virtual environment with pinned dependencies
- GitHub Actions CI workflow (runs on push to main)
- Conventional commits (`init:`, `chore:`, `ci:`, `feat:`)
- `.gitignore` excludes `data/`, `*.csv`, `venv/`
- Project structure: `scripts/`, `notebooks/`, `tests/`, `app/`

### CI Status: Passing

## Task 2: Data Profiling & Cleaning Approach

### Countries Analyzed:
1. Ethiopia (Addis Ababa) - Highland, ~2,355m elevation
2. Kenya (Nairobi) - Highland, ~1,795m
3. Sudan (Khartoum) - Hot desert, ~400m
4. Tanzania (Dar es Salaam) - Tropical coastal
5. Nigeria (Lagos) - Tropical coastal

### Data Pipeline:
- **Loading**: Standardized function `load_and_clean_country()`
- **Sentinel handling**: Replace `-999` with `NaN`
- **Date parsing**: `YEAR` + `DOY` → `datetime` column
- **Quality checks**: Missing values, duplicates, Z-score outliers (|Z| > 3)

### Analysis Plan:
1. Monthly temperature trends (line charts)
2. Monthly precipitation totals (bar charts)
3. Seasonal climatology patterns
4. Extreme event frequency (heat days, dry spells)
5. Correlation analysis (heatmaps, scatter plots)
6. Cross-country vulnerability ranking

### Data Observations:
- Ethiopia: Low pressure (77 kPa), large diurnal range, bimodal rainfall
- Sudan: Extreme heat (T2M_MAX > 44°C), very low precipitation
- Kenya: Moderate temps, distinct wet/dry seasons
- Tanzania/Nigeria: Coastal influence, high humidity

## Next Steps for Final Submission:
1. Complete individual country EDA notebooks
2. Cross-country comparison with ANOVA testing
3. Climate vulnerability composite index
4. COP32 negotiation-grade insights
5. Optional: Streamlit dashboard
