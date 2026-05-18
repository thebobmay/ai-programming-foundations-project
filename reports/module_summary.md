# Reproducible Data Workflow for Video Game Sales, Ratings, and Genre Trends

**Robert Mayfield**
Udacity AI MBA Capstone: Project 1 of 7

---

## Overview

This project builds a reproducible data workflow to examine commercial and critical patterns in the video game industry using historical sales and ratings data. The workflow loads, cleans, explores, and visualizes a dataset of approximately 17,000 commercially released titles spanning 1976 through 2017. The goal is not to train predictive models but to establish a documented, rerunnable foundation that characterizes genre distribution, platform concentration, sales structure, and the relationship between critic and user scores. Danchev (2022) describes this type of workflow as one that integrates research questions, data inputs, code, documentation, and narrative in a single reproducible document, which this project implements through a structured Jupyter notebook backed by modular Python source files.

---

## Dataset Description

The dataset is a combined video game sales and ratings table sourced from Kaggle, derived from VGChartz retail sales estimates and Metacritic critic and user review scores (kendallgillies, 2017). It contains 17,416 rows and 15 columns before cleaning, covering fields including game name, platform, release year, genre, publisher, regional sales figures for North America, Europe, Japan, and other markets, global sales totals, critic score, critic review count, user score, user review count, and ESRB content rating. After cleaning, the working dataset retains 17,408 rows across 12 genre categories and more than 30 platform labels.

The dataset was compiled by kendallgillies (2017), building on prior work by Rush Kirubi, who extended a VGChartz scrape originally created by Gregory Smith to include Metacritic review data.

The dataset represents the physical disc based console market sold primarily through Western retail channels. It does not include mobile titles, PC digital storefronts, free to play games, or releases after 2016. Sales figures are estimates derived from retail scanner data and community contributions and should be treated as directional rather than authoritative.

---

## Workflow Description

The workflow is implemented in five stages, each corresponding to a section of the Jupyter notebook.

**Ingestion.** The raw dataset is stored as a zip archive in `data/raw/` and extracted programmatically at runtime. The notebook uses `pd.read_csv` to load the extracted CSV and displays the first rows to confirm successful ingestion.

**Cleaning.** Three functions in `src/cleaning.py` apply sequential transformations. `clean_column_names` standardizes column names to lowercase with underscores. `handle_missing_values` drops duplicate rows and removes rows missing values in four essential fields: name, genre, publisher, and year of release. Review related fields retain NaN because their missingness is era driven rather than a data error, and removing those rows would eliminate nearly all pre-2000 titles from the dataset. `clean_column_types` runs last and converts `year_of_release` from float64 to int64, a step that is only safe after rows with missing year values have been removed.

**Inspection.** A reusable `inspect_dataframe` function in `src/inspection.py` prints a structured report covering shape, data types, memory usage, missing values, duplicate rows, numeric and categorical statistics, and sample rows. This function is applied to both the raw and cleaned datasets to document the effect of each cleaning step.

**Exploratory analysis.** A `summarize_game_market` function in `src/eda.py` returns four grouped summary tables: game counts with total and mean global sales by genre, the same by platform, and mean critic and user scores by genre and by platform. Seven targeted EDA questions build on these summaries to examine genre distribution, sales concentration, regional breakdown, score patterns, and release volume over time.

**Visualization.** Four polished figures are saved to `outputs/figures/` and displayed in the notebook. Each figure is followed by a Markdown interpretation cell.

---

## Key Decisions and Assumptions

**Retaining NaN in review columns.** Dropping all rows missing critic or user scores would remove nearly all pre-2000 titles and produce a dataset skewed toward the 2000 to 2012 era. The decision to retain these rows for sales and genre analysis, while restricting score analysis to the reviewed subset, preserves the full commercial picture at the cost of a smaller score analysis pool. Danchev (2022) notes that transparency about such decisions is central to reproducible data science practice.

**Dropping rows missing essential structural fields.** Name, genre, publisher, and year of release are required for every analysis in the project. Rows missing any of these values cannot be meaningfully categorized and are dropped. This removes 8 rows, a loss of less than 0.1 percent of the original data.

