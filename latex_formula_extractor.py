import re
import argparse
from pathlib import Path


file_path = 'file.tex'

def extract_latex_formulas(tex_content):
    """
    Extract mathematical formulas from LaTeX content
    Supported environments:
    - Inline formulas: \(...\), $...$
    - Display formulas: \[...\], $$...$$
    - Environment formulas: \begin{equation}...\end{equation}, align, gather, etc.
    - Custom environments: \begin{env}...\end{env}
    """
    # Preprocessing: Remove comments
    tex_content = remove_comments(tex_content)

    # Store extracted formulas
    formulas = []

    # 1. Extract inline formulas: \(...\)
    formulas.extend(re.findall(r'\\\((.*?)\\\)', tex_content, re.DOTALL))

    # 2. Extract inline formulas: $...$ (non-greedy match)
    formulas.extend(re.findall(r'(?<!\\)\$(.*?)(?<!\\)\$', tex_content, re.DOTALL))

    # 3. Extract display formulas: \[...\]
    formulas.extend(re.findall(r'\\\[(.*?)\\\]', tex_content, re.DOTALL))

    # 4. Extract traditional display formulas: $$...$$
    formulas.extend(re.findall(r'\$\$(.*?)\$\$', tex_content, re.DOTALL))

    # 5. Extract environment formulas (supports nesting)
    formula_environments = [
        'equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
        'multline', 'multline*', 'flalign', 'flalign*', 'alignat', 'alignat*',
        'cases', 'matrix', 'bmatrix', 'pmatrix', 'vmatrix', 'smallmatrix'
    ]

    for env in formula_environments:
        pattern = rf'\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}'
        formulas.extend(re.findall(pattern, tex_content, re.DOTALL))

    # 6. Extract arbitrary math environments (generic pattern)
    generic_envs = re.findall(
        r'\\begin\{([^}]*)\}(.*?)\\end\{\1\}',
        tex_content,
        re.DOTALL
    )

    # Filter non-math environments
    for env_name, content in generic_envs:
        if env_name not in formula_environments and is_math_environment(env_name):
            formulas.append(content)

    # Post-processing: Clean whitespace and empty formulas
    cleaned_formulas = []
    for formula in formulas:
        formula = formula.strip()
        # Remove extra blank lines and indentation
        formula = re.sub(r'^\s*\n', '', formula, flags=re.MULTILINE)
        formula = re.sub(r'\n\s*', '\n', formula)
        if formula:
            cleaned_formulas.append(formula)

    return cleaned_formulas


def is_math_environment(env_name):
    """Check if environment name is a math environment"""
    math_env_patterns = [
        r'^eq', r'^align', r'^gather', r'^multline',
        r'^matrix', r'^cases', r'^array', r'^split'
    ]
    return any(re.match(pattern, env_name) for pattern in math_env_patterns)


def remove_comments(tex_content):
    """Remove LaTeX comments while handling escaped characters"""
    lines = []
    for line in tex_content.split('\n'):
        # Handle escaped % characters
        clean_line = []
        i = 0
        while i < len(line):
            if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '%':
                clean_line.append('\\%')
                i += 2
            elif line[i] == '%':
                break
            else:
                clean_line.append(line[i])
                i += 1
        lines.append(''.join(clean_line))
    return '\n'.join(lines)


def process_tex_file(file_path):
    """Process a single .tex file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        formulas = extract_latex_formulas(content)

        print(f"📄 Extracted {len(formulas)} formulas from {file_path}:")
        for i, formula in enumerate(formulas, 1):
            print(f"\n🔹 Formula {i}:")
            print('-' * 50)
            print(formula)
            print('-' * 50)

        return formulas
    except Exception as e:
        print(f"❌ Error processing file {file_path}: {str(e)}")
        return []


def main():
    parser = argparse.ArgumentParser(description='Extract mathematical formulas from LaTeX files')
    parser.add_argument('file_path', type=str, help='Path to .tex file')
    args = parser.parse_args()

    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    if file_path.suffix.lower() != '.tex':
        print(f"⚠️ Warning: File extension is not .tex ({file_path.suffix})")

    process_tex_file(file_path)


if __name__ == "__main__":
    main()