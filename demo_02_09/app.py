import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter
from pathlib import Path


# ----helping functions
def recall_at_k(row, col_gt, col_pred, k=999):
    """
    Calculates the recall at k for a given row of ground truth and predicted values.

    :param row: A pandas series containing the ground truth and predicted values for a single instance.
    :param col_gt: The name of the column containing the ground truth values.
    :param col_pred: The name of the column containing the predicted values.
    :param k: The number of predicted values to consider. Default is 999.
    :return: The recall at k for the given row, or None if there are no ground truth values.
    """
    gt = set(row[col_gt])
    pred = set(row[col_pred][:k])
    intersection = gt.intersection(pred)
    if len(gt) > 0:
        return len(intersection) / len(gt)
    else:
        return None


def compute_recall_multiple_cols(df, col_gt, col_preds, k_list):
    """
    Calculates the recall at multiple values of k for multiple columns of predicted values.

    :param df: A pandas DataFrame containing the ground truth and predicted values.
    :param col_gt: The name of the column containing the ground truth values.
    :param col_preds: A list of column names containing the predicted values.
    :param k_list: A list of values of k to calculate recall at.
    :return: A pandas DataFrame containing the recall at each value of k for each column of predicted values.
    """

    recalls = {}
    for col_pred in col_preds:
        for k in k_list:
            col_name = f"{col_pred}_recall@{k}"
            recall = df.apply(lambda row: recall_at_k(row, col_gt, col_pred, k), axis=1)
            recalls[col_name] = recall
    return pd.DataFrame(recalls)


def compute_precision_multiple_cols(df, col_gt, col_preds, k_list):
    """
    Calculates the precision at multiple values of k for multiple columns of predicted values.

    :param df: A pandas DataFrame containing the ground truth and predicted values.
    :param col_gt: The name of the column containing the ground truth values.
    :param col_preds: A list of column names containing the predicted values.
    :param k_list: A list of values of k to calculate precision at.
    :return: A pandas DataFrame containing the precision at each value of k for each column of predicted values.
    """

    precisions = {}
    for col_pred in col_preds:
        for k in k_list:
            col_name = f"{col_pred}_precision@{k}"
            precision = df.apply(
                lambda row: precision_at_k(row, col_gt, col_pred, k), axis=1
            )
            precisions[col_name] = precision
    return pd.DataFrame(precisions)


def precision_at_k(row, col_gt, col_pred, k=999):
    """
    Calculates the precision at k for a given row of ground truth and predicted values.

    :param row: A pandas series containing the ground truth and predicted values for a single instance.
    :param col_gt: The name of the column containing the ground truth values.
    :param col_pred: The name of the column containing the predicted values.
    :param k: The number of predicted values to consider. Default is 999.
    :return: The precision at k for the given row, or None if there are no predicion values.
    """
    gt = set(row[col_gt])
    pred = set(row[col_pred][:k])
    intersection = gt.intersection(pred)
    if len(pred) > 0:
        return len(intersection) / len(pred)
    else:
        return None


def count_skills_multiple_cols(df: pd.DataFrame, cols):
    """

    :param df: A pandas DataFrame containing multiple columns with skills.
    :param cols: names of the columns to count skills on
    :return: A pandas DataFrame containing the count of skills for each row of each column in 'cols'
    """
    counts = {}
    for col in cols:
        col_name = f"{col}_count"
        count = df[col].map(lambda x: len(x))
        counts[col_name] = count
    return pd.DataFrame(counts)


# ----
ROOT = Path(__file__).parent.parent.resolve()

st.set_page_config(layout="wide")


@st.cache_data
def read_skill_df():
    df = pd.read_csv(f"{ROOT}/demo_02_09/data/2023_05_09_10_28_52_data_skills_1.csv")
    return df


@st.cache_data
def read_df_clean():
    df = pd.read_csv(f"{ROOT}/demo_02_09/data/2023_05_09_10_29_27_data_clean.csv")
    return df


df = read_skill_df()


st.title("SKILL ANALYSIS")

col1, col2 = st.columns(2)
col1.metric(
    "Total number of contents",
    df.drop_duplicates(subset=["filename", "idorg"]).shape[0],
    None,
)
col2.metric("Total number of platforms", df["url"].nunique(), None)

st.dataframe(df.head(10).reset_index(drop=True))


st.subheader("Total skills")
st.text(
    """This section shows how skill tags are used - counting each occurence of a skill tag on each course"""
)
col1, col2, col3 = st.columns(3)
col1.metric("Total number of skills", df["title"].explode().count(), None)
col2.metric(
    "Mean number of skills per content",
    df.explode("title").groupby(["filename", "idorg"])["title"].count().mean().round(1),
    None,
)
col3.metric(
    "Mean number of skills per customer",
    df.explode("title").groupby(["url"])["title"].count().mean().round(1),
    None,
)

st.text("-----------------------------------------------------")

st.subheader("Frequency skills")
top_n = st.slider("Insert number of skills:", min_value=0, value=60, max_value=500)
freq_skills_df = df["title"].explode().value_counts()
fig = px.bar(
    freq_skills_df[:top_n],
    orientation="h",
    title=f"Most frequent {top_n} skills",
)
fig.update_layout(width=800, height=600)
fig.update_xaxes(title="Total number of tags")
fig.update_yaxes(title=None)
st.plotly_chart(fig, use_container_width=True)

