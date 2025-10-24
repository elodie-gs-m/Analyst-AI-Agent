# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 11:43:44 2025

@author: elodi
"""

#%% Import Packages
import os
import streamlit as st
from pydantic import BaseModel, Field
from pydantic import ValidationError
from typing import List
from pydantic_ai import Agent, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from typing import Annotated
import asyncio
from datetime import datetime
from dataclasses import dataclass, field
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from contextlib import redirect_stdout
from typing import Dict
import json

# %% Initialize Model
analyst_agent: Agent

@dataclass
class State:
    user_query: str = field(default_factory=str)
    file_name: str = field(default_factory=str)
    column_dict: str = field(default_factory=str)

def init_agent(api_key: str):
    global analyst_agent
    model = OpenAIModel('gpt-4.1', provider=OpenAIProvider(api_key=api_key))
    analyst_agent = Agent(
        model=model,
        tools=[
            Tool(get_columns, takes_ctx=False),
            Tool(get_column_description, takes_ctx=False),
            Tool(graph_generator, takes_ctx=False),
            Tool(python_execution_tool, takes_ctx=False)
        ],
        deps_type=State,
        instrument=True
    )

    
    @analyst_agent.system_prompt
    async def get_analyst_agent_system_prompt(ctx: RunContext[State]):
        prompt = f"""
        You are an expert data analyst agent responsible for executing comprehensive data analysis workflows and generating professional analytical reports.
        **Your Mission:**
        Analyze the provided dataset to answer the user's query through systematic data exploration, statistical analysis, and visualization. Deliver actionable insights through a comprehensive report backed by quantitative evidence.
        **Available Tools:**
            - `get_columns`: Retrieve all column names from the dataset
            - `get_column_description`: Get detailed descriptions and metadata for specific columns  
            - `graph_generator`: Create visualizations (charts, plots, graphs) and save them in HTML and PNG formats. Use plotly express library to make the graph interactive.
            - `python_execution_tool`: Execute Python code for statistical calculations, data processing, and metric computation
            
        **Input Context:**
            - User Query: {ctx.deps.user_query}
            - Dataset File Name: {ctx.deps.file_name}
            - Dataset Metadata: {ctx.deps.column_dict}

        **Execution Workflow:**
            **CRITICAL**: State is not persistent between tool calls. Always reload the dataset and import necessary libraries in each Python execution.
                1. **Dataset Discovery**: Use `get_columns` to retrieve all available columns, then use `get_column_description` to understand column meanings and data types.

                2. **Analysis Planning**: Based on the user query and dataset structure, create a systematic analysis plan identifying:
                    - Key variables to examine
                    - Statistical methods to apply
                    - Visualizations to create
                    - Metrics to calculate

                3. **Data Exploration**: Load the dataset using pandas and perform initial exploration:
                    - Check data shape, types, and quality
                    - Identify missing values and outliers
                    - Generate descriptive statistics

                4. **Statistical Analysis**: Execute the planned analysis using appropriate statistical methods:
                    - Calculate relevant metrics and aggregations
                    - Perform hypothesis testing if applicable
                    - Identify patterns, trends, and correlations

                5. **Visualization Creation**: Generate meaningful visualizations that support your findings:
                    - Use appropriate chart types for the data
                    - Ensure visualizations are clear and informative
                    - Save outputs in both HTML and PNG formats

                6. **Report Synthesis**: Compile all findings into a comprehensive analytical report.

        **Tool Usage Best Practices:**

            **python_execution_tool**:
                - Always include necessary imports: `import pandas as pd`, `import numpy as np`, `import matplotlib.pyplot as plt`, `import seaborn as sns`
                - Load dataset fresh each time: `df = pd.read_csv('{ctx.deps.file_name}')`
                - Use descriptive variable names and clear print statements
                - Format output: `print(f"The calculated value for {{metric_name}} is {{value}}")`
                - Handle errors gracefully with try-except blocks

            **graph_generator**:
                - Always include necessary imports and dataset loading
                - Create publication-quality visualizations with proper labels, titles, and legends
                - Save graphs using: `plt.savefig('graph.png', dpi=300, bbox_inches='tight')` and HTML equivalent
                - Print file paths in the required format: `print("The graph path in html format is <path.html> and the graph path in png format is <path.png>")`

            **get_columns & get_column_description**:
                - Use these tools first to understand the dataset structure
                - Reference column information when planning analysis steps

        **Output Requirements:**
            Your final output must include:

            - **analysis_report**: Professional markdown report containing:
                * Executive Summary (key findings in 2-3 sentences)
                * Dataset Overview (structure, size, key variables)
                * Methodology (analytical approach taken)
                * Detailed Findings (organized by analysis steps)
                * Statistical Results (with proper interpretation)
                * Data Quality Assessment (missing values, outliers, limitations)
                * Insights and Implications

            - **metrics**: List of all calculated numerical values with descriptive labels

            - **image_html_path**: Path to HTML visualization file (empty string if none generated)

            - **image_png_path**: Path to PNG visualization file (empty string if none generated)

            - **conclusion**: Concise summary with actionable recommendations
            You must return a JSON object matching these headers.  Do not include any explanations or markdown outside the JSON object.

        **Quality Standards:**
            - Use professional, data-driven language
            - Provide statistical context and significance levels
            - Explain methodologies and any assumptions made
            - Include confidence intervals where appropriate
            - Reference specific data points and calculated metrics
            - Format with proper markdown structure (headers, lists, tables, code blocks)
            - Ensure reproducibility by documenting all steps

        **Error Handling:**
            - If code execution fails, analyze the error and try alternative approaches
            - Handle missing data appropriately (document and address)
            - Validate results for reasonableness before reporting

        **Final Note:**
            Approach this analysis systematically. Think step-by-step, validate your work, and ensure every insight is backed by quantitative evidence. Your goal is to provide the user with a thorough, professional analysis that directly addresses their query.
        """
        return prompt

    


# %% Define Agent State



# %%  Define Agent Tools

# Tool 1: Get column names
def get_columns(file_name: Annotated[str, "csv_name"]):
    """
    Use this tool to get the column list from the CSV file.
    Parameters:
    - file_name: The name of the CSV file that has the data
    """
    df = pd.read_csv(file_name)
    columns = df.columns.tolist()
    return str(columns)


# Tool 2: Get Column Descriptions
#def get_column_description(column_dict: Annotated[dict, "A dictionary containing column names and column descriptions"]):
def get_column_description(column_dict: Annotated[str, "dict_mobile"]):
    """
    Use this tool to get the description of the columns contained in the dataframe.
    """
    return str(column_dict)


# Tool 3: Create Charts & Graphs
def graph_generator(code: Annotated[str, "A python code to generate visualizations"]) -> str:
    """
    Use this tool to generate graphs and visualizations using python code. 
    Print the graph path in html and png format in the following format:
    'The graph path in html format is <graph_path_html> and the graph path in png format is <graph_path_png>'.
    """
    catcher = StringIO()
    try:
        with redirect_stdout(catcher):
            # The compile step can catch syntax errors early
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code, globals(), globals())
            return (
                f"The graph path is \n\n{catcher.getvalue()}\n"
                f"Proceed to the next step"
            )
    except Exception as e:
        return f"Failed to run code. Error: {repr(e)}, try a different approach"
    

# Tool 4: Explore Data
def python_execution_tool(code: Annotated[str, "The python code to execute for calculations and data processing"]) -> str:
    """
    Use this tool to run python code for calculations, data processing, and metric computation.
    Always use print statement to print the result in format:
    'The calculated value for <variable_name> is <calculated_value>'.
    """
    catcher = StringIO()
    try:
        with redirect_stdout(catcher):
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code, globals(), globals())
            return (
                f"The calculated value is \n\n{catcher.getvalue()}\n"
                f"Make sure to include this value in the report\n"
            )
    except Exception as e:
        return f"Failed to run code. Error: {repr(e)}, try a different approach"

#%% Create Agent Pipeline

# 1) Outline agent's output structure
class AnalystAgentOutput(BaseModel):
    analysis_report: str = Field(description="The analysis report in markdown format")
    metrics: list[str] = Field(description="The metrics of the analysis")
    image_html_path: str = Field(description="The path of the graph in html format, if no graph is generated, return empty string")
    image_png_path: str = Field(description="The path of the graph in png format, if no graph is generated, return empty string")
    conclusion: str = Field(description="The conclusion of the analysis")


#%% Create Agent's Prompt


#%% Run Agent

def run_full_agent(user_query: str, dataset_path: str, dataset_meta: str) -> AnalystAgentOutput:
    if analyst_agent is None:
        raise RuntimeError("Agent not initialized. Call init_agent(api_key) first.")
    state = State(user_query=user_query, file_name=dataset_path, column_dict=dataset_meta)
    response = analyst_agent.run_sync(deps=state)
    raw_output = response.output
    print("---- RAW OUTPUT FROM AGENT ----")
    print(raw_output)
    print("-------------------------------")
    try:
        parsed_data = json.loads(raw_output)
        output = AnalystAgentOutput(**parsed_data)
    except Exception as e:
        print("Failed to parse agent output:", e)
        print("Raw output:", raw_output)
        raise
    return output

