import re
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser
from typing import Union


class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print(f"DEBUG: Received LLM output:\n{llm_output}\n")

        # Check for a 'Final Answer' or 'result' output directly
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        if "\nObservation" in llm_output:
            print("here we are")

        # Parse out the action and action input
        regex = r"Action\s*:?(.+?)\s*Action\s*Input\s*:?(.+)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            print(f"DEBUG: Could not parse LLM output. Output:\n{llm_output}\n")
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")

        action = match.group(1).strip()
        action_input = match.group(2).strip().strip('"')

        return AgentAction(tool=action, tool_input=action_input, log=llm_output)
