# Is your model going stale? Detecting drift

Video: (link added after upload)
Short (extended): (link added after upload)
Short (hook): (link added after upload)

Needs Python 3.10 or newer, `pandas`, and
[`evidently`](https://github.com/evidentlyai/evidently) (0.7.23 or newer).

    pip install pandas evidently

This uses a real, public dataset: the classic 1990 U.S. census housing
data (20,640 rows), the same one used in Aurélien Géron's
*Hands-On Machine Learning*. It is not included in this folder. Download
it into `data/housing.csv` before running:

    mkdir -p data
    curl -o data/housing.csv https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv

Everything else here is fictional: the company ("Harborview Homes"),
its pricing model, and the story of it expanding into a new market.
The data is real; what it's used for is not.

## Run it

    python main.py

This walks through the whole story from the video:
1. A simple pricing formula is calibrated on inland listings (the
   market the company started in).
2. It's applied to near-ocean listings with no check at all: the
   average offer comes in far below the real market value.
3. The fix: before trusting the model's output, run Evidently's
   `DataDriftPreset`, a Kolmogorov-Smirnov test per column, comparing
   today's data to the reference batch the pricing was built on.
4. If enough columns have drifted (2 or more out of 2, the library's
   own default threshold), offers are paused and sent to review
   instead of made automatically.

## What this is (and isn't)

The "pricing model" here is a plain formula (`price_per_income`), not
a trained ML model, standing in for any automated scoring logic. The
drift check itself doesn't need a trained model either: it only
compares two batches of data. That's called data drift. Catching a
model whose actual predictions or accuracy have degraded is a
different problem, called concept drift, and needs the model itself
in the loop.

## Real-world anchor

The video opens with the Zillow Offers / Zestimate shutdown
(November 2021): a $304 million write-down in one quarter, after the
pricing model's assumptions and the real housing market split apart.
Source: GeekWire, 2021. That part is real and documented; the rest of
this repo is a fictional company built to demonstrate the same failure
mode on a small scale.

## Limits

`data/housing.csv` has a handful of null rows; `load_data()` drops
them (`dropna()`). Evidently's default drift-share threshold (0.5,
i.e. at least half the checked columns must have drifted) is the
library's own default, not something tuned for this demo.