**Treating post-2012 release data as structurally incomplete.** Release counts drop sharply after 2012, reflecting the transition to digital distribution channels not captured by VGChartz retail tracking. The analysis notes this boundary explicitly and avoids drawing trend conclusions from post-2012 data.

**Global sales as the primary sales metric.** Regional breakdowns are analyzed descriptively, but global sales is used as the single summary metric for genre and platform comparisons because it is the most complete and consistent column across all titles.

**Pearson correlation for the score to sales relationship.** Global sales is right skewed. Applying Pearson correlation to this distribution assumes approximate linearity, which the data only weakly satisfies. The resulting coefficient should be interpreted as a rough directional indicator rather than a precise measure of association.

---

## Results and Interpretation

Figure 1 shows genre distribution by title count and total global sales. Action is the most represented genre with 3,500 titles. Sports and role playing games rank second and third by count. By total global sales, however, Sports produces more revenue than most higher count genres, indicating that Sports titles sell at a higher average rate per game than Action titles. Shooter and Platform genres also generate disproportionately high revenue relative to their title counts, pointing to a systematic difference between volume driven and revenue-efficient genre segments.

Figure 2 shows the global sales distribution on a log scale. The distribution is strongly right skewed: a small number of titles account for a large share of total industry sales, while the majority of games sell fewer than one million units globally. This long tail structure, in which a small number of hits dominate revenue while a large volume of modest sellers collectively contribute the remainder, is a well documented pattern in media and entertainment markets (Anderson, 2006). The Moderate commercial tier, defined as 0.1 to 1 million global sales, contains 48.3 percent of all titles and serves as the realistic benchmark for midrange commercial performance.

Figure 3 is a diverging bar chart showing the gap between mean critic and mean user scores by genre, with both scores placed on a 0 to 100 scale for direct comparison. Bars extending right indicate genres where critics rate higher than users; bars extending left indicate genres where users rate higher. Sports and Shooter are the only genres where critics assign higher scores, with Sports showing the largest critic-favoring gap at 2.86 points. Adventure shows the largest user-favoring gap at 5.23 points, suggesting that players assign more value to narrative experience than critics do. Role Playing and Platform show similar user-favoring gaps in the 3 to 4 point range. The exploratory analysis also computes Pearson correlations between review scores and global sales: critic score produces a modest positive relationship at r = 0.237, while user score is nearly uncorrelated at r = 0.088. Both values are point estimates subject to the weakly satisfied linearity assumption given the right-skewed sales distribution.

Figure 4 shows release volume by year. Release counts rose through the 1990s and peaked in 2009 at 1,550 titles before declining sharply. The decline after 2012 reflects the shift toward digital distribution channels and does not indicate an actual contraction in game market activity.

North America accounts for the largest share of global sales in this dataset, followed by Europe. Japan accounts for roughly 15 percent of global sales. Combined, North America and Europe represent approximately 76 percent of tracked global sales, reflecting the Western retail focus of the underlying VGChartz data.

---

## Responsible Practice

This analysis applies the bias taxonomy described in the NIST AI Risk Management Framework (National Institute of Standards and Technology, 2023), which identifies historical bias, measurement bias, and aggregation bias as recurring sources of systematic error in data-driven work.

**Historical bias** is present in the sales estimates, which were built retrospectively from retail scanner data and community contributions. Early console generations have sparse coverage, and the Japanese market is systematically underrepresented relative to its actual share of global game revenue. Sales figures for pre-1985 titles are unreliable and treated as indicative only.

**Measurement bias** is present in the review data. Metacritic launched in 2001, so titles released before that year carry almost no review data. The analysis quantifies this gap: pre-2000 titles have a review coverage rate near zero percent, compared to typically between 36 and 76 percent for post-2000 titles. The disparate coverage ratio is approximately 0.07, meaning early era titles are reviewed at about 7 percent of the rate of later titles. Any score based conclusion reflects the post-2000 era and cannot be generalized to earlier game history. When missing data are not random, common cleaning approaches can shift results and amplify the underlying bias (Danchev, 2022).