st.text("-----------------------------------------------------")

st.subheader("Frequency of unique skills per content/customer")
st.text(
    """
This section shows how unique skill are used - counting each skill only once per customer
"""
)
col1, col2, col3 = st.columns(3)
col1.metric("Total number of unique skills", df["title"].explode().nunique(), None)
col2.metric(
    "Mean number of unique skill per content",
    df.explode("title")
    .groupby(["filename", "idorg"])["title"]
    .nunique()
    .mean()
    .round(1),
    None,
)
col3.metric(
    "Mean number of unique skill per customer",
    df.explode("title").groupby(["url"])["title"].nunique().mean().round(1),
    None,
)
list_of_skillsets = (
    df.explode("title")
    .groupby("url")["title"]
    .apply(set)
    .reset_index()["title"]
    .to_list()
)

c = Counter(
    [item for sublist in [list(x) for x in list_of_skillsets] for item in sublist]
)
c = dict(sorted(dict(c).items(), key=lambda x: x[1]))
counts = pd.Series(c)

fig = px.bar(
    counts[-top_n:][::-1],
    orientation="h",
    title=f"Most frequent {top_n} skills (counting each skill once per customer)",
)
fig.update_layout(width=800, height=600)
fig.update_xaxes(title="Number of customers using this tag")
fig.update_yaxes(title=None)
st.plotly_chart(fig, use_container_width=True)

n_contents = st.slider(
    "Select a number of contents:", min_value=1, value=10, max_value=max(counts)
)
st.metric(
    f"Skills that appear on at least {n_contents} contents",
    (counts >= n_contents).sum(),
    None,
)

n_customers = st.slider("Select a number of customers:", min_value=1, value=3)
st.metric(
    f"Skills used by at least {n_customers} customers",
    (counts >= n_customers).sum(),
    None,
)

st.text("-----------------------------------------------------")

st.subheader(" Skill usage by customers")
x = df.explode("title").groupby("url")["title"].apply(lambda x: len(set(x)))
fig = px.histogram(x, histfunc="count")
fig.update_layout(width=800, height=600)
fig.update_xaxes(title="Number of unique skills used")
fig.update_yaxes(title="Number of customers")
fig.add_vline(
    x=x.mean(),
    line_dash="dash",
    annotation_text=f"Mean number of skills = {x.mean().round(0)}",
    line_color="red",
)
st.plotly_chart(fig, use_container_width=True)

st.text("-----------------------------------------------------")

df_clean = read_df_clean()

skill_content_columns = [
    "lms_skills",
    "skill_tagger_skills",
]


st.header("Performance of AI Skill tagger")
st.text(
    "This section presents precision and recall metrics of the AI skill tagger service."
)
with st.expander("See explanation"):
    st.markdown(
        """
    Precision and Recall are measures of the quality of a model.

    **Recall**

    recall is the fraction of correct skills (lms skills/skills added by the customer) that the skill tagger manages to predict.
    Being a fraction, recall is bounded between 0 and 1.

    *recall@k* is the fraction when considering only the best k  predictions by skill tagger. *recall* is expected to grow as k increases
    We compute recall per content. We present the average across all contents.

    **_recall = len(intersection(predicted skills, lms skills)) / len(lms skills)_**

    **Precision**

    precision is the fraction of predicted skills (skill tagger skills/ skills generated by the AI) that match an lms skill.
    Being a fraction, precision is bounded between 0 and 1.

    *precision@k* is the fraction when considering only the best k  predictions by skill tagger. *precision* is expected to decrease as k increases
    We compute precision per content. We present the average across all contents.

    **_precision = len(intersection(predicted skills, lms skills)) / len(predicted skills)_**
    """
    )
st.subheader("Statistics using ESCO and custom skills for LMS")
col_preds = [
    # "esco_matched_skills",
    "skill_tagger_skills",
    # "skill_tagger_transcript_skills",
]
col_res = ["mean", "std"]
st.text("Recall:")
st.table(
    compute_recall_multiple_cols(
        df_clean, col_gt="lms_skills", col_preds=col_preds, k_list=[1, 3, 5]
    )
    .describe()
    .loc[col_res]
    .T
)

st.text("Precision:")
st.table(
    compute_precision_multiple_cols(
        df_clean, col_gt="lms_skills", col_preds=col_preds, k_list=[1, 3, 5]
    )
    .describe()
    .loc[col_res]
    .T
)

st.text("Count:")
st.table(
    count_skills_multiple_cols(df_clean, cols=skill_content_columns)
    .describe()
    .loc[col_res]
    .T
)


st.subheader("Statistics considering only ESCO skills for LMS")
df_clean_not_custom = df_clean[df_clean["lms_skills_esco_fraction"] != 0]

st.text("Recall:")
st.table(
    compute_recall_multiple_cols(
        df_clean_not_custom, col_gt="lms_skills", col_preds=col_preds, k_list=[1, 3, 5]
    )
    .describe()
    .loc[col_res]
    .T
)

st.text("Precision:")
st.table(
    compute_precision_multiple_cols(
        df_clean_not_custom, col_gt="lms_skills", col_preds=col_preds, k_list=[1, 3, 5]
    )
    .describe()
    .loc[col_res]
    .T
)

st.text("Count:")
st.table(
    count_skills_multiple_cols(df_clean_not_custom, cols=skill_content_columns)
    .describe()
    .loc[col_res]
    .T
)
