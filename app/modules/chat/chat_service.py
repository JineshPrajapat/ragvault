from uuid import UUID
from app.modules.embedding.retrieval_service import RetrievalService
from app.modules.chat.chat_memory_service import ChatMemoryService
from app.core.llm.service import LLMService
from app.schemas.api_response import AppServiceResult
import time


class ChatService:

    @staticmethod
    def _get_system_prompt(self) -> str:
        return (
            """
                You are a helpful AI assistant to answer questions based solely on the provided documentation. Please follow these guidelines:
                - **Answer Precisely**: Your responses should be accurate and based only on the provided content. Avoid speculation, assumptions or external knowledge..
                - **Use Exact Terminology**: Use the exact wording, acronyms, and descriptions as they appear in the context.
                - **Be Concise and Relevant**: Keep answers brief and directly relevant to the user's question. Avoid unnecessary elaboration else user request.
                - **Markdown Formatting**: Use headings, bullet points, numbered lists, tables, diagram or code blocks where applicable to structure your response clearly.
                - **Handle Ambiguity**: If a question is unclear or cannot be answered based on the documentation, respond with:  
                    `I don’t have relevant documentation to answer your question.`
                - **Contextual Consistency**: For follow-up questions, reference previous responses where relevant.
                - **Error Handling**: If the documentation is insufficient to answer the question, state:  
                    `The provided documentation does not cover this topic.`
                - **Directness**: Answer the question directly and stop. Avoid additional explanations unless they are directly relevant.
                - **Elaboration and Explanation**: If the user requests further detail, clarification, or examples, provide them **within the documentation's context**. Stay within the provided content, and include **diagrams or visuals** if relevant and requested.
                - **Visuals**: If the user asks for a diagram, chart, or other visual aids, provide appropriate **visualizations** from the documentation to clarify the topic.
                * Format all responses strictly in Markdown.
            """
        )

    @staticmethod
    async def ask_question(
        cs_id: UUID,
        question: str,
    ) -> AppServiceResult[dict]:
        start_time = time.perf_counter()
        try:
            # 1️. Load history
            print(f"[1/5] Loading history for session {cs_id}")
            history = await ChatMemoryService().get_history(cs_id)

            # 2. Retrieve session-isolated context
            print(f"[2/5] Retrieving context for query: {question[:50]}...")
            retrieval = await RetrievalService.retrieve_context(
                cs_id=cs_id,
                question=question
            )

            if not retrieval.success:
                print(f"[!] RETRIEVAL_FAILED | Error: {retrieval.error}")
                return AppServiceResult(success=False, error=retrieval.error)

            context_data = retrieval.data

            # 3️. Build conversation block
            print( f"[3/5] PROMPT_BUILD | Context Size: {len(context_data)} chars")
            conversation_block = "\n".join( [f"{msg['role']}: {msg['content']}" for msg in history])

            # 3. Build hallucination-guard prompt
            system_prompt = ChatService._get_system_prompt()

            user_prompt = f""" 
    Conversation:
    {conversation_block}

    Context:
    {context_data}

    Question:
    {question}
    """

            # 4. LLM Call
            print(f"[4/5] LLM_GENERATE | Provider: Gemini")
            llm_service = LLMService("gemini")
            result = await llm_service.generate(system_prompt, user_prompt)

            if not result.success:
                print(f"[!] LLM_FAILED | Error: {result.error}")
                return AppServiceResult(success=False, error=result.error)

            # Save messages
            print(f"[5/5] PERSISTENCE | Saving history...")
            await ChatMemoryService().save_message(
                cs_id=cs_id,
                role="user",
                content={"type": "text", "text": question}
            )

            await ChatMemoryService().save_message(
                cs_id=cs_id,
                role="assistant",
                content={"type": "text", "text": result.content},
                meta={"rag": True}
            )

            total_duration = time.perf_counter() - start_time
            print(f"[*] SUCCESS | Time: {total_duration:.2f}s | Tokens: {result.tokens_used}")

            return AppServiceResult(
                success=True,
                data={
                    "role": "assistant",
                    "content": {"type": "text", "text": result.content},
                    "tokens_used": result.tokens_used
                }
            )

        except Exception as e:
            print(f"[CRITICAL] ask_question exception: {str(e)}")
            return AppServiceResult(success=False, error="Chat processing failed")
