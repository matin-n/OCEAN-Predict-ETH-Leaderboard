# OCEAN-Predict-ETH-Leaderboard

This application serves as a leaderboard for the Ocean Protocol's weekly "[Challenge DF](https://df.oceandao.org/challenge-df)" where participants forecast the price of Ethereum (ETH). Users can view, analyze, and compare the performance of different submissions right from this application.


## Features

- **Leaderboard View:** Display the leaderboard of a particular challenge round showing participant addresses, scores, and rankings.
- **Individual Lookup:** Lookup and analyze the performance of a specific wallet address.
- **Multiple Submission Analysis:** View and analyze addresses that have multiple submissions.
- **Round Range Selector:** Select and view leaderboard of different rounds easily.
- **Metric Summary:** Summarized metrics like the total number of submissions, best score, worst score, and average score for a particular round.

## Getting Started

### Live Application

The application is hosted on Streamlit Cloud and can be accessed [here](https://forecast-ethereum.streamlit.app).

### Local Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/matin-n/OCEAN-Predict-ETH-Leaderboard.git
cd OCEAN-Predict-ETH-Leaderboard
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Streamlit app:
```bash
streamlit run app.py
```

Now, navigate to http://localhost:8501 in your web browser to use the application.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://docs.python-requests.org/en/master/)