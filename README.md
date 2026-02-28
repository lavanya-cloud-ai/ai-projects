# 🤖 Lavanya GenAI Projects

Personal GenAI learning projects built on AWS Bedrock and Snowflake Cortex AI.
This repository showcases hands-on AI engineering POCs developed as part of my transition into AI Data Engineering.

> **Author:** Lavanya Lanka | Lead Data Integration Engineer | AI & Cloud Technologies
> **AWS Account:** lavanya-cloud-ai-lab
> **LinkedIn:** [lavanya-l-80b52a92](https://linkedin.com/in/lavanya-l-80b52a92/)

---

## 📁 Projects

| Project | Description | AWS Services |
|---|---|---|
| [🛍️ Bedrock Gift Recommendation Chatbot](#-project-1--bedrock-gift-recommendation-chatbot) | Conversational gift-finder using multi-agent collaboration | Bedrock Agents, Lambda, S3 |
| [📄 Snowflake Cortex AI Document Extraction](#-project-2--snowflake-cortex-ai-document-extraction) | AI-powered NPI & Tax ID extraction from provider contracts | Snowflake Cortex, Python |

---

## 🛍️ Project 1 — Bedrock Gift Recommendation Chatbot

A conversational AI shopping assistant that helps users find the perfect gift using
Amazon Bedrock Agents, multi-agent collaboration, RAG-based knowledge retrieval,
and personalized product recommendations.

### 💡 What It Does
- Gathers user preferences through natural conversation
- Queries a product catalog API to find matching gift items
- Manages shopping cart (add items, view cart details)
- Up-sells complementary products using Amazon Personalize
- Suggests contextual gift ideas using a Bedrock Knowledge Base (RAG)
- Coordinates everything using a multi-agent supervisor architecture

### 🏗️ Architecture

```
User
 │
 ▼
┌──────────────────────────────────┐
│         Supervisor Agent         │  ← Orchestrates all agents
│      (Amazon Bedrock Agent)      │
└───────────────┬──────────────────┘
                │
       ┌────────┴────────┐
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ Recommend-  │   │    Cart     │
│ ation Agent │   │   Agent     │
└──────┬──────┘   └──────┬──────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Product    │   │  Cart API   │
│  API        │   │  (Lambda)   │
│  (Lambda)   │   └─────────────┘
└─────────────┘
       │
       ▼
┌──────────────────┐   ┌───────────────────┐
│ Amazon           │   │ Bedrock           │
│ Personalize API  │   │ Knowledge Base    │
│ (Up-sell)        │   │ (Gift Ideas RAG)  │
└──────────────────┘   └───────────────────┘
```

### 🤖 Agent Instructions (System Prompt)
```
You are a product recommendations agent for gift products. The user is trying
to buy a gift for someone and you are trying to help identify the best product.
Do not recommend any products that are not retrieved from the products API.
Do not ask about the gender if it is obvious from the user input already.
Always start by getting the full list of products from the API so you can know
the proper filter values to be used in the API parameters.
Always use a single value for each filter field, and adhere to the filtration
values based on the first API call.
Never tell the user about the API and its details.
```

### 📦 Repository Structure

```
lavanya-genai-projects/
│
├── README.md
│
├── project1-bedrock-gift-chatbot/
│   ├── agents/
│   │   ├── recommendation_agent/
│   │   │   └── prompt_template.txt
│   │   └── cart_agent/
│   │       └── prompt_template.txt
│   ├── lambda/
│   │   ├── product_api/
│   │   │   ├── lambda_function.py
│   │   │   └── product_api_schema.json
│   │   └── cart_api/
│   │       ├── lambda_function.py
│   │       └── cart_api_schema.json
│   ├── iam/
│   │   └── bedrock_agent_trust_policy.json
│   └── docs/
│       ├── setup_guide.md
│       └── sample_conversations/
│
└── project2-snowflake-cortex-ai/
    ├── extract_npi_federal_id.sql
    ├── validation_logic.sql
    └── docs/
        └── poc_findings.md
```

### 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Agents | Amazon Bedrock Agents |
| LLM | Claude Sonnet 4.6 (Anthropic via Bedrock) |
| Knowledge Base | Amazon Bedrock Knowledge Base (RAG) |
| Personalization | Amazon Personalize (simulated API) |
| Action Groups | AWS Lambda (Python 3.12) |
| Storage | Amazon S3 |
| IAM | AWS IAM roles & policies |
| Version Control | GitHub |

### 🚀 Setup Guide

#### Prerequisites
- AWS account with Bedrock access enabled
- Python 3.12+
- Claude Sonnet 4.6 access enabled in Bedrock Model catalog
- IAM Identity Center — enable Centralized root access for AWS Marketplace subscriptions

#### Step 1 — Deploy Lambda Function
1. Go to **AWS Lambda → Create function → Author from scratch**
2. Runtime: `Python 3.12`
3. Paste code from `lambda/product_api/lambda_function.py`
4. Click **Deploy**
5. Go to **Configuration → Resource-based policy → Add permissions**
6. Principal: `bedrock.amazonaws.com` | Action: `lambda:InvokeFunction`

#### Step 2 — Create IAM Role for Bedrock Agent
1. Go to **IAM → Roles → Create role → Custom trust policy**
2. Paste trust policy from `iam/bedrock_agent_trust_policy.json`
3. Attach `AmazonBedrockFullAccess`
4. Add inline policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "*"
    }
  ]
}
```

#### Step 3 — Create Bedrock Agent
1. Go to **Amazon Bedrock → Agents → Create Agent**
2. Name: `gift-recommendation-agent`
3. Model: `Claude Sonnet 4.6`
4. Instructions: paste from `agents/recommendation_agent/prompt_template.txt`
5. Agent resource role: select your IAM role from Step 2
6. Add action group → select Lambda → paste schema
7. Click **Save → Prepare**

#### Step 4 — Test
Try: *"I want to buy a birthday gift for my mom who loves cooking"*

### 💬 Sample Conversation
```
User:    I want to buy a gift
Agent:   I'd love to help! Who is this gift for and what is the occasion?

