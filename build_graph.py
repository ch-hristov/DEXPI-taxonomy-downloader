from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import json

def read_query(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# Use the updated endpoint
endpoint = "https://endpoint.dexpi.org/rdl/"
sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat(JSON)
sparql.addCustomHttpHeader("Accept", "application/sparql-results+json")

# --- Step 1: Fetch metadata ---
sparql.setQuery(read_query("fetch_metadata.rq"))
meta_results = sparql.query().convert()

metadata = {}
for r in meta_results["results"]["bindings"]:
    label = r.get("label", {}).get("value", "")
    metadata[label] = {
        "uri": r.get("class", {}).get("value", ""),
        "label": label,
        "comment": r.get("comment", {}).get("value", ""),
        "designation": r.get("designation", {}).get("value", ""),
        "definition": r.get("definition", {}).get("value", ""),
        "type": r.get("type", {}).get("value", "")
    }

# --- Step 2: Fetch hierarchy ---
sparql.setQuery(read_query("fetch_hierarchy.rq"))
hierarchy_results = sparql.query().convert()

graph = defaultdict(list)
for r in hierarchy_results["results"]["bindings"]:
    parent = r.get("superLabel", {}).get("value") or r["super"]["value"].split("/")[-1]
    child = r.get("subLabel", {}).get("value") or r["sub"]["value"].split("/")[-1]

    graph[parent].append({
    "label": child,
    "uri": metadata.get(child, {}).get("uri"),
    "designation": metadata.get(child, {}).get("designation"),
    "comment": metadata.get(child, {}).get("comment"),
    "definition": metadata.get(child, {}).get("definition"),
    "type": metadata.get(child, {}).get("type")
})

# --- Step 3: Merge metadata and hierarchy ---
final = {}
for parent, children in graph.items():
    final[parent] = {
        "label": parent,
        "uri": metadata.get(parent, {}).get("uri"),
        "designation": metadata.get(parent, {}).get("designation"),
        "comment": metadata.get(parent, {}).get("comment"),
        "children": children
    }

# --- Step 4: Save output ---
with open("dexpi_full_taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2)

print("✅ Saved full joined taxonomy graph to dexpi_full_taxonomy.json")