**Aggregation bias** is introduced by the 12 genre labels in the dataset. These labels collapse substantial internal variation. Action games range from 2D platformers to open world shooters. Sports games include both simulation and arcade titles. Genre level summaries are useful for market characterization but mask the within genre diversity that would matter in a content recommendation or design context.

Mitigation steps taken in this project include separating sales based conclusions from score based conclusions, explicitly documenting the reviewed subset size relative to the full dataset, and scoping all findings to the 2000 to 2012 disc based console market rather than the game industry as a whole.

---

## Reproducibility

The project is structured to allow full reproduction by a reviewer with Python and Git installed. All source code is version controlled in a GitHub repository with multiple commits across a development branch and main branch. The notebook is designed to run from a clean kernel state using Kernel > Restart and Run All without modification to any file paths or configuration values.

The `requirements.txt` file captures exact package versions from the development environment. Core dependencies are pandas 2.3.0, numpy 2.4.3, matplotlib 3.10.8, and seaborn 0.13.2. The raw dataset is included in the repository as a zip archive in `data/raw/` and is extracted automatically during notebook execution. No external API calls or network requests are made during any step of the workflow.

The `src/` directory separates reusable cleaning, inspection, and EDA logic from the notebook itself, allowing each function to be imported and tested independently of the Jupyter environment. This structure reflects the principle that reproducible workflows benefit from modular, version controlled code components (Danchev, 2022).

---

## Future Integration

This analysis was designed as a market context layer, not a model training pipeline. It establishes patterns in genre distribution, sales structure, and review behavior that can inform downstream AI and data science work.

**Supporting machine learning.** The cleaned dataset is a flat feature table suitable for supervised learning experiments. Genre, platform, publisher, release year, and ESRB rating are categorical features that can be encoded with minimal additional preprocessing. Global sales and critic score are plausible regression targets for commercial viability or quality prediction models. The modular src/ design transfers directly to an ML pipeline, with the cleaning functions serving as preprocessing steps and the EDA summaries serving as a validation layer to detect distribution shift between training and evaluation data.

**Preparing for neural networks.** Neural networks are generally not well suited to tabular data at this scale. Research has shown that tree based models consistently outperform deep learning on structured tabular datasets, particularly at smaller scales where the inductive biases of neural networks provide little advantage (Grinsztajn et al., 2022). The cleaned dataset has roughly 17,000 rows, which is likely too small for deep learning to outperform tree based models without additional data. A neural approach would require enriching the dataset with review text, cover art, or gameplay feature embeddings extracted from descriptions. With richer inputs of that kind, transformer architectures could learn latent genre representations that go beyond discrete labels (Vaswani et al., 2017). The systematic review coverage gap for pre-2000 titles would also become a more serious problem in a deep learning setting, requiring explicit era conditioning or targeted data collection for classic titles.

**Agentic automation.** The current workflow is reproducible but manual. A planning agent could inspect a new dataset, identify column types and missing value patterns, propose a cleaning strategy, and execute it without step by step direction. A monitoring agent could ingest updated sales or review data on a schedule, rerun the EDA summaries, and flag statistically significant shifts in genre distribution or score patterns. The modular function design in this project, with cleaning, inspection, and EDA in distinct callable units, is already structured to make each stage straightforward to wrap as an agent tool.

---

## References

Anderson, C. (2006). *The long tail: Why the future of business is selling less of more*. Hyperion.

Danchev, V. (2022). Reproducible Data Science with Python: An Open Learning Resource. *Journal of Open Source Education, 5*(56), 156. [https://doi.org/10.21105/jose.00156](https://doi.org/10.21105/jose.00156)

Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why tree-based models still outperform deep learning on tabular data. *Advances in Neural Information Processing Systems, 35*, 507–520.

kendallgillies. (2017). *Video game sales and ratings* [Data set]. Kaggle. https://www.kaggle.com/datasets/kendallgillies/video-game-sales-and-ratings/data

National Institute of Standards and Technology. (2023). *Artificial intelligence risk management framework (AI RMF 1.0)*. U.S. Department of Commerce. [https://doi.org/10.6028/NIST.AI.100-1](https://doi.org/10.6028/NIST.AI.100-1)

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*, 5998–6008.