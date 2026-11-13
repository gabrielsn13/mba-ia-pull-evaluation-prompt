"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

PROMPT_FILE = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")


@pytest.fixture(scope="module")
def prompt():
    return load_prompts(PROMPT_FILE)["bug_to_user_story_v2"]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert prompt.get("system_prompt", "").strip()

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert "Você é um" in prompt["system_prompt"]

    def test_prompt_mentions_format(self, prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        text = prompt["system_prompt"]
        assert "Como um" in text and "eu quero" in text and "para que" in text
        assert "Dado que" in text and "Quando" in text and "Então" in text

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        text = prompt["system_prompt"]
        assert text.count("Relato:") >= 2
        assert text.count("Resposta:") >= 2

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        assert "[TODO]" not in prompt["system_prompt"]
        assert "[TODO]" not in prompt.get("user_prompt", "")

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        assert len(prompt.get("techniques_applied", [])) >= 2

    def test_prompt_structure_is_valid(self, prompt):
        """Valida a estrutura geral via utils."""
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, errors

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])