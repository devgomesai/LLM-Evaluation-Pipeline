RELEVANCE_PROMPT = """
You are an expert evaluator. Rate how well the following response addresses the user query.
Return ONLY a number between 0.0 and 1.0, where 1.0 is perfectly relevant and 0.0 is completely irrelevant.

Query: {query}
Response: {response}

Score:
"""

COMPLETENESS_PROMPT = """
You are an expert evaluator. Does the response FULLY answer the query based on the provided intent?
Return ONLY a number between 0.0 and 1.0.

Query: {query}
Response: {response}

Score:
"""

HALLUCINATION_PROMPT = """
Given the following claim and the provided context, determine if the claim is supported by the context.
Answer with one of the following: SUPPORTED, UNSUPPORTED, CONTRADICTED.

Claim: {claim}
Context: {context}

Answer:
"""
