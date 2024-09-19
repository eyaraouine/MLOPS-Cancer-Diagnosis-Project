import os
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import ( 
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_exa import ExaSearchRetriever
from ..llm import llm


# Fonction pour exécuter la chaîne de récupération et génération
def execute_chain(question):

    retriever = ExaSearchRetriever(k=3, highlights=True)
    document_prompt = PromptTemplate.from_template(
        """
        <source>
            <url>{url}</url>
            <highlights>{highlights}</highlights>
        </source>
        """
    )

    document_chain = (
        RunnableLambda(
            lambda document: {
                "highlights": document.metadata["highlights"],
                "url": document.metadata["url"],
            }
        )
        | document_prompt
    )

    retrieval_chain = (
        retriever | document_chain.map() | (lambda docs: "\n".join([i.text for i in docs]))
    )

    generation_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", 
                "You are a medical expert research assistant. You use xml-formatted context to research people's questions.",
            ),
            (
                "human",
                """
                Please answer the following question based on the provided context. Cite your sources at the end of your response:
                     
                Question: {question}
                ---
                <context>
                {context}
                </context>
                """,
            ),
        ]
    )

    output_parser = StrOutputParser()
    chain = RunnableParallel({
    "question": RunnablePassthrough(),
    "context": retrieval_chain,
    }) | generation_prompt | llm | output_parser

    return chain.invoke(question)

