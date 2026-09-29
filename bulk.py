import asyncio
import csv
import json
import os
from datetime import datetime

from app.models import CopyRequest
from app.prompts import build_prompt
from app.async_generator import generate_multiple


def load_products():

    products = []

    with open(
        "data/products.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            request = CopyRequest(
                product_name=row["product_name"],
                product_description=row["description"],
                platform=row["platform"],
                tone=row["tone"],
                temperature=float(row["temperature"]),
                top_p=float(row["top_p"])
            )

            prompt = build_prompt(
                request.product_name,
                request.product_description,
                request.platform,
                request.tone
            )

            products.append({
                "request": request,
                "prompt": prompt,
                "temperature": request.temperature,
                "top_p": request.top_p
            })

    return products


async def main():

    products = load_products()

    requests = [
        {
            "prompt": product["prompt"],
            "temperature": product["temperature"],
            "top_p": product["top_p"]
        }
        for product in products
    ]

    print("\n======================================")
    print("       BULK COPYWRITING ENGINE")
    print("======================================")

    print(
        f"\nGenerating {len(requests)} pieces of copy..."
    )

    results = await generate_multiple(
        requests
    )

    output = []

    for product, result in zip(
        products,
        results
    ):

        if isinstance(result, Exception):

            generated = f"ERROR: {result}"

        else:

            generated = result

        output.append({
            "product_name":
                product["request"].product_name,

            "platform":
                product["request"].platform,

            "tone":
                product["request"].tone,

            "temperature":
                product["request"].temperature,

            "top_p":
                product["request"].top_p,

            "generated_copy":
                generated
        })

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "outputs/bulk_%Y%m%d_%H%M%S.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n✅ Bulk generation complete.")

    print(
        f"Results saved to: {filename}"
    )


if __name__ == "__main__":

    asyncio.run(main())