from openai import OpenAI
from neo4j import GraphDatabase
import re

# === OpenRouter API Setup ===
API_KEY = "your-openrouter-api-key-here"  
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# === Neo4j Setup ===
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your-neo4j-password-here"

def extract_cypher(text):
    """
    Extracts the Cypher query from LLM response, removing any explanation or markdown.
    """
    block = re.search(r"```(?:cypher)?\s*(.*?)```", text, re.DOTALL)
    if block:
        return block.group(1).strip()

    lines = text.splitlines()
    cypher_lines = []
    in_cypher = False
    for line in lines:
        if "MATCH" in line or "RETURN" in line:
            in_cypher = True
        if in_cypher:
            cypher_lines.append(line)
            if ";" in line:
                break
    return "\n".join(cypher_lines).strip()

def generate_cypher_from_question(question):
    messages = [
        {"role": "system", "content": "You are a Cypher expert. Convert natural language questions into Cypher queries for a Neo4j database."},
        {"role": "user", "content": f"{question}"}
    ]

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "GraphAgent CLI"
        }
    )

    raw_output = completion.choices[0].message.content.strip()
    cypher_query = extract_cypher(raw_output)
    return cypher_query

def analyze_graph_results(question, graph_data):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Given a user's question and the corresponding Neo4j query results, provide a clear and concise answer."},
        {"role": "user", "content": f"Question: {question}\nGraph Data: {graph_data}"}
    ]

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "GraphAgent CLI"
        }
    )

    return completion.choices[0].message.content.strip()

def query_neo4j(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(cypher_query)
        return [record.data() for record in result]

if __name__ == "__main__":
    user_question = input("Ask your question: ")

    print("\nGenerating Cypher query...")
    try:
        cypher_query = generate_cypher_from_question(user_question)
        print("\nGenerated Cypher Query:\n", cypher_query)
    except Exception as e:
        print("Error during Cypher generation:", e)
        exit()

    print("\nRunning query on Neo4j...")
    try:
        graph_results = query_neo4j(cypher_query)
        if not graph_results:
            print("No results.")
            exit()
        print("Query Results:")
        for record in graph_results:
            print(record)
    except Exception as e:
        print("Neo4j Error:", e)
        exit()

    print("\nAnalyzing results with DeepSeek...")
    try:
        answer = analyze_graph_results(user_question, graph_results)
        print("\nAnswer:", answer)
    except Exception as e:
        print("Answer generation failed:", e)
