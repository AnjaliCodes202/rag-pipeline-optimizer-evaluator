# backend/app/core/generation.py
# Define what a text generator must do, not how it does it.
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class GeneratorClient:
    """
    Interface for any text generator.
    """
    def generate(self,prompt:str):
        raise NotImplementedError


class HFGeneratorClient(GeneratorClient):
    MODEL_MAP = {
        "distilgpt2": "distilgpt2",
        "facebook/opt-125m": "facebook/opt-125m",
        "facebook/opt-350m": "facebook/opt-350m",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0":
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    }
    def __init__(
        self,
        model: str,
        temperature: float = 0.2,
        max_new_tokens: int = 250,
    ):
        if model not in self.MODEL_MAP:
            raise ValueError(f"Unsupported model: {model}")
        model_id = self.MODEL_MAP[model]
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cpu", torch_dtype=torch.float32)
        self.model.eval()
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens

    def generate(self, prompt: str) -> str:
            # tokenize prompt
            inputs = self.tokenizer(prompt, return_tensors="pt")
            prompt_length = inputs["input_ids"].shape[1]

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    min_new_tokens=30,
                    temperature=self.temperature,
                    do_sample=True,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            # keep ONLY newly generated tokens
            generated_tokens = outputs[0][prompt_length:]


            answer = self.tokenizer.decode(
                  generated_tokens,
                  skip_special_tokens=True
                ).strip()
            
            if not answer:
               return "The answer could not be generated from the provided context."
            return answer


def get_generator_client(
    generator_model: str,
    temperature: float,
    max_new_tokens: int = 250,
) -> GeneratorClient:
    """
    Factory used by executor.
    """
    return HFGeneratorClient(
        model=generator_model,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
    )



# Convert retrieved chunks into a single context string.
def build_context(chunks: List[str], max_chars: int = 3000) -> str:
    context = ""
    for chunk in chunks:
        if len(context) + len(chunk) > max_chars:
            break
        context += chunk + "\n\n"
    return context.strip()


# backend/app/core/generation.py
# Define what a text generator must do, not how it does it.
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class GeneratorClient:
    """
    Interface for any text generator.
    """
    def generate(self,prompt:str):
        raise NotImplementedError


class HFGeneratorClient(GeneratorClient):
    MODEL_MAP = {
        "distilgpt2": "distilgpt2",
        "facebook/opt-125m": "facebook/opt-125m",
        "facebook/opt-350m": "facebook/opt-350m",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0":
            "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    }
    def __init__(
        self,
        model: str,
        temperature: float = 0.2,
        max_new_tokens: int = 250,
    ):
        if model not in self.MODEL_MAP:
            raise ValueError(f"Unsupported model: {model}")
        model_id = self.MODEL_MAP[model]
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cpu", torch_dtype=torch.float32)
        self.model.eval()
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens

    def generate(self, prompt: str) -> str:
            # tokenize prompt
            inputs = self.tokenizer(prompt, return_tensors="pt")
            prompt_length = inputs["input_ids"].shape[1]

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            # keep ONLY newly generated tokens
            generated_tokens = outputs[0][prompt_length:]


            answer = self.tokenizer.decode(
                  generated_tokens,
                  skip_special_tokens=True
                ).strip()
            
            if not answer:
               return "The answer could not be generated from the provided context."
            return answer


def get_generator_client(
    generator_model: str,
    temperature: float,
    max_new_tokens: int = 250,
) -> GeneratorClient:
    """
    Factory used by executor.
    """
    return HFGeneratorClient(
        model=generator_model,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
    )



# Convert retrieved chunks into a single context string.
def build_context(chunks: List[str], max_chars: int = 3000) -> str:
    context = ""
    for chunk in chunks:
        if len(context) + len(chunk) > max_chars:
            break
        context += chunk + "\n\n"
    return context.strip()


def generate_answer(
    query: str,
    chunks: List[str],
    generator: GeneratorClient,
) -> str:
    """
    Generate an answer using retrieved context.
    """
    context = build_context(chunks)
    prompt = (
        "You are a factual assistant.\n"
        "Answer ONLY using the provided context.\n"
        "If the answer is not in the context, say so.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{query}\n\n"
        "Answer:"
    )

    return generator.generate(prompt)