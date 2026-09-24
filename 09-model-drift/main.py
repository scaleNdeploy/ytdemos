import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

COMPANY = "Harborview Homes"
DATA = "data/housing.csv"
COLS = ["median_income", "housing_median_age"]


def load_data():
    """Real 1990 U.S. census housing data, one row per
    neighborhood block. Not our invention. The company
    using it, Harborview Homes, is fictional."""
    return pd.read_csv(DATA).dropna()


def reference_batch(df):
    """Inland listings. This is the market the pricing
    model was built and tuned on."""
    return df[df["ocean_proximity"] == "INLAND"].sample(
        400, random_state=0)


def current_batch(df):
    """Harborview expands to near-ocean listings. Same
    company, same model, a different market."""
    return df[df["ocean_proximity"] == "NEAR OCEAN"].sample(
        200, random_state=0)


def price_estimate(row, ref_price_per_income):
    """The pricing model: value per unit of income,
    calibrated on the reference market. It has no idea
    this is a different market now."""
    return row["median_income"] * ref_price_per_income


def auto_offer(current, ref_price_per_income):
    """The mistake: score every listing and make an
    offer, with no check on whether this market still
    looks like the one the model was built on."""
    offers = current.apply(
        lambda r: price_estimate(r, ref_price_per_income),
        axis=1)
    print(f"{COMPANY}: {len(offers)} offers made")
    print(f"Average offer: ${offers.mean():,.0f}")
    actual = current["median_house_value"].mean()
    print(f"Actual market value: ${actual:,.0f}")


def check_drift(ref, cur):
    """The fix: before trusting the model, compare
    today's data to the reference it was built on.
    Evidently runs a K-S test per column: a low p-value
    means that column's distribution has shifted."""
    report = Report([DataDriftPreset()])
    result = report.run(
        reference_data=ref[COLS], current_data=cur[COLS])
    m = result.dict()["metrics"][0]
    return m["value"]["share"], m["value"]["count"]


def auto_offer_guarded(current, ref, ref_price_per_income):
    """Same model, now gated on a drift check first."""
    share, count = check_drift(ref, current)
    if share >= 0.5:
        print(f"DRIFT DETECTED: {int(count)} of "
              f"{len(COLS)} columns shifted")
        print(f"{COMPANY}: offers paused, sent to review")
        return
    auto_offer(current, ref_price_per_income)


def main():
    df = load_data()
    ref = reference_batch(df)
    cur = current_batch(df)
    ref_price_per_income = (
        ref["median_house_value"].mean()
        / ref["median_income"].mean())

    print("-- before the fix --")
    auto_offer(cur, ref_price_per_income)

    print()
    print("-- after the fix --")
    auto_offer_guarded(cur, ref, ref_price_per_income)


main()
