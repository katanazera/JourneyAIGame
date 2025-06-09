import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, MessagesState

load_dotenv()

llm = init_chat_model(model="gpt-4o-mini",model_provider="openai")

#thx TWT for rly nice prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are now the guide of a mystical journey in the Whispering Woods. 
            A traveler named Elara seeks the lost Gem of Serenity. 
            You must navigate her through challenges, choices, and consequences, 
            dynamically adapting the tale based on the traveler's decisions. 
            Your goal is to create a branching narrative experience where each choice 
            leads to a new path, ultimately determining Elara's fate. Never help Elara.

            Here are some rules to follow:
            1. Start by asking the player to choose some kind of weapons that will be used later in the game
            2. Have a few paths that lead to success
            3. Have some paths that lead to death. If the user dies generate a response that explains the death and ends in the text: "The End.", I will search for this text to end the game
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = llm.invoke(prompt)
    return {"messages": response}

workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START,"model")

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

print('This is Journey Game AI\nType go to start\nType quit to stop')

while True:
    query = input("Your choice: ")
    if query.lower() == 'quit':
        break
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()
    if 'The End' in output["messages"][-1].content:
        break