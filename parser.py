import re
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentOutputParser
from typing import Union


class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print(f"DEBUG: Received LLM output:\n{llm_output}\n")
        if "result" in llm_output:
            # Attempt to extract the answer after 'result' field.
            match = re.search(r"'result':\s*'(.*?)'", llm_output)
            if match:
                result_text = match.group(1).strip()
                return AgentFinish(
                    return_values={"output": result_text},
                    log=llm_output
                )

        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
            # Check for a direct answer format without explicit "Final Answer"
        if not re.search(r"Action\s*\d*:", llm_output):
            # If it contains a direct response, treat it as the final answer
            direct_answer = llm_output.strip()
            return AgentFinish(
                return_values={"output": direct_answer},
                log=llm_output
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            print(f"DEBUG: Received LLM output:\n{llm_output}\n")
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
