import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="WHO Triple Billion Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_and_process_data():
    """Load and process WHO data with caching for performance"""
    try:
        # Load Data
        df_WHO = pd.read_csv("RELAY_3B_DATA.csv")
        
        # Drop unnecessary columns
        columns_to_drop = ['RATE_PER_100_NL', 'RATE_PER_100_NU', 'RATE_PER_100_N',
                          'IND_PER_CODE', 'IND_UUID', 'IND_ID', 'IND_NAME', 'IND_CODE']
        # Only drop columns that exist in the dataframe
        columns_to_drop = [col for col in columns_to_drop if col in df_WHO.columns]
        df_WHO = df_WHO.drop(columns_to_drop, axis=1)
        
        # WHO 6개 지역과 소속 국가들을 매핑하는 딕셔너리
        region_mapping = {
            'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
            'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cabo Verde': 'Africa', 'Cameroon': 'Africa',
            'Central African Republic': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa', 'Congo': 'Africa',
            "Côte d'Ivoire": 'Africa', 'Democratic Republic of the Congo': 'Africa', 'Equatorial Guinea': 'Africa',
            'Eritrea': 'Africa', 'Eswatini': 'Africa', 'Ethiopia': 'Africa', 'Gabon': 'Africa',
            'Gambia': 'Africa', 'Ghana': 'Africa', 'Guinea': 'Africa', 'Guinea-Bissau': 'Africa',
            'Kenya': 'Africa', 'Lesotho': 'Africa', 'Liberia': 'Africa', 'Madagascar': 'Africa',
            'Malawi': 'Africa', 'Mali': 'Africa', 'Mauritania': 'Africa', 'Mauritius': 'Africa',
            'Mozambique': 'Africa', 'Namibia': 'Africa', 'Niger': 'Africa', 'Nigeria': 'Africa',
            'Rwanda': 'Africa', 'Sao Tome and Principe': 'Africa', 'Senegal': 'Africa', 'Seychelles': 'Africa',
            'Sierra Leone': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa', 'Togo': 'Africa',
            'Uganda': 'Africa', 'United Republic of Tanzania': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
            
            'Antigua and Barbuda': 'Americas', 'Argentina': 'Americas', 'Bahamas': 'Americas',
            'Barbados': 'Americas', 'Belize': 'Americas', 'Bolivia (Plurinational State of)': 'Americas',
            'Brazil': 'Americas', 'Canada': 'Americas', 'Chile': 'Americas', 'Colombia': 'Americas',
            'Costa Rica': 'Americas', 'Cuba': 'Americas', 'Dominica': 'Americas',
            'Dominican Republic': 'Americas', 'Ecuador': 'Americas', 'El Salvador': 'Americas',
            'Grenada': 'Americas', 'Guatemala': 'Americas', 'Guyana': 'Americas', 'Haiti': 'Americas',
            'Honduras': 'Americas', 'Jamaica': 'Americas', 'Mexico': 'Americas', 'Nicaragua': 'Americas',
            'Panama': 'Americas', 'Paraguay': 'Americas', 'Peru': 'Americas',
            'Saint Kitts and Nevis': 'Americas', 'Saint Lucia': 'Americas',
            'Saint Vincent and the Grenadines': 'Americas', 'Suriname': 'Americas',
            'Trinidad and Tobago': 'Americas', 'United States of America': 'Americas', 'Uruguay': 'Americas',
            'Venezuela (Bolivarian Republic of)': 'Americas',
            
            'Afghanistan': 'Eastern Mediterranean', 'Bahrain': 'Eastern Mediterranean', 'Djibouti': 'Eastern Mediterranean',
            'Egypt': 'Eastern Mediterranean', 'Iran (Islamic Republic of)': 'Eastern Mediterranean',
            'Iraq': 'Eastern Mediterranean', 'Jordan': 'Eastern Mediterranean', 'Kuwait': 'Eastern Mediterranean',
            'Lebanon': 'Eastern Mediterranean', 'Libya': 'Eastern Mediterranean', 'Morocco': 'Eastern Mediterranean',
            'Oman': 'Eastern Mediterranean', 'Pakistan': 'Eastern Mediterranean', 'Qatar': 'Eastern Mediterranean',
            'Saudi Arabia': 'Eastern Mediterranean', 'Somalia': 'Eastern Mediterranean',
            'Sudan': 'Eastern Mediterranean', 'Syrian Arab Republic': 'Eastern Mediterranean',
            'Tunisia': 'Eastern Mediterranean', 'United Arab Emirates': 'Eastern Mediterranean', 'Yemen': 'Eastern Mediterranean',
            
            'Albania': 'Europe', 'Andorra': 'Europe', 'Armenia': 'Europe', 'Austria': 'Europe',
            'Azerbaijan': 'Europe', 'Belarus': 'Europe', 'Belgium': 'Europe', 'Bosnia and Herzegovina': 'Europe',
            'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Cyprus': 'Europe', 'Czechia': 'Europe',
            'Denmark': 'Europe', 'Estonia': 'Europe', 'Finland': 'Europe', 'France': 'Europe',
            'Georgia': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hungary': 'Europe',
            'Iceland': 'Europe', 'Ireland': 'Europe', 'Israel': 'Europe', 'Italy': 'Europe',
            'Kazakhstan': 'Europe', 'Kyrgyzstan': 'Europe', 'Latvia': 'Europe', 'Lithuania': 'Europe',
            'Luxembourg': 'Europe', 'Malta': 'Europe', 'Monaco': 'Europe', 'Montenegro': 'Europe',
            'Netherlands (Kingdom of the)': 'Europe', 'North Macedonia': 'Europe', 'Norway': 'Europe',
            'Poland': 'Europe', 'Portugal': 'Europe', 'Republic of Moldova': 'Europe', 'Romania': 'Europe',
            'Russian Federation': 'Europe', 'San Marino': 'Europe', 'Serbia': 'Europe', 'Slovakia': 'Europe',
            'Slovenia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe',
            'Tajikistan': 'Europe', 'Türkiye': 'Europe', 'Turkmenistan': 'Europe', 'Ukraine': 'Europe',
            'United Kingdom of Great Britain and Northern Ireland': 'Europe', 'Uzbekistan': 'Europe',
            
            'Bangladesh': 'South-East Asia', 'Bhutan': 'South-East Asia',
            "Democratic People's Republic of Korea": 'South-East Asia', 'India': 'South-East Asia',
            'Indonesia': 'South-East Asia', "Lao People's Democratic Republic": 'South-East Asia',
            'Maldives': 'South-East Asia', 'Myanmar': 'South-East Asia', 'Nepal': 'South-East Asia',
            'Sri Lanka': 'South-East Asia', 'Thailand': 'South-East Asia', 'Timor-Leste': 'South-East Asia',
            
            'Australia': 'Western Pacific', 'Brunei Darussalam': 'Western Pacific', 'Cambodia': 'Western Pacific',
            'China': 'Western Pacific', 'Cook Islands': 'Western Pacific', 'Fiji': 'Western Pacific',
            'Japan': 'Western Pacific', 'Kiribati': 'Western Pacific', 'Malaysia': 'Western Pacific',
            'Marshall Islands': 'Western Pacific', 'Micronesia (Federated States of)': 'Western Pacific',
            'Mongolia': 'Western Pacific', 'Nauru': 'Western Pacific', 'New Zealand': 'Western Pacific',
            'Niue': 'Western Pacific', 'Palau': 'Western Pacific', 'Papua New Guinea': 'Western Pacific',
            'Philippines': 'Western Pacific', 'Republic of Korea': 'Western Pacific', 'Samoa': 'Western Pacific',
            'Singapore': 'Western Pacific', 'Solomon Islands': 'Western Pacific', 'Tonga': 'Western Pacific',
            'Tuvalu': 'Western Pacific', 'Vanuatu': 'Western Pacific', 'Viet Nam': 'Western Pacific'
        }
        
        def get_who_region(geo_name):
            if geo_name in region_mapping:
                return region_mapping[geo_name]
            elif geo_name in ['Africa', 'Americas', 'Eastern Mediterranean', 'Europe', 'South-East Asia', 'Western Pacific']:
                return geo_name
            else:
                return 'Other'
        
        df_WHO['WHO_Region'] = df_WHO['GEO_NAME_SHORT'].apply(get_who_region)
        
        # Prepare Summary Data
        summary_df = df_WHO[['TRIPLE_BILLION', 'TRIPLE_BILLION_TRACER', 'WHO_Region', 'DIM_TIME', 'COUNT_N']]
        summary_df = summary_df.rename(columns={'DIM_TIME': 'Year'})
        summary_df['COUNT_N_Millions'] = summary_df['COUNT_N'] / 1_000_000
        
        return summary_df
        
    except FileNotFoundError:
        st.error("❌ Could not find RELAY_3B_DATA.csv file. Please ensure the file is in the correct location.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

def create_enhanced_pie_chart(region_sum, billion_types):
    """Create an enhanced pie chart with better styling"""
    fig = px.pie(
        region_sum, 
        values='COUNT_N_Millions', 
        names='WHO_Region',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value:.1f}M<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title=f"Regional Distribution for {', '.join(billion_types)}",
        title_x=0.5,
        font=dict(size=12),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    return fig

def create_enhanced_line_chart(yearly_impact, billion_types):
    """Create an enhanced line chart with better styling"""
    fig = px.line(
        yearly_impact, 
        x='Year', 
        y='COUNT_N_Millions', 
        color='WHO_Region',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Count: %{y:.1f}M<extra></extra>'
    )
    
    fig.update_layout(
        title=f"Yearly Trends for {', '.join(billion_types)} by Region",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Count (Millions)",
        hovermode='x unified',
        font=dict(size=12),
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    )
    
    return fig

def create_summary_metrics(filtered_df):
    """Create summary metrics cards"""
    total_count = filtered_df['COUNT_N_Millions'].sum()
    total_years = filtered_df['Year'].nunique()
    total_regions = filtered_df['WHO_Region'].nunique()
    avg_per_year = total_count / total_years if total_years > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Count", f"{total_count:.1f}M")
    with col2:
        st.metric("Years Covered", str(total_years))
    with col3:
        st.metric("Regions", str(total_regions))
    with col4:
        st.metric("Avg per Year", f"{avg_per_year:.1f}M")

# Main App
def main():
    # Header
    st.title("🌍 WHO Triple Billion Dashboard")
    st.markdown("*Analyzing global health impact across WHO regions*")
    
    # Load data
    summary_df = load_and_process_data()
    
    if summary_df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # TRIPLE_BILLION selection
    billion_options = summary_df['TRIPLE_BILLION'].unique()
    billion_types = st.sidebar.multiselect(
        "Select TRIPLE BILLION(s)", 
        billion_options, 
        default=billion_options,
        help="Choose which Triple Billion categories to analyze"
    )
    
    if not billion_types:
        st.warning("⚠️ Please select at least one TRIPLE BILLION category.")
        st.stop()
    
    # TRACER selection (filtered based on BILLION selection)
    tracer_options = summary_df[summary_df['TRIPLE_BILLION'].isin(billion_types)]['TRIPLE_BILLION_TRACER'].unique()
    tracer_types = st.sidebar.multiselect(
        "Select TRIPLE BILLION TRACER(s)", 
        tracer_options, 
        default=tracer_options,
        help="Choose specific tracers within the selected categories"
    )
    
    if not tracer_types:
        st.warning("⚠️ Please select at least one TRIPLE BILLION TRACER.")
        st.stop()
    
    # Year range filter
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(summary_df['Year'].min()),
        max_value=int(summary_df['Year'].max()),
        value=(int(summary_df['Year'].min()), int(summary_df['Year'].max())),
        help="Filter data by year range"
    )
    
    # Filter data
    filtered_df = summary_df[
        (summary_df['TRIPLE_BILLION'].isin(billion_types)) &
        (summary_df['TRIPLE_BILLION_TRACER'].isin(tracer_types)) &
        (summary_df['Year'] >= year_range[0]) &
        (summary_df['Year'] <= year_range[1])
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        st.stop()
    
    # Summary metrics
    st.subheader("📈 Key Metrics")
    create_summary_metrics(filtered_df)
    
    # Charts
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie Chart
        region_sum = filtered_df.groupby('WHO_Region').agg({'COUNT_N_Millions': 'sum'}).reset_index()
        fig_pie = create_enhanced_pie_chart(region_sum, billion_types)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Line Chart
        yearly_impact = filtered_df.groupby(['Year', 'WHO_Region']).agg({'COUNT_N_Millions': 'sum'}).reset_index()
        fig_line = create_enhanced_line_chart(yearly_impact, billion_types)
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Additional Analysis
    st.subheader("🔍 Detailed Analysis")
    
    # Top performing regions
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 5 Regions by Total Count**")
        top_regions = region_sum.nlargest(5, 'COUNT_N_Millions')
        st.dataframe(top_regions.round(2), hide_index=True)
    
    with col2:
        st.write("**Year-over-Year Growth**")
        # Calculate growth rates
        yearly_total = yearly_impact.groupby('Year')['COUNT_N_Millions'].sum().reset_index()
        yearly_total['Growth_Rate'] = yearly_total['COUNT_N_Millions'].pct_change() * 100
        recent_growth = yearly_total.tail(3)[['Year', 'Growth_Rate']].round(2)
        st.dataframe(recent_growth, hide_index=True)
    
    # Raw data section
    with st.expander("📋 View Raw Data"):
        st.dataframe(filtered_df.round(2))
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name=f"who_triple_billion_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()