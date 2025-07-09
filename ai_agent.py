from llama_cpp import Llama

# Load model
llm = Llama(
    model_path="PATH_TO_THE_MODEL",
    n_ctx=2048,
    n_threads=6
)

# Load static company info
with open("company_info.txt", "r") as f:
    company_info = f.read()

def build_prompt(user_question: str, info: str) -> str:
    return (
        "You are a helpful AI assistant.\n\n"
        "Use this company information to answer the user's question:\n\n"
        f"{info}\n\n"
        f"User: {user_question}\n"
        "Assistant:"
    )

def get_answer(user_input: str) -> str:
    prompt = build_prompt(user_input, company_info)
    output = llm(prompt, max_tokens=200, stop=["User:", "You:"])
    return output["choices"][0]["text"].strip()