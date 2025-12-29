# Cohere LLM Migration Guide

This guide explains how to use the financial assistant labs with Cohere's LLM instead of Amazon Bedrock.

## Overview

The Strands Agents SDK supports Cohere models through the OpenAI compatibility layer. This allows you to leverage Cohere's powerful language models while maintaining the same agent architecture across all three labs.

## Files

### Lab 1: Budget Assistant
- **Original Bedrock Version**: `lab1-develop_a_personal_budget_assistant_strands_agent.ipynb`
- **New Cohere Version**: `lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb`
- **Standalone Script**: `budget_agent_cohere.py`

### Lab 2: Multi-Agent Workflows
- **Original Bedrock Version**: `lab2-build_multi_agent_workflows_with_strands.ipynb`
- **New Cohere Version**: `lab2-build_multi_agent_workflows_with_strands_cohere.ipynb`
- **Standalone Scripts**:
  - `financial_analysis_agent_cohere.py`
  - `main_cohere.py`

### Lab 3: Deployment
- **Original Bedrock Version**: `lab3-deploy_agents_on_amazon_bedrock_agentcore.ipynb` (AWS-specific)
- **New Cohere Version**: `lab3-deploy_cohere_agents_locally.ipynb` (Production deployment guide)
- **Standalone Scripts**:
  - `app.py` (FastAPI application)
  - `Dockerfile` (Container configuration)

## Key Changes

### 1. Dependencies

The `requirements.txt` has been updated to include the OpenAI compatibility layer:

```txt
strands-agents[openai]==1.7.1
openai==1.59.7
```

Install dependencies:
```bash
pip install --force-reinstall -U -r requirements.txt
```

### 2. Model Configuration

**Before (Bedrock)**:
```python
from strands.models import BedrockModel

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="us-west-2",
    temperature=0.0,
    guardrail_id=guardrail_id,
    guardrail_version="DRAFT",
    guardrail_trace="enabled",
)
```

**After (Cohere)**:
```python
from strands.models.openai import OpenAIModel
import os

cohere_model = OpenAIModel(
    client_args={
        "api_key": os.environ.get("COHERE_API_KEY", "<COHERE_API_KEY>"),
        "base_url": "https://api.cohere.ai/compatibility/v1",
    },
    model_id="command-a-03-2025",
    params={
        "temperature": 0.0,
        "stream_options": None
    }
)
```

### 3. Guardrails Removal

The Bedrock-specific guardrail functionality has been removed since it's an AWS-specific feature. If you need content filtering with Cohere, you can:

- Implement custom filtering in your application layer
- Use Cohere's built-in safety features (check Cohere documentation)
- Add middleware validation in your agent tools

### 4. API Key Setup

You need a Cohere API key. Get one from [Cohere Dashboard](https://dashboard.cohere.com/api-keys).

Set it as an environment variable:

**Linux/Mac**:
```bash
export COHERE_API_KEY="your-api-key-here"
```

**Windows (PowerShell)**:
```powershell
$env:COHERE_API_KEY="your-api-key-here"
```

**Windows (CMD)**:
```cmd
set COHERE_API_KEY=your-api-key-here
```

Or add it to a `.env` file:
```
COHERE_API_KEY=your-api-key-here
```

## Running the Notebooks

### Option 1: Google Colab (Recommended for Quick Start)

1. Upload the Cohere version notebook to [Google Colab](https://colab.research.google.com/)
2. The notebook will automatically install all required dependencies in the first cell
3. Set your Cohere API key:
   ```python
   import os
   os.environ['COHERE_API_KEY'] = 'your-api-key-here'
   ```
   Or use Colab's Secrets feature (🔑 icon in left sidebar)
4. Run all cells

**Note**: All Cohere notebooks are Colab-ready with automatic dependency installation!

### Option 2: Local Jupyter

1. Install dependencies:
   ```bash
   pip install -r colab_requirements.txt
   ```
   Or use the full requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Cohere API key (see above)

3. Open the Cohere version notebook:
   ```bash
   jupyter notebook lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb
   ```

4. Run all cells

## Running the Standalone Script

```bash
export COHERE_API_KEY="your-api-key-here"
python budget_agent_cohere.py
```

## Available Cohere Models

The notebook uses `command-a-03-2025`, but you can use other Cohere models:

- `command-a-03-2025` - Latest Command model (recommended)
- `command-r-plus` - Command R Plus
- `command-r` - Command R
- `command` - Base Command model

See [Cohere Models Documentation](https://docs.cohere.com/docs/models) for the full list.

## Features Maintained

All original functionality is preserved:

✅ **System Prompts** - Custom financial advisor persona
✅ **Conversation Management** - Context summarization
✅ **Async Streaming** - Real-time response streaming
✅ **Custom Tools** - Budget calculator, chart generator
✅ **Structured Outputs** - Pydantic model validation

## Differences from Bedrock Version

| Feature | Bedrock | Cohere |
|---------|---------|--------|
| **Model Provider** | AWS Bedrock | Cohere API |
| **Authentication** | AWS credentials | API key |
| **Guardrails** | Native support | Not available* |
| **Region** | AWS region-specific | Global API |
| **Pricing** | AWS pricing | Cohere pricing |

*You can implement custom content filtering if needed.

## Troubleshooting

### ModuleNotFoundError: No module named 'openai'

Install the OpenAI dependency:
```bash
pip install 'strands-agents[openai]'
```

### Authentication Error

Ensure your `COHERE_API_KEY` is set correctly:
```python
import os
print(os.environ.get("COHERE_API_KEY"))
```

### Unexpected Model Behavior

- Verify you're using a valid model ID from [Cohere's model list](https://docs.cohere.com/docs/models)
- Ensure `base_url` is set to `https://api.cohere.ai/compatibility/v1`
- Check that `stream_options` is set to `None` in params

## Lab-Specific Notes

### Lab 1: Budget Assistant
- Single agent with budgeting tools
- Structured output for financial reports
- Async streaming support

### Lab 2: Multi-Agent Workflows
- Orchestrator pattern with two specialized agents
- Budget agent + Financial analysis agent
- Agent-as-tool wrapper pattern
- Complex multi-agent queries

### Lab 3: Deployment
- **Important**: AWS AgentCore is AWS Bedrock-specific
- Cohere version focuses on production deployment alternatives
- Includes FastAPI application with streaming
- Docker containerization guide
- Multi-cloud deployment options (GCP, AWS, Azure)
- Kubernetes deployment manifests

## Next Steps

Once you have the agents working with Cohere, you can:

1. **Lab 1**: Experiment with different Cohere models and parameters
2. **Lab 2**: Build custom multi-agent workflows for your use case
3. **Lab 3**: Deploy to production using cloud platforms
4. Implement custom content filtering and safety measures
5. Add authentication and rate limiting
6. Set up monitoring and observability

## Resources

- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/)
- [Cohere API Documentation](https://docs.cohere.com/)
- [Cohere Models](https://docs.cohere.com/docs/models)
- [OpenAI Compatibility](https://docs.cohere.com/docs/cohere-openai-compatibility)
