# Google Colab Quick Start Guide

This guide shows you how to run the Cohere-based financial assistant notebooks in Google Colab with zero setup required.

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your Cohere API Key

1. Visit [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
2. Sign up or log in
3. Copy your API key

### Step 2: Upload Notebook to Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File → Upload notebook**
3. Choose one of these notebooks:
   - `lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb` (Start here!)
   - `lab2-build_multi_agent_workflows_with_strands_cohere.ipynb`
   - `lab3-deploy_cohere_agents_locally.ipynb`

### Step 3: Set Your API Key and Run

**Option A: In the first code cell (Quick & Easy)**
```python
import os
os.environ['COHERE_API_KEY'] = 'your-api-key-here'  # Replace with your actual key
```

**Option B: Using Colab Secrets (Secure)**
1. Click the 🔑 **Secrets** icon in the left sidebar
2. Click **+ Add new secret**
3. Name: `COHERE_API_KEY`
4. Value: paste your API key
5. Toggle it ON for this notebook
6. In the first code cell:
```python
from google.colab import userdata
import os
os.environ['COHERE_API_KEY'] = userdata.get('COHERE_API_KEY')
```

Then **run all cells** (Runtime → Run all)!

## 📚 What Each Lab Teaches

### Lab 1: Personal Budget Assistant
**Best for**: Learning the basics of Strands Agents with Cohere

**You'll build**:
- A budget agent that calculates 50/30/20 budgets
- Tools for financial analysis and visualization
- Structured outputs for financial reports
- Async streaming for real-time responses

**Try this**: "I make $5000/month and spend $800 on dining. Create a budget for me."

### Lab 2: Multi-Agent Workflows
**Best for**: Understanding agent orchestration patterns

**You'll build**:
- Budget Agent: Spending analysis and budgeting
- Financial Analysis Agent: Stock research and portfolios
- Orchestrator Agent: Coordinates both specialists

**Try this**: "Compare Tesla and Apple stocks, and tell me if I can invest $2000 with my $4000/month income."

### Lab 3: Production Deployment
**Best for**: Deploying agents to production

**You'll learn**:
- FastAPI application with REST endpoints
- Docker containerization
- Cloud deployment (GCP, AWS, Azure, Kubernetes)
- Monitoring and security best practices

## 💡 Tips for Colab

### Installing Dependencies
The first cell automatically installs all required packages:
```python
!pip install -q strands-agents[openai]==1.7.1 \
             strands-agents-tools==0.2.6 \
             openai==1.59.7 \
             yfinance==0.2.65 \
             matplotlib==3.10.6 \
             pandas==2.3.2 \
             pydantic==2.11.7
```

**This takes about 30-60 seconds.** ☕ Grab a coffee!

### Viewing Charts
Financial charts will display inline in Colab. No additional setup needed!

### Saving Your Work
- **File → Save a copy in Drive** to save your progress
- **File → Download → Download .ipynb** to save locally

### Runtime Disconnections
If your runtime disconnects:
1. Reconnect: **Runtime → Reconnect**
2. Re-run the first cell to reinstall dependencies
3. Set your API key again
4. Continue where you left off!

## 🎯 Example Session

Here's what a typical Colab session looks like:

```python
# Cell 1: Install dependencies (auto-included in notebook)
!pip install -q strands-agents[openai]==1.7.1 ...
# Output: ✓ All packages installed successfully!

# Cell 2: Set API key
import os
os.environ['COHERE_API_KEY'] = 'your-key-here'

# Cell 3: Import and configure
from strands import Agent, tool
from strands.models.openai import OpenAIModel

cohere_model = OpenAIModel(
    client_args={
        "api_key": os.environ.get("COHERE_API_KEY"),
        "base_url": "https://api.cohere.ai/compatibility/v1",
    },
    model_id="command-a-03-2025",
    params={"temperature": 0.0, "stream_options": None}
)

# Cell 4: Create agent
budget_agent = Agent(model=cohere_model, system_prompt=BUDGET_SYSTEM_PROMPT)

# Cell 5: Test it!
response = budget_agent("I make $6000/month. Help me create a budget.")
print(response)
# Output: Your personalized budget with recommendations!
```

## 🔧 Troubleshooting

### "Module not found" error
- **Solution**: Re-run the first cell to install dependencies
- Colab sometimes needs a fresh installation after disconnecting

### "Invalid API key" error
- **Solution**: Double-check your COHERE_API_KEY
- Make sure there are no extra spaces or quotes
- Verify the key is active at [Cohere Dashboard](https://dashboard.cohere.com/api-keys)

### Charts not displaying
- **Solution**: Make sure you ran the matplotlib import cell
- Try restarting the runtime: **Runtime → Restart runtime**

### "Rate limit exceeded"
- **Solution**: You've hit Cohere's API rate limits
- Wait a few minutes or upgrade your Cohere plan
- Free tier: 20 requests/minute, 1000 requests/month

## 📖 Next Steps

After completing the labs:

1. **Experiment**: Try different prompts and use cases
2. **Customize**: Modify the system prompts for your needs
3. **Extend**: Add new tools and capabilities
4. **Deploy**: Follow Lab 3 to deploy to production
5. **Share**: Save to Drive and share with your team!

## 🆘 Need Help?

- **Documentation**: [Strands Agents Docs](https://strandsagents.com/latest/documentation/)
- **Cohere Docs**: [Cohere Documentation](https://docs.cohere.com/)
- **Issues**: [Report on GitHub](https://github.com/hoodini/amazon-bedrock-agentcore-samples/issues)

## 🎉 Have Fun!

You're now ready to build sophisticated multi-agent financial advisory systems using Cohere in Google Colab. No local setup, no environment hassles - just upload and run!

Happy coding! 🚀
