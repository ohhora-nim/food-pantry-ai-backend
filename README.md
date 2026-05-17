# The Gemma 4 Good Hackathon

## Food Pantry AI - Backend

### Developer: Ho Seok (Brandon) Oh (Username: ohhora-nim)

### Website URL

[https://food-pantry-ai-frontend.vercel.app](https://food-pantry-ai-frontend.vercel.app)

### Frontend

[food-pantry-ai-frontend](https://github.com/ohhora-nim/food-pantry-ai-frontend)

### AI Model

[Gemma 4:e2b](https://github.com/ohhora-nim/food-pantry-ai-backend/blob/main/ai/run_ollama.py)

### Install

```
$ pip install -r requirements.txt
```

### Run the app on the local machine

```
$ uvicorn app.main:app --reload
```

## Project Description

**Food Pantry AI** is an AI-powered food intelligence platform designed to help users reduce food waste, save money, improve nutrition, and make smarter daily food decisions.

The application allows users to add pantry foods with simple inputs such as food name, quantity, and expiry date. The system then analyzes those foods using a hybrid intelligence architecture: fast rule-based engines handle pantry scoring, nutrition analysis, expiry risk, and food recommendations, while Gemma AI is used on demand for creative and human-like tasks such as meal generation, coaching, summaries, and explanations.

Food Pantry AI helps users understand what foods they have, what should be used first, what meals they can prepare, and how their food choices affect health, budget, and sustainability.

**Key Features**

- Smart Pantry Management: Tracks pantry foods, expiry dates, quantities, nutrition tags, processing level, priority score, and waste risk.
- AI Meal Planning: Generates practical meal ideas using available pantry foods, prioritizing foods that are close to expiry.
- Nutrition Analytics: Analyzes food quality, fresh food ratio, processing level, nutrition tags, and pantry health score.
- Food Waste Forecasting: Identifies foods at risk of being wasted and provides actionable recommendations to use them before expiry.
- Smart Food Recommendations: Suggests healthier, budget-friendly, and versatile foods to improve pantry balance.
- AI Explanations and Coaching: Uses Gemma AI to provide human-like explanations, personalized health coaching, and pantry summaries only when users request them.

**Why It Matters**

Food waste is a global issue with serious environmental, economic, and social impact. At the same time, many people struggle to plan healthy meals, manage groceries efficiently, and understand what foods they should prioritize. Food Pantry AI addresses these problems by combining AI reasoning, nutrition intelligence, sustainability awareness, and practical meal planning into one simple application.

**Technology**

Food Pantry AI uses a modern full-stack architecture:

- Frontend: React, Tailwind CSS, Vite, React Router
- Backend: FastAPI
- AI Model: Google Gemma 4:e2b / Ollama Client
- Storage: Browser localStorage for pantry data and generated AI outputs
- Architecture: Hybrid AI system combining fast Python rule engines with on-demand generative AI

**Core Vision**

The goal of Food Pantry AI is to become a practical AI assistant for everyday food decisions:

### Eat smarter. Waste less. Save money. Live healthier.
