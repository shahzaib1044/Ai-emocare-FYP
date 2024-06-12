from ctransformers import AutoModelForCausalLM
from fastapi import FastAPI, Form
from pydantic import BaseModel

#Model loading
llm = AutoModelForCausalLM.from_pretrained("carl-llama-2-13b.Q3_K_S.gguf",
model_type='llama',
max_new_tokens = 1096,
threads = 3,
)
   

#Pydantic object
class validation(BaseModel):
    prompt: str
    
#Fast API
app = FastAPI()

#Zephyr completion
@app.post("/llm_on_cpu")
async def stream(item: validation):
    system_prompt = 'Below is an instruction that describes a task. Write a response that appropriately completes the request.'
    E_INST = "</s>"
    user, assistant = "<|user|>", "<|Therapy Assistant|>"
    prompt = f"{system_prompt}{E_INST}\n{user}\n{item.prompt.strip()}{E_INST}\n{assistant}\n"
    return llm(prompt)
