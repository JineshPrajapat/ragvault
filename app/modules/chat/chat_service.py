from uuid import UUID
from app.modules.embedding.retrieval_service import RetrievalService
from app.modules.chat.chat_memory_service import ChatMemoryService
from app.core.llm.service import LLMService


class ChatService:

    @staticmethod
    async def ask_question(
        cs_id: UUID,
        question: str,
    ) -> dict:
        
        # 1️. Load history
        history = await ChatMemoryService().get_history(cs_id)

        # 2. Retrieve session-isolated context
        context = await RetrievalService.retrieve_context(
            cs_id=cs_id,
            question=question
        )

        if not context.strip():
            return {
                "error": "No relevant documents found for this session."
            }

        # 3️. Build conversation block
        conversation_block = ""
        for msg in history:
            conversation_block += f"{msg['role']}: {msg['content']}\n"


        # 3. Build hallucination-guard prompt
        system_prompt = """
You are a helpful AI assistant to answer questions about relevant documentation provided to you. Your responses should be precise, accurate, and sourced exclusively from the provided information. Please follow these guidelines:
* Only use information from the provided documentation. Avoid opinions, speculation, or assumptions.
* Use the exact terminology and descriptions found in the provided content.
* Keep answers concise and relevant to the user's question.
* Use acronyms and abbreviations exactly as they appear in the documentation or query.
* Apply markdown if your response includes lists, tables, or code.
* Directly answer the question, then STOP. Avoid additional explanations unless specifically relevant.
* If the information is irrelevant, simply respond that you don't have relevant documentation and do not provide additional comments or suggestions. Ignore anything that cannot be used to directly answer this query.
"""

        user_prompt = f"""
Conversation:
{conversation_block}

Context:
{context}

Question:
{question}
"""
        
        print("prompt", user_prompt)
        print("prompt lenght", len(user_prompt))


        # 4. LLM Call
        llm_service = LLMService()
        result = await llm_service.generate(system_prompt, user_prompt)

        # 5️⃣ Persist user + assistant messages
        await ChatMemoryService().save_message(
            cs_id=cs_id,
            role="user",
            content={"type": "text", "text": question}
        )

        await ChatMemoryService().save_message(
            cs_id=cs_id,
            role="assistant",
            content={"type": "text", "text": result["answer"]},
            meta={"rag": True}
        )

        print("llm result", result)

        if result["success"]:
            return {"answer": result["answer"], "tokens_used": result["tokens_used"]}
        else:
            return {"error": result["error"]}
        