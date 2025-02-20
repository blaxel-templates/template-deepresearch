import os
from logging import getLogger
from typing import Union

from blaxel.agents import agent
from fastapi import Request
from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import CompiledGraph, RunnableConfig
from rich.console import Console
from rich.markdown import Markdown as RichMarkdown

from llmlogic import (generate_queries, generate_report_plan, search_web,
                      write_final_sections, write_section)
from searchtypes import (ReportState, ReportStateInput, ReportStateOutput,
                         SectionOutputState, SectionState)
from writer import (compile_final_report, format_completed_sections,
                    parallelize_final_section_writing,
                    parallelize_section_writing)

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
builder.add_conditional_edges("generate_report_plan",
                              parallelize_section_writing,
                              ["section_builder_with_web_search"])
builder.add_edge("section_builder_with_web_search", "format_completed_sections")
builder.add_conditional_edges("format_completed_sections",
                              parallelize_final_section_writing,
                              ["write_final_sections"])
builder.add_edge("write_final_sections", "compile_final_report")
builder.add_edge("compile_final_report", END)

reporter_agent = builder.compile()

@agent(
    agent={
        "metadata": {
            "name": "template-deepresearch",
        },
        "spec": {
            "model": "gpt-4o",
            "description": "",
            "runtime": {
                "envs": [
                    {
                        "name": "TAVILY_API_KEY",
                        "value": "${secrets.TAVILY_API_KEY}",
                    }
                ]
            },
        },
    },
    override_agent=reporter_agent
)
async def main(request: Request, agent: CompiledGraph):
    body = await request.json()
    console = Console()
    if body.get("inputs"):
        body["input"] = body["inputs"]

    recursion_limit = body.get("recursion_limit", 50)
    report_plan_depth = body.get("report_plan_depth", 8)
    config = RunnableConfig(
        recursion_limit=recursion_limit,
        metadata={
            "report_plan_depth": report_plan_depth
        }
    )
    message = {"topic" : body["input"]}
    events = agent.astream(message, config, stream_mode="values")

    async for event in events:
        for k, v in event.items():
            if os.getenv("VERBOSE"):
                if k != "__end__":
                    console.print(RichMarkdown(repr(k) + ' -> ' + repr(v)))
            if k == 'final_report':
                logger.info('='*50)
                logger.info('Final Report:')
                return v
    return "No report found, you probably have an issue with tavily or openai connection"