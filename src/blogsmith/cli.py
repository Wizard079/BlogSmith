import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="🧠 BlogSmith AI - Autonomously generate SEO-friendly blog posts with smart agents."
    )

    parser.add_argument(
        "topic",
        type=str,
        help="Main blog topic. Example: 'How Python is used in AI'"
    )

    parser.add_argument(
        "--tone",
        type=str,
        choices=["formal", "educational", "creative", "technical"],
        default="educational",
        help="Tone of the blog post (default: educational)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Directory to save the generated blog and metadata (default: ./output)"
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching for API calls"
    )

    parser.add_argument(
        "--batch-file",
        type=str,
        help="Optional path to a file containing multiple topics (one per line)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose logs during processing"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(f"📘 Topic: {args.topic}")