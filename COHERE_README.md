# Cohere LLM Integration for Amazon Bedrock AgentCore Samples

This repository now includes **Cohere LLM** versions of all agent samples, providing an alternative to AWS Bedrock models. All Cohere-based notebooks are **Google Colab ready** with automatic dependency installation.

## 🎯 Quick Start

1. **Get Cohere API Key**: [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
2. **Upload notebook to Google Colab**: Any `*_cohere.ipynb` file
3. **Set API key** in the first cell:
   ```python
   import os
   os.environ['COHERE_API_KEY'] = 'your-api-key-here'
   ```
4. **Run all cells** - dependencies install automatically!

## 📚 Converted Use Cases

### Finance Personal Assistant (3 Labs)
**Location**: `02-use-cases/finance-personal-assistant/`

- **Lab 1**: [Budget Assistant](02-use-cases/finance-personal-assistant/lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb)
  - Personal budgeting with 50/30/20 rule
  - Financial charts and visualizations
  - Structured financial reports

- **Lab 2**: [Multi-Agent Workflows](02-use-cases/finance-personal-assistant/lab2-build_multi_agent_workflows_with_strands_cohere.ipynb)
  - Orchestrator pattern with specialist agents
  - Budget agent + Financial analysis agent
  - Stock research and portfolio management

- **Lab 3**: [Production Deployment](02-use-cases/finance-personal-assistant/lab3-deploy_cohere_agents_locally.ipynb)
  - FastAPI application with streaming
  - Docker containerization
  - Multi-cloud deployment guide

**📖 Guides**:
- [Migration Guide](02-use-cases/finance-personal-assistant/COHERE_MIGRATION.md)
- [Colab Quick Start](02-use-cases/finance-personal-assistant/COLAB_QUICKSTART.md)

### Site Reliability Agent Workshop (2 Labs Converted)
**Location**: `02-use-cases/site-reliability-agent-workshop/`

- **Lab 3a**: [Remediation Agent (Cohere)](02-use-cases/site-reliability-agent-workshop/Lab-03a-remediation-agent_cohere.ipynb)
  - Automated incident remediation
  - System diagnostics and recovery

- **Lab 4**: [Prevention Agent (Cohere)](02-use-cases/site-reliability-agent-workshop/Lab-04-prevention-agent_cohere.ipynb)
  - Proactive issue prevention
  - Predictive maintenance

## 🔧 What Was Changed

### 1. Model Configuration
**Before (Bedrock)**:
```python
from strands.models import BedrockModel

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="us-west-2",
    temperature=0.0
)
```

**After (Cohere)**:
```python
from strands.models.openai import OpenAIModel
import os

cohere_model = OpenAIModel(
    client_args={
        "api_key": os.environ.get("COHERE_API_KEY"),
        "base_url": "https://api.cohere.ai/compatibility/v1",
    },
    model_id="command-a-03-2025",
    params={
        "temperature": 0.0,
        "stream_options": None
    }
)
```

### 2. Dependencies (All requirements.txt Files Updated)
```diff
- strands-agents==1.7.1
+ strands-agents[openai]==1.7.1
+ openai==1.59.7
```

### 3. Google Colab Compatibility
All `*_cohere.ipynb` notebooks include inline dependency installation:
```python
!pip install -q strands-agents[openai]==1.7.1 \
             strands-agents-tools==0.2.6 \
             openai==1.59.7 \
             ...

print("✓ All packages installed successfully!")
```

## 📦 Updated Requirements.txt Files

The batch converter updated **all** requirements.txt files across the project:

- ✅ A2A-multi-agent-incident-response
- ✅ AWS-operations-agent
- ✅ customer-support-assistant
- ✅ customer-support-assistant-vpc
- ✅ DB-performance-analyzer
- ✅ device-management-agent
- ✅ enterprise-web-intelligence-agent
- ✅ farm-management-advisor
- ✅ finance-personal-assistant
- ✅ healthcare-appointment-agent
- ✅ local-prototype-to-agentcore
- ✅ market-trends-agent
- ✅ site-reliability-agent-workshop
- ✅ slide-deck-generator-memory-agent
- ✅ text-to-python-ide
- ✅ video-games-sales-assistant

All now support Cohere via the OpenAI compatibility layer!

## 🚀 Features Maintained

All Cohere versions maintain **100% feature parity** with Bedrock versions:

- ✅ **Strands Agent SDK**: Full agent functionality
- ✅ **Tools**: Custom tools and built-in tools
- ✅ **Streaming**: Async streaming for real-time responses
- ✅ **Conversation Management**: Context summarization
- ✅ **Structured Outputs**: Pydantic model validation
- ✅ **Multi-Agent**: Orchestrator patterns
- ✅ **Memory**: Conversation history and context

## 🆚 Cohere vs Bedrock

| Feature | Bedrock | Cohere |
|---------|---------|--------|
| **Model Provider** | AWS Bedrock | Cohere API |
| **Authentication** | AWS credentials | API key |
| **Guardrails** | Native support | Not available* |
| **Region** | AWS region-specific | Global API |
| **Pricing** | AWS pricing | Cohere pricing |
| **Deployment** | AWS AgentCore | Any cloud/local |
| **Vendor Lock-in** | High (AWS-specific) | Low (portable) |

*Custom content filtering can be implemented if needed

## 🛠️ Conversion Scripts

Two automated scripts are included for batch processing:

### `batch_convert_to_cohere.py`
Simple, focused batch converter:
- Updates all requirements.txt files
- Converts Bedrock notebooks to Cohere
- Creates Colab-compatible versions

### `convert_all_to_cohere.py`
Full-featured converter with:
- Interactive confirmation
- Detailed scanning and reporting
- Generates conversion report

**Usage**:
```bash
python batch_convert_to_cohere.py
```

## 📖 Documentation

### Main Guides
- **This File**: Overview of all Cohere conversions
- **[Finance Assistant Migration Guide](02-use-cases/finance-personal-assistant/COHERE_MIGRATION.md)**: Detailed migration instructions
- **[Colab Quick Start](02-use-cases/finance-personal-assistant/COLAB_QUICKSTART.md)**: 3-step guide for Google Colab

### External Resources
- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/)
- [Cohere API Documentation](https://docs.cohere.com/)
- [Cohere Models](https://docs.cohere.com/docs/models)
- [OpenAI Compatibility](https://docs.cohere.com/docs/cohere-openai-compatibility)

## 🎓 Getting Started

### For Finance Personal Assistant
Start with Lab 1:
1. Download [lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb](02-use-cases/finance-personal-assistant/lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb)
2. Upload to [Google Colab](https://colab.research.google.com/)
3. Set your `COHERE_API_KEY`
4. Run all cells!

Try: _"I make $5000/month and spend $800 on dining. Create a budget for me."_

### For Site Reliability Workshop
Start with Lab 3a:
1. Download [Lab-03a-remediation-agent_cohere.ipynb](02-use-cases/site-reliability-agent-workshop/Lab-03a-remediation-agent_cohere.ipynb)
2. Upload to Google Colab
3. Set your `COHERE_API_KEY`
4. Run all cells!

## 🤝 Contributing

To convert additional use cases:
1. Use the batch converter: `python batch_convert_to_cohere.py`
2. Test the Cohere notebooks in Google Colab
3. Submit a pull request

## ⚠️ Important Notes

### AWS-Specific Features
Some AWS-specific features are not available with Cohere:
- **Amazon Bedrock Guardrails**: AWS-only, implement custom filtering if needed
- **Amazon Bedrock AgentCore Runtime**: AWS-only, use alternative deployment (Docker, K8s, etc.)
- **AWS Cognito Integration**: Use alternative auth (JWT, OAuth, API keys)

### Cohere API Key
Keep your API key secure:
- ✅ Use environment variables
- ✅ Use Google Colab Secrets (🔑 icon)
- ❌ Never commit API keys to git
- ❌ Never share API keys publicly

### Rate Limits
Cohere free tier limits:
- 20 requests/minute
- 1000 requests/month
- Upgrade for production use

## 📊 Conversion Statistics

- **Total Use Cases**: 18
- **Requirements.txt Updated**: 16
- **Notebooks Converted**: 5
  - Finance Personal Assistant: 3
  - Site Reliability Workshop: 2
- **Colab-Ready**: All converted notebooks

## 🎉 Acknowledgments

- **AWS**: Original AgentCore samples and architecture
- **Strands AI**: Excellent agent SDK with multi-provider support
- **Cohere**: Powerful LLMs via OpenAI compatibility layer
- **Community**: Feedback and contributions

## 📄 License

This project maintains the original license from amazon-bedrock-agentcore-samples.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/hoodini/amazon-bedrock-agentcore-samples/issues)
- **Strands**: [Documentation](https://strandsagents.com/latest/documentation/)
- **Cohere**: [Documentation](https://docs.cohere.com/)

---

**Happy building with Cohere!** 🚀

Last Updated: December 29, 2024
