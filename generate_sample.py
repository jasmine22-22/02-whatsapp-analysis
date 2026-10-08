from datetime import date, datetime, timedelta
from pathlib import Path
import random

SEED = 42
MESSAGE_COUNT = 2_000
MEDIA_COUNT = 300
MULTILINE_COUNT = 8
START_DATE = date(2026, 5, 1)
SENDER_COUNTS = (
    ("Novi", 720),
    ("Tavi", 560),
    ("Lumo", 430),
    ("Rami", 290),
)
DAY_WEIGHTS = (1.25, 1.0, 1.3, 1.0, 1.45, 0.9, 0.85)
ENGLISH_PHRASES = (
    "That sounds good to me.",
    "I'll check the timing.",
    "Let's keep it simple.",
    "The plan feels clear.",
    "Maybe after sunset.",
    "Sending a tiny update.",
    "That was a calm evening.",
    "Let's try another route.",
)
ARABIC_PHRASES = (
    "تمام، الفكرة واضحة.",
    "خلينا نبدأ بهدوء.",
    "يمكن نكمل بعد قليل.",
    "الوقت مناسب اليوم.",
    "هذه ملاحظة صغيرة.",
    "نرتبها خطوة خطوة.",
    "كل شيء يبدو جيداً.",
    "نؤجلها إلى المساء.",
)
MULTILINE_MESSAGES = (
    ("I found a quieter option.", "The timing should work.", "Let's keep it flexible."),
    ("بدأت الفكرة تتضح.", "نرتب الباقي لاحقاً."),
    ("A small update from me.", "Nothing urgent here."),
    ("خلينا نرتبها بهدوء.", "ونكمل الحديث بعد قليل."),
)


def make_timestamp(rng, dates):
    chosen_date = rng.choices(
        dates,
        weights=[DAY_WEIGHTS[day.weekday()] for day in dates],
        k=1,
    )[0]
    period = rng.choices(
        ("evening", "late", "daytime", "early"),
        weights=(48, 15, 30, 7),
        k=1,
    )[0]
    hours = {
        "evening": range(18, 24),
        "late": range(0, 3),
        "daytime": range(9, 18),
        "early": range(5, 9),
    }
    hour = rng.choice(tuple(hours[period]))
    return datetime(
        chosen_date.year,
        chosen_date.month,
        chosen_date.day,
        hour,
        rng.randrange(60),
    )


def main():
    rng = random.Random(SEED)
    dates = [START_DATE + timedelta(days=offset) for offset in range(42)]
    phrases = ENGLISH_PHRASES + ARABIC_PHRASES
    records = []

    for sender, count in SENDER_COUNTS:
        for _ in range(count):
            records.append(
                [make_timestamp(rng, dates), sender, rng.choice(phrases)]
            )

    records.sort(key=lambda record: record[0])
    media_indexes = set(rng.sample(range(MESSAGE_COUNT), MEDIA_COUNT))
    for index in media_indexes:
        records[index][2] = "<Media omitted>"

    multiline_candidates = [
        index for index in range(MESSAGE_COUNT) if index not in media_indexes
    ]
    for index in rng.sample(multiline_candidates, MULTILINE_COUNT):
        records[index][2] = "\n".join(rng.choice(MULTILINE_MESSAGES))

    lines = []
    for timestamp, sender, message in records:
        date_text = f"{timestamp.month}/{timestamp.day}/{timestamp.year % 100:02d}"
        hour = timestamp.hour % 12 or 12
        period = timestamp.strftime("%p").lower()
        lines.append(
            f"{date_text}, {hour}:{timestamp.minute:02d} {period} - "
            f"{sender}: {message}"
        )

    output_path = Path(__file__).resolve().parent / "data" / "sample_chat.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as chat_file:
        chat_file.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()