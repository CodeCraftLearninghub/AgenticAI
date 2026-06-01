from langchain_core.prompts import ChatPromptTemplate

# Create prompt template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms for a {audience}."
)

# Dynamically inject values
formatted_prompt = prompt.invoke({
    "topic": "Agentic AI",
    "audience": "college student"
})

print("\n\n",formatted_prompt,"\n\n")