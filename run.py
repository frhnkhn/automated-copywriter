import argparse
import asyncio
import json
import os
from datetime import datetime

from app.models import CopyRequest
from app.prompts import build_prompt
from app.generator import generate_copy


def get_arguments():

    parser = argparse.ArgumentParser(
        description="Automated Copywriting & Tone Transformer"
    )

    parser.add_argument(
        "--product",
        required=True,
        help="Product name"
    )

    parser.add_argument(
        "--description",
        required=True,
        help="Product description"
    )

    parser.add_argument(
        "--platform",
        required=True,
        choices=[
            "linkedin",
            "instagram",
            "email"
        ],
        help="Target platform"
    )

    parser.add_argument(
        "--tone",
        required=True,
        choices=[
            "professional",
            "friendly",
            "energetic",
            "funny",
            "persuasive"
        ],
        help="Writing tone"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Model temperature"
    )

    parser.add_argument(
        "--top-p",
        type=float,
        default=0.9,
        help="Top-P value"
    )

    return parser.parse_args()


def save_output(data):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "outputs/copy_%Y%m%d_%H%M%S.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filename


def main():

    args = get_arguments()

    print("\n======================================")
    print("   AUTOMATED COPYWRITING ENGINE")
    print("======================================")

    print("\nValidating input...")

    try:

        request = CopyRequest(
            product_name=args.product,
            product_description=args.description,
            platform=args.platform,
            tone=args.tone,
            temperature=args.temperature,
            top_p=args.top_p
        )

    except Exception as error:

        print("\n❌ Invalid input:")
        print(error)
        return

    print("✅ Input valid.")

    print("\nBuilding dynamic prompt...")

    prompt = build_prompt(
        request.product_name,
        request.product_description,
        request.platform,
        request.tone
    )

    print("✅ Prompt created.")

    print("\nGenerating copy with Qwen3:8b...")
    print("Please wait...\n")

    try:

        result = generate_copy(
            prompt,
            request.temperature,
            request.top_p
        )

    except Exception as error:

        print("\n❌ AI generation failed:")
        print(error)
        return

    print("======================================")
    print("          GENERATED COPY")
    print("======================================\n")

    print(result)

    output_data = {
        "product_name": request.product_name,
        "platform": request.platform,
        "tone": request.tone,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "generated_copy": result
    }

    filename = save_output(
        output_data
    )

    print("\n======================================")
    print(f"Saved to: {filename}")
    print("======================================")


if __name__ == "__main__":
    main()