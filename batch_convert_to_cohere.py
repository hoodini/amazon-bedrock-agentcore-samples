#!/usr/bin/env python3
"""
Batch convert all Bedrock notebooks to Cohere in the amazon-bedrock-agentcore-samples project.
"""

import os
import json
import re
import sys
import io
from pathlib import Path

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent / "02-use-cases"

# Inline installation for Colab
COLAB_INSTALL_TEMPLATE = """# Install required dependencies for Google Colab
!pip install -q strands-agents[openai]==1.7.1 \\
             strands-agents-tools==0.2.6 \\
             openai==1.59.7{extra_packages}

print("✓ All packages installed successfully!")"""


def update_notebook_for_cohere(notebook_path: Path) -> bool:
    """Convert a notebook to use Cohere LLM."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except Exception as e:
        print(f"  Error reading {notebook_path.name}: {e}")
        return False

    modified = False

    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue

        source = ''.join(cell['source'])

        # 1. Replace requirements.txt installation
        if 'requirements.txt' in source and 'pip install' in source:
            # Try to detect extra packages
            extra = ""
            if 'yfinance' in source or any('yfinance' in str(nb) for nb in notebook['cells']):
                extra = " \\\n             yfinance"
            if 'matplotlib' not in extra and any('matplotlib' in str(nb) for nb in notebook['cells']):
                extra += " \\\n             matplotlib"
            if 'pandas' not in extra and any('pandas' in str(nb) for nb in notebook['cells']):
                extra += " \\\n             pandas"

            new_cell = COLAB_INSTALL_TEMPLATE.format(extra_packages=extra)
            cell['source'] = [line + '\n' if i < len(new_cell.split('\n')) - 1 else line
                             for i, line in enumerate(new_cell.split('\n'))]
            modified = True

        # 2. Replace BedrockModel imports
        if 'from strands.models import BedrockModel' in source:
            new_source = source.replace(
                'from strands.models import BedrockModel',
                'from strands.models.openai import OpenAIModel\nimport os'
            )
            cell['source'] = [line + '\n' if i < len(new_source.split('\n')) - 1 else line
                             for i, line in enumerate(new_source.split('\n'))]
            modified = True

        # 3. Replace BedrockModel instantiation
        if re.search(r'BedrockModel\s*\(', source):
            # Extract parameters
            temp_match = re.search(r'temperature\s*=\s*([0-9.]+)', source)
            temperature = temp_match.group(1) if temp_match else '0.0'

            # Create Cohere model configuration
            cohere_config = f'''cohere_model = OpenAIModel(
    client_args={{
        "api_key": os.environ.get("COHERE_API_KEY", "<COHERE_API_KEY>"),
        "base_url": "https://api.cohere.ai/compatibility/v1",
    }},
    model_id="command-a-03-2025",
    params={{
        "temperature": {temperature},
        "stream_options": None
    }}
)'''
            cell['source'] = [line + '\n' if i < len(cohere_config.split('\n')) - 1 else line
                             for i, line in enumerate(cohere_config.split('\n'))]
            modified = True

    if modified:
        # Save as Cohere version
        new_name = notebook_path.stem + '_cohere' + notebook_path.suffix
        new_path = notebook_path.parent / new_name

        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)

        print(f"  ✓ Created {new_path.name}")
        return True

    return False


def update_requirements_txt(req_path: Path) -> bool:
    """Update requirements.txt to include openai extra."""
    try:
        with open(req_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"  Error reading {req_path}: {e}")
        return False

    new_lines = []
    modified = False

    for line in lines:
        # Update strands-agents to include [openai]
        if line.strip().startswith('strands-agents==') and '[openai]' not in line:
            match = re.search(r'strands-agents==(\S+)', line)
            if match:
                version = match.group(1).strip()
                new_lines.append(f'strands-agents[openai]=={version}\n')
                modified = True
                continue
        new_lines.append(line)

    # Add openai if not present
    if not any('openai==' in line for line in new_lines):
        new_lines.append('openai==1.59.7\n')
        modified = True

    if modified:
        with open(req_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"  ✓ Updated {req_path.name}")
        return True

    return False


def process_use_case(use_case_dir: Path):
    """Process a single use case directory."""
    print(f"\n{use_case_dir.name}:")

    # Find all notebooks
    notebooks = list(use_case_dir.glob("*.ipynb"))
    # Exclude already converted Cohere notebooks
    notebooks = [nb for nb in notebooks if '_cohere' not in nb.stem]

    # Find requirements.txt
    req_files = list(use_case_dir.glob("**/requirements.txt"))

    if not notebooks and not req_files:
        print("  (No notebooks or requirements.txt found)")
        return

    # Update requirements.txt files
    for req_file in req_files:
        update_requirements_txt(req_file)

    # Convert notebooks
    converted = 0
    for notebook in notebooks:
        # Check if it uses Bedrock
        try:
            with open(notebook, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'BedrockModel' in content or 'bedrock_model' in content:
                    if update_notebook_for_cohere(notebook):
                        converted += 1
        except Exception:
            pass

    if converted == 0 and notebooks:
        print("  (No Bedrock notebooks found)")


def main():
    print("=" * 60)
    print("Batch Cohere Conversion for AgentCore Samples")
    print("=" * 60)

    if not BASE_DIR.exists():
        print(f"Error: {BASE_DIR} not found")
        return 1

    use_cases = [d for d in BASE_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print(f"\nProcessing {len(use_cases)} use cases...")

    for use_case_dir in sorted(use_cases):
        process_use_case(use_case_dir)

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
