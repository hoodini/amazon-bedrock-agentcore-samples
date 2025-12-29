#!/usr/bin/env python3
"""
Update Cohere notebooks to be Google Colab compatible by replacing
requirements.txt installation with direct pip install commands.
"""

import json
import sys

# The installation cell content
COLAB_INSTALL_CELL = """# Install required dependencies for Google Colab
# This downloads the colab requirements file and installs all necessary packages

!wget -q https://raw.githubusercontent.com/hoodini/amazon-bedrock-agentcore-samples/main/02-use-cases/finance-personal-assistant/colab_requirements.txt
!pip install -q -r colab_requirements.txt

print("✓ All packages installed successfully!")"""

# Alternative inline installation (if wget fails)
INLINE_INSTALL_CELL = """# Install required dependencies directly
!pip install -q strands-agents[openai]==1.7.1 \\
             strands-agents-tools==0.2.6 \\
             openai==1.59.7 \\
             yfinance==0.2.65 \\
             matplotlib==3.10.6 \\
             pandas==2.3.2 \\
             pydantic==2.11.7

print("✓ All packages installed successfully!")"""


def update_notebook(notebook_path):
    """Update a notebook to use Colab-compatible installation."""
    print(f"Updating {notebook_path}...")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Find and replace the installation cell
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'requirements.txt' in source and 'pip install' in source:
                # Replace with Colab-compatible installation
                cell['source'] = INLINE_INSTALL_CELL.split('\n')
                # Add newline to each line except the last
                cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line
                                 for i, line in enumerate(cell['source'])]
                print(f"  ✓ Updated installation cell")
                break

    # Write back the notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"  ✓ Saved {notebook_path}")


def main():
    notebooks = [
        'lab1-develop_a_personal_budget_assistant_strands_agent_cohere.ipynb',
        'lab2-build_multi_agent_workflows_with_strands_cohere.ipynb',
        'lab3-deploy_cohere_agents_locally.ipynb',
    ]

    for notebook in notebooks:
        try:
            update_notebook(notebook)
        except Exception as e:
            print(f"  ✗ Error updating {notebook}: {e}", file=sys.stderr)
            return 1

    print("\n✓ All notebooks updated successfully!")
    print("\nYou can now upload these notebooks to Google Colab and they will install dependencies automatically.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
