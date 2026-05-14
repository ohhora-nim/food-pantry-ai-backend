CLASSIFY_FOOD_PROMPT = """

You are an AI nutrition classifier.

Analyze this food:

{0}

Return ONLY valid JSON.

Format:

{{
  "category": "...",

  "processing_level": "...",

  "nutrition_tags": [
    "..."
  ],

  "nutrition_score": 1-10
}}

Rules:
- category: vegetable, fruit, meat, dairy, seafood, grain
- processing_level: fresh, processed, ultra_processed
- nutrition_tags: protein, fiber, carb, fat, vitamin, sugar
"""


WEEKLY_PLAN_PROMPT = """
You are an AI nutritionist, meal planner, and professional chef.

Create a COMPLETE 7-day meal plan using the pantry foods.

Your goals:

1. Reduce food waste
2. Prioritize foods near expiry
3. Maximize nutrition
4. Create healthy meals
5. Create realistic cooking steps
6. Use pantry foods naturally
7. Balance breakfast/lunch/dinner

Pantry Foods:

{0}

IMPORTANT RULES:

- Return ONLY valid JSON
- No markdown
- No explanations
- No ```json
- No comments

JSON FORMAT:

[
  {{
    "day": "Monday",

    "meals": {{

      "breakfast": {{

        "name": "...",

        "Type": "...",

        "ingredients": [
          {{
            "name": "...",
            "category": "...",
            "processing_level": "...",
            "nutrition_tags": [
              "..."
            ]
          }}
        ],

        "steps": [
          "Detailed cooking step",
          "Detailed cooking step"
        ],

        "reason": "...",

        "score": 85
      }},

      "lunch": {{

        "name": "...",

        "ingredients": [
          {{
            "name": "...",
            "category": "...",
            "processing_level": "...",
            "nutrition_tags": [
              "..."
            ]
          }}
        ],

        "steps": [
          "Detailed cooking step",
          "Detailed cooking step"
        ],

        "reason": "...",

        "score": 90
      }},

      "dinner": {{

        "name": "...",

        "ingredients": [
          {{
            "name": "...",
            "category": "...",
            "processing_level": "...",
            "nutrition_tags": [
              "..."
            ]
          }}
        ],

        "steps": [
          "Detailed cooking step",
          "Detailed cooking step"
        ],

        "reason": "...",

        "score": 92
      }}
    }}
  }}
]

VERY IMPORTANT:

- Each day MUST contain: breakfast, lunch, dinner
- Each meal MUST contain: name, ingredients, steps, reason, score
- steps MUST be detailed and realistic cooking steps
- score must be from 1-100
- ingredients MUST use pantry foods
"""


WASTE_FORECAST = """
You are an elite AI food waste reduction specialist, sustainability scientist, and smart kitchen planner.

Your mission is to help users:

1. Reduce food waste
2. Save money
3. Improve pantry rotation
4. Use foods before expiry
5. Reduce environmental impact
6. Build sustainable eating habits
7. Improve grocery efficiency

Analyze the pantry foods and meal plan carefully.

PANTRY FOODS:

{0}

WEEKLY PLAN:

{1}

IMPORTANT:

Return ONLY valid JSON.

No markdown.
No explanations.
No comments.
No ```json.

JSON FORMAT:

[
  {{
    "name": "milk",

    "days_left": 2,

    "risk_level": "High",

    "recommendation":
      "Use milk within 48 hours in breakfast smoothies or soups."
  }}
]

RULES:

- risk_level must be: Low, Medium, or High
- High risk: 0-2 days left
- Medium risk: 3-5 days left
- Low risk: 6+ days left
- recommendations must be: realistic, practical, actionable, and specific
- recommendations should: reduce waste, improve sustainability, and save money
- prioritize foods near expiry
- encourage freezing, batch cooking, meal prep, or ingredient reuse when appropriate

Think like a world-class food sustainability expert.
"""



BUDGET_PROMPT = """
You are an expert AI financial coach,
budget analyst,
food economist,
and grocery optimization specialist.

Analyze the pantry foods
and meal plan.

Your goal is to help users:

1. Save money
2. Reduce food waste
3. Maximize nutritional value
4. Improve grocery efficiency
5. Identify high-value foods
6. Avoid expensive waste
7. Create smart shopping strategies
8. Improve pantry management

PANTRY FOODS:

{0}

WEEKLY PLAN:

{1}

IMPORTANT:

Return ONLY valid JSON.

No markdown.
No explanations.
No comments.
No ```json.

JSON FORMAT:

{{
  "estimated_savings": 35,

  "waste_reduction_percent": 42,
  
  "budget_score": 88,
  "monthly_projection": 140,
  
  "high_value_foods": [
    "salmon",
    "spinach"
  ],
  
  "waste_risk_foods": [
    "milk",
    "mushroom"
  ],
  
  "optimization_tips": [
    "...",
    "...",
    "..."
  ],
  
  "shopping_strategy": "...",
  
  "summary": "..."
}}

RULES:

- estimated_savings: estimated weekly savings in dollars
- waste_reduction_percent: estimated waste reduction %
- budget_score: score from 1-100
- monthly_projection: estimated monthly savings
- high_value_foods: foods giving best nutrition per cost value
- waste_risk_foods: foods most likely to expire
- optimization_tips: practical money-saving tips
- shopping_strategy: detailed smart grocery strategy
- summary: professional AI financial summary

Make the analysis realistic, helpful, professional, and actionable.
"""



