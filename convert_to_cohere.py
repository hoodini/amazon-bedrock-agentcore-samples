#!/usr/bin/env python3
"""
Script to convert all Jupyter notebooks and requirements.txt files
from Amazon Bedrock to Cohere LLM using Strands Agents SDK
"""

import os
import json
import re
from pathlib import Path

def convert_requirements_file(filepath):
    """Convert a requirements.txt file to use Cohere dependencies"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already converted or if it needs conversion
        if 'strands-agents[openai]' in content:
            print(f"  [OK] Already converted: {filepath}")
            return False

        # Only convert if it has strands-agents or bedrock-related dependencies
        if 'strands-agents' not in content and 'bedrock' not in content.lower():
            print(f"  [SKIP] No relevant dependencies: {filepath}")
            return False

        # Add Cohere dependencies
        lines = content.strip().split('\n')
        new_lines = []
        strands_found = False

        for line in lines:
            # Replace strands-agents with strands-agents[openai]
            if line.strip().startswith('strands-agents') and '[openai]' not in line:
                new_lines.append('strands-agents[openai]')
                strands_found = True
            else:
                new_lines.append(line)

        # Add strands-agents-tools if strands-agents is present
        if strands_found or 'strands-agents' in content:
            if 'strands-agents-tools' not in content:
                new_lines.append('strands-agents-tools')

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines) + '\n')

        print(f"  [DONE] Converted: {filepath}")
        return True
    except Exception as e:
        print(f"  [ERROR] Error converting {filepath}: {e}")
        return False

def convert_notebook_cell(cell):
    """Convert a notebook cell from Bedrock to Cohere"""
    if cell.get('cell_type') != 'code':
        return False, cell

    source = ''.join(cell.get('source', []))
    original_source = source
    modified = False

    # Replace BedrockModel imports with OpenAIModel
    if 'from strands.models.bedrock import BedrockModel' in source:
        source = source.replace(
            'from strands.models.bedrock import BedrockModel',
            'from strands.models.openai import OpenAIModel'
        )
        modified = True

    # Replace BedrockModel instantiation with OpenAIModel for Cohere
    # Pattern: BedrockModel(model_id="...", ...)
    bedrock_pattern = r'BedrockModel\s*\(\s*model_id\s*=\s*["\']([^"\']+)["\']([^)]*)\)'

    def replace_bedrock_model(match):
        nonlocal modified
        modified = True
        original_model = match.group(1)
        other_params = match.group(2)

        # Remove guardrail-related parameters
        other_params = re.sub(r',?\s*guardrail_identifier\s*=\s*[^,)]+', '', other_params)
        other_params = re.sub(r',?\s*guardrail_version\s*=\s*[^,)]+', '', other_params)
        other_params = re.sub(r',?\s*guardrailConfig\s*=\s*\{[^}]+\}', '', other_params)

        # Build Cohere model configuration
        cohere_config = '''OpenAIModel(
    client_args={
        "api_key": os.environ.get("COHERE_API_KEY"),
        "base_url": "https://api.cohere.ai/compatibility/v1",
    },
    model_id="command-a-03-2025"'''

        if other_params.strip():
            # Clean up params
            other_params = other_params.strip()
            if other_params.startswith(','):
                other_params = other_params[1:].strip()
            if other_params:
                cohere_config += f',\n    params={{{other_params}}}'

        cohere_config += '\n)'

        return cohere_config

    source = re.sub(bedrock_pattern, replace_bedrock_model, source)

    # Add import for os if COHERE_API_KEY is used and os not imported
    if 'COHERE_API_KEY' in source and 'import os' not in source:
        # Add import at the beginning
        source = 'import os\n' + source
        modified = True

    # Update cell source if modified
    if modified:
        cell['source'] = source.split('\n')
        # Ensure each line ends with newline except last
        cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]

    return modified, cell

def convert_notebook(filepath):
    """Convert a Jupyter notebook from Bedrock to Cohere"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        modified = False
        for cell in notebook.get('cells', []):
            cell_modified, updated_cell = convert_notebook_cell(cell)
            if cell_modified:
                modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            print(f"  [DONE] Converted: {filepath}")
            return True
        else:
            print(f"  [SKIP] No changes needed: {filepath}")
            return False
    except Exception as e:
        print(f"  [ERROR] Error converting {filepath}: {e}")
        return False

def main():
    """Main conversion function"""
    root_dir = Path(__file__).parent

    print("=" * 80)
    print("Converting Amazon Bedrock AgentCore Samples to Cohere LLM")
    print("=" * 80)
    print()

    # Convert all requirements.txt files
    print("Converting requirements.txt files...")
    print("-" * 80)
    requirements_files = list(root_dir.rglob('requirements.txt'))
    requirements_converted = 0

    for req_file in requirements_files:
        if convert_requirements_file(req_file):
            requirements_converted += 1

    print(f"\nConverted {requirements_converted} requirements.txt files")
    print()

    # Convert all Jupyter notebooks
    print("Converting Jupyter notebooks...")
    print("-" * 80)
    notebook_files = list(root_dir.rglob('*.ipynb'))
    # Exclude .ipynb_checkpoints
    notebook_files = [nb for nb in notebook_files if '.ipynb_checkpoints' not in str(nb)]
    notebooks_converted = 0

    for notebook_file in notebook_files:
        if convert_notebook(notebook_file):
            notebooks_converted += 1

    print(f"\nConverted {notebooks_converted} notebook files")
    print()

    print("=" * 80)
    print("Conversion Complete!")
    print(f"Total requirements.txt converted: {requirements_converted}")
    print(f"Total notebooks converted: {notebooks_converted}")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Set COHERE_API_KEY environment variable")
    print("2. Run: pip install -r requirements.txt (in relevant directories)")
    print("3. Test notebooks with Cohere models")

if __name__ == '__main__':
    main()
