import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(session_history):
    if not session_history:
        st.info("No sessions yet.")
        return

    df = pd.DataFrame(session_history)
    st.subheader("Patient Progress")

    # Line chart for mood over time
    if 'mood' in df.columns:
        fig_line = px.line(df, x='date', y='mood', title='Mood Progress Over Time')
        st.plotly_chart(fig_line)

    # Bar chart for risk levels
    if 'risk_level' in df.columns:
        risk_df = df['risk_level'].value_counts().reset_index()
        risk_df.columns = ['risk_level', 'count']

        fig_bar = px.bar(
            risk_df,
            x='risk_level',
            y='count',
            title='Risk Level Distribution'
        )
        st.plotly_chart(fig_bar)

    # Pie chart for session types
    if 'session_type' in df.columns:
        fig_pie = px.pie(df, names='session_type', title='Session Types')
        st.plotly_chart(fig_pie)
