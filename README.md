# Reproducible Data Workflow for Video Game Sales, Ratings, and Genre Trends

**Udacity AI MBA Capstone: Project 1 of 7**

---

## Project Description

This project builds a reproducible data workflow that explores commercial and critical patterns in the video game industry using historical sales and ratings data. The analysis covers genre distribution, platform concentration, global sales structure, and the relationship between critic and user review scores.

The workflow is organized as a Jupyter notebook backed by reusable Python modules for data inspection, cleaning, and exploratory analysis. All cleaning decisions are documented and justified. Visualizations are saved as standalone figures. The project does not train machine learning models. It establishes the market context layer that is meant to inform future machine learning, statistical analysis, data science, and AI based projects.

---

## Dataset

**Source:** Kaggle (kendallgillies, 2017). Combined web scrape from VGChartz and Metacritic, with manually entered year of release values. The dataset was compiled by kendallgillies, building on prior work by Rush Kirubi, who extended a VGChartz scrape originally created by Gregory Smith to include Metacritic review data.

**File:** `data/raw/Video_Game_Sales_as_of_Jan_2017.csv.zip`

**Fields:** game name, platform, year of release, genre, publisher, North American sales, European sales, Japanese sales, other regional sales, global sales, critic score, critic count, user score, user count, ESRB rating.

**Coverage:** Approximately 17,000 titles spanning 1976 through 2017, with meaningful review data concentrated in the 2000 to 2012 period. Pre-2000 titles are systematically underrepresented in critic and user score columns due to the later emergence of digital review platforms.

**License:** Public domain / CC0 as published on Kaggle. No personally identifiable information is present.

---

## Files Included

```
notebooks/
  data_workflow.ipynb       # Main analysis notebook (10 sections)

src/
  cleaning.py               # clean_column_names, handle_missing_values, clean_column_types
  eda.py                    # summarize_game_market
  inspection.py             # inspect_dataframe

data/
  raw/
    Video_Game_Sales_as_of_Jan_2017.csv.zip   # Source dataset
  processed/
    video_games_clean.csv      # Cleaned dataset output

outputs/
  figures/
    fig1_genre_market_overview.png
    fig2_sales_distribution.png
    fig3_score_divergence.png
    fig4_release_volume.png
    fig_bias_representation.png

reports/
  module_summary.pdf        # Written project report

requirements.txt            # Python dependencies
README.md                   # This file
```

---

## How to Run

**Requirements:** Python 3.9 or later, Jupyter Notebook or JupyterLab.

1. Clone the repository:
  ```
   git clone https://github.com/thebobmay/ai-programming-foundations-project.git
   cd ai-programming-foundations-project
  ```
2. Install dependencies:
  ```
   pip install -r requirements.txt
  ```
3. Extract the dataset. The zip file is already in `data/raw/`. The notebook extracts it automatically during the Data Ingestion section. No manual extraction is needed.
4. Launch the notebook:
  ```
   jupyter notebook notebooks/data_workflow.ipynb
  ```
5. Run all cells from top to bottom using **Kernel > Restart & Run All**. The notebook is designed to execute fully without errors from a clean kernel state.

Output figures are written to `outputs/figures/` and the cleaned dataset is written to `data/processed/video_games_clean.csv` during notebook execution.

---

## Bias and Responsible Data Handling

This dataset carries several well defined biases that affect how results should be interpreted. The bias types below follow the taxonomy defined in the NIST AI Risk Management Framework (National Institute of Standards and Technology, 2023).

**Historical bias.** VGChartz sales estimates were built retrospectively from retail scanner data and community contributions. Early console generations (pre-NES) have little to no coverage, and Japanese domestic titles are systematically underrepresented relative to their actual market share. Sales figures should be treated as directional estimates rather than authoritative counts.

**Measurement bias.** Critic and user scores come from Metacritic, which launched in 2001. Titles released before that year have almost no review coverage. The analysis quantifies this gap: pre-2000 titles have a coverage rate near zero percent compared to 41.6 to 57.2 percent for post-2000 titles. Any score based analysis reflects the modern era, not the full history of the industry.

**Aggregation bias.** The 12 genre labels in this dataset collapse substantial internal variation. Action games range from 2D platformers to open world shooters. Sports games include both simulation and arcade titles. Genre level summaries mask the within genre diversity that would matter most in a real content recommendation or design context.

**Scope.** The dataset reflects the physical disc based console market sold through Western retail channels. It does not include mobile, PC digital, free to play, or post 2016 titles. Conclusions about the game industry as a whole should not be drawn from this data alone.

**How cleaning choices can introduce bias.** The cleaning decisions in this project were made deliberately to avoid distorting the dataset, but different choices would have produced systematically different results. The most consequential decision was retaining NaN values in the review columns rather than dropping rows that lack critic or user scores. If those rows had been dropped, nearly all pre-2000 titles would have been eliminated from the dataset, because review coverage for that era is near zero percent. Every downstream genre distribution count, platform sales summary, and era comparison would then reflect the 2000 to 2012 disc based console market rather than the full commercial history. The pattern would appear to be a real market finding when it was actually an artifact of how missing data were handled. A similar risk applies to duplicate removal and the choice of essential fields for null filtering. If the criteria for dropping rows had been applied more aggressively, for example by also dropping rows missing ESRB rating or critic score, genre counts and global sales totals would shift in ways that look like legitimate market patterns but are driven entirely by which rows the cleaning pipeline chose to exclude (Danchev, 2022).

These limitations are discussed in detail in Section 8 of the notebook and in the `module_summary.pdf` report.

---

## Future Integration Reflection

### How this workflow could support machine learning

The cleaned dataset is structured as a flat feature table suitable for supervised learning experiments. Genre, platform, publisher, release year, and ESRB rating are categorical features that require minimal additional preprocessing before encoding. Global sales and critic score are plausible regression targets for commercial viability or quality prediction models. The modular src/ design transfers directly to an ML pipeline: the cleaning functions run as preprocessing steps, and the EDA summaries serve as a validation layer to check for distribution shift between training and scoring data.

### How this dataset would need to change for neural networks

Neural networks are not well suited to tabular data at this scale. The cleaned dataset has roughly 17,000 rows, which is likely too small for deep learning to outperform tree based models (Grinsztajn et al., 2022). A neural approach would require augmenting the dataset with richer inputs: review text from Metacritic or Steam, cover art, genre tag graphs, or gameplay feature embeddings derived from descriptions. The systematic review coverage gap for pre-2000 titles would also become a more serious problem in a neural setting, because a model trained on this data would have almost no signal for that era and would need explicit era conditioning to handle it appropriately.

### How agentic automation could assist this workflow

The current workflow is reproducible but manual. A planning agent could inspect a new dataset, identify column types and missing value patterns, propose a cleaning strategy, and execute it without step by step human direction. A second agent could generate candidate visualizations, score them against a legibility rubric, and surface only the most informative ones for review. For ongoing market monitoring, an agentic pipeline could ingest updated sales or review data on a schedule, rerun the EDA summaries, compare them against a stored baseline, and flag statistically significant shifts in genre distribution or score patterns. The modular function design in this project, with cleaning, inspection, and EDA separated into distinct callable units, is already structured to make each stage straightforward to wrap as an agent tool.

---

## Requirements

See `requirements.txt` for the full dependency list. Core libraries:

- pandas
- numpy
- matplotlib
- seaborn
- jupyter

Install all dependencies with:

```
pip install -r requirements.txt
```

