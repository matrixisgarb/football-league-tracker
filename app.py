import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='English Football League Tracker', layout='wide')
st.title('⚽ English Football League Tracker')

# Load data
@st.cache_data
def load_data():
    standings = pd.read_csv('standings.csv')
    return standings[['season', 'tier', 'team_name', 'division']].drop_duplicates()

df = load_data()

# Sidebar
st.sidebar.header('Filter')

# Club search
all_clubs = sorted(df['team_name'].unique().tolist())
selected_clubs = st.sidebar.multiselect('Select Clubs', all_clubs,
                                         default=list(all_clubs))

min_season = int(df['season'].min())
max_season = int(df['season'].max())
season_range = st.sidebar.slider('Season Range', min_season, max_season,
                                  (min_season, max_season))

# Filter data
filtered = df[
    (df['team_name'].isin(selected_clubs)) &
    (df['season'] >= season_range[0]) &
    (df['season'] <= season_range[1])
]
tier_labels = {1: 'Top Flight', 2: 'Second Tier', 3: 'Third Tier', 4: 'Fourth Tier'}
filtered['division_label'] = filtered['tier'].map(tier_labels)

# Plot
fig = px.line(filtered, x='season', y='tier', color='team_name',
              markers=True,
              labels={'season': 'Season', 'tier': 'Division', 'team_name': 'Club'},
              title='English Football League History',
              color_discrete_sequence=px.colors.qualitative.Set1)

fig.update_yaxes(autorange='reversed', tickvals=[1, 2, 3, 4],
                 ticktext=['Premier League', 'Championship', 'League One', 'League Two'])
fig.update_layout(
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#1a1a2e',
    font_color='white',
    legend_title='Club',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Stats table
st.subheader('📊 Club Summary')
if selected_clubs:
    summary = []
    for club in selected_clubs:
        club_df = df[df['team_name'] == club]
        summary.append({
            'Club': club,
            'First Season': int(club_df['season'].min()),
            'Seasons in Top Flight': len(club_df[club_df['tier'] == 1]),
            'Seasons in Data': len(club_df)
        })
    st.dataframe(pd.DataFrame(summary), hide_index=True, use_container_width=True)
    