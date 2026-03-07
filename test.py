# from sentence_transformers import SentenceTransformer

# models_to_check = [
#     "all-mpnet-base-v2",
#     "BAAI/bge-large-en-v1.5"
# ]

# for model_name in models_to_check:
#     try:
#         model = SentenceTransformer(model_name)
#         print(f"✅ Model '{model_name}' is available locally or can be downloaded.")
#     except Exception as e:
#         print(f"❌ Model '{model_name}' is NOT available. Error: {e}")



import asyncio
from app.modules.embedding.retrieval_service import RetrievalService
from uuid import UUID

async def retriever():
    cs_id = UUID("15d2efb3-7193-4d27-ac44-df0a1245989f")
    question="IAS memory format"
    # question="Memory management and garbage collection"
    # cs_id = UUID("d8483037-e554-4e96-8d3a-eb6245ef8dcc")


    context = await RetrievalService.retrieve_context(cs_id, question)
    print(context)

async def test_embedding_service():
    from app.modules.embedding.embedding_service import EmbeddingService
    cd_id = UUID("c5c72577-ea6b-4251-a7cb-dff27ffe77af")
    # cd_id = UUID("8d773b71-82f0-447d-a38f-b5bd37419398")
    embedding = await EmbeddingService().process_document(cd_id)
    print(embedding)

# Run the async main function
asyncio.run(retriever())