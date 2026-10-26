"""Turn the Kaggle r/movies dump into a pool of candidate posts to read and label.

    python prepare_data.py

Needs KAGGLE_API_TOKEN in .env (see below). Downloads
thedevastator/unlocking-movie-engagements-and-insights-through, cleans it, and
writes raw_posts.csv. It never touches labels.csv -- that file is yours.
"""
import os
import re
from pathlib import Path

import kagglehub
import pandas as pd

DATASET = "thedevastator/unlocking-movie-engagements-and-insights-through"
MIN_CHARS, MAX_CHARS = 80, 2500
OUT = Path(__file__).parent / "raw_posts.csv"


def load_env(path=Path(__file__).parent / ".env"):
    """Read `export KEY=value` / `KEY=value` lines into os.environ."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip().removeprefix("export ").strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def fix_text(s):
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def main():
    load_env()
    folder = Path(kagglehub.dataset_download(DATASET))
    df = pd.read_csv(next(folder.glob("*.csv")))
    df["body"] = df["body"].fillna("").astype(str).map(fix_text)

    df["kind"] = df["title"].eq("Comment").map({True: "comment", False: "post"})
    df["text"] = df.apply(
        lambda r: r["body"] if r["kind"] == "comment"
        else f'{fix_text(str(r["title"]))}\n\n{r["body"]}', axis=1)

    n0 = len(df)
    df = df[~df["body"].isin(["", "[removed]", "[deleted]"])]
    df = df[df["body"].str.len().between(MIN_CHARS, MAX_CHARS)]
    df = df.drop_duplicates("body")
    print(f"{n0} rows -> {len(df)} kept ({df['kind'].value_counts().to_dict()})")

    # Rough flag for posts likely to be `analysis`, so you can find enough of them.
    # It is a search aid only; read the post before you label it.
    def hint(t):
        marks = [bool(re.search(r"\b(19|20)\d\d\b|\d[\d,.]*%|\$\d", t)),
                 bool(re.search(r'"[^"]{3,}"|“[^”]{3,}”', t)),
                 len(re.findall(r"(?<=[a-z,] )[A-Z][a-z]+(?: [A-Z][a-z]+)+", t)) >= 2,
                 bool(re.search(r"^\s*[-*•] ", t, re.M))]
        first_line = t.split("\n")[0]
        return (len(t) >= 200 and "?" not in first_line
                and not t.rstrip().endswith("?") and sum(marks) >= 2)

    df["analysis_hint"] = df["text"].map(hint)
    print(f"{int(df['analysis_hint'].sum())} flagged as possible analysis")

    out = df[["id", "text", "kind", "score", "analysis_hint"]].sample(frac=1, random_state=0)
    out.to_csv(OUT, index=False, encoding="utf-8")
    print(f"wrote {OUT.name}: read it, then copy the ones you label into labels.csv")


if __name__ == "__main__":
    main()
