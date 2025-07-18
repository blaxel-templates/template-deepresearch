from logging import getLogger

from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import RunnableConfig

from ..inputs import DeepSearchInput
from .llmlogic import (
    generate_queries,
    generate_report_plan,
    search_web,
    write_final_sections,
    write_section,
)
from .searchtypes import (
    ReportState,
    ReportStateInput,
    ReportStateOutput,
    SectionOutputState,
    SectionState,
)
from .writer import (
    compile_final_report,
    format_completed_sections,
    parallelize_final_section_writing,
    parallelize_section_writing,
)

logger = getLogger(__name__)

# Add nodes and edges
section_builder = StateGraph(SectionState, output=SectionOutputState)
section_builder.add_node("generate_queries", generate_queries)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)
section_builder.add_edge(START, "generate_queries")
section_builder.add_edge("generate_queries", "search_web")
section_builder.add_edge("search_web", "write_section")
section_builder.add_edge("write_section", END)
section_builder_subagent = section_builder.compile()

builder = StateGraph(ReportState, input=ReportStateInput, output=ReportStateOutput)

builder.add_node("generate_report_plan", generate_report_plan)
builder.add_node("section_builder_with_web_search", section_builder_subagent)
builder.add_node("format_completed_sections", format_completed_sections)
builder.add_node("write_final_sections", write_final_sections)
builder.add_node("compile_final_report", compile_final_report)

builder.add_edge(START, "generate_report_plan")
builder.add_conditional_edges(
    "generate_report_plan",
    parallelize_section_writing,
    ["section_builder_with_web_search"],
)
builder.add_edge("section_builder_with_web_search", "format_completed_sections")
builder.add_conditional_edges(
    "format_completed_sections",
    parallelize_final_section_writing,
    ["write_final_sections"],
)
builder.add_edge("write_final_sections", "compile_final_report")
builder.add_edge("compile_final_report", END)

reporter_agent = builder.compile()


async def agent(request: DeepSearchInput):
    config = RunnableConfig(
        recursion_limit=request.recursion_limit,
        metadata={
            "report_plan_depth": request.report_plan_depth,
        },
    )
    message = {"topic": request.inputs}

    # Stream both custom logs and final values
    events = reporter_agent.astream(message, config, stream_mode=["custom", "values"])

    async for mode, event in events:
        if mode == "custom":
            # Handle custom logs from nodes
            if "log" in event:
                yield f"{event['level']}: {event['log']}\n"
        elif mode == "values":
            # Handle state updates including final report
            for k, v in event.items():
                if k == "final_report":
                    yield "INFO: Final Report\n"
                    yield v
                    return

    yield "No report found, you probably have an issue with tavily or openai connection\n"
