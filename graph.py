from langgraph.graph import StateGraph
from state_schema import AgentState
from nodes.video_generator import video_generator, video_approver, video_decider
from nodes.video_uploader import video_uploader
from nodes.prompt_generator import prompt_generator
from nodes.topic_selector import topic_selector, topic_approver, topic_decider
from nodes.metadata_generator import metadata_generator
from nodes.final_logger import final_logger
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)


graph = StateGraph(AgentState)

graph.add_node("topic_selection", topic_selector)
graph.add_node("topic_approval", topic_approver)
graph.add_node("prompt_generation", prompt_generator)
graph.add_node("video_generation", video_generator)
graph.add_node("video_approval", video_approver)
graph.add_node("metadata_generation", metadata_generator)
graph.add_node("video_upload", video_uploader)
graph.add_node("final_logger", final_logger)

graph.add_edge("topic_selection", "topic_approval")
graph.add_edge("prompt_generation", "video_generation")
graph.add_edge("video_generation", "video_approval")
graph.add_conditional_edges("topic_approval", topic_decider)
graph.add_conditional_edges("video_approval", video_decider)
graph.add_edge("metadata_generation", "video_upload")
graph.add_edge("video_upload", "final_logger")

graph.set_entry_point("topic_selection")
graph.set_finish_point("final_logger")

# Compile the graph
app = graph.compile(checkpointer=memory)