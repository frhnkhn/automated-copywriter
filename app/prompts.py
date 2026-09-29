PLATFORM_RULES = {
    "linkedin": """
Create professional LinkedIn content.

Requirements:
- Professional and informative
- Suitable for a business audience
- Clearly explain the product benefit
- Use a strong but natural call-to-action
- Avoid excessive emojis
- Do not use unnecessary hashtags
""",

    "instagram": """
Create Instagram marketing content.

Requirements:
- Engaging and visually appealing writing
- Short paragraphs
- Strong hook
- Include a clear call-to-action
- Use relevant hashtags
- Emojis may be used when appropriate
""",

    "email": """
Create marketing email content.

Requirements:
- Include a subject line
- Include a greeting
- Write a clear email body
- Highlight product benefits
- Include a call-to-action
- End with a professional closing
"""
}


def build_prompt(
    product_name,
    product_description,
    platform,
    tone
):
    platform_rules = PLATFORM_RULES[platform]

    prompt = f"""
You are an expert marketing copywriter.

Your task is to create marketing copy for a product.

PRODUCT INFORMATION
-------------------
Product Name:
{product_name}

Product Description:
{product_description}

TARGET PLATFORM
---------------
{platform}

REQUIRED TONE
-------------
{tone}

PLATFORM REQUIREMENTS
---------------------
{platform_rules}

GENERAL RULES
-------------
- Match the requested tone.
- Focus on the product's real benefits.
- Do not invent technical specifications.
- Do not explain your reasoning.
- Return only the final marketing copy.
- Make the content polished and ready to publish.

Now generate the final marketing copy.
"""

    return prompt