# 🔎 DEXPI Taxonomy Extractor

This Python script extracts the full taxonomy from the [DEXPI RDL (Reference Data Library)](https://dexpi.org), including class definitions, metadata, and hierarchical relationships, using the public SPARQL endpoint.

It merges metadata and subclass relationships into a structured JSON file ready for downstream processing or database insertion.

---

## 📦 Output

**`dexpi_full_taxonomy.json`**

A nested JSON structure representing the DEXPI hierarchy:

```json
{
  "ISO 6708 OBJECT": {
    "label": "ISO 6708 OBJECT",
    "uri": "http://sandbox.dexpi.org/rdl/ISO_6708_OBJECT",
    "designation": "ISO 6708 OBJECT",
    "comment": "...",
    "definition": "...",
    "type": "...",
    "children": [
      {
        "label": "ISO 6708 OBJECT DN 1400",
        "uri": "...",
        "designation": "...",
        ...
      }
    ]
  }
}
