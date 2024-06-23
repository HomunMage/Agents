---
categories: agents
---

# [Skyler - LangGraph with Ollama](https://chatgpt.com/g/g-V2vtIT5RH)

## prompt

{% raw %}
here are langgraph sample codes with ollama that make agent and use tool
```
from langgraph.graph import Graph

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import json


# Specify the local language model
local_llm = "phi3"

# Initialize the ChatOllama model with desired parameters
llm = ChatOllama(model=local_llm, format="json", temperature=0)


def Agent(question):
    # Define the prompt template
    template = """
        Question: {question} Let's think step by step.
        your output format is filename:"" and  content:""
        make sure your output is right json
    """
    
    prompt = PromptTemplate.from_template(template)

    # Format the prompt with the input variable
    formatted_prompt = prompt.format(question=question)

    llm_chain = prompt | llm | StrOutputParser()
    generation = llm_chain.invoke(formatted_prompt)
    
    return generation



def Tool(input):
    print("Tool Stage input:" + input)
    # Parse the JSON input
    data = json.loads(input)
    # Extract the "content" and "filename" parts
    content = data.get("content", "")
    filename = data.get("filename", "output.md")
    # Write the content to the specified filename
    with open(filename, 'w') as file:
        file.write(content)
    return input

# Define a Langchain graph
workflow = Graph()

workflow.add_node("agent", Agent)
workflow.add_node("tool", Tool)

workflow.add_edge('agent', 'tool')

workflow.set_entry_point("agent")
workflow.set_finish_point("tool")

app = workflow.compile()

app.invoke("write an article, content is startup.md ")
```


```
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
import random
import json
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod

# Specify the local language model
local_llm = "mistral"
llm = ChatOllama(model=local_llm, format="json", temperature=0)

# Clip the history to the last 8000 characters
def clip_history(history: str, max_chars: int = 8000) -> str:
    if len(history) > max_chars:
        return history[-max_chars:]
    return history

# State Machine
class TRPGState(TypedDict):
    history: str
    need_roll: bool
    roll_number: int

# Define the base class for tasks
class AgentBase(ABC):
    def __init__(self, state: TRPGState):
        self.state = state

    @abstractmethod
    def get_prompt_template(self) -> str:
        pass

    def execute(self) -> TRPGState:
        # Clip the history to the last 8000 characters
        self.state["history"] = clip_history(self.state["history"])
        
        # Define the prompt template
        template = self.get_prompt_template()
        prompt = PromptTemplate.from_template(template)        
        llm_chain = prompt | llm | StrOutputParser()
        generation = llm_chain.invoke({"history": self.state["history"], "roll_number": self.state["roll_number"]})
        
        data = json.loads(generation)
        self.state["need_roll"] = data.get("need_roll", "")        
        self.state["roll_number"] = -1


        self.state["history"] += "\n" + generation
        self.state["history"] = clip_history(self.state["history"])

        return self.state

# Define agents
class DM(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            {history}
            As DnD DM, describe the current scenario for the player. (in short, we do fast play)
            sometimes roll dice, sometimes not.            
            player roll {roll_number}, if > 0 you need explain what the roll affect result, start from your roll {roll_number} blablabla
            Output the JSON in the format: {{"scenario": "your action description", "need_roll": True/False}}
        """

class Player(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            Here is the scenario: {history}
            As a Player, I want to perform an action. (in short, we do fast play)
            Output the JSON in the format: {{"action": "I want xxxx"}}
        """


# Define tool
def RollDice(state: TRPGState) -> TRPGState:
    random_number = random.randint(1, 20)
    state["history"] += "\n" +  "roll result:" + str(random_number)
    state["history"] = clip_history(state["history"])
    state["need_roll"] = False
    state["roll_number"] = random_number
    return state

# for conditional edges
def check_need_roll(state: TRPGState) -> Literal["roll", "not roll"]:
    if state.get("need_roll") == True:
        return "roll"
    else:
        return "not roll"

# Define the state machine
workflow = StateGraph(TRPGState)

# Initialize tasks for DM and Player
def dm_task(state: TRPGState) -> TRPGState:
    return DM(state).execute()

def player_task(state: TRPGState) -> TRPGState:
    return Player(state).execute()

workflow.add_node("dm", dm_task)
workflow.add_node("player", player_task)
workflow.add_node("RollDice", RollDice)

workflow.set_entry_point("dm")

# Define edges between nodes

workflow.add_conditional_edges(
    "dm",
    check_need_roll,
    {
        "not roll": "player",
        "roll": "RollDice"
    }
)

workflow.add_edge("player", "dm")
workflow.add_edge("RollDice", "dm")


# Compile the workflow into a runnable app
app = workflow.compile()

# Initialize the state
initial_state = TRPGState(
    history="A monster appears in front of you.",
    need_roll=False, 
    roll_number=-1
    )

for s in app.stream(initial_state):
    # Print the current state
    print("for s in app.stream(initial_state):")
    print(s)
```

{% endraw %}


<img src="image.webp" Height="200" style="border-radius: 50%; overflow: hidden;" />