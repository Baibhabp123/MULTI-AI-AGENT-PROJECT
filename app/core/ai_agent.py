from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

from langchain_core.messages import AIMessage


def get_response_from_ai_agents(
    llm_id: str,
    query: str,
    allow_search: bool,
    system_prompt: str
):

    # ---------------------------------------------------------
    # 1. Create LLM
    # ---------------------------------------------------------

    llm = ChatGroq(
        model=llm_id,
        temperature=0
    )

    # ---------------------------------------------------------
    # 2. Create tools
    # ---------------------------------------------------------

    tools = []

    if allow_search:

        tavily_tool = TavilySearch(
            max_results=2
        )

        tools.append(tavily_tool)

    # ---------------------------------------------------------
    # 3. Create agent
    # ---------------------------------------------------------

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )

    # ---------------------------------------------------------
    # 4. Prepare input
    # ---------------------------------------------------------

    state = {
        "messages": [
            ("user", query)
        ]
    }

    # ---------------------------------------------------------
    # 5. Invoke agent
    # ---------------------------------------------------------

    response = agent.invoke(state)

    # ---------------------------------------------------------
    # 6. Extract final AI response
    # ---------------------------------------------------------

    messages = response.get("messages", [])

    ai_messages = [
        message.content
        for message in messages
        if isinstance(message, AIMessage)
    ]

    if not ai_messages:
        raise RuntimeError(
            "Agent completed but no AI response was returned."
        )

    return ai_messages[-1]