"""Build a CSV of every word in words_alpha.txt, tagged for length & commonness.

Reads words_alpha.txt and writes words.csv with columns:
    word, longornot, commonornot

longornot:    "yes" when len(word) > 10
commonornot:  "yes" when wordfreq Zipf >= 4.0 (~known to most speakers)

NOTE: no words are filtered out — every entry in words_alpha.txt is kept,
even oddities like "aaa". If you want to exclude them at lookup time use
blacklist.txt in the app.
"""

import csv
from pathlib import Path

from wordfreq import zipf_frequency

HERE = Path(__file__).parent
SRC = HERE / "words_alpha.txt"
OUT = HERE / "words.csv"

LONG_THRESHOLD = 10        # strictly longer than this is "long"
COMMON_ZIPF = 4.0          # Zipf >= 4.0 ~ "common" everyday word


def main() -> None:
    total = 0
    long_count = 0
    common_count = 0

    with SRC.open("r", encoding="utf-8") as f_in, OUT.open(
        "w", encoding="utf-8", newline=""
    ) as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["word", "longornot", "commonornot"])

        for line in f_in:
            word = line.strip().lower()
            if not word:
                continue

            long_flag = "yes" if len(word) > LONG_THRESHOLD else "no"
            common_flag = (
                "yes" if zipf_frequency(word, "en") >= COMMON_ZIPF else "no"
            )

            writer.writerow([word, long_flag, common_flag])
            total += 1
            if long_flag == "yes":
                long_count += 1
            if common_flag == "yes":
                common_count += 1

    print(f"total:  {total:,}")
    print(f"long  (>{LONG_THRESHOLD} letters): {long_count:,}")
    print(f"common (Zipf >= {COMMON_ZIPF}):    {common_count:,}")
    print(f"wrote -> {OUT}")


if __name__ == "__main__":
    main()
