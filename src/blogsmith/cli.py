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
        default="educational",
        help="Tone of the blog post (default: educational)"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(f"📘 Topic: {args.topic}")