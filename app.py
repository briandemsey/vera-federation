"""
VERA Federation: Cross-Jurisdiction Comparison Engine
Compare Type 4 oral-written deltas, achievement gaps, and EL outcomes
across all 55 H-EDU jurisdictions worldwide.

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_HEDU_BLACK = "#000000"
HEDU_BLACK = "#000000"
HEDU_GOLD = "#FFD700"
HEDU_BLUE = "#002B5C"
HEDU_RED = "#CC0000"

# ============================================================================
# UNIFIED JURISDICTION REGISTRY — All 55 Jurisdictions
# ============================================================================

def load_jurisdictions():
    """
    Unified schema for all H-EDU jurisdictions.
    Each row: jurisdiction, country, region, el_assessment, academic_test,
    districts, total_students, el_count, el_pct, avg_speaking, avg_writing,
    avg_delta, type4_pct, ela_proficiency_all, ela_proficiency_el,
    ela_gap, equity_hook, app_url
    """
    data = [
        # US States — sorted alphabetically
        ("Alabama", "US", "Southeast", "WIDA ACCESS", "ACAP", 141, 740000, 29600, 4.0, 365, 318, 47, 12.8, 42.0, 18.5, 23.5, "Albertville 56% EL, RAISE Act $158M", "vera-al"),
        ("Arizona", "US", "West", "AZELLA", "AASA", 230, 1150000, 100000, 8.7, 372, 325, 47, 13.1, 45.0, 19.2, 25.8, "HB 2170 Say Dyslexia, 100K+ ESA", "vera-az"),
        ("Arkansas", "US", "South", "ELPA21", "ATLAS", 235, 490000, 42000, 8.6, 360, 315, 45, 12.2, 40.0, 16.8, 23.2, "Marshallese diaspora (Springdale)", "vera-ar"),
        ("California", "US", "West", "ELPAC", "CAASPP", 1000, 5900000, 1100000, 18.6, 378, 330, 48, 14.5, 51.0, 22.0, 29.0, "SB 1288 AI compliance, LCAP", "vera-ca"),
        ("Colorado", "US", "West", "WIDA ACCESS", "CMAS", 178, 900000, 130000, 14.4, 370, 322, 48, 13.8, 47.0, 20.5, 26.5, "SPF integration", "vera-co"),
        ("Connecticut", "US", "Northeast", "WIDA ACCESS", "SBAC", 169, 508000, 57000, 11.3, 368, 320, 48, 14.2, 56.0, 18.0, 38.0, "Largest EL gap nationally (54%)", "vera-ct"),
        ("Delaware", "US", "Mid-Atlantic", "WIDA ACCESS", "DeSSA", 19, 140000, 18800, 13.4, 362, 316, 46, 12.5, 44.0, 19.0, 25.0, "District merger debate, 135% MLL growth", "vera-de"),
        ("District of Columbia", "US", "Mid-Atlantic", "WIDA ACCESS", "DC CAPE", 67, 95000, 12500, 13.2, 358, 310, 48, 14.0, 38.0, 14.5, 23.5, "DCPS/charter EL divide", "vera-dc"),
        ("Florida", "US", "Southeast", "WIDA ACCESS", "FAST", 67, 2900000, 360000, 12.4, 375, 328, 47, 13.2, 54.0, 23.0, 31.0, "HB 1255 literacy, largest EL count", "vera-fl"),
        ("Georgia", "US", "Southeast", "WIDA ACCESS", "Milestones", 180, 1800000, 120000, 6.7, 366, 320, 46, 12.6, 43.0, 18.0, 25.0, "CCRPI integration", "vera-ga"),
        ("Hawaii", "US", "Pacific", "WIDA ACCESS", "SBA", 1, 180000, 12600, 7.0, 360, 312, 48, 13.5, 46.0, 22.0, 24.0, "Policy 105-14, Pacific Islander ELs", "vera-hi"),
        ("Idaho", "US", "Mountain", "WIDA ACCESS", "ISAT", 188, 320000, 17000, 5.3, 358, 312, 46, 12.4, 48.0, 18.5, 29.5, "Rural EL teacher shortage 4x", "vera-id"),
        ("Illinois", "US", "Midwest", "WIDA ACCESS", "IAR", 852, 1900000, 333000, 17.5, 374, 326, 48, 14.2, 52.4, 20.1, 32.3, "SB 1920 AI mandate, 38-pt gap", "vera-il"),
        ("Indiana", "US", "Midwest", "WIDA ACCESS", "GPS", 290, 1100000, 85000, 7.7, 362, 318, 44, 11.8, 44.0, 17.0, 27.0, "GPS Year Zero", "vera-in"),
        ("Iowa", "US", "Midwest", "ELPA21", "Iowa Statewide", 327, 510000, 40000, 7.8, 360, 316, 44, 11.5, 50.0, 20.0, 30.0, "SF 72 dyslexia, Students First ESA", "vera-ia"),
        ("Kansas", "US", "Midwest", "KELPA", "KAP", 286, 470000, 42000, 8.9, 364, 316, 48, 14.0, 44.0, 16.0, 28.0, "Golden Triangle 50% EL, Gannon", "vera-ks"),
        ("Kentucky", "US", "Southeast", "WIDA ACCESS", "KSA", 171, 650000, 21000, 3.2, 358, 314, 44, 11.6, 46.0, 18.0, 28.0, "JCPS 21K MLs, United We Learn", "vera-ky"),
        ("Louisiana", "US", "South", "ELPT", "LEAP 2025", 69, 710000, 35000, 4.9, 356, 308, 48, 13.8, 35.0, 12.0, 23.0, "Grow.Achieve.Thrive, GATOR ESA", "vera-la"),
        ("Maine", "US", "Northeast", "WIDA ACCESS", "MAST", 192, 172000, 8000, 4.7, 362, 318, 44, 11.8, 65.1, 28.0, 37.1, "Portland/Lewiston 25% EL, refugees", "vera-me"),
        ("Maryland", "US", "Mid-Atlantic", "WIDA ACCESS", "MCAP", 24, 900000, 112000, 12.4, 370, 322, 48, 13.9, 50.8, 18.0, 32.8, "Blueprint $3.8B, PG+Mont 52%", "vera-md"),
        ("Massachusetts", "US", "Northeast", "WIDA ACCESS", "MCAS", 400, 900000, 90000, 10.0, 372, 326, 46, 12.8, 55.0, 22.0, 33.0, "MCAS grad req repealed, LOOK Act", "vera-ma"),
        ("Michigan", "US", "Midwest", "WIDA ACCESS", "M-STEP", 537, 1500000, 100000, 6.7, 366, 318, 48, 14.0, 45.0, 16.0, 29.0, "Dearborn 47%, Hamtramck 66% EL", "vera-mi"),
        ("Minnesota", "US", "Midwest", "WIDA ACCESS", "MCA", 327, 870000, 91000, 10.5, 370, 320, 50, 14.8, 49.5, 18.0, 31.5, "Largest gaps nationally, READ Act", "vera-mn"),
        ("Mississippi", "US", "Southeast", "WIDA ACCESS", "MAAP", 148, 440000, 13000, 3.0, 354, 310, 44, 11.5, 47.4, 16.0, 31.4, "Mississippi Miracle, poultry belt", "vera-ms"),
        ("Missouri", "US", "Midwest", "WIDA ACCESS", "MAP", 554, 880000, 40000, 4.5, 360, 314, 46, 12.5, 42.0, 15.0, 27.0, "Only 25% districts have EL teacher", "vera-mo"),
        ("Montana", "US", "Mountain", "WIDA ACCESS", "MAST", 400, 149000, 3500, 2.3, 356, 312, 44, 11.2, 50.0, 20.0, 30.0, "IEFA constitutional mandate", "vera-mt"),
        ("Nebraska", "US", "Midwest", "ELPA21", "NSCAS", 245, 330000, 33000, 10.0, 364, 316, 48, 13.8, 52.0, 20.0, 32.0, "Lexington 42% EL, meatpacking", "vera-ne"),
        ("Nevada", "US", "West", "WIDA ACCESS", "SBAC", 17, 490000, 70000, 14.3, 370, 320, 50, 14.5, 44.0, 18.0, 26.0, "Clark County, NSPF", "vera-nv"),
        ("New Hampshire", "US", "Northeast", "WIDA ACCESS", "NH SAS", 160, 170000, 5000, 2.9, 362, 318, 44, 11.4, 58.0, 24.0, 34.0, "Fastest EL growth New England", "vera-nh"),
        ("New Jersey", "US", "Mid-Atlantic", "WIDA ACCESS", "NJSLA", 600, 1400000, 90000, 6.4, 372, 326, 46, 12.8, 52.0, 20.0, 32.0, "ESSA infrastructure", "vera-nj"),
        ("New Mexico", "US", "Mountain", "WIDA ACCESS", "NM-MSSA", 153, 312000, 56000, 17.9, 358, 308, 50, 15.0, 35.0, 12.0, 23.0, "Yazzie/Martinez, top 5 EL state", "vera-nm"),
        ("New York", "US", "Mid-Atlantic", "NYSESLAT", "NYSTP", 700, 2500000, 250000, 10.0, 374, 328, 46, 13.0, 48.0, 18.0, 30.0, "Reimagine Phase", "vera-ny"),
        ("North Carolina", "US", "Southeast", "WIDA ACCESS", "EOG/EOC", 115, 1550000, 163000, 10.5, 368, 320, 48, 13.8, 55.0, 20.0, 35.0, "EXIT threshold lowered to 4.5", "vera-nc"),
        ("North Dakota", "US", "Plains", "WIDA ACCESS", "ND A+", 168, 115000, 4100, 3.6, 356, 312, 44, 11.3, 52.0, 22.0, 30.0, "Fargo Somali/Nepali refugees", "vera-nd"),
        ("Ohio", "US", "Midwest", "OELPA", "OST", 607, 1650000, 80000, 4.8, 364, 316, 48, 13.6, 60.4, 22.0, 38.4, "HB 96 AI mandate", "vera-oh"),
        ("Oklahoma", "US", "South", "WIDA ACCESS", "OSTP", 509, 700000, 68000, 9.7, 366, 318, 48, 13.8, 40.0, 14.0, 26.0, "Honesty gap, OKC 35% EL", "vera-ok"),
        ("Oregon", "US", "West", "ELPA", "OSAS", 197, 580000, 70000, 12.1, 368, 320, 48, 13.5, 46.0, 18.0, 28.0, "OSAS integration", "vera-or"),
        ("Pennsylvania", "US", "Mid-Atlantic", "WIDA ACCESS", "PSSA", 500, 1700000, 100000, 5.9, 370, 322, 48, 13.8, 49.9, 16.0, 33.9, "50th Hispanic-white gap", "vera-pa"),
        ("Rhode Island", "US", "Northeast", "WIDA ACCESS", "RICAS", 66, 140000, 15000, 10.7, 364, 316, 48, 13.5, 45.0, 16.0, 29.0, "Providence 33% MLL, state takeover", "vera-ri"),
        ("South Carolina", "US", "Southeast", "WIDA ACCESS", "SC READY", 79, 780000, 55000, 7.1, 366, 318, 48, 13.4, 48.0, 18.0, 30.0, "800% EL growth, fastest in SE", "vera-sc"),
        ("South Dakota", "US", "Plains", "WIDA ACCESS", "SPI", 150, 135000, 5000, 3.7, 360, 314, 46, 12.5, 52.0, 18.0, 34.0, "36-pt Native-White gap, H-EDU HQ", "vera-sd"),
        ("Tennessee", "US", "Southeast", "WIDA ACCESS", "TNReady", 140, 1000000, 50000, 5.0, 362, 316, 46, 12.4, 40.0, 14.0, 26.0, "ASD shutdown, 3-tier intervention", "vera-tn"),
        ("Texas", "US", "South", "TELPAS", "STAAR", 1200, 5400000, 1050000, 19.4, 376, 328, 48, 14.2, 48.0, 20.0, 28.0, "A-F accountability", "vera-tx"),
        ("Utah", "US", "Mountain", "WIDA ACCESS", "RISE", 41, 690000, 54000, 7.8, 364, 316, 48, 13.4, 48.0, 18.0, 30.0, "Fastest EL growth in US, Fits All", "vera-ut"),
        ("Vermont", "US", "Northeast", "WIDA ACCESS", "VTCAP", 119, 82000, 2500, 3.0, 358, 314, 44, 11.2, 52.0, 22.0, 30.0, "Winooski 33%, Act 46 consolidation", "vera-vt"),
        ("Virginia", "US", "Mid-Atlantic", "WIDA ACCESS", "SOL", 131, 1300000, 145000, 11.2, 372, 324, 48, 13.8, 74.0, 32.0, 42.0, "6th worst EL graduation rate", "vera-va"),
        ("Washington", "US", "West", "WIDA ACCESS", "SBAC", 295, 1150000, 130000, 11.3, 370, 322, 48, 13.6, 50.0, 20.0, 30.0, "SBE Phase II", "vera-wa"),
        ("West Virginia", "US", "Southeast", "ELPA21", "WVGSA", 55, 250000, 2000, 0.8, 352, 310, 42, 10.5, 44.0, 18.0, 26.0, "Lowest EL % nationally (0.8%)", "vera-wv"),
        ("Wisconsin", "US", "Midwest", "WIDA ACCESS", "Forward", 421, 860000, 55000, 6.4, 368, 318, 50, 14.8, 50.0, 16.0, 34.0, "WIDA HQ, worst B-W NAEP gap", "vera-wi"),
        ("Wyoming", "US", "Mountain", "WIDA ACCESS", "WY-TOPP", 48, 94500, 3500, 3.7, 356, 312, 44, 11.2, 50.0, 20.0, 30.0, "Energy boom/bust EL instability", "vera-wy"),
        # International
        ("New South Wales", "Australia", "Pacific", "LBOTE/EAL/D", "NAPLAN", 2200, 800000, 120000, 15.0, 370, 325, 45, 12.0, 55.0, 28.0, 27.0, "FOEI/ICSEA equity risk", "vera-nsw"),
        ("New Zealand", "New Zealand", "Pacific", "EQI/NCEA", "NCEA", 2500, 800000, 40000, 5.0, 365, 322, 43, 11.5, 58.0, 30.0, 28.0, "Ako principle, global model", "vera-nz"),
        ("Ontario", "Canada", "North America", "STEP", "EQAO", 72, 2100000, 250000, 11.9, 368, 318, 50, 14.5, 52.0, 22.0, 30.0, "Toronto 50K ELs, 100+ languages", "vera-on"),
        ("Netherlands", "Netherlands", "Europe", "NT2", "Doorstroomtoets", 150, 2600000, 30000, 1.2, 362, 318, 44, 11.8, 65.0, 32.0, 33.0, "ISK newcomers, DUO open data", "vera-nl"),
        ("Tokyo", "Japan", "Asia", "DLA", "National Test", 23, 950000, 6300, 0.7, 360, 310, 50, 15.2, 70.0, 35.0, 35.0, "ESAT-J, Shinjuku 12.4% foreign", "vera-tokyo"),
    ]

    columns = [
        'jurisdiction', 'country', 'region', 'el_assessment', 'academic_test',
        'districts', 'total_students', 'el_count', 'el_pct',
        'avg_speaking', 'avg_writing', 'avg_delta', 'type4_pct',
        'ela_proficiency_all', 'ela_proficiency_el', 'ela_gap',
        'equity_hook', 'app_slug'
    ]

    return pd.DataFrame(data, columns=columns)


# ============================================================================
# AUTHENTICATION
# ============================================================================


# ============================================================================
# PAGES
# ============================================================================

def render_global_overview(df):
    st.header("Global Overview")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Jurisdictions", len(df))
    with col2: st.metric("Countries", df['country'].nunique())
    with col3: st.metric("Total Students", f"{df['total_students'].sum():,.0f}")
    with col4: st.metric("English Learners", f"{df['el_count'].sum():,.0f}")
    with col5: st.metric("Avg Type 4 Rate", f"{df['type4_pct'].mean():.1f}%")

    st.divider()

    # EL population by jurisdiction
    st.subheader("English Learner Population by Jurisdiction")
    top20 = df.nlargest(20, 'el_count')
    fig = px.bar(top20.sort_values('el_count', ascending=True),
                 x='el_count', y='jurisdiction', orientation='h',
                 color='country', color_discrete_sequence=['#002B5C', '#006B3F', '#CC0000', '#FF6600', '#6B3FA0'],
                 labels={'el_count': 'English Learners', 'jurisdiction': '', 'country': 'Country'})
    fig.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

    # Map by region
    st.subheader("Jurisdictions by Region")
    region_summary = df.groupby('region').agg(
        jurisdictions=('jurisdiction', 'count'),
        total_el=('el_count', 'sum'),
        avg_delta=('avg_delta', 'mean'),
        avg_type4=('type4_pct', 'mean')
    ).reset_index().sort_values('total_el', ascending=False)
    st.dataframe(region_summary, use_container_width=True, hide_index=True)

    # Full table
    st.subheader("All Jurisdictions")
    display = df[['jurisdiction', 'country', 'el_assessment', 'districts', 'el_count', 'el_pct',
                   'avg_delta', 'type4_pct', 'ela_gap', 'equity_hook']].copy()
    display.columns = ['Jurisdiction', 'Country', 'EL Test', 'Districts', 'EL Count', 'EL %',
                       'Avg Delta', 'Type 4 %', 'ELA Gap', 'Key Hook']
    st.dataframe(display, use_container_width=True, hide_index=True)


def render_compare_deltas(df):
    st.header("Compare Oral-Written Deltas")

    st.markdown("Select jurisdictions to compare their Speaking vs Writing deltas — the core Type 4 indicator.")

    selected = st.multiselect("Select Jurisdictions (up to 12)",
                               df['jurisdiction'].tolist(),
                               default=['California', 'Pennsylvania', 'Illinois', 'Ontario', 'Tokyo', 'New South Wales'],
                               max_selections=12)

    if not selected:
        st.warning("Select at least one jurisdiction.")
        return

    filtered = df[df['jurisdiction'].isin(selected)].sort_values('avg_delta', ascending=True)

    st.divider()

    # Delta comparison bar chart
    st.subheader("Oral-Written Delta Comparison")
    colors = [HEDU_RED if d >= 50 else HEDU_GOLD if d >= 46 else HEDU_BLUE for d in filtered['avg_delta']]
    fig = go.Figure(go.Bar(
        x=filtered['avg_delta'], y=filtered['jurisdiction'], orientation='h',
        marker_color=colors,
        text=[f"{d:.0f} pts" for d in filtered['avg_delta']], textposition='outside'
    ))
    fig.update_layout(title="Average Speaking - Writing Delta (Scale Score Points)",
                     xaxis_title="Delta", height=max(300, len(selected) * 45))
    st.plotly_chart(fig, use_container_width=True)

    # Speaking vs Writing scatter
    st.subheader("Speaking vs Writing Scores")
    fig2 = px.scatter(filtered, x='avg_writing', y='avg_speaking',
                      text='jurisdiction', size='el_count', color='country',
                      labels={'avg_writing': 'Avg Writing Score', 'avg_speaking': 'Avg Speaking Score',
                              'el_count': 'EL Count', 'country': 'Country'})
    fig2.add_shape(type="line", x0=300, y0=300, x1=390, y1=390,
                   line=dict(dash="dash", color="gray"))
    fig2.update_traces(textposition='top center')
    fig2.update_layout(title="Speaking vs Writing — Above the line = oral exceeds written",
                      height=500)
    st.plotly_chart(fig2, use_container_width=True)

    # Type 4 prevalence
    st.subheader("Type 4 Prevalence")
    fig3 = go.Figure(go.Bar(
        x=filtered['jurisdiction'], y=filtered['type4_pct'],
        marker_color=[HEDU_RED if t >= 14 else HEDU_GOLD if t >= 12 else HEDU_BLUE for t in filtered['type4_pct']],
        text=[f"{t:.1f}%" for t in filtered['type4_pct']], textposition='outside'
    ))
    fig3.update_layout(title="Estimated Type 4 Rate by Jurisdiction",
                      yaxis_title="% of EL Cohorts Flagged", height=400)
    st.plotly_chart(fig3, use_container_width=True)


def render_compare_gaps(df):
    st.header("Compare Achievement Gaps")

    st.markdown("Compare ELA proficiency gaps (All Students vs EL Students) across jurisdictions.")

    selected = st.multiselect("Select Jurisdictions (up to 12)",
                               df['jurisdiction'].tolist(),
                               default=['Connecticut', 'Pennsylvania', 'Minnesota', 'Wisconsin', 'Virginia', 'New Mexico'],
                               max_selections=12, key="gap_select")

    if not selected:
        st.warning("Select at least one jurisdiction.")
        return

    filtered = df[df['jurisdiction'].isin(selected)].sort_values('ela_gap', ascending=False)

    st.divider()

    # Gap comparison
    st.subheader("ELA Proficiency Gap (All Students vs EL Students)")
    fig = go.Figure()
    fig.add_trace(go.Bar(name='All Students', x=filtered['jurisdiction'],
                         y=filtered['ela_proficiency_all'], marker_color=HEDU_BLUE))
    fig.add_trace(go.Bar(name='EL Students', x=filtered['jurisdiction'],
                         y=filtered['ela_proficiency_el'], marker_color=HEDU_GOLD))
    fig.update_layout(barmode='group', title="ELA Proficiency: All vs EL",
                     yaxis_title="% Proficient", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Gap magnitude
    st.subheader("Gap Magnitude (percentage points)")
    fig2 = go.Figure(go.Bar(
        x=filtered['jurisdiction'], y=filtered['ela_gap'],
        marker_color=[HEDU_RED if g >= 35 else HEDU_GOLD if g >= 28 else HEDU_BLUE for g in filtered['ela_gap']],
        text=[f"{g:.1f} pts" for g in filtered['ela_gap']], textposition='outside'
    ))
    fig2.update_layout(title="All-EL Proficiency Gap", yaxis_title="Gap (pp)", height=400)
    st.plotly_chart(fig2, use_container_width=True)

    # Scatter: EL % vs Gap
    st.subheader("Does EL Concentration Predict the Gap?")
    fig3 = px.scatter(filtered, x='el_pct', y='ela_gap', text='jurisdiction',
                      size='el_count', color='country',
                      labels={'el_pct': 'EL % of Enrollment', 'ela_gap': 'ELA Gap (pp)'})
    fig3.update_traces(textposition='top center')
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)


def render_compare_assessments(df):
    st.header("Compare Assessment Systems")

    st.markdown("See which EL assessment each jurisdiction uses and how they compare.")

    # Assessment type distribution
    st.subheader("EL Assessment Distribution")
    assess_counts = df['el_assessment'].value_counts().reset_index()
    assess_counts.columns = ['Assessment', 'Count']
    fig = px.pie(assess_counts, values='Count', names='Assessment',
                 title="EL Assessment Types Across 55 Jurisdictions",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # By assessment type
    st.subheader("Jurisdictions by EL Assessment Type")
    for assess_type in df['el_assessment'].unique():
        subset = df[df['el_assessment'] == assess_type].sort_values('el_count', ascending=False)
        with st.expander(f"{assess_type} ({len(subset)} jurisdictions)"):
            display = subset[['jurisdiction', 'country', 'el_count', 'el_pct', 'avg_delta', 'type4_pct']].copy()
            display.columns = ['Jurisdiction', 'Country', 'EL Count', 'EL %', 'Avg Delta', 'Type 4 %']
            st.dataframe(display, use_container_width=True, hide_index=True)

    # Academic test comparison
    st.subheader("Academic Assessment Landscape")
    st.dataframe(df[['jurisdiction', 'country', 'academic_test', 'ela_proficiency_all']].rename(
        columns={'jurisdiction': 'Jurisdiction', 'country': 'Country',
                 'academic_test': 'Academic Test', 'ela_proficiency_all': 'ELA Prof %'}
    ).sort_values('ELA Prof %', ascending=False), use_container_width=True, hide_index=True)


def render_rankings(df):
    st.header("Jurisdiction Rankings")

    metric = st.selectbox("Rank by:", [
        "Largest Oral-Written Delta",
        "Highest Type 4 Rate",
        "Largest ELA Achievement Gap",
        "Highest EL Concentration",
        "Most EL Students",
        "Lowest EL Proficiency"
    ])

    st.divider()

    if metric == "Largest Oral-Written Delta":
        ranked = df.nlargest(20, 'avg_delta')
        fig = px.bar(ranked, x='jurisdiction', y='avg_delta', color='country',
                     title="Top 20: Largest Oral-Written Delta",
                     labels={'avg_delta': 'Delta (pts)', 'jurisdiction': ''})
    elif metric == "Highest Type 4 Rate":
        ranked = df.nlargest(20, 'type4_pct')
        fig = px.bar(ranked, x='jurisdiction', y='type4_pct', color='country',
                     title="Top 20: Highest Type 4 Rate",
                     labels={'type4_pct': 'Type 4 %', 'jurisdiction': ''})
    elif metric == "Largest ELA Achievement Gap":
        ranked = df.nlargest(20, 'ela_gap')
        fig = px.bar(ranked, x='jurisdiction', y='ela_gap', color='country',
                     title="Top 20: Largest All-EL Proficiency Gap",
                     labels={'ela_gap': 'Gap (pp)', 'jurisdiction': ''})
    elif metric == "Highest EL Concentration":
        ranked = df.nlargest(20, 'el_pct')
        fig = px.bar(ranked, x='jurisdiction', y='el_pct', color='country',
                     title="Top 20: Highest EL % of Enrollment",
                     labels={'el_pct': 'EL %', 'jurisdiction': ''})
    elif metric == "Most EL Students":
        ranked = df.nlargest(20, 'el_count')
        fig = px.bar(ranked, x='jurisdiction', y='el_count', color='country',
                     title="Top 20: Most EL Students",
                     labels={'el_count': 'EL Count', 'jurisdiction': ''})
    else:
        ranked = df.nsmallest(20, 'ela_proficiency_el')
        fig = px.bar(ranked, x='jurisdiction', y='ela_proficiency_el', color='country',
                     title="Bottom 20: Lowest EL Proficiency",
                     labels={'ela_proficiency_el': 'EL Prof %', 'jurisdiction': ''})

    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Full Ranking Table")
    st.dataframe(ranked[['jurisdiction', 'country', 'el_assessment', 'el_count', 'el_pct',
                          'avg_delta', 'type4_pct', 'ela_gap', 'equity_hook']],
                 use_container_width=True, hide_index=True)


def render_cross_country(df):
    st.header("Cross-Country Comparison")

    st.markdown("Compare education systems across national boundaries — the question no single jurisdiction can answer alone.")

    # Country-level aggregates
    country_agg = df.groupby('country').agg(
        jurisdictions=('jurisdiction', 'count'),
        total_students=('total_students', 'sum'),
        total_el=('el_count', 'sum'),
        avg_el_pct=('el_pct', 'mean'),
        avg_delta=('avg_delta', 'mean'),
        avg_type4=('type4_pct', 'mean'),
        avg_gap=('ela_gap', 'mean'),
        avg_ela_all=('ela_proficiency_all', 'mean'),
        avg_ela_el=('ela_proficiency_el', 'mean')
    ).reset_index().sort_values('total_el', ascending=False)

    st.subheader("National Aggregates")
    st.dataframe(country_agg.rename(columns={
        'country': 'Country', 'jurisdictions': 'Jurisdictions', 'total_students': 'Students',
        'total_el': 'ELs', 'avg_el_pct': 'Avg EL %', 'avg_delta': 'Avg Delta',
        'avg_type4': 'Avg Type 4 %', 'avg_gap': 'Avg Gap', 'avg_ela_all': 'Avg ELA All',
        'avg_ela_el': 'Avg ELA EL'
    }), use_container_width=True, hide_index=True)

    st.divider()

    # Country comparison charts
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(country_agg, x='country', y='avg_delta', color='country',
                     title="Average Oral-Written Delta by Country",
                     labels={'avg_delta': 'Avg Delta', 'country': ''})
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(country_agg, x='country', y='avg_gap', color='country',
                     title="Average ELA Gap by Country",
                     labels={'avg_gap': 'Avg Gap (pp)', 'country': ''})
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    # EL assessment diversity
    st.subheader("Assessment Diversity by Country")
    for country in df['country'].unique():
        subset = df[df['country'] == country]
        assessments = subset['el_assessment'].unique()
        st.markdown(f"**{country}** ({len(subset)} jurisdictions): {', '.join(assessments)}")


def render_export(df):
    st.header("Export Federation Data")

    st.subheader("Complete Jurisdiction Dataset")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Download Full Dataset (CSV)", df.to_csv(index=False),
                      "vera_federation_all_jurisdictions.csv", "text/csv", use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("US Only")
        us = df[df['country'] == 'US']
        st.download_button("Download US Jurisdictions (CSV)", us.to_csv(index=False),
                          "vera_federation_us.csv", "text/csv", use_container_width=True)
    with col2:
        st.subheader("International Only")
        intl = df[df['country'] != 'US']
        st.download_button("Download International (CSV)", intl.to_csv(index=False),
                          "vera_federation_international.csv", "text/csv", use_container_width=True)


# ============================================================================
# MAIN
# ============================================================================

def main():
    st.set_page_config(page_title="VERA Federation | Cross-Jurisdiction Comparison",
                       page_icon="🌐", layout="wide")

    st.markdown(f"""
    <style>
        .stApp {{ background-color: #fafafa; }}
        .block-container {{ padding-top: 2rem; }}
        h1, h2, h3 {{ color: {HEDU_BLACK}; }}
        .stButton > button {{ background-color: {HEDU_BLACK}; color: white; }}
        .stButton > button:hover {{ background-color: #333; color: white; }}
    </style>
    """, unsafe_allow_html=True)

    df = load_jurisdictions()

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <a href="https://h-edu.solutions" style="
            display: inline-block;
            color: {HEDU_BLACK};
            text-decoration: none;
            font-size: 0.85rem;
            padding: 6px 14px;
            border: 1px solid {HEDU_BLACK};
            border-radius: 4px;
            margin-bottom: 16px;
        ">&#8592; H-EDU.Solutions</a>
        <h2 style="color: {HEDU_BLACK}; margin: 0;">VERA</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Federation Engine</p>
        <p style="color: #999; font-size: 0.75rem;">55 Jurisdictions | 6 Countries</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.divider()

    page = st.sidebar.radio("Navigation", [
        "Global Overview",
        "Compare Deltas",
        "Compare Achievement Gaps",
        "Compare Assessments",
        "Rankings",
        "Cross-Country",
        "Export Data"
    ])

    st.sidebar.divider()
    st.sidebar.markdown("**Launch a Jurisdiction**")
    jurisdiction_names = df['jurisdiction'].tolist()
    selected_jx = st.sidebar.selectbox("Select Jurisdiction", jurisdiction_names, label_visibility="collapsed")
    slug = df[df['jurisdiction'] == selected_jx]['app_slug'].values[0]
    url = f"https://{slug}.onrender.com"
    st.sidebar.markdown(
        f"<a href='{url}' target='_blank'>"
        f"<button style='width:100%;background:#000;color:#fff;border:none;padding:8px;cursor:pointer;font-size:0.9rem;'>"
        f"Open {selected_jx} VERA</button></a>",
        unsafe_allow_html=True,
    )

    st.sidebar.divider()
    st.sidebar.markdown("""
    **Coverage:**
    - 50 US States + DC
    - New South Wales, Australia
    - New Zealand
    - Ontario, Canada
    - Netherlands
    - Tokyo, Japan

    **EL Assessment Types:**
    - WIDA ACCESS (37 states)
    - ELPA21 (AR, IA, NE, WV)
    - OELPA, KELPA, ELPT
    - ELPAC, AZELLA, NYSESLAT
    - TELPAS, ELPA
    - STEP, DLA, NT2, LBOTE

    ---
    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    if page == "Global Overview": render_global_overview(df)
    elif page == "Compare Deltas": render_compare_deltas(df)
    elif page == "Compare Achievement Gaps": render_compare_gaps(df)
    elif page == "Compare Assessments": render_compare_assessments(df)
    elif page == "Rankings": render_rankings(df)
    elif page == "Cross-Country": render_cross_country(df)
    elif page == "Export Data": render_export(df)


if __name__ == "__main__":
    main()
