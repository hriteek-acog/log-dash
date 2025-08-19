import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="HCRIS Hospital Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .critical-card {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 6px solid #f44336;
        box-shadow: 0 2px 8px rgba(244, 67, 54, 0.15);
        margin-bottom: 1rem;
    }
    .high-priority {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff9800;
        margin: 0.5rem 0;
    }
    .medium-priority {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #9c27b0;
        margin: 0.5rem 0;
    }
    .low-priority {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4caf50;
        margin: 0.5rem 0;
    }
    .issue-item {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 0.3rem;
    }
    .critical-issue {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .high-issue {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .medium-issue {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .status-icon {
        font-size: 1.2em;
        margin-right: 0.5rem;
    }
    .main-title {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1 class='main-title'>🏥 HCRIS Hospital Analytics Dashboard</h1>", unsafe_allow_html=True)

# Sample data based on the log file (you would replace this with actual database connections)
@st.cache_data
def load_sample_data():
    # Contract Labor Data
    contract_labor_data = {
        'Year': [2021, 2022, 2023, 2024] * 10,
        'State': ['TX', 'CA', 'FL', 'OH'] * 10,
        'Hospital_Count': [343, 338, 196, 167, 332, 330, 197, 163, 330, 327, 199, 161, 179, 189, 126, 111] + [100] * 24,
        'Mean_Contract_Pct': [2.4, 2.2, 2.0, 2.4, 2.4, 2.4, 2.1, 2.4, 2.4, 2.3, 2.2, 2.4, 2.6, 2.5, 2.4, 2.6] + [2.0] * 24,
        'Within_Target': [11.8, 12.6, 14.2, 15.4] * 10,
        'Below_Target': [85.0, 84.0, 82.3, 79.8] * 10,
        'Above_Target': [3.2, 3.4, 3.6, 4.8] * 10
    }
    
    # Operating Cost Data
    operating_cost_data = {
        'Year': [2021, 2022, 2023, 2024],
        'Total_Hospitals': [6056, 6066, 6103, 3424],
        'Revenue_Complete': [96.2, 96.0, 96.0, 97.9],
        'Cost_Complete': [98.7, 98.6, 98.6, 99.2],
        'FTE_Complete': [84.1, 83.3, 82.8, 83.1],
        'Contract_Complete': [72.6, 71.7, 71.0, 71.5]
    }
    
    # State-wise financial data (sample)
    state_financial_data = {
        'State': ['TX', 'CA', 'FL', 'OH', 'PA', 'LA', 'IL', 'IN', 'NY', 'GA'],
        'Hospital_Count_2023': [570, 396, 261, 220, 203, 195, 199, 169, 164, 160],
        'Mean_Operating_Cost_2023': [186662556, 439031724, 303463674, 299311128, 325987469, 103938058, 266668769, 192137948, 704628680, 226425251],
        'Outlier_Percentage': [14.9, 5.8, 8.4, 10.9, 11.3, 16.4, 7.5, 10.7, 9.8, 10.0]
    }
    
    # High outlier hospitals
    outlier_hospitals = {
        'Hospital': ['STANFORD HEALTH CARE', 'UCSF MEDICAL CENTER', 'NEW YORK PRESBYTERIAN HOSPITAL', 
                    'NYU LANGONE HOSPITALS', 'CLEVELAND CLINIC HOSPITAL', 'UT MD ANDERSON CANCER CENTER'],
        'State': ['CA', 'CA', 'NY', 'NY', 'OH', 'TX'],
        'Operating_Cost_2023': [7425866725, 5835800029, 9818337999, 8956110402, 8323985995, 5471697134],
        'Type': ['Teaching', 'Teaching', 'Teaching', 'Teaching', 'Teaching', 'Teaching']
    }
    
    return (pd.DataFrame(contract_labor_data), 
            pd.DataFrame(operating_cost_data),
            pd.DataFrame(state_financial_data),
            pd.DataFrame(outlier_hospitals))

# Load data
contract_df, operating_df, state_df, outlier_df = load_sample_data()

# Sidebar for navigation
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.selectbox(
    "Select Analysis View",
    ["Overview", "Contract Labor Analysis", "Financial Metrics", "State Comparisons", "Outlier Analysis", "Data Quality"]
)

if page == "Overview":
    st.header("📈 Database Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>6,229</h3>
            <p>Total Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>4 Years</h3>
            <p>Data Coverage (2021-2024)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>1,496</h3>
            <p>Teaching Hospitals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>56</h3>
            <p>States Covered</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Data Completeness Over Time")
    
    # Data completeness chart
    fig_completeness = go.Figure()
    
    fig_completeness.add_trace(go.Scatter(
        x=operating_df['Year'], y=operating_df['Revenue_Complete'],
        mode='lines+markers', name='Revenue Data', line=dict(color='#1f77b4')
    ))
    fig_completeness.add_trace(go.Scatter(
        x=operating_df['Year'], y=operating_df['Cost_Complete'],
        mode='lines+markers', name='Cost Data', line=dict(color='#ff7f0e')
    ))
    fig_completeness.add_trace(go.Scatter(
        x=operating_df['Year'], y=operating_df['FTE_Complete'],
        mode='lines+markers', name='FTE Data', line=dict(color='#2ca02c')
    ))
    fig_completeness.add_trace(go.Scatter(
        x=operating_df['Year'], y=operating_df['Contract_Complete'],
        mode='lines+markers', name='Contract Labor Data', line=dict(color='#d62728')
    ))
    
    fig_completeness.update_layout(
        title="Data Completeness Percentage by Year",
        xaxis_title="Year",
        yaxis_title="Completeness (%)",
        yaxis=dict(range=[60, 100]),
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig_completeness, use_container_width=True)
    
    # Hospital count by year
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hospitals = px.bar(
            operating_df, x='Year', y='Total_Hospitals',
            title="Total Hospitals by Year",
            color='Total_Hospitals',
            color_continuous_scale='Blues'
        )
        fig_hospitals.update_layout(template="plotly_white", height=350)
        st.plotly_chart(fig_hospitals, use_container_width=True)
    
    with col2:
        # Data quality indicators
        st.subheader("Data Quality Indicators")
        st.markdown("""
        <div class="critical-card">
            <h4 style="color: #d32f2f; margin-top: 0;">🚨 Critical Issues Identified</h4>
            <div class="issue-item critical-issue">
                <span class="status-icon">❌</span>
                <strong>Negative revenue records: 25</strong> (Data integrity violation)
            </div>
            <div class="issue-item high-issue">
                <span class="status-icon">⚠️</span>
                <strong>Negative operating costs: 5</strong> (Validation needed)
            </div>
            <div class="issue-item medium-issue">
                <span class="status-icon">⚠️</span>
                <strong>Negative contract labor: 9</strong> (Review required)
            </div>
            <div class="issue-item high-issue">
                <span class="status-icon">📊</span>
                <strong>Contract labor data coverage: ~71%</strong> (Incomplete reporting)
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "Contract Labor Analysis":
    st.header("👷 Contract Labor Analysis")
    
    # Year selector
    year_col1, year_col2 = st.columns([1, 3])
    with year_col1:
        selected_year = st.selectbox("Select Year", [2021, 2022, 2023, 2024], index=2)
    
    # Contract labor statistics based on year
    contract_stats = {
        2021: {'mean': 2.1, 'median': 1.9, 'std': 1.6, 'max': 41.9, 'within_target': 11.8},
        2022: {'mean': 2.1, 'median': 1.9, 'std': 1.7, 'max': 43.3, 'within_target': 12.6},
        2023: {'mean': 2.2, 'median': 1.9, 'std': 1.6, 'max': 41.1, 'within_target': 14.2},
        2024: {'mean': 2.3, 'median': 2.0, 'std': 1.6, 'max': 20.2, 'within_target': 15.4}
    }
    
    stats = contract_stats[selected_year]
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean Contract %", f"{stats['mean']:.1f}%")
    with col2:
        st.metric("Median Contract %", f"{stats['median']:.1f}%")
    with col3:
        st.metric("Max Contract %", f"{stats['max']:.1f}%")
    with col4:
        st.metric("Within Target (3-5%)", f"{stats['within_target']:.1f}%")
    
    # Contract labor distribution simulation
    np.random.seed(42)
    # Generate array of 1000 values for distribution
    contract_dist = np.random.gamma(2, 1, 1000) * stats['mean'] / 2
    contract_dist = np.clip(contract_dist, 0, 45)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution histogram - create DataFrame for plotly
        dist_df = pd.DataFrame({'Contract_Labor_Pct': contract_dist})
        fig_dist = px.histogram(
            dist_df, 
            x='Contract_Labor_Pct',
            nbins=50,
            title=f"Contract Labor Distribution - {selected_year}",
            labels={'Contract_Labor_Pct': 'Contract Labor %', 'count': 'Number of Hospitals'}
        )
        
        # Add target range
        fig_dist.add_vline(x=3, line_dash="dash", line_color="green", annotation_text="Target Min (3%)")
        fig_dist.add_vline(x=5, line_dash="dash", line_color="green", annotation_text="Target Max (5%)")
        fig_dist.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Target range analysis
        target_data = pd.DataFrame({
            'Category': ['Below Target (<3%)', 'Within Target (3-5%)', 'Above Target (>5%)'],
            'Percentage': [85.0, 11.8, 3.2] if selected_year == 2021 else 
                         [84.0, 12.6, 3.4] if selected_year == 2022 else
                         [82.3, 14.2, 3.6] if selected_year == 2023 else
                         [79.8, 15.4, 4.8],
            'Color': ['#ff4444', '#44ff44', '#ffaa44']
        })
        
        fig_target = px.pie(
            target_data, values='Percentage', names='Category',
            title=f"Target Range Distribution - {selected_year}",
            color='Category',
            color_discrete_map={
                'Below Target (<3%)': '#ff4444',
                'Within Target (3-5%)': '#44ff44', 
                'Above Target (>5%)': '#ffaa44'
            }
        )
        fig_target.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_target, use_container_width=True)
    
    # State-wise analysis
    st.subheader("State-wise Contract Labor Analysis")
    
    # Top states data
    top_states_data = pd.DataFrame({
        'State': ['TX', 'CA', 'FL', 'IL', 'OH', 'PA', 'NY', 'MI', 'WI', 'GA'],
        'Hospital_Count': [330, 327, 199, 177, 161, 150, 141, 138, 123, 122],
        'Mean_Contract_Pct': [2.4, 2.3, 2.2, 1.9, 2.4, 1.8, 2.4, 2.4, 2.1, 2.3]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_states = px.bar(
            top_states_data, x='State', y='Hospital_Count',
            title="Hospital Count by State",
            color='Hospital_Count',
            color_continuous_scale='Blues'
        )
        fig_states.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_states, use_container_width=True)
    
    with col2:
        fig_contract_states = px.bar(
            top_states_data, x='State', y='Mean_Contract_Pct',
            title="Mean Contract Labor % by State",
            color='Mean_Contract_Pct',
            color_continuous_scale='Reds'
        )
        fig_contract_states.add_hline(y=3, line_dash="dash", line_color="green", annotation_text="Target Min")
        fig_contract_states.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Target Max")
        fig_contract_states.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_contract_states, use_container_width=True)
    
    # High outlier hospitals
    st.subheader("⚠️ High Contract Labor Outliers")
    outlier_hospitals_cl = pd.DataFrame({
        'Hospital': ['SAME DAY SURGERY CENTER', 'BLACK HILLS SURGICAL HOSPITAL LLP', 'SALINA SURGICAL HOSPITAL', 'STRAITH HOSPITAL FOR SPECIAL SURGERY'],
        'Contract_Labor_Pct': [41.1, 20.2, 17.8, 18.6],
        'State': ['SD', 'SD', 'KS', 'MI'],
        'Year': [2023, 2023, 2023, 2023]
    })
    
    fig_outliers = px.bar(
        outlier_hospitals_cl, x='Hospital', y='Contract_Labor_Pct',
        color='State',
        title="Hospitals with >15% Contract Labor (2023)",
        labels={'Contract_Labor_Pct': 'Contract Labor %'}
    )
    fig_outliers.update_layout(template="plotly_white", height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig_outliers, use_container_width=True)

elif page == "Financial Metrics":
    st.header("💰 Financial Metrics Analysis")
    
    # Operating margin analysis
    st.subheader("Operating Margin Trends")
    
    margin_data = pd.DataFrame({
        'Year': [2021, 2022, 2023, 2024],
        'Mean_Margin': [-891856.3, -2734069.7, -2228747.8, -7.7],
        'Median_Margin': [-2.3, -4.6, -2.6, -1.1],
        'Extreme_Negative': [299, 350, 354, 173],
        'Extreme_Positive': [21, 14, 29, 13]
    }
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_margin_trend = go.Figure()
        fig_margin_trend.add_trace(go.Scatter(
            x=margin_data['Year'], y=margin_data['Median_Margin'],
            mode='lines+markers', name='Median Margin',
            line=dict(color='#1f77b4', width=3)
        ))
        fig_margin_trend.update_layout(
            title="Median Operating Margin Trend",
            xaxis_title="Year",
            yaxis_title="Operating Margin (%)",
            template="plotly_white",
            height=400
        )
        fig_margin_trend.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        st.plotly_chart(fig_margin_trend, use_container_width=True)
    
    with col2:
        # Extreme margins
        fig_extreme = go.Figure()
        fig_extreme.add_trace(go.Bar(
            x=margin_data['Year'], y=margin_data['Extreme_Negative'],
            name='Extreme Losses (<-50%)', marker_color='#ff4444'
        ))
        fig_extreme.add_trace(go.Bar(
            x=margin_data['Year'], y=margin_data['Extreme_Positive'],
            name='Extreme Gains (>50%)', marker_color='#44ff44'
        ))
        fig_extreme.update_layout(
            title="Hospitals with Extreme Margins",
            xaxis_title="Year",
            yaxis_title="Number of Hospitals",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_extreme, use_container_width=True)
    
    # Revenue per bed analysis
    st.subheader("Revenue per Bed Analysis")
    
    revenue_per_bed_data = {
        2021: {'mean': 1431014, 'median': 1161710, 'outliers': 222},
        2022: {'mean': 1488651, 'median': 1200171, 'outliers': 233},
        2023: {'mean': 1597886, 'median': 1276304, 'outliers': 233},
        2024: {'mean': 1721527, 'median': 1367647, 'outliers': 120}
    }
    
    revenue_df = pd.DataFrame([
        {'Year': year, 'Mean': data['mean'], 'Median': data['median'], 'Outliers': data['outliers']}
        for year, data in revenue_per_bed_data.items()
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=revenue_df['Year'], y=revenue_df['Mean'],
            mode='lines+markers', name='Mean Revenue/Bed',
            line=dict(color='#2ca02c', width=3)
        ))
        fig_revenue.add_trace(go.Scatter(
            x=revenue_df['Year'], y=revenue_df['Median'],
            mode='lines+markers', name='Median Revenue/Bed',
            line=dict(color='#ff7f0e', width=3)
        ))
        fig_revenue.update_layout(
            title="Revenue per Bed Trends",
            xaxis_title="Year",
            yaxis_title="Revenue per Bed ($)",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        fig_outliers_rev = px.bar(
            revenue_df, x='Year', y='Outliers',
            title="Revenue per Bed Outliers by Year",
            color='Outliers',
            color_continuous_scale='Oranges'
        )
        fig_outliers_rev.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_outliers_rev, use_container_width=True)

elif page == "State Comparisons":
    st.header("🗺️ State-wise Financial Comparisons")
    
    # State financial overview
    st.subheader("Operating Costs by State (2023)")
    
    # Convert to millions for better readability
    state_df['Mean_Operating_Cost_Millions'] = state_df['Mean_Operating_Cost_2023'] / 1_000_000
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_state_costs = px.bar(
            state_df.sort_values('Mean_Operating_Cost_Millions', ascending=True),
            x='Mean_Operating_Cost_Millions', y='State',
            orientation='h',
            title="Mean Operating Costs by State (2023)",
            color='Mean_Operating_Cost_Millions',
            color_continuous_scale='Viridis',
            labels={'Mean_Operating_Cost_Millions': 'Operating Cost ($ Millions)'}
        )
        fig_state_costs.update_layout(template="plotly_white", height=500)
        st.plotly_chart(fig_state_costs, use_container_width=True)
    
    with col2:
        fig_hospital_count = px.scatter(
            state_df, x='Hospital_Count_2023', y='Mean_Operating_Cost_Millions',
            size='Hospital_Count_2023', color='Outlier_Percentage',
            hover_name='State',
            title="Hospital Count vs Mean Operating Cost",
            labels={
                'Hospital_Count_2023': 'Number of Hospitals',
                'Mean_Operating_Cost_Millions': 'Mean Operating Cost ($ Millions)',
                'Outlier_Percentage': 'Outlier %'
            }
        )
        fig_hospital_count.update_layout(template="plotly_white", height=500)
        st.plotly_chart(fig_hospital_count, use_container_width=True)
    
    # Outlier percentage by state
    st.subheader("Financial Outlier Distribution by State")
    
    fig_outlier_pct = px.bar(
        state_df.sort_values('Outlier_Percentage', ascending=False),
        x='State', y='Outlier_Percentage',
        title="Percentage of Financial Outliers by State",
        color='Outlier_Percentage',
        color_continuous_scale='Reds'
    )
    fig_outlier_pct.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_outlier_pct, use_container_width=True)
    
    # State rankings table
    st.subheader("State Rankings Summary")
    
    state_summary = state_df.copy()
    state_summary['Mean_Operating_Cost_Millions'] = state_summary['Mean_Operating_Cost_Millions'].round(1)
    state_summary = state_summary.sort_values('Mean_Operating_Cost_Millions', ascending=False)
    
    st.dataframe(
        state_summary[['State', 'Hospital_Count_2023', 'Mean_Operating_Cost_Millions', 'Outlier_Percentage']]
        .rename(columns={
            'Hospital_Count_2023': 'Hospital Count',
            'Mean_Operating_Cost_Millions': 'Mean Cost ($M)',
            'Outlier_Percentage': 'Outlier %'
        }),
        use_container_width=True
    )

elif page == "Outlier Analysis":
    st.header("🚨 Hospital Outlier Analysis")
    
    # Top financial outliers
    st.subheader("Top Financial Outliers (2023)")
    
    outlier_df['Operating_Cost_Billions'] = outlier_df['Operating_Cost_2023'] / 1_000_000_000
    
    fig_outliers = px.bar(
        outlier_df.sort_values('Operating_Cost_Billions', ascending=True),
        x='Operating_Cost_Billions', y='Hospital',
        orientation='h',
        color='State',
        title="Highest Operating Costs ($ Billions)",
        labels={'Operating_Cost_Billions': 'Operating Cost ($ Billions)'}
    )
    fig_outliers.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_outliers, use_container_width=True)
    
    # FTE Analysis
    st.subheader("FTE Analysis and Outliers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # FTE outliers (simulated based on log data)
        fte_outliers = pd.DataFrame({
            'Hospital': ['HEBREW REHABILITATION CENTER', 'DALLAS CO. HOSP. DIST.', 'OU MEDICAL CENTER', 'YALE NEW HAVEN HOSPITAL', 'CHRISTIANA CARE HEALTH SYSTEM'],
            'FTE': [172130, 123354, 108157, 107099, 95767],
            'Beds': [667, 786, 819, 1306, 1172]
        })
        
        fig_fte = px.scatter(
            fte_outliers, x='Beds', y='FTE',
            hover_name='Hospital',
            title="FTE vs Bed Count - Top Outliers",
            size='FTE',
            color='FTE',
            color_continuous_scale='Blues'
        )
        fig_fte.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_fte, use_container_width=True)
    
    with col2:
        # FTE per bed ratio
        fte_outliers['FTE_per_Bed'] = fte_outliers['FTE'] / fte_outliers['Beds']
        
        fig_fte_ratio = px.bar(
            fte_outliers.sort_values('FTE_per_Bed', ascending=True),
            x='FTE_per_Bed', y='Hospital',
            orientation='h',
            title="FTE per Bed Ratio - Top Outliers",
            color='FTE_per_Bed',
            color_continuous_scale='Oranges'
        )
        fig_fte_ratio.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_fte_ratio, use_container_width=True)
    
    # Contract labor outliers
    st.subheader("Contract Labor Outliers Across Years")
    
    cl_outliers_all = pd.DataFrame({
        'Hospital': ['SAME DAY SURGERY CENTER', 'BLACK HILLS SURGICAL HOSPITAL LLP', 'SALINA SURGICAL HOSPITAL'] * 4,
        'Year': [2021, 2021, 2021, 2022, 2022, 2022, 2023, 2023, 2023, 2024, 2024, 2024],
        'Contract_Pct': [41.9, 22.9, 17.5, 43.3, 22.0, 18.0, 41.1, 20.2, 17.8, np.nan, 20.2, 16.7],
        'State': ['SD', 'SD', 'KS'] * 4
    })
    
    cl_outliers_all = cl_outliers_all.dropna()
    
    fig_cl_trend = px.line(
        cl_outliers_all, x='Year', y='Contract_Pct',
        color='Hospital',
        title="Contract Labor Trends - Persistent Outliers",
        markers=True
    )
    fig_cl_trend.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_cl_trend, use_container_width=True)

elif page == "Data Quality":
    st.header("🔍 Data Quality Assessment")
    
    # Data completeness matrix
    st.subheader("Data Completeness Matrix")
    
    completeness_matrix = operating_df[['Year', 'Revenue_Complete', 'Cost_Complete', 'FTE_Complete', 'Contract_Complete']].set_index('Year')
    
    fig_heatmap = px.imshow(
        completeness_matrix.T,
        aspect="auto",
        color_continuous_scale='RdYlGn',
        title="Data Completeness Heatmap (%)",
        labels={'x': 'Year', 'y': 'Data Type', 'color': 'Completeness %'}
    )
    fig_heatmap.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Data quality issues
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Quality Issues")
        
        quality_issues = pd.DataFrame({
            'Issue Type': ['Negative Revenue', 'Negative Operating Cost', 'Negative FTE', 'Negative Contract Labor'],
            'Count': [25, 5, 0, 9],
            'Severity': ['High', 'High', 'None', 'Medium']
        })
        
        fig_issues = px.bar(
            quality_issues, x='Issue Type', y='Count',
            color='Severity',
            color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa44', 'None': '#44ff44'},
            title="Data Quality Issues Count"
        )
        fig_issues.update_layout(template="plotly_white", height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_issues, use_container_width=True)
    
    with col2:
        st.subheader("Database Integrity")
        
        integrity_metrics = pd.DataFrame({
            'Metric': ['Orphaned Financial Records', 'Orphaned Department Records', 'Total Records', 'Data Consistency'],
            'Value': ['0', '0', '150,338', 'Good'],
            'Status': ['✅ Good', '✅ Good', '📊 Info', '✅ Good']
        })
        
        st.dataframe(integrity_metrics, use_container_width=True, hide_index=True)
    
    # Year-over-year data availability
    st.subheader("Data Availability Trends")
    
    fig_availability = go.Figure()
    
    for column in ['Revenue_Complete', 'Cost_Complete', 'FTE_Complete', 'Contract_Complete']:
        fig_availability.add_trace(go.Scatter(
            x=operating_df['Year'], 
            y=operating_df[column],
            mode='lines+markers',
            name=column.replace('_Complete', ' Data'),
            line=dict(width=3)
        ))
    
    fig_availability.update_layout(
        title="Data Completeness Trends Over Time",
        xaxis_title="Year",
        yaxis_title="Completeness (%)",
        template="plotly_white",
        height=400,
        yaxis=dict(range=[65, 100])
    )
    st.plotly_chart(fig_availability, use_container_width=True)
    
    # Data quality recommendations
    st.subheader("🔧 Data Quality Recommendations")
    
    st.markdown("""
    <div class="critical-card">
        <h4 style="color: #d32f2f; margin-top: 0;">🎯 Priority Issues to Address</h4>
        
        <div class="high-priority">
            <h5 style="color: #e65100; margin-top: 0;">🔴 HIGH PRIORITY</h5>
            <div style="margin-left: 1rem;">
                <strong>1. Contract Labor Coverage:</strong> Only ~71% of hospitals report contract labor data<br>
                <em>→ Implement mandatory reporting requirements and data validation checks</em>
            </div>
        </div>
        
        <div class="high-priority">
            <h5 style="color: #e65100; margin-top: 0;">🔴 CRITICAL</h5>
            <div style="margin-left: 1rem;">
                <strong>2. Negative Values:</strong> 25 hospitals with negative revenue need investigation<br>
                <em>→ Immediate data audit and correction procedures required</em>
            </div>
        </div>
        
        <div class="medium-priority">
            <h5 style="color: #7b1fa2; margin-top: 0;">🟡 MEDIUM PRIORITY</h5>
            <div style="margin-left: 1rem;">
                <strong>3. FTE Ratios:</strong> 3,337 hospitals have unreasonable FTE/bed ratios<br>
                <em>→ Review staffing calculation methodologies and outlier detection</em>
            </div>
        </div>
        
        <div class="medium-priority">
            <h5 style="color: #7b1fa2; margin-top: 0;">🟡 MEDIUM PRIORITY</h5>
            <div style="margin-left: 1rem;">
                <strong>4. Extreme Margins:</strong> High number of hospitals with extreme operating margins<br>
                <em>→ Investigate business model variations and reporting accuracy</em>
            </div>
        </div>
        
        <div class="low-priority">
            <h5 style="color: #388e3c; margin-top: 0;">🟢 ONGOING</h5>
            <div style="margin-left: 1rem;">
                <strong>5. Data Validation:</strong> Implement stronger validation rules for financial metrics<br>
                <em>→ Establish automated quality checks and alert systems</em>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif page == "Contract Labor Analysis":
    # This section was already implemented above
    pass

else:  # Default to Overview if somehow no match
    st.header("📈 Database Overview")
    st.write("Select a page from the sidebar to view detailed analysis.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>HCRIS Hospital Analytics Dashboard | Data covers 2021-2024 | Last updated: August 18, 2025</p>
    <p>Database contains 6,229 hospitals across 56 states with 21,649 financial records</p>
</div>
""", unsafe_allow_html=True)

# Sidebar additional info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Dashboard Features")
st.sidebar.markdown("""
- **Overview**: Key database metrics and trends
- **Contract Labor**: Detailed contract labor analysis
- **Financial Metrics**: Operating margins and revenue analysis
- **State Comparisons**: Regional financial comparisons
- **Outlier Analysis**: Identification of unusual hospitals
- **Data Quality**: Assessment of data completeness and issues
""")

st.sidebar.markdown("### ⚙️ Data Sources")
st.sidebar.markdown("""
- **Hospitals**: 6,229 facilities
- **Years**: 2021-2024
- **Financial Records**: 21,649
- **Department Records**: 150,338
""")

# Add download functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 Export Data")

if st.sidebar.button("Download Sample Data"):
    # Create downloadable CSV
    sample_data = pd.concat([
        contract_df.assign(source='contract_labor'),
        operating_df.assign(source='operating_metrics'),
        state_df.assign(source='state_financial'),
        outlier_df.assign(source='outliers')
    ], ignore_index=True)
    
    csv = sample_data.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"hcris_dashboard_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )