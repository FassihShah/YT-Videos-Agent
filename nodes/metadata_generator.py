from dotenv import load_dotenv
from state_schema import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()


class MetadataOutput(BaseModel):
    title: str = Field(description="A catchy YouTube Shorts title under 100 characters")
    description: str = Field(description="A 1–2 line description for the video, SEO-friendly, with hashtags")



parser = PydanticOutputParser(pydantic_object=MetadataOutput)


prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're a professional YouTube content strategist."),
    ("human", """
Based on the topic and visual description below, create structured metadata:

Topic: {topic}

Video Description (prompt): {prompt}

Return only the structured output in this JSON format:
{format_instructions}
""")
])



def generate_metadata(topic: str, prompt: str) -> tuple[str, str]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
    )

    full_prompt = prompt_template.format_messages(
        topic=topic,
        prompt=prompt,
        format_instructions=parser.get_format_instructions()
    )

    output = llm.invoke(full_prompt)
    parsed = parser.parse(output.content)
    return parsed.title, parsed.description


# LangGraph node function to generate metadata
def metadata_generator(state: AgentState) -> AgentState:
    """ Generates metadata for the video based on the topic and prompt in the state.
    """
    topic = state.get("topic", "")
    prompt = state.get("prompt", "")

    title, description = generate_metadata(topic, prompt)

    state["title"] = title
    state["description"] = description

    return state
