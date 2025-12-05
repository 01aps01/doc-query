from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

MAX_CONTEXT_CHARS = 15000  
TEMPERATURE = 0.0          


def ask_llm(question, context):

    if context and len(context) > MAX_CONTEXT_CHARS:
        context = context[-MAX_CONTEXT_CHARS:]

    prompt = f"""
You are an assistant for PDF question-answering.

RULES:
- Use ONLY the information given in the Context.
- If the answer is not found in the context, reply: "Answer not found in the document."
- Do NOT guess or create new information.

Context:
\"\"\"
{context}
\"\"\"

Question: {question}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=TEMPERATURE,
            stream=False,                
            stop=["Context:", "Question:"],  
        )

        msg = response.choices[0].message.content
        return msg if msg else "Answer not found in the document."

    except Exception as e:
        return f"[Groq Error] {str(e)}"
