from logging import getLogger

from langgraph.constants import Send

from .searchtypes import ReportState, Section

logger = getLogger(__name__)


def parallelize_section_writing(state: ReportState):
    """This is the "map" step when we kick off web research for some sections of the report in parallel and then write the section"""

    # Kick off section writing in parallel via Send() API for any sections that require research
    return [
        Send(
            "section_builder_with_web_search",  # name of the subagent node
            {"section": s},
        )
        for s in state["sections"]
        if s.research
    ]


def format_sections(sections: list[Section]) -> str:
    """Format a list of report sections into a single text string"""
    formatted_str = ""
    for idx, section in enumerate(sections, 1):
        formatted_str += f"""
{"=" * 60}
Section {idx}: {section.name}
{"=" * 60}
Description:
{section.description}
Requires Research:
{section.research}

Content:
{section.content if section.content else "[Not yet written]"}

"""
    return formatted_str


def format_completed_sections(state: ReportState):
    """Gather completed sections from research and format them as context for writing the final sections"""

    logger.info("--- Formatting Completed Sections ---")
    # List of completed sections
    completed_sections = state["completed_sections"]
    # Format completed section to str to use as context for final sections
    completed_report_sections = format_sections(completed_sections)

    logger.info("--- Formatting Completed Sections is Done ---")
    return {"report_sections_from_research": completed_report_sections}


def compile_final_report(state: ReportState):
    """Compile the final report"""

    # Get sections
    sections = state["sections"]
    completed_sections = {s.name: s.content for s in state["completed_sections"]}

    logger.info("--- Compiling Final Report ---")
    # Update sections with completed content while maintaining original order
    for section in sections:
        section.content = completed_sections[section.name]

    # Compile final report
    all_sections = "\n\n".join([s.content for s in sections])
    # Escape unescaped $ symbols to display properly in Markdown
    formatted_sections = all_sections.replace(
        "\\$", "TEMP_PLACEHOLDER"
    )  # Temporarily mark already escaped $
    formatted_sections = formatted_sections.replace("$", "\\$")  # Escape all $
    formatted_sections = formatted_sections.replace(
        "TEMP_PLACEHOLDER", "\\$"
    )  # Restore originally escaped $

    # Now escaped_sections contains the properly escaped Markdown text
    logger.info("--- Compiling Final Report Done ---")
    return {"final_report": formatted_sections}


def parallelize_final_section_writing(state: ReportState):
    """Write any final sections using the Send API to parallelize the process"""

    # Kick off section writing in parallel via Send() API for any sections that do not require research
    return [
        Send(
            "write_final_sections",
            {
                "section": s,
                "report_sections_from_research": state["report_sections_from_research"],
            },
        )
        for s in state["sections"]
        if not s.research
    ]
