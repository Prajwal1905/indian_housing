import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="India Housing Price Dashboard", layout="wide")
st.title("🏠 Indian Metropolitan Housing Price Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_housing_data.csv")

    
    yes_no_cols = [col for col in df.columns if df[col].dropna().isin(['Yes', 'No']).all()]
    for col in yes_no_cols:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    
    amenities = [
        "SwimmingPool", "LandscapedGardens", "JoggingTrack", "RainWaterHarvesting",
        "Gymnasium", "Intercom", "LiftAvailable", "24x7Security", "CarParking"
    ]
    for col in amenities:
        if col in df.columns:
            df[col] = df[col].replace(9, pd.NA)
            df[col] = df[col].fillna(0).astype(int)

    df['PricePerSqft'] = df['Price'] / df['Area']
    return df

df = load_data()


cities = df["City"].unique().tolist()
selected_cities = st.sidebar.multiselect("Select Cities", cities, default=cities)
filtered_df = df[df["City"].isin(selected_cities)]


st.markdown("### 📊 Market Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Listings", f"{len(filtered_df):,}")
col2.metric("Avg Price (INR)", f"₹{int(filtered_df['Price'].mean()):,}")
col3.metric("Avg Area (sqft)", f"{int(filtered_df['Area'].mean()):,} sqft")


st.markdown("### 🏙️ Average Price by City")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(data=filtered_df, x="City", y="Price", estimator="mean", palette="viridis", ax=ax1)
ax1.set_title("Average Property Price by City")
ax1.set_ylabel("Price (INR)")
ax1.set_xlabel("")
st.pyplot(fig1)


st.markdown("### Price Distribution (Log Scale)")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.histplot(data=filtered_df, x='Price', hue='City', bins=50, log_scale=True, element='step', ax=ax2)
ax2.set_title("Log-scaled Price Distribution")
st.pyplot(fig2)


st.markdown("### Feature Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include='number')
corr = numeric_df.corr()
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, cmap='coolwarm', linewidths=0.5, annot=True, fmt=".2f", ax=ax3)
st.pyplot(fig3)



st.markdown("### Bedrooms vs Average Price")
if 'No. of Bedrooms' in filtered_df.columns:
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    sns.barplot(data=filtered_df, x="No. of Bedrooms", y="Price", estimator="mean", palette="coolwarm", ax=ax5)
    ax5.set_title("Avg Price by Number of Bedrooms")
    ax5.set_ylabel("Avg Price (INR)")
    st.pyplot(fig5)


st.markdown("### Area vs Price Scatter")
fig6, ax6 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_df, x="Area", y="Price", hue="City", alpha=0.6, ax=ax6)
ax6.set_title("Area vs Price")
ax6.set_xlabel("Area (sqft)")
ax6.set_ylabel("Price (INR)")
st.pyplot(fig6)


st.markdown("### Property Listings by City")
city_counts = filtered_df['City'].value_counts().reset_index()
city_counts.columns = ['City', 'Count']
fig7, ax7 = plt.subplots(figsize=(8, 4))
sns.barplot(data=city_counts, x="City", y="Count", palette="pastel", ax=ax7)
ax7.set_title("Number of Listings by City")
st.pyplot(fig7)

st.markdown("---")
st.caption(" Built by Prajwal • Data: Indian Housing Prices")