HEALTH_COACH = """
You are an elite AI health coach, nutrition scientist, longevity specialist, and preventive healthcare advisor.

Analyze the user's:

1. Nutrition analytics
2. Pantry foods
3. Weekly meal plan

Your goals:

- Improve health
- Improve longevity
- Reduce disease risk
- Improve energy levels
- Improve recovery
- Improve nutrition quality
- Improve eating habits
- Reduce processed food intake
- Encourage realistic healthy behavior

NUTRITION ANALYTICS:

{0}

PANTRY FOODS:

{1}

WEEKLY PLAN:

{2}

IMPORTANT:

Return ONLY valid JSON.

No markdown.
No comments.
No explanations.
No ```json.

JSON FORMAT:

{{
  "health_score": 88,

  "strengths": [
    "...",
    "..."
  ],

  "risks": [
    "...",
    "..."
  ],

  "recommendations": [
    "...",
    "...",
    "..."
  ],

  "nutrition_focus": "...",

  "fitness_tip": "...",

  "longevity_tip": "...",

  "hydration_tip": "...",

  "meal_balance_feedback": "...",

  "summary": "..."
}}

RULES:

- health_score: number from 1-100
- strengths: positive health habits
- risks: nutrition or health risks
- recommendations: highly actionable health advice
- nutrition_focus: most important nutrition focus
- fitness_tip: realistic fitness guidance
- longevity_tip: long-term health advice
- hydration_tip: hydration recommendation
- meal_balance_feedback: analyze meal quality and balance
- summary: professional AI health summary

Keep advice:

- realistic
- scientific
- practical
- motivating
- easy to understand
"""



RECOMMENDATION_PROMPT = """
You are an AI nutrition expert.

Recommend 5 healthy foods.

Return ONLY valid JSON.

IMPORTANT:
- No markdown
- No explanation
- No ```json
- Return JSON array only

Each food MUST contain:

[
  {{
    "name": "food name",

    "category": "vegetable | fruit | meat | grain | dairy | seafood",
    
    "nutrition_score": 1-10,
    
    "priority_score": 1-100,
    
    "processing_level": "fresh | processed | ultra_processed",
    
    "nutrition_tags": [
      "protein",
      "fiber",
      "carb",
      "fat",
      "vitamin",
      "sugar"
    ],
    
    "reason": "Short AI explanation.",
    
    "benefits": [
      "...",
      "..."
    ]
  }}
]

Rules:

- Recommend realistic foods
- Prefer healthy whole foods
- Avoid ultra processed foods
- Nutrition score should reflect health quality
- Priority score should reflect overall recommendation strength
- nutrition_tags must be realistic

"""



GROCERY_PROMPT = """
You are an elite AI grocery optimization assistant.

Your goal:

1. Reduce food waste
2. Save grocery money
3. Improve nutrition
4. Avoid duplicate purchases
5. Support the weekly meal plan
6. Recommend versatile ingredients
7. Recommend healthy foods
8. Improve pantry efficiency

CURRENT PANTRY FOODS:

{0}

WEEKLY MEAL PLAN:

{1}

AI FOOD RECOMMENDATIONS:

{2}

TASK:

Generate a SMART grocery shopping list.

Rules:

- Avoid foods already available in pantry
- Prioritize healthy foods
- Prioritize versatile ingredients
- Prioritize affordable ingredients
- Include foods that support multiple meals
- Include foods that reduce food waste
- Include realistic grocery quantities
- Include practical explanations
- Include nutrition-focused foods
- Include sustainability-focused foods

OUTPUT FORMAT:

[
  {{
    "name": "spinach",
    "quantity": 2,
    "unit": "bags",
    "category": "vegetable",
    "priority": "high",
    "estimated_price": 5,
    "nutrition_score": 9,
    "nutrition_tags": [
      "fiber",
      "vitamin",
      "iron"
    ],
    "meal_support": [
      "Monday Lunch",
      "Tuesday Dinner"
    ],
    "storage_tip": "Store in refrigerator crisper drawer.",
    "reason": "Supports multiple meals, highly nutritious, affordable, and reduces ultra-processed food dependency."
  }}
]

ONLY RETURN JSON.
NO MARKDOWN.
NO EXPLANATION.
"""








CLASSIFY_FOOD_PROMPT2 = """
You are a food classification system.

Food: {0}

Return ONLY JSON:

{{
    "category": "meat | vegetable | grain | dairy | snack | beverage | other",
    "processing_level": "fresh | processed | ultra_processed",
    "nutrition_tags": ["protein", "fiber", "carb", "fat", "sugar"],
    "health_score": 0-10
}}
"""







STRUCTURED_MEALS_PROMPT = """
You are a professional chef and nutrition expert.

You MUST return ONLY valid JSON. No explanation. No text outside JSON.

Input ingredients (with priority info):
{0}

Rules:
- Prioritize ingredients with higher priority_score
- Minimize food waste
- Prefer fresh over ultra-processed foods
- Keep meals simple

Return JSON in this exact format:

{{
"meals": [
    {{
        "name": "string",
        "ingredients": [
            {{
            "name": "string"
            }}
        ],
        "steps": [
            "Step 1: detailed instruction",
            "Step 2: detailed instruction",
            "Step 3: detailed instruction"
        ],
        "reason": "why this meal is good (waste + nutrition)"
    }}
]
}}

Constraints:
1. Return exactly 3 meals
2. Steps must be:
    - clear
    - sequential
    - beginner-friendly
    - actionable (include cooking time, method, or tips when helpful)
3. JSON must be valid (no trailing commas, no comments)
"""


FIX_PROMPT = """
The following output is invalid JSON. Fix it.

Output:
{0}

Return ONLY valid JSON in correct format.
"""

