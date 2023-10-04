import streamlit as st
import requests
import pandas as pd


@st.cache_data
def get_challenge_results(round_number: int) -> pd.DataFrame:
    """Fetches and returns the challenge results for a given round."""
    url = "https://df-sql.oceandao.org/challenge/data"
    data = {"query": {"round": round_number}}
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    return pd.DataFrame(result).sort_values("nmse", ascending=True)


def get_round_range() -> tuple[int, int]:
    """Fetches and returns the minimum and maximum round numbers."""

    url = "https://df-sql.oceandao.org/rewardsSummary"

    data = {
        "query": {"round": {"$gt": -1}, "challenge_amt": {"$gt": 0}},
        "fields": [
            {"expression": {"pattern": "min(round) AS min_round"}},
            {"expression": {"pattern": "max(round) AS max_round"}},
        ],
    }

    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()[0]
    return result.get("min_round", None), result.get("max_round", None)


# Sets up the Streamlit page configuration.
st.set_page_config(
    page_title="OCEAN Leaderboard Results",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Main layout of the app ---
main_title = st.title("OCEAN Leaderboard Results")
sidebar = st.sidebar.container()
leaderboard = st.container()
individual_score = st.container()
st.divider()
duplicate_leaderboard = st.container()

# --- Sidebar ---
min_round, max_round = get_round_range()
challenge_round = sidebar.selectbox(
    label="Select challenge round",
    options=range(max_round, min_round - 1, -1),
    help="Select a challenge round to view the leaderboard details.",
)

# --- Main Metrics ---
# Get leaderboard data based on user input and calculcate metrics
round_results_df = get_challenge_results(challenge_round) # type: ignore

round_metrics = {
    "num_submissions": len(round_results_df),  # Total number of submissions
    "num_duplicates": round_results_df["from_addr"]
    .duplicated()
    .sum(),  # Total number of duplicate addresses
    "best_score": round_results_df["nmse"].min(),  # Best score
    "worst_score": round_results_df["nmse"].max(),  # Worst score
    "avg_score": round_results_df["nmse"].mean(),  # Average score
}

leaderboard_agg = (
    round_results_df.groupby("from_addr")
    .agg(
        total_submissions=("from_addr", "count"),
        best_score=("nmse", "min"),
        worst_score=("nmse", "max"),
        avg_score=("nmse", "mean"),
    )
    .reset_index()
)

duplicate_addresses = leaderboard_agg.query("total_submissions > 1")

# --- Main Metrics ---
# Display leaderboard data for the selected round
leaderboard.header(f"Challenge Round {challenge_round}")

(
    submissions_col,
    best_score_col,
    worst_score_col,
    avg_score_col,
) = leaderboard.columns(4)
submissions_col.metric(label="Submissions", value=round_metrics["num_submissions"])
best_score_col.metric(label="Best score", value=round(round_metrics["best_score"], 3))
worst_score_col.metric(
    label="Worst score", value=round(round_metrics["worst_score"], 3)
)
avg_score_col.metric(label="Average score", value=round(round_metrics["avg_score"], 3))

leaderboard.dataframe(
    round_results_df,
    use_container_width=True,
    hide_index=True,
    column_order=["from_addr", "nft_addr", "nmse"],
)

# --- Individual Metrics ---
# Lookup a single wallet address from the selected round leaderboard
individual_lookup = individual_score.expander("Individual Wallet Lookup", expanded=True)

individual_lookup.subheader("Wallet Lookup")

wallet_lookup = individual_lookup.selectbox(
    label="Lookup score of a specific wallet",
    options=[None] + leaderboard_agg["from_addr"].unique().tolist(),
    index=None,
    placeholder="Select a wallet address",
    help="Select a wallet address to view submission results.",
)

if wallet_lookup:
    wallet_filtered = round_results_df.query(f"from_addr == '{wallet_lookup}'")

    wallet_submissions = len(wallet_filtered)
    wallet_best_score = wallet_filtered["nmse"].min()
    wallet_worst_score = wallet_filtered["nmse"].max()
    wallet_avg_score = wallet_filtered["nmse"].mean()

    (
        individual_submission_col,
        individual_best_score_col,
        individual_worst_score_col,
        individual_avg_score_col,
    ) = individual_lookup.columns(4)
    individual_submission_col.metric(label="Submissions", value=wallet_submissions)
    individual_best_score_col.metric(
        label="Best score", value=round(wallet_best_score, 3)
    )
    individual_worst_score_col.metric(
        label="Worst score", value=round(wallet_worst_score, 3)
    )
    individual_avg_score_col.metric(
        label="Average score", value=round(wallet_avg_score, 3)
    )

    individual_lookup.dataframe(
        wallet_filtered,
        use_container_width=True,
        hide_index=True,
        column_order=[
            "from_addr",
            "nft_addr",
            "nmse",
        ],
    )


# --- Duplicate Addresses ---
# View addresses that have multiple submissions
duplicate_leaderboard.header("Multiple Submissions")
duplicate_address_col = duplicate_leaderboard.columns(1)[0]
duplicate_address_col.metric(
    label="Duplicate addresses",
    value=round_metrics["num_duplicates"],
    help="Total count of addresses with multiple submissions.",
)


duplicate_leaderboard.dataframe(
    duplicate_addresses,
    use_container_width=True,
    hide_index=True,
    column_order=[
        "from_addr",
        "total_submissions",
        "best_score",
        "worst_score",
        "avg_score",
    ],
)
