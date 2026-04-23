# src/streamlit_app.py
"""
Streamlit Web App for the 2026 FIFA World Cup Simulator.

This app provides an interactive interface to run simulations, visualize results,
and compare different prediction engines (Default, XGBoost, LLM).
It uses 'fifa_wc_48_sorted.json' as the primary data source.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import plotly.express as px

# Add the src directory to the path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulator import WorldCupSimulator


# -----------------------------
# Helper Functions
# -----------------------------

def load_simulation_results() -> List[Dict[str, Any]]:
    """Load the latest simulation result JSON file."""
    results_dir = "."
    json_files = [f for f in os.listdir(results_dir) if f.startswith("world_cup_simulation_") and f.endswith(".json")]
    if not json_files:
        return []
    
    # Get the most recent file
    latest_file = max(json_files, key=lambda x: os.path.getmtime(x))
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['all_matches']


def create_group_stage_dataframe(matches: List[Dict]) -> pd.DataFrame:
    """Create a DataFrame for group stage matches."""
    group_matches = [m for m in matches if m['stage'] == 'Group Stage']
    df = pd.DataFrame(group_matches)
    if not df.empty:
        # Extract goals
        df[['goals_team1', 'goals_team2']] = df['score'].str.split('-', expand=True).astype(int)
        # Determine result
        df['result'] = np.where(df['goals_team1'] > df['goals_team2'], 'Win',
                       np.where(df['goals_team1'] < df['goals_team2'], 'Loss', 'Draw'))
    return df


def create_knockout_dataframe(matches: List[Dict]) -> pd.DataFrame:
    """Create a DataFrame for knockout stage matches."""
    knockout_matches = [m for m in matches if m['stage'] != 'Group Stage']
    return pd.DataFrame(knockout_matches)


def get_champion(matches: List[Dict]) -> str:
    """Extract the champion from the final match."""
    finals = [m for m in matches if m['stage'] == 'Final']
    if finals:
        return finals[0]['winner']
    return "N/A"


# -----------------------------
# Main App Logic
# -----------------------------

def main():
    st.set_page_config(
        page_title="🏆 2026 FIFA World Cup Simulator",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🏆 2026 FIFA World Cup AI Simulation Dashboard")
    st.markdown("""
    Welcome to the official simulation dashboard for the **2026 FIFA World Cup**!
    This app simulates the entire tournament based on team statistics from `fifa_wc_48_sorted.json` 
    and your choice of AI prediction engine.
    The format is **48 teams, 12 groups of 4, with 32 teams advancing** (Top 2 + 8 best 3rd-place).
    """)
    
    # --- Sidebar Controls ---
    with st.sidebar:
        st.header("⚙️ Simulation Controls")
        
        predictor_choice = st.selectbox(
            "Select Prediction Engine:",
            options=["default", "xgboost", "llm"],
            format_func=lambda x: x.upper()
        )
        
        # Hardcoded to use the specified data file in the 'data' directory
        data_file = "data/fifa_wc_48_sorted.json"
        st.text_input("Team Stats File (Fixed):", value=data_file, disabled=True)
        
        if st.button("🚀 Run New Simulation", type="primary", use_container_width=True):
            with st.spinner("Running simulation... This may take a moment."):
                try:
                    simulator = WorldCupSimulator(team_stats_file=data_file, predictor_type=predictor_choice)
                    champion = simulator.run_simulation(verbose=False)
                    st.session_state['simulation_done'] = True
                    st.session_state['champion'] = champion
                    st.success(f"Simulation complete! Champion: **{champion}**")
                except Exception as e:
                    st.error(f"Simulation failed: {e}")
        
        st.divider()
        st.subheader("ℹ️ About")
        st.info("""
        - **Default**: Simple statistical model.
        - **XGBoost**: Fast, local ML model (requires pre-trained models).
        - **LLM**: Uses OpenAI API for natural language predictions (requires API key).
        """)
    
    # --- Main Content ---
    if 'simulation_done' not in st.session_state or not st.session_state['simulation_done']:
        st.info("👈 Please configure your settings in the sidebar and click 'Run New Simulation' to begin.")
        return
    
    # Load results
    all_matches = load_simulation_results()
    if not all_matches:
        st.error("No simulation results found. Please run a new simulation.")
        return
    
    champion = st.session_state.get('champion', get_champion(all_matches))
    st.success(f"### 🏆 And the winner is... **{champion}**! 🏆")
    
    # --- Tabs for Different Views ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🥅 Group Stage", "🔥 Knockout Stage", "📈 Raw Data"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        total_matches = len(all_matches)
        group_matches = len([m for m in all_matches if m['stage'] == 'Group Stage'])
        knockout_matches = total_matches - group_matches
        
        col1.metric("Total Matches", total_matches)
        col2.metric("Group Stage Matches", group_matches)
        col3.metric("Knockout Matches", knockout_matches)
        
        st.subheader("Interactive Match Schedule")
        
        # Prepare schedule data for Plotly
        if all_matches:
            # Create a sequential match number
            schedule_data = []
            for idx, match in enumerate(all_matches):
                schedule_data.append({
                    'Match': f"Match {idx+1}",
                    'Stage': match['stage'],
                    'Team A': match['team1'],
                    'Team B': match['team2'],
                    'Score': match['score'],
                    'Winner': match['winner']
                })
            
            schedule_df = pd.DataFrame(schedule_data)
            
            # Create an interactive scatter plot with Plotly
            fig = px.scatter(
                schedule_df,
                x='Match',
                y='Stage',
                color='Stage',
                hover_data=['Team A', 'Team B', 'Score', 'Winner'], # This adds the specific match data on hover
                title="Tournament Match Schedule (Hover for Details)",
                height=600
            )
            
            # Ensure stages are ordered correctly on the Y-axis
            stage_order = ['Group Stage', 'Round of 32', 'Round of 16', 'Quarter-finals', 'Semi-finals', 'Final']
            fig.update_layout(
                yaxis={'categoryorder':'array', 'categoryarray': stage_order}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No match data to display.")
    
    with tab2:
        st.subheader("Group Stage Results")
        group_df = create_group_stage_dataframe(all_matches)
        if not group_df.empty:
            # Show a sample of matches
            st.dataframe(group_df[['group', 'team1', 'team2', 'score', 'winner']].head(15), use_container_width=True)
            
            # Goals Distribution
            st.subheader("Goals Distribution")
            goals_data = pd.concat([
                group_df[['team1', 'goals_team1']].rename(columns={'team1': 'team', 'goals_team1': 'goals'}),
                group_df[['team2', 'goals_team2']].rename(columns={'team2': 'team', 'goals_team2': 'goals'})
            ])
            top_scorers = goals_data.groupby('team')['goals'].sum().sort_values(ascending=False).head(10)
            st.bar_chart(top_scorers, color="#ff7f0e")
        else:
            st.write("No group stage data available.")
    
    with tab3:
        st.subheader("Knockout Stage Bracket")
        knockout_df = create_knockout_dataframe(all_matches)
        if not knockout_df.empty:
            # Create a simple bracket visualization using a dataframe
            bracket_data = []
            for _, row in knockout_df.iterrows():
                bracket_data.append({
                    'Round': row['stage'],
                    'Matchup': f"{row['team1']} vs {row['team2']}",
                    'Result': f"{row['score']} ({row['winner']})"
                })
            bracket_df = pd.DataFrame(bracket_data)
            st.dataframe(bracket_df, use_container_width=True)
            
            # Finalists
            finalists = set()
            for stage in ['Semi-finals', 'Final']:
                stage_matches = knockout_df[knockout_df['stage'] == stage]
                for _, m in stage_matches.iterrows():
                    finalists.add(m['team1'])
                    finalists.add(m['team2'])
            st.markdown(f"**Finalists**: {', '.join(finalists)}")
        else:
            st.write("No knockout stage data available.")
    
    with tab4:
        st.subheader("Raw Simulation Data")
        st.write("This is the complete list of all simulated matches.")
        full_df = pd.DataFrame(all_matches)
        st.dataframe(full_df, use_container_width=True)
        
        # Download button
        csv = full_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Results as CSV",
            data=csv,
            file_name=f"world_cup_2026_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()