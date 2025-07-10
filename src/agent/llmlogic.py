from logging import getLogger

from blaxel.langgraph import bl_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.graph import RunnableConfig

from .prompts import (
    DEFAULT_REPORT_STRUCTURE,
    FINAL_SECTION_WRITER_PROMPT,
    REPORT_PLAN_QUERY_GENERATOR_PROMPT,
    REPORT_PLAN_SECTION_GENERATOR_PROMPT,
    REPORT_SECTION_QUERY_GENERATOR_PROMPT,
    SECTION_WRITER_PROMPT,
)
from .search import SearchQuery, format_search_query_results, run_search_queries
from .searchtypes import Queries, ReportState, Sections, SectionState

logger = getLogger(__name__)
model = bl_model("sandbox-openai")


async def generate_report_plan(state: ReportState, config: RunnableConfig):
    """Generate the overall plan for building the report"""
    llm = await model
    topic = state["topic"]
    logger.info(
        f"--- Generating Report Plan, report_plan_depth: {config['metadata']['report_plan_depth']} ---"
    )

    report_structure = DEFAULT_REPORT_STRUCTURE
    number_of_queries = config["metadata"]["report_plan_depth"]

    structured_llm = llm.with_structured_output(Queries)

    system_instructions_query = REPORT_PLAN_QUERY_GENERATOR_PROMPT.format(
        topic=topic,
        report_organization=report_structure,
        number_of_queries=number_of_queries,
    )

    try:
        # Generate queries
        results = structured_llm.invoke(
            [
                SystemMessage(content=system_instructions_query),
                HumanMessage(
                    content="Generate search queries that will help with planning the sections of the report."
                ),
            ]
        )
        # Convert SearchQuery objects to strings
        query_list = [
            query.search_query if isinstance(query, SearchQuery) else str(query)
            for query in results.queries
        ]
        # Search web and ensure we wait for results
        search_docs = await run_search_queries(
            query_list, num_results=5, include_raw_content=False
        )
        if not search_docs:
            logger.warning("Warning: No search results returned")
            search_context = "No search results available."
        else:
            search_context = format_search_query_results(
                search_docs, include_raw_content=False
            )
        # Generate sections
        system_instructions_sections = REPORT_PLAN_SECTION_GENERATOR_PROMPT.format(
            topic=topic,
            report_organization=report_structure,
            search_context=search_context,
        )
        structured_llm = llm.with_structured_output(Sections)
        report_sections = structured_llm.invoke(
            [
                SystemMessage(content=system_instructions_sections),
                HumanMessage(
                    content="Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. Each section must have: name, description, plan, research, and content fields."
                ),
            ]
        )

        logger.info("--- Generating Report Plan Completed ---")
        return {"sections": report_sections.sections}

    except Exception as e:
        logger.error(f"Error in generate_report_plan: {e}")
        return {"sections": []}


async def generate_queries(state: SectionState):
    """Generate search queries for a specific report section"""

    # Get state
    llm = await model
    section = state["section"]
    logger.info("--- Generating Search Queries for Section: " + section.name + " ---")
    # Get configuration
    number_of_queries = 5
    # Generate queries
    structured_llm = llm.with_structured_output(Queries)
    # Format system instructions
    system_instructions = REPORT_SECTION_QUERY_GENERATOR_PROMPT.format(
        section_topic=section.description, number_of_queries=number_of_queries
    )
    # Generate queries
    user_instruction = "Generate search queries on the provided topic."
    search_queries = structured_llm.invoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(content=user_instruction),
        ]
    )

    logger.info(
        "--- Generating Search Queries for Section: " + section.name + " Completed ---"
    )
    return {"search_queries": search_queries.queries}


async def search_web(state: SectionState):
    """Search the web for each query, then return a list of raw sources and a formatted string of sources."""

    # Get state
    search_queries = state["search_queries"]
    logger.info("--- Searching Web for Queries ---")
    # Web search
    query_list = [query.search_query for query in search_queries]
    search_docs = await run_search_queries(
        search_queries, num_results=6, include_raw_content=True
    )
    # Deduplicate and format sources
    search_context = format_search_query_results(
        search_docs, max_tokens=4000, include_raw_content=True
    )

    logger.info("--- Searching Web for Queries Completed ---")
    return {"source_str": search_context}


async def write_section(state: SectionState):
    """Write a section of the report"""
    llm = await model

    # Get state
    section = state["section"]
    source_str = state["source_str"]
    logger.info("--- Writing Section : " + section.name + " ---")
    # Format system instructions
    system_instructions = SECTION_WRITER_PROMPT.format(
        section_title=section.name,
        section_topic=section.description,
        context=source_str,
    )
    # Generate section
    user_instruction = "Generate a report section based on the provided sources."
    section_content = llm.invoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(content=user_instruction),
        ]
    )
    # Write content to the section object
    section.content = section_content.content

    logger.info("--- Writing Section : " + section.name + " Completed ---")
    # Write the updated section to completed sections
    return {"completed_sections": [section]}


async def write_final_sections(state: SectionState):
    """Write the final sections of the report, which do not require web search and use the completed sections as context"""
    llm = await model
    # Get state
    section = state["section"]
    completed_report_sections = state["report_sections_from_research"]

    logger.info("--- Writing Final Section: " + section.name + " ---")
    # Format system instructions
    system_instructions = FINAL_SECTION_WRITER_PROMPT.format(
        section_title=section.name,
        section_topic=section.description,
        context=completed_report_sections,
    )

    # Generate section
    user_instruction = "Craft a report section based on the provided sources."
    section_content = llm.invoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(content=user_instruction),
        ]
    )

    # Write content to section
    section.content = section_content.content

    logger.info("--- Writing Final Section: " + section.name + " Completed ---")
    # Write the updated section to completed sections
    return {"completed_sections": [section]}
