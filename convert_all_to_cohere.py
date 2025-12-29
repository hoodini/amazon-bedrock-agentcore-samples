#!/usr/bin/env python3
"""
Comprehensive script to convert all Amazon Bedrock AgentCore samples to use Cohere LLM.

This script:
1. Scans all use-case folders for notebooks and requirements.txt files
2. Converts BedrockModel to OpenAIModel with Cohere configuration
3. Updates requirements.txt to include strands-agents[openai]
4. Creates Colab-compatible versions of notebooks
5. Generates migration documentation
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Base directory
BASE_DIR = Path(__file__).parent / "02-use-cases"

# Cohere model configuration template
COHERE_MODEL_TEMPLATE = '''cohere_model = OpenAIModel(
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

# Inline installation for Colab
COLAB_INSTALL_CELL = """# Install required dependencies for Google Colab
!pip install -q strands-agents[openai]==1.7.1 \\
             strands-agents-tools==0.2.6 \\
             openai==1.59.7 \\
             matplotlib \\
             pandas \\
             pydantic

print("✓ All packages installed successfully!")"""


class CohereConverter:
    def __init__(self, use_case_dir: Path):
        self.use_case_dir = use_case_dir
        self.use_case_name = use_case_dir.name
        self.notebooks = list(use_case_dir.glob("*.ipynb"))
        self.requirements_files = list(use_case_dir.glob("**/requirements.txt"))

    def scan(self) -> Dict:
        """Scan the use case for convertible content."""
        return {
            "name": self.use_case_name,
            "path": str(self.use_case_dir),
            "notebooks": [str(nb) for nb in self.notebooks],
            "requirements": [str(req) for req in self.requirements_files],
            "has_bedrock": self._check_bedrock_usage(),
        }

    def _check_bedrock_usage(self) -> bool:
        """Check if any notebook uses BedrockModel."""
        for notebook_path in self.notebooks:
            try:
                with open(notebook_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'BedrockModel' in content or 'bedrock' in content.lower():
                        return True
            except Exception:
                pass
        return False

    def update_requirements(self):
        """Update requirements.txt files to include openai extra."""
        for req_file in self.requirements_files:
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                updated = False
                new_lines = []

                for line in lines:
                    # Update strands-agents line to include [openai]
                    if line.strip().startswith('strands-agents==') and '[openai]' not in line:
                        # Extract version
                        match = re.search(r'strands-agents==(\S+)', line)
                        if match:
                            version = match.group(1)
                            new_lines.append(f'strands-agents[openai]=={version}\n')
                            updated = True
                            continue
                    new_lines.append(line)

                # Add openai if not present
                if not any('openai==' in line for line in new_lines):
                    new_lines.append('openai==1.59.7\n')
                    updated = True

                if updated:
                    with open(req_file, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"  ✓ Updated {req_file}")

            except Exception as e:
                print(f"  ✗ Error updating {req_file}: {e}")

    def convert_notebook(self, notebook_path: Path) -> bool:
        """Convert a single notebook to use Cohere."""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)

            modified = False

            # Update cells
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])

                    # Replace requirements.txt installation
                    if 'requirements.txt' in source and 'pip install' in source:
                        cell['source'] = COLAB_INSTALL_CELL.split('\n')
                        cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line
                                         for i, line in enumerate(cell['source'])]
                        modified = True

                    # Replace BedrockModel imports
                    if 'from strands.models import BedrockModel' in source:
                        new_source = source.replace(
                            'from strands.models import BedrockModel',
                            'from strands.models.openai import OpenAIModel\nimport os'
                        )
                        cell['source'] = new_source.split('\n')
                        cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line
                                         for i, line in enumerate(cell['source'])]
                        modified = True

                    # Replace BedrockModel configuration
                    if 'BedrockModel(' in source:
                        # Extract temperature if present
                        temp_match = re.search(r'temperature\s*=\s*([0-9.]+)', source)
                        temperature = temp_match.group(1) if temp_match else '0.0'

                        # Simple replacement - create new cell content
                        new_source = COHERE_MODEL_TEMPLATE.format(temperature=temperature)
                        cell['source'] = new_source.split('\n')
                        cell['source'] = [line + '\n' if i < len(cell['source']) - 1 else line
                                         for i, line in enumerate(cell['source'])]
                        modified = True

            if modified:
                # Save as new Cohere version
                new_name = notebook_path.stem + '_cohere' + notebook_path.suffix
                new_path = notebook_path.parent / new_name

                with open(new_path, 'w', encoding='utf-8') as f:
                    json.dump(notebook, f, indent=1, ensure_ascii=False)

                print(f"  ✓ Created {new_path.name}")
                return True

            return False

        except Exception as e:
            print(f"  ✗ Error converting {notebook_path}: {e}")
            return False


def scan_all_use_cases() -> List[Dict]:
    """Scan all use cases and return their information."""
    use_cases = []

    for item in BASE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            converter = CohereConverter(item)
            info = converter.scan()
            if info['notebooks'] or info['requirements']:
                use_cases.append(info)

    return use_cases


def generate_report(use_cases: List[Dict]) -> str:
    """Generate a markdown report of all use cases."""
    report = ["# Cohere Conversion Report\n"]
    report.append(f"Total use cases scanned: {len(use_cases)}\n\n")

    bedrock_cases = [uc for uc in use_cases if uc['has_bedrock']]
    report.append(f"Use cases with Bedrock: {len(bedrock_cases)}\n\n")

    report.append("## Use Cases\n\n")

    for uc in use_cases:
        report.append(f"### {uc['name']}\n")
        report.append(f"- Notebooks: {len(uc['notebooks'])}\n")
        report.append(f"- Requirements files: {len(uc['requirements'])}\n")
        report.append(f"- Uses Bedrock: {'✓' if uc['has_bedrock'] else '✗'}\n")

        if uc['notebooks']:
            report.append("\n**Notebooks:**\n")
            for nb in uc['notebooks']:
                report.append(f"- {Path(nb).name}\n")

        report.append("\n")

    return ''.join(report)


def main():
    print("=" * 60)
    print("Amazon Bedrock AgentCore to Cohere Converter")
    print("=" * 60)
    print()

    # Scan all use cases
    print("[*] Scanning all use cases...")
    use_cases = scan_all_use_cases()
    print(f"Found {len(use_cases)} use cases\n")

    # Generate report
    report = generate_report(use_cases)
    report_path = BASE_DIR.parent / "COHERE_CONVERSION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Generated report: {report_path}\n")

    # Ask user for confirmation
    bedrock_cases = [uc for uc in use_cases if uc['has_bedrock']]
    print(f"Found {len(bedrock_cases)} use cases with Bedrock models")
    print("\nDo you want to convert all use cases? (y/n): ", end='')

    response = input().strip().lower()
    if response != 'y':
        print("Conversion cancelled.")
        return 0

    print("\n[*] Converting use cases...\n")

    # Convert each use case
    converted_count = 0
    for uc_info in bedrock_cases:
        print(f"Converting: {uc_info['name']}")
        use_case_dir = Path(uc_info['path'])
        converter = CohereConverter(use_case_dir)

        # Update requirements
        converter.update_requirements()

        # Convert notebooks
        for notebook_path in converter.notebooks:
            if converter.convert_notebook(Path(notebook_path)):
                converted_count += 1

        print()

    print("=" * 60)
    print(f"✓ Conversion complete!")
    print(f"  - Converted {converted_count} notebooks")
    print(f"  - Updated {sum(len(uc['requirements']) for uc in use_cases)} requirements files")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nConversion cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
