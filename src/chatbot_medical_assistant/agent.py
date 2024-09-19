from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain import hub
from ..chatbot_medical_assistant.tools.research_tool import execute_chain
from  ..chatbot_medical_assistant.llm import llm


chat_prompt = ChatPromptTemplate.from_messages(
       [
        ("system", (
            "You are a highly skilled medical expert specialized in cancer diagnosis and treatment. "
            "Your role is to provide detailed medical explanations, insights into cancer diagnostics, "
            "treatment options, and best practices for managing patient care. You offer advice and guidance "
            "on test interpretations, biopsy results, and treatment paths."
        )),
        ("human", "{input}"),
    ]
)

cancer_chat = chat_prompt | llm | StrOutputParser()
tools = [
 Tool.from_function(
    name="Medical Research Assistant",
    description="Use this tool to retrieve scientific articles and medical research reports relevant to the user's query. It gathers insights from highly reputable sources and delivers answers based on the latest research findings.",
    func=execute_chain
),
]

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_prompt = PromptTemplate.from_template("""
You are a medical expert providing specialized information on cancer diagnosis and treatment.
Be as helpful as possible and return as much information as possible.

Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
    )

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def generate_response(user_input,session_id):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = chat_agent.invoke(
        {"input": user_input},
         {"configurable": {"session_id": session_id}},
    )

    return response['output']