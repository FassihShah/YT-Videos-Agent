from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from state_schema import AgentState


# LangGraph node function
def generate_prompt(topic: str) -> str:
    """Generates a high-quality video generation prompt based on the topic.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.9,
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a professional creative AI that generates high-quality YouTube Shorts prompts.",
        ),
        (
            "human",
            """Create a very high-quality, immersive video generation prompt based on the following topic:
            
Topic: {topic}

Requirements:
- Include immersive sound descriptions (e.g., tapping, crumbling, snapping)
- Visually cinematic: textures, lighting, detail
- Only return the full video generation prompt.
- Keep it concise, under 100 words."""
        )
    ])

    chain = prompt | llm
    response = chain.invoke({"topic": topic})
    return response.content.strip()



def prompt_generator(state: AgentState) -> AgentState:
    topic = state["topic"]
    prompt = generate_prompt(topic)
    print(f"Prompt Generated: {prompt}")
    state["prompt"] = prompt
    return state