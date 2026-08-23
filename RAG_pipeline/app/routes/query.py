from fastapi import APIRouter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
router = APIRouter(
    prefix="/query",
    tags = ["query"]
)

openai_client = OpenAI()
embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large",)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding = embedding_model,
    collection_name = "sample_collection",
    url = "http://localhost:6333"
)






@router.post("/")
async def query(question: str):
    search_result = vector_db.similarity_search(query= question,)
    context = "\n\n".join(
        f"[Page {result.metadata.get('page', 0) + 1}] {result.page_content}"
        for result in search_result
    )
    SYSTEM_PROMPT = f"""
    You are helpful assistant that answers questions based on the provided context. If the context does not contain the answer
    respond with I don't know. Cite the page number from the context when you answer.
    
    Also, include the page number of the context in your answer if applicable
    context:{context}
    """


    response = openai_client.chat.completions.create(
        model='gpt-5',
        messages=[
            {"role":"system","content":  SYSTEM_PROMPT},
            {"role":"user", "content": question}       
        ]
    )

    return {"question":question, "answer": response.choices[0].message.content}