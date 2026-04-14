import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Book Store Analytics", layout="wide", page_icon="📚")

@st.cache_data
def load_data(dataset_name):
    try:
        daily_revenue = pd.read_csv(f'daily_revenue_{dataset_name}.csv')
        top_5 = pd.read_csv(f'top_5_revenue_{dataset_name}.csv')
        daily_revenue['date'] = pd.to_datetime(daily_revenue['date']).dt.strftime('%Y-%m-%d')
        top_5['date'] = pd.to_datetime(top_5['date']).dt.strftime('%Y-%m-%d')
        
        with open(f'dashboard_metrics_{dataset_name}.json', 'r') as f:
            metrics = json.load(f)
            
        return daily_revenue, top_5, metrics
    except FileNotFoundError:
        return None, None, None

def render_dashboard(dataset_name):
    daily_revenue, top_5, metrics = load_data(dataset_name)
    
    if metrics is None:
        st.warning(f"Data for {dataset_name} not found. Please run preprocessing first.")
        return

    st.subheader("1. Top 5 Days by Revenue")
    st.dataframe(
        top_5.rename(columns={'date': 'Date', 'daily_revenue': 'Revenue (USD)'}), 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="2. Unique Users", value=f"{metrics.get('unique_users', 0):,}")

    with col2:
        st.metric(label="3. Unique Sets of Authors", value=f"{metrics.get('unique_author_sets', 0):,}")
        
    with col3:
        popular_author_raw = str(metrics.get('most_popular_author(s)', 'N/A'))
        popular_author_clean = popular_author_raw.replace("'", "").strip("()")
        st.caption("4. Most Popular Author(s)")
        st.markdown(f"##### {popular_author_clean}")
        
    with col4:
        aliases = metrics.get('best_buyer_aliases', [])
        if isinstance(aliases, str):
            aliases_display = aliases
        else:
            aliases_display = f"[{', '.join(map(str, aliases))}]"
            
        st.caption("5. Best Buyer (With Aliases)")
        st.markdown(f"##### {aliases_display}")

    st.markdown("---")
    st.subheader("6. Daily Revenue Trend")
    fig = px.bar(
        daily_revenue, 
        x='date', 
        y='daily_revenue',
        labels={'date': 'Date', 'daily_revenue': 'Total Revenue (USD)'},
        color_discrete_sequence=['#1f77b4'],
        text_auto='.2s' 
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)', 
        yaxis=(dict(showgrid=True, gridcolor='lightgray')),
        margin=dict(l=25, r=25, t=25, b=25)
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    
    st.plotly_chart(fig, use_container_width=True)


st.title("📊 Book Store Analytics Dashboard")
st.markdown("Select a dataset below to view its isolated metrics.")

tab_data1, tab_data2, tab_data3 = st.tabs(["📁 DATA1", "📁 DATA2", "📁 DATA3"])

with tab_data1:
    render_dashboard("DATA1")

with tab_data2:
    render_dashboard("DATA2")

with tab_data3:
    render_dashboard("DATA3")