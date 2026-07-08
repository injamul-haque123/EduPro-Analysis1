"""
EduPro - Learner Demographics & Course Enrollment Behavior Dashboard
Run locally with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="EduPro Learner Analytics", layout="wide", page_icon="🎓")

# ---------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------
@st.cache_data
def load_data():
    users = pd.read_csv("users.csv")
    courses = pd.read_csv("courses.csv")
    transactions = pd.read_csv("transactions.csv")
    transactions["TransactionDate"] = pd.to_datetime(transactions["TransactionDate"])

    bins = [0, 17, 25, 35, 45, 200]
    labels = ["<18", "18-25", "26-35", "36-45", "45+"]
    users["AgeGroup"] = pd.cut(users["Age"], bins=bins, labels=labels)

    df = (transactions
          .merge(users, on="UserID", how="left")
          .merge(courses, on="CourseID", how="left"))
    return users, courses, transactions, df, labels


users, courses, transactions, df, age_labels = load_data()

# ---------------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------------
st.sidebar.title("🎓 EduPro Filters")

age_filter = st.sidebar.multiselect(
    "Age Group", options=age_labels, default=age_labels
)
gender_filter = st.sidebar.multiselect(
    "Gender", options=sorted(users["Gender"].unique()), default=sorted(users["Gender"].unique())
)
category_filter = st.sidebar.multiselect(
    "Course Category", options=sorted(courses["CourseCategory"].unique()),
    default=sorted(courses["CourseCategory"].unique())
)
level_filter = st.sidebar.multiselect(
    "Course Level", options=sorted(courses["CourseLevel"].unique()),
    default=sorted(courses["CourseLevel"].unique())
)

filtered = df[
    df["AgeGroup"].isin(age_filter)
    & df["Gender"].isin(gender_filter)
    & df["CourseCategory"].isin(category_filter)
    & df["CourseLevel"].isin(level_filter)
]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing {len(filtered):,} of {len(df):,} enrollments")

# ---------------------------------------------------------------------
# HEADER + KPI ROW
# ---------------------------------------------------------------------
st.title("EduPro: Learner Demographics & Enrollment Behavior")
st.caption("Descriptive learner intelligence dashboard — not prediction or monetization.")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Enrollments", f"{len(filtered):,}")
k2.metric("Unique Learners", f"{filtered['UserID'].nunique():,}")
k3.metric("Courses Offered", f"{courses['CourseID'].nunique():,}")
avg_per_learner = (filtered.groupby("UserID").size().mean()
                    if filtered["UserID"].nunique() > 0 else 0)
k4.metric("Avg Enrollments / Learner", f"{avg_per_learner:.2f}")
top_cat = (filtered["CourseCategory"].value_counts().idxmax()
           if len(filtered) > 0 else "—")
k5.metric("Top Category", top_cat)

st.markdown("---")

# ---------------------------------------------------------------------
# TABS FOR CORE MODULES
# ---------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Learner Demographics",
    "📈 Age-wise Enrollment",
    "⚧ Gender-based Preferences",
    "📚 Category Popularity"
])

# --- TAB 1: Learner Demographic Overview -----------------------------
with tab1:
    st.subheader("Learner Demographic Overview")

    c1, c2 = st.columns(2)
    with c1:
        filtered_users = users[
            users["AgeGroup"].isin(age_filter) & users["Gender"].isin(gender_filter)
        ]
        fig = px.histogram(
            filtered_users, x="Age", nbins=20, marginal="box",
            title="Age Distribution of Learners", color_discrete_sequence=["#4C72B0"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        gender_counts = filtered_users["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig = px.pie(
            gender_counts, names="Gender", values="Count",
            title="Gender Distribution", hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Participation by demographic group (unique learners with at least one enrollment)**")
    active_users = filtered["UserID"].unique()
    participation = users[users["UserID"].isin(active_users)]
    part_table = pd.crosstab(participation["AgeGroup"], participation["Gender"])
    st.dataframe(part_table, use_container_width=True)

# --- TAB 2: Age-wise Enrollment ---------------------------------------
with tab2:
    st.subheader("Age-wise Enrollment Charts")

    age_enroll = filtered["AgeGroup"].value_counts().reindex(age_labels).reset_index()
    age_enroll.columns = ["AgeGroup", "Enrollments"]
    fig = px.bar(
        age_enroll, x="AgeGroup", y="Enrollments",
        title="Enrollments by Age Group", color="Enrollments", color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Age Group vs Course Category (heatmap)**")
    pivot = pd.crosstab(filtered["AgeGroup"], filtered["CourseCategory"])
    fig2 = px.imshow(
        pivot, text_auto=True, aspect="auto", color_continuous_scale="YlGnBu",
        title="Age Group vs Course Category — Enrollment Counts"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Age Group vs Course Level**")
    pivot2 = pd.crosstab(filtered["AgeGroup"], filtered["CourseLevel"], normalize="index") * 100
    fig3 = px.bar(
        pivot2.reset_index().melt(id_vars="AgeGroup", var_name="CourseLevel", value_name="Percent"),
        x="AgeGroup", y="Percent", color="CourseLevel", barmode="stack",
        title="Course Level Mix within Each Age Group (%)"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: Gender-based Course Preference ----------------------------
with tab3:
    st.subheader("Gender-based Course Preference Analysis")

    c1, c2 = st.columns(2)
    with c1:
        gender_cat = pd.crosstab(filtered["Gender"], filtered["CourseCategory"])
        fig = px.imshow(
            gender_cat, text_auto=True, aspect="auto", color_continuous_scale="Purples",
            title="Gender vs Course Category"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        gender_level = pd.crosstab(filtered["Gender"], filtered["CourseLevel"], normalize="index") * 100
        fig = px.bar(
            gender_level.reset_index().melt(id_vars="Gender", var_name="CourseLevel", value_name="Percent"),
            x="Gender", y="Percent", color="CourseLevel", barmode="stack",
            title="Course Level Preference by Gender (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    gender_type = pd.crosstab(filtered["Gender"], filtered["CourseType"], normalize="index") * 100
    st.markdown("**Course Type Preference by Gender (%)**")
    st.dataframe(gender_type.round(1), use_container_width=True)

# --- TAB 4: Course Category Popularity ---------------------------------
with tab4:
    st.subheader("Course Category Popularity")

    cat_counts = filtered["CourseCategory"].value_counts().reset_index()
    cat_counts.columns = ["CourseCategory", "Enrollments"]
    fig = px.bar(
        cat_counts.sort_values("Enrollments", ascending=True),
        x="Enrollments", y="CourseCategory", orientation="h",
        title="Category Popularity Index (Enrollments)", color="Enrollments",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        type_counts = filtered["CourseType"].value_counts().reset_index()
        type_counts.columns = ["CourseType", "Enrollments"]
        fig = px.pie(type_counts, names="CourseType", values="Enrollments", title="Enrollments by Course Type")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        level_counts = filtered["CourseLevel"].value_counts().reset_index()
        level_counts.columns = ["CourseLevel", "Enrollments"]
        fig = px.pie(level_counts, names="CourseLevel", values="Enrollments", title="Level Preference Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------
# BEHAVIORAL INSIGHTS FOOTER
# ---------------------------------------------------------------------
st.markdown("---")
st.subheader("📌 Behavioral Insights (based on current filters)")

if len(filtered) > 0:
    enroll_per_user = filtered.groupby("UserID").size()
    top10_share = (
        enroll_per_user.sort_values(ascending=False)
        .head(max(1, int(len(enroll_per_user) * 0.10)))
        .sum() / enroll_per_user.sum() * 100
    )
    st.markdown(
        f"""
- **Average courses per learner:** {enroll_per_user.mean():.2f}
- **Enrollment concentration:** the top 10% most active learners in this segment drive **{top10_share:.1f}%** of enrollments
- **Most popular category:** {filtered['CourseCategory'].value_counts().idxmax()}
- **Most common course level:** {filtered['CourseLevel'].value_counts().idxmax()}
        """
    )
else:
    st.info("No enrollments match the current filter selection.")

st.caption("EduPro Learner Intelligence Dashboard · Data is descriptive only, no PII beyond UserName is used.")