User:    It's for my mom, her birthday. She loves cooking.
Agent:   Here are my top recommendations for your mom:

         1. 🍳 Cooking Masterclass Cookbook - $29.99 ⭐ 4.9/5
            Award-winning cookbook with 150 recipes from professional chefs.

         2. 🌿 Herb Garden Starter Kit - $32.99 ⭐ 4.5/5
            Indoor herb garden with basil, mint, parsley and cilantro.

         Would you like to add any of these to your cart?
```

### 💡 Key Learnings
- Multi-agent collaboration allows complex workflows to be broken into focused specialist agents
- Prompt engineering is critical — small changes significantly affect tool-use behavior
- RAG via Knowledge Base enriches responses with domain-specific context beyond what the LLM knows
- IAM setup requires both agent role trust policy AND Lambda resource-based policy
- AWS Marketplace subscription must be enabled at account level for Claude models
- Enable **Centralized root access** in IAM Account settings to unlock Marketplace subscriptions

---

## 📄 Project 2 — Snowflake Cortex AI Document Extraction

AI-powered extraction of provider NPI and Federal Tax IDs from 2,000+ unstructured
provider contract documents using Snowflake Cortex AI functions.

### 💡 What It Does
- Uploads provider contracts (PDF/DOCX) to Snowflake internal stage
- Uses `PARSE_DOCUMENT` to extract raw text from each document
- Applies `COMPLETE` and `EXTRACT_ANSWER` with targeted prompts to identify NPI and Tax IDs
- Validates extracted values using regex pattern checks
- Benchmarks three LLMs: Claude 3.5 Sonnet, LLaMA4 Maverick
- Cross-references results against QNXT and PDM for accuracy measurement

### 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Functions | Snowflake Cortex (PARSE_DOCUMENT, COMPLETE, EXTRACT_ANSWER) |
| Storage | Snowflake Internal Stage |
| Validation | SQL regex pattern matching |
| Language | Python, SQL |
| Models Tested | Claude 3.5 Sonnet, LLaMA4 Maverick |

### 💡 Key Learnings
- Snowflake Cortex AI functions can process large volumes of unstructured documents at scale
- Prompt engineering significantly impacts extraction accuracy across different document layouts
- Post-extraction validation with regex is essential for regulated healthcare data
- Claude 3.5 Sonnet showed highest accuracy for structured data extraction from contracts

---

## 🎯 About This Repository

This repository documents my hands-on GenAI learning journey transitioning from
Lead Data Integration Engineer into AI Data Engineering. Each project demonstrates
real-world application of AI technologies to healthcare and enterprise use cases.

**Skills demonstrated:**
- Amazon Bedrock Agents & multi-agent collaboration
- Prompt engineering & RAG pipelines
- LLM evaluation & benchmarking
- AWS Lambda, IAM, S3
- Snowflake Cortex AI functions
- Python, SQL

---

## 📄 License
This repository is for personal learning and portfolio purposes.
