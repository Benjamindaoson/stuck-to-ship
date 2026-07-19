def test_source_type_values_are_stable():
    from models.schemas import SourceType

    assert SourceType.course_note == "course_note"
    assert SourceType.project_code == "project_code"
    assert SourceType.error_recipe == "error_recipe"
    assert SourceType.faq == "faq"


def test_citation_requires_source_path():
    from models.schemas import Citation

    citation = Citation(source_path="knowledge/courses/agent/lesson-01.md", title="Lesson 1")
    assert citation.source_path.endswith("lesson-01.md")


def test_agent_course_tables_are_registered():
    from models.db_models import Base

    table_names = set(Base.metadata.tables)
    assert "faq_entries" in table_names
    assert "error_recipes" in table_names
    assert "rag_traces" in table_names
