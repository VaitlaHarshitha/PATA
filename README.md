# PATA 📍
## Indian Address Intelligence for Last-Mile Delivery

> **AI Build 2026 · E-Commerce in India · Student Edition**
>
> **Track 1 — Pata: Location Intelligence for Last-Mile Delivery**

PATA is an Indian address intelligence system that converts messy, real-world Indian addresses into structured address information and verifies ambiguous locations using pincode data and real-world landmark evidence.

It is built on top of the **BharatAddress** offline Indian address-resolution library and extends it with a hackathon-focused verification and user interface layer.

The core library handles:

- Indian address parsing
- Pincode resolution
- City / district / state identification
- Landmark and locality extraction
- Address validation
- Geocoding
- DIGIPIN
- Indic-language support
- Phonetic matching
- Address similarity
- Batch processing
- CSV / DataFrame processing
- GSTIN enrichment
- CLI usage
- Testing and benchmarking

The PATA application adds:

- Streamlit interface
- Messy-address input
- Original-address preservation
- Pincode reference-data verification
- Multiple pincode candidate detection
- OpenStreetMap landmark verification
- Evidence-based location resolution
- Confidence and verification status
- Delivery-focused user experience

---

# 🚀 What is PATA?

Indian delivery addresses are often written as free text rather than as clean postal addresses.

For example:

```text
Opposite Ganesh temple, near Sai bakery, Ramalingapuram, Tenali
```

A traditional address parser may be able to identify:

```text
Landmark: Ganesh temple; Sai bakery
Locality: Ramalingapuram
City: Tenali
```

But that does not necessarily provide enough information to safely determine an exact geographic location.

PATA addresses this problem by adding an additional verification layer.

```text
Messy Address
      │
      ▼
Address Parser
      │
      ▼
Structured Address
      │
      ├───────────────┐
      ▼               ▼
Pincode Data      OpenStreetMap
Verification      Landmark Search
      │               │
      └───────┬───────┘
              ▼
       Evidence Analysis
              │
              ▼
      Confidence / Status
              │
              ▼
       Verified Location
       or Needs Review
```

The key principle is:

> **PATA should not silently guess when the available evidence is insufficient.**

---

# 🎯 The Problem

Indian addresses create unique challenges for last-mile delivery.

They can contain:

- Landmark-based directions
- Informal colony names
- Missing pincodes
- Incorrect pincodes
- Mixed English and regional scripts
- Hinglish
- Transliteration differences
- Abbreviations
- Inconsistent locality names
- Multiple possible locations for the same locality
- No formal street numbering

Examples:

```text
Near Hanuman temple, 2nd lane, Srinagar Colony, Hyderabad
```

```text
Opp SBI Bank, beside Lakshmi bakery, Tenali
```

```text
H.No 12-45, Gandhi Nagar, near temple, Vijayawada
```

```text
Opposite Ganesh temple, near Sai bakery, Ramalingapuram, Tenali
```

For a delivery partner handling many deliveries per day, an ambiguous address can result in:

- Phone calls to customers
- Searching for landmarks
- Driving around the wrong locality
- Delayed deliveries
- Failed deliveries
- Customer dissatisfaction

PATA attempts to reduce this problem by combining address parsing with external geographic evidence.

---

# 💡 Our Solution

PATA uses a layered approach.

### Layer 1 — Address Parsing

The existing BharatAddress parser extracts:

```text
Building
Landmark
Locality
City
District
State
Pincode
```

### Layer 2 — Pincode Verification

PATA checks available address information against a pincode reference dataset.

### Layer 3 — Landmark Verification

PATA searches OpenStreetMap for real-world landmarks mentioned in the address.

### Layer 4 — Evidence

The system combines the available information to determine whether the candidate location is sufficiently supported.

### Layer 5 — Confidence

Instead of always returning a location, PATA can report:

```text
High confidence
Medium confidence
Needs verification
```

### Layer 6 — User Interface

A Streamlit application presents:

- Original address
- Parsed address
- Pincode candidates
- Landmark evidence
- Coordinates when available
- Confidence
- Verification status

---

# 🧠 PATA Architecture

```text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │   Streamlit UI    │
                 │      app.py       │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ BharatAddress     │
                 │ Address Parser    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ ParsedAddress     │
                 └─────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
        ┌─────────────────┐  ┌──────────────────┐
        │ Pincode         │  │ OpenStreetMap    │
        │ Verification    │  │ Landmark Search  │
        └────────┬────────┘  └────────┬─────────┘
                 │                    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Evidence &        │
                 │ Confidence Layer  │
                 └─────────┬─────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
        Verified Location       Needs Verification
                 │
                 ▼
            Final Result
```

---

# 🤖 AI / Intelligence Workflow

PATA follows a specialized multi-stage workflow instead of relying on one large model call.

```text
                    Messy Address
                         │
                         ▼
                ┌─────────────────┐
                │ Address Parser  │
                └────────┬────────┘
                         │
                         ▼
                 Parsed Components
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       Pincode        Locality       Landmark
          │              │              │
          ▼              ▼              ▼
    Reference DB       City         OpenStreetMap
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                Candidate Locations
                         │
                         ▼
                 Evidence Checking
                         │
                         ▼
                  Confidence Score
                         │
                         ▼
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
          Sufficient            Insufficient
          Evidence              Evidence
              │                     │
              ▼                     ▼
       Location Result       Needs Verification
```

The system is designed so that routine address parsing can remain local and lightweight, while external geographic verification is used where additional evidence is needed.

---

# 📍 Example

Input:

```text
Opposite Ganesh temple, near Sai bakery, Ramalingapuram, Tenali
```

The parser can produce:

```text
Landmark:
Ganesh temple; Sai bakery

Locality:
Ramalingapuram

City:
Tenali
```

If the pincode is not present, PATA can search the pincode reference data using the available locality/city information.

For example:

```text
Found 6 possible pincode records.
```

Instead of selecting one immediately:

```text
Multiple pincode candidates found.

PATA will use landmark evidence from
OpenStreetMap before selecting one.
```

This prevents the application from simply taking the first matching record.

---

# 🗺️ OpenStreetMap Landmark Verification

Landmarks are extremely important in Indian addresses.

Examples include:

```text
Ganesh temple
Sai bakery
SBI bank
Hanuman temple
Government hospital
```

PATA uses OpenStreetMap as a source of real-world POI information.

The workflow is:

```text
Address
   │
   ▼
Landmark Extraction
   │
   ▼
"Ganesh temple"
"Sai bakery"
   │
   ▼
OpenStreetMap Search
   │
   ▼
Nearby POI Candidates
   │
   ▼
Evidence for Candidate Location
```

The purpose is not simply to search for a similarly named place.

The landmark is treated as geographic evidence that can help distinguish between multiple possible pincode/locality candidates.

---

# 📮 Pincode Verification

Pincode information is one of the strongest signals available for Indian addresses.

The original BharatAddress library contains an embedded India Post-derived pincode directory.

PATA additionally supports a pincode reference dataset for verification.

Typical fields include:

```text
Pincode
Office Name
District
State
Latitude
Longitude
```

The PATA workflow is:

```text
Address
   │
   ▼
Pincode present?
   │
 ┌─┴───────────────┐
 │                 │
Yes               No
 │                 │
 ▼                 ▼
Validate       Search using
pincode        locality/city
 │                 │
 └───────┬─────────┘
         ▼
 Candidate Records
         │
         ▼
 Multiple candidates?
         │
     ┌───┴───┐
     │       │
    No      Yes
     │       │
     │       ▼
     │   OSM Landmark
     │   Verification
     │       │
     └───┬───┘
         ▼
     Evidence
```

---

# 🎯 Confidence and Evidence

Confidence is an important part of PATA.

The original parser uses weighted component presence:

```text
Pincode                  0.40
City matches pincode    0.20
Locality                 0.20
Building                 0.10
Landmark                 0.10
```

The score is represented between:

```text
0.0 → 1.0
```

For example:

```text
Confidence: 40%
```

can be presented as:

```text
⚠️ Location needs verification.

Pincode or coordinates are missing.
```

The important behavior is:

> **Low-confidence results are flagged rather than silently presented as correct.**

PATA can use multiple evidence sources:

| Evidence | Purpose |
|---|---|
| Pincode | Administrative location |
| City | Candidate filtering |
| District | Administrative consistency |
| State | Administrative consistency |
| Locality | Area matching |
| Landmark | Geographic clue |
| OpenStreetMap | Real-world POI evidence |
| Coordinates | Geographic output |

---

# 🔎 Auditability

PATA keeps the original address visible.

For example:

```text
Original Address

Opposite Ganesh temple, near Sai bakery,
Ramalingapuram, Tenali
```

followed by:

```text
AI Parsed Address

Landmark:
Ganesh temple; Sai bakery

Locality:
Ramalingapuram

City:
Tenali
```

and then:

```text
Verification

Pincode candidates:
6

Landmark evidence:
Searching OpenStreetMap...

Confidence:
40%

Status:
Needs verification
```

This makes the automated processing easier to understand and audit.

The original input is never silently replaced by the processed output.

---

# 🖥️ Streamlit Application

PATA includes a Streamlit interface for the hackathon MVP.

The application allows the user to enter a messy Indian address and see the complete processing flow.

The interface includes:

```text
PATA 📍

Indian Address Intelligence

Enter a messy Indian address

[ Address input ]

Address parsed successfully!

Original Address
        ↓
AI Parsed Address
        ↓
Pincode Verification
        ↓
OpenStreetMap Landmark Evidence
        ↓
Confidence
        ↓
Verification Status
```

---

# ▶️ Running the PATA Application

From the project directory:

```bash
python -m streamlit run app.py
```

Streamlit will start the local web application.

The browser can then be opened at the local Streamlit URL displayed in the terminal.

---

# 🛠️ Installation

## Install from PyPI

```bash
pip install bharataddress
```

## Install PATA from source

```bash
git clone https://github.com/devi30232/PATA

cd PATA

pip install -e .
```

The core library requires Python 3.10 or later.

---

# 🌐 Install Streamlit

For the PATA application:

```bash
python -m pip install streamlit
```

Then run:

```bash
python -m streamlit run app.py
```

---

# 🌏 Optional Indic-Language Support

Native-script support can be installed with:

```bash
pip install "bharataddress[indic]"
```

The optional Indic support allows addresses written in scripts including:

- Devanagari
- Bengali
- Tamil
- Telugu
- Kannada
- Malayalam

Example:

```python
from bharataddress import parse

result = parse(
    "मुंबई, महाराष्ट्र 400001",
    transliterate=True
)
```

---

# 📦 BharatAddress Core Library

PATA is built on the BharatAddress address-resolution engine.

The core library provides offline Indian address parsing without requiring a model download, API key, or network request for normal parsing.

```python
from bharataddress import parse

result = parse(
    "Flat 302, Raheja Atlantis, Near Hanuman Mandir, Sector 31, Gurgaon 122001"
)

print(result)
```

JSON-friendly output:

```python
result.to_dict()
```

Example:

```json
{
  "building_number": "302",
  "building_name": "Raheja Atlantis",
  "landmark": "Hanuman mandir",
  "locality": "Sector 31",
  "city": "Gurgaon",
  "district": "Gurgaon",
  "state": "Haryana",
  "pincode": "122001",
  "confidence": 1.0
}
```

---

# 🧩 Address Components

A parsed address can contain:

| Field | Description |
|---|---|
| `building_number` | Numeric building / house / flat number |
| `building_name` | Building name |
| `landmark` | Near/Opp/Behind/Beside landmark |
| `locality` | Sector/Nagar/Colony/Layout etc. |
| `sub_locality` | Additional locality |
| `city` | City |
| `district` | District |
| `state` | State |
| `pincode` | Six-digit Indian pincode |
| `digipin` | DIGIPIN when coordinates are available |
| `latitude` | Latitude when available |
| `longitude` | Longitude when available |
| `confidence` | Parser confidence |
| `components_found` | Components detected |
| `cleaned` | Normalized address |
| `raw` | Original input |

---

# ⚙️ How the Core Parser Works

```text
Input Address
     │
     ▼
Layer 1 — Preprocess
     │
     ├── Unicode normalization
     ├── Abbreviation expansion
     ├── Vernacular normalization
     └── Whitespace cleanup
     │
     ▼
Layer 2 — Pincode Extraction
     │
     ├── Detect six-digit pincode
     └── India Post lookup
     │
     ▼
Layer 3 — Segment & Classify
     │
     ├── Building
     ├── Landmark
     └── Locality
     │
     ▼
Layer 4 — Confidence
     │
     ▼
ParsedAddress
```

The embedded pincode data contains Indian pincode information derived from the India Post directory.

It can be refreshed using:

```bash
python scripts/build_pincode_data.py
```

---

# 📮 Pincode Lookup

Pincode lookup can be used independently.

```python
from bharataddress import pincode

result = pincode.lookup("122001")

print(result)
```

Example:

```text
{
    'pincode': '122001',
    'district': 'Gurgaon',
    'city': 'Gurgaon',
    'state': 'Haryana',
    'offices': [...]
}
```

---

# 🗺️ Geocoder

The original BharatAddress library supports pincode-centroid geocoding.

```python
from bharataddress import parse, geocode

result = parse("Sector 31, Gurgaon 122001")

coordinates = geocode(result)

print(coordinates)
```

Example:

```text
(28.47, 77.04)
```

Online Nominatim geocoding can be explicitly enabled:

```python
geocode(
    parse("Some Locality, Town 999999"),
    online=True
)
```

Or:

```python
result = parse(
    "Connaught Place, New Delhi 110001",
    geocode=True
)

print(result.latitude)
print(result.longitude)
```

The core parser does not require online geocoding for normal operation.

---

# 📍 PATA vs Core Geocoding

The distinction is important.

### BharatAddress

Provides:

```text
Pincode
   ↓
Pincode centroid
   ↓
Latitude / Longitude
```

### PATA

Adds:

```text
Pincode candidates
       +
Locality
       +
Landmarks
       +
OpenStreetMap evidence
       ↓
Candidate verification
       ↓
Confidence
```

Therefore PATA is designed to handle the ambiguity that a simple pincode centroid cannot solve by itself.

---

# 🔢 DIGIPIN

BharatAddress ships a Python implementation of the official India Post DIGIPIN algorithm.

```python
from bharataddress import digipin

code = digipin.encode(
    28.6129,
    77.2295
)

print(code)
```

Decode:

```python
digipin.decode("39J-429-L4TK")
```

Validate:

```python
digipin.validate("39J-429-L4TK")
```

`parse()` can also accept coordinates:

```python
from bharataddress import parse

result = parse(
    "Plot 88, Basheer Bagh, Hyderabad 500001",
    latlng=(17.3850, 78.4867)
)

print(result.digipin)
```

The parser does not generate a DIGIPIN unless a coordinate is available.

---

# 🧾 Formatter

The formatter reconstructs a clean address from parsed components.

```python
from bharataddress import parse, format

p = parse(
    "Flat 302, Raheja Atlantis, Sector 31, Gurgaon 122001"
)

print(format(p, style="india_post"))
```

Single-line format:

```python
format(p, style="single_line")
```

Label format:

```python
print(format(p, style="label"))
```

---

# ✅ Validator

The validator checks address consistency.

```python
from bharataddress import parse, validate, is_deliverable

p = parse(
    "Flat 302, Sector 31, Gurgaon 122001"
)

print(is_deliverable(p))

print(validate(p))
```

`validate()` can identify inconsistencies between:

```text
Pincode
State
District
City
```

`is_deliverable()` performs the minimum required-field check.

---

# 🔤 Phonetic Matching

Indian addresses frequently contain spelling and transliteration variations.

Examples:

```text
Gurgaon
Gurugram
Gudgaon
```

BharatAddress provides normalization and fuzzy matching.

```python
from bharataddress import phonetic

phonetic.normalise("Gurugram")
```

Fuzzy comparison:

```python
phonetic.fuzzy_ratio(
    "Bengaluru",
    "Bangalore"
)
```

Best match:

```python
phonetic.best_match(
    "Kolkatta",
    ["Kolkata", "Delhi", "Mumbai"]
)
```

The library contains a hand-tuned alias map for common Indian city-name changes and transliteration differences.

---

# 🔗 Address Similarity

Addresses can be compared using:

```python
from bharataddress import address_similarity

score = address_similarity(
    "MG Road, Bengaluru 560001",
    "Mahatma Gandhi Road, Bangalore 560001"
)

print(score)
```

The result is between:

```text
0 → completely different
1 → highly similar
```

Pincode is treated as a strong signal, followed by city and locality information.

---

# 📦 Batch Processing

Multiple addresses can be parsed together.

```python
from bharataddress import parse_batch

addresses = [
    "Sector 31, Gurgaon 122001",
    "Anna Salai, Chennai 600002"
]

results = parse_batch(addresses)
```

---

# 📄 CSV Processing

CSV files can be processed directly.

```python
from bharataddress import parse_csv

output = parse_csv(
    "addresses.csv",
    column="address"
)

print(output)
```

This produces:

```text
addresses_parsed.csv
```

PATA's pincode verification layer can additionally use a pincode reference CSV for location verification.

---

# 🐼 Pandas DataFrame Support

For data-processing workflows:

```python
from bharataddress import parse_dataframe

result = parse_dataframe(
    df,
    column="address"
)
```

Pandas is loaded only when this functionality is used.

---

# 🧾 GSTIN Enrichment

The library can extract the state associated with a GSTIN.

```python
from bharataddress import extract_state_from_gstin

state = extract_state_from_gstin(
    "29ABCDE1234F1Z5"
)

print(state)
```

The first two digits represent the GST Council state code.

---

# 💻 CLI

Parse an address:

```bash
bharataddress parse \
"12, Dalal Street, Fort, Mumbai 400001" \
--pretty
```

Lookup a pincode:

```bash
bharataddress lookup 560001
```

Check version:

```bash
bharataddress --version
```

---

# 📊 Data Sources

PATA uses several sources for different purposes.

## 1. India Post Pincode Data

Used for:

- Pincode validation
- City lookup
- District lookup
- State lookup
- Pincode candidates
- Geographic reference information

The core library contains an embedded pincode directory.

---

## 2. Pincode Reference CSV

The PATA application can use the provided pincode reference CSV for additional verification.

Typical fields:

```text
Pincode
Office Name
District
State
Latitude
Longitude
```

This provides a separate reference layer for the hackathon workflow.

---

## 3. OpenStreetMap

Used for:

- Landmark verification
- Nearby POI search
- Geographic evidence

Examples:

```text
Temple
Bank
ATM
Bakery
Hospital
School
Shop
Restaurant
```

---

# 🔐 Privacy and Security

Address information can contain sensitive location information.

PATA follows an evidence-first and minimal-retention approach.

### Original Address

The original address is retained during processing so that automated changes can be audited.

### No Silent Replacement

The application shows the original input alongside the processed information.

### Low Confidence

The application does not need to pretend that an uncertain result is correct.

### External Services

OpenStreetMap is used specifically for geographic evidence where required.

### Production Deployment

A production implementation should process and store address/location data according to applicable Indian privacy and data-residency requirements.

---

# ⚡ Performance

The BharatAddress core parser is intentionally lightweight.

Its design avoids requiring:

- Large language models
- Large model downloads
- GPU infrastructure
- API keys
- Network calls for normal parsing

The original project reports approximately 5 ms per parser call for its deterministic core workflow.

PATA keeps the fast local parser as the first stage and uses external geographic verification only when required.

Conceptually:

```text
Fast Local Parsing
        │
        ▼
Is more evidence required?
        │
    ┌───┴───┐
    │       │
   No      Yes
    │       │
    │       ▼
    │   OSM / Reference
    │   Verification
    │       │
    └───┬───┘
        ▼
      Result
```

This approach avoids unnecessary external requests.

---

# 💰 Cost Optimization

PATA follows a local-first architecture.

Routine operations can use:

```text
Local parser
+
Pincode lookup
+
Rules
+
Reference data
```

These do not require an expensive AI API call.

External geographic verification is performed only when additional evidence is required.

A future production system could further improve this using:

```text
Cache
   ↓
Pincode lookup
   ↓
Cached OSM results
   ↓
OSM request only when required
```

For highly ambiguous addresses, a small open-source model or other reasoning component could be introduced without requiring it for every transaction.

---

# 🧪 Self-Check

The PATA verification layer is designed around a final consistency check.

Before accepting a location, the system can consider:

```text
Does the pincode match?

Does the locality match?

Does the city match?

Are multiple candidates present?

Does the landmark exist?

Is the landmark geographically relevant?

Are coordinates available?

Is the confidence sufficient?
```

If evidence is insufficient:

```text
Needs Verification
```

rather than:

```text
False certainty
```

---

# 🏗️ Project Structure

The project combines the original BharatAddress package with the PATA application.

```text
PATA/
│
├── app.py
│
├── bharataddress/
│   ├── __init__.py
│   ├── parser.py
│   ├── geocoder.py
│   ├── database.py
│   ├── formatter.py
│   ├── validator.py
│   ├── phonetic.py
│   ├── similarity.py
│   ├── batch.py
│   ├── enrichment.py
│   ├── digipin.py
│   │
│   └── data/
│       ├── pincodes.json
│       └── vernacular_mappings.json
│
├── tests/
│
├── scripts/
│
├── docs/
│
├── reports/
│
├── private/
│
├── bharataddress-site/
│
├── .githooks/
│
├── .gitignore
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

The main PATA application is:

```text
app.py
```

The original address-resolution engine remains inside:

```text
bharataddress/
```

---

# 🔄 Complete PATA Data Flow

```text
                         INPUT
                           │
                           ▼
        "Opposite Ganesh temple, near Sai bakery,
             Ramalingapuram, Tenali"
                           │
                           ▼
                  ┌─────────────────┐
                  │   app.py        │
                  │   Streamlit     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ BharatAddress   │
                  │ parse()         │
                  └────────┬────────┘
                           │
                           ▼
                  ParsedAddress
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Landmark         Locality          City
          │                │                │
          │                └──────┬─────────┘
          │                       │
          ▼                       ▼
   OpenStreetMap             Pincode CSV
     Evidence                Verification
          │                       │
          └──────────┬────────────┘
                     │
                     ▼
              Candidate Matching
                     │
                     ▼
               Confidence
                     │
             ┌───────┴────────┐
             │                │
             ▼                ▼
         Verified        Needs Verification
             │                │
             └───────┬────────┘
                     ▼
                 UI Result
```

---

# 🧪 Testing

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run:

```bash
pytest
```

The original project contains tests covering:

- Parser
- DIGIPIN
- Formatter
- Validator
- Geocoder
- Similarity
- Batch processing
- Enrichment

There is also an architectural test that ensures the default parser does not make network calls.

---

# 📈 Benchmarks

The original BharatAddress project includes a hand-labelled evaluation dataset:

```text
tests/data/gold_200.jsonl
```

It covers:

- Metro addresses
- Tier-2 addresses
- Rural addresses
- Landmark-heavy addresses
- Vernacular inputs
- No-pincode addresses
- Irregular punctuation
- S/O formats

The benchmark reports per-field precision, recall and F1.

## Current accuracy

| Tier | Fields | F1 |
|---|---|---|
| Rock-solid | `pincode` | 0.995 |
| Rock-solid | `state` | 0.982 |
| Rock-solid | `district` | 0.965 |
| Rock-solid | `city` | 0.959 |
| Rock-solid | `building_number` | 0.962 |
| Good | `landmark` | 0.918 |
| Good | `locality` | 0.813 |
| Best-effort | `building_name` | 0.727 |
| Best-effort | `sub_locality` | 0.458 |

Exact match across all nine fields is lower because free-text fields such as `building_name` and `sub_locality` are inherently harder to resolve.

This is why PATA adds external verification instead of treating parser output as perfect ground truth.

---

# ⚖️ BharatAddress vs TinyBERT

The original project includes a comparison against Shiprocket's TinyBERT Indian address NER model.

| Field | BharatAddress | TinyBERT |
|---|---:|---:|
| Pincode | **0.995** | 0.984 |
| City | **0.959** | 0.718 |
| Building number | 0.958 | **0.973** |
| State | **0.923** | 0.268 |
| Landmark | **0.918** | 0.580 |
| District | **0.933** | N/A |
| Locality | **0.723** | 0.634 |
| Building name | 0.635 | **0.643** |
| Sub-locality | 0.472 | 0.470 |

The core advantage of BharatAddress is that pincode-derived administrative fields are resolved through the embedded India Post directory instead of being purely predicted.

PATA builds on that deterministic foundation with real-world geographic evidence.

---

# 🚚 Business Impact

PATA is designed specifically for last-mile delivery.

## 1. Reduce delivery failures

More reliable address resolution can help reduce situations where delivery partners cannot find customers.

## 2. Reduce driver search time

Landmark evidence can help narrow down ambiguous locations.

## 3. Improve address quality

Messy customer-entered addresses can be converted into structured information.

## 4. Detect risky addresses earlier

Confidence scores allow uncertain addresses to be flagged before they cause delivery problems.

## 5. Improve customer experience

Customers may spend less time explaining their location to delivery partners.

---

# 🏪 Example Delivery Scenario

Customer enters:

```text
Opposite Ganesh temple, near Sai bakery,
Ramalingapuram, Tenali
```

PATA performs:

```text
1. Parse address
        ↓
2. Extract landmarks
        ↓
3. Extract locality
        ↓
4. Identify city
        ↓
5. Search pincode reference data
        ↓
6. Detect possible pincode candidates
        ↓
7. Search OpenStreetMap landmarks
        ↓
8. Compare available evidence
        ↓
9. Calculate confidence
        ↓
10. Return location or request verification
```

This is the core location-intelligence workflow.

---

# 🧩 Hackathon Requirement Alignment

| AI Build 2026 Requirement | PATA Implementation |
|---|---|
| Messy Indian addresses | BharatAddress parser |
| Landmark directions | Landmark extraction |
| Informal colony names | Locality extraction |
| Wrong/missing pincodes | Pincode verification |
| Real landmarks | OpenStreetMap |
| Resolve ambiguity | Multiple candidate detection + evidence |
| Low-confidence handling | Confidence / verification status |
| Evidence | Pincode + landmark evidence |
| Fast processing | Local deterministic parsing |
| Indian language support | Indic/transliteration support |
| Auditability | Original + processed address |
| Privacy | Minimal processing / retention approach |
| Working MVP | Streamlit application |
| Architecture | Documented layered architecture |
| Business value | Last-mile delivery workflow |

---

# 📋 What the System Returns

A `ParsedAddress` contains fields such as:

```text
raw
cleaned
building_number
building_name
landmark
locality
sub_locality
city
district
state
pincode
digipin
latitude
longitude
confidence
components_found
```

PATA additionally presents verification information in the UI.

Example:

```text
Original Address
----------------
Opposite Ganesh temple, near Sai bakery,
Ramalingapuram, Tenali

Parsed Address
--------------
Landmark: Ganesh temple; Sai bakery
Locality: Ramalingapuram
City: Tenali

Pincode
-------
Not found

Pincode Verification
--------------------
Multiple candidate records found.

OpenStreetMap
-------------
Searching real nearby landmarks...

Confidence
----------
40%

Status
------
Location needs verification.
```

---

# 🌐 Language Support

Indian addresses can contain multiple writing styles.

Examples:

```text
Hyderabad
హైదరాబాద్
Mumbai
मुंबई
Bengaluru
ಬೆಂಗಳೂರು
```

The core library supports optional Indic-script transliteration.

PATA's architecture is designed so language normalization can occur before address verification.

Future versions can improve:

- Hinglish handling
- Telugu transliteration
- Hindi transliteration
- Tamil transliteration
- Kannada transliteration
- Bengali transliteration
- Mixed-script addresses

---

# 📊 Why Evidence Matters

Consider:

```text
Ramalingapuram, Tenali
```

Suppose the pincode reference database returns multiple candidates.

A naive system might:

```text
Candidate 1
     ↓
Return Candidate 1
```

PATA instead follows:

```text
Candidate 1
Candidate 2
Candidate 3
Candidate 4
Candidate 5
Candidate 6
       │
       ▼
Landmark evidence
       │
       ▼
OpenStreetMap
       │
       ▼
Compare geographic evidence
       │
       ▼
Select only when sufficiently supported
```

This is particularly important for landmark-relative Indian addresses.

---

# 🔮 Future Production Architecture

A production version can expose PATA as an API.

```text
                 E-COMMERCE PLATFORM
                         │
                         ▼
                 ┌──────────────┐
                 │   PATA API   │
                 └──────┬───────┘
                        │
                        ▼
                Address Parser
                        │
                        ▼
               Candidate Generator
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
    Pincode Service             Landmark Service
          │                           │
          │                      OpenStreetMap
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
                Evidence Engine
                        │
                        ▼
               Confidence Engine
                        │
                        ▼
              Final Location Result
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
     High Confidence             Low Confidence
          │                           │
          ▼                           ▼
     Auto Process              Manual Verification
```

---

# 🔐 Production Security Considerations

A production implementation should additionally provide:

- Encryption in transit
- Encryption at rest
- Access control
- Authentication
- Role-based permissions
- Audit logging
- Data-retention policies
- Monitoring
- Rate limiting
- Secure API credentials
- External-service request controls

The hackathon MVP focuses on the address-resolution workflow rather than a complete production security platform.

---

# ⚡ Scalability Strategy

PATA can scale by separating fast local operations from external verification.

```text
                 Address
                    │
                    ▼
              Local Parser
                    │
                    ▼
             Cached Pincode
                    │
                    ▼
          Is evidence enough?
              │          │
             Yes         No
              │          │
              │          ▼
              │      OSM Search
              │          │
              └────┬─────┘
                   ▼
                Result
```

Future optimizations include:

- Pincode caching
- Landmark caching
- Candidate pre-filtering
- Local geographic indexes
- Async OSM requests
- Batch verification
- Local/open-source models for difficult cases

---

# 💰 AI Cost Strategy

PATA does not need an expensive AI model for every address.

The basic pipeline can rely on:

```text
Rules
+
Local Parser
+
Pincode Database
+
OpenStreetMap
```

For difficult cases, a future implementation could introduce an AI reasoning layer.

```text
Easy Address
     ↓
Deterministic Parser
     ↓
Result

Ambiguous Address
     ↓
Deterministic Parser
     ↓
Evidence Search
     ↓
AI Reasoning if required
     ↓
Result
```

This keeps the average processing cost low.

---

# 🛣️ Roadmap

## Completed in the original BharatAddress foundation

- Parser
- Pincode lookup
- Formatter
- Validator
- Phonetic matching
- Address similarity
- Batch processing
- CSV helpers
- DataFrame helpers
- GSTIN enrichment
- Pincode-centroid geocoding
- DIGIPIN
- Indic-language support
- CLI
- Tests
- Benchmarks

## Added for PATA

- Streamlit application
- Messy Indian address workflow
- Original-address display
- Pincode CSV verification
- Multiple pincode candidate detection
- OpenStreetMap landmark search
- Landmark evidence workflow
- Confidence display
- Low-confidence verification status
- Hackathon-oriented location intelligence workflow

## Future

- Improved landmark ranking
- Distance-based landmark scoring
- Better pincode candidate ranking
- Interactive map
- Delivery-partner navigation
- More regional-language normalization
- Hinglish support
- Cached OSM results
- Production REST API
- Authentication
- Monitoring
- Larger evaluation dataset
- Human feedback loop
- Local/open-source reasoning model for ambiguous addresses

---

# 🧪 Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the PATA application:

```bash
python -m streamlit run app.py
```

---

# 🤝 Contributing

Useful contributions include:

1. Real-world difficult Indian address examples
2. New landmark patterns
3. Regional-language mappings
4. Pincode verification improvements
5. OpenStreetMap matching improvements
6. Better candidate ranking
7. Additional test cases
8. Performance improvements
9. Documentation
10. UI improvements

For parser-related improvements, useful locations include:

```text
bharataddress/data/
tests/
scripts/
```

---

# 🗂️ Development Data

The project can use:

```text
India Post pincode data
        │
        ▼
Embedded BharatAddress database

PATA Pincode CSV
        │
        ▼
Pincode verification

OpenStreetMap
        │
        ▼
Landmark verification
```

These sources serve different purposes and are not treated as interchangeable.

---

# 📌 Important Design Principle

PATA intentionally separates:

```text
Parsing
```

from:

```text
Verification
```

A parser answers:

> "What components appear to be present in this address?"

A verification system answers:

> "Does the available geographic evidence support this interpretation?"

This distinction is central to the PATA architecture.

---

# 🧠 Why Not Just Use a Generic Geocoder?

A generic geocoder may receive:

```text
Opposite Ganesh temple, near Sai bakery,
Ramalingapuram, Tenali
```

and return a generic point.

PATA instead exposes the intermediate reasoning:

```text
Landmark detected
        ↓
Locality detected
        ↓
Pincode candidates found
        ↓
Landmark searched in OpenStreetMap
        ↓
Evidence compared
        ↓
Confidence calculated
```

This makes the result more explainable for delivery operations.

---

# 🎯 Core Value Proposition

PATA combines the strengths of deterministic Indian address parsing with external geographic verification.

```text
             BharatAddress
                   │
                   ▼
          Structured Address
                   │
                   ├───────────────┐
                   │               │
                   ▼               ▼
             Pincode Data       OSM
                   │               │
                   └───────┬───────┘
                           ▼
                       Evidence
                           │
                           ▼
                      Confidence
                           │
                           ▼
                  Location Decision
```

The goal is not simply to produce a coordinate.

The goal is to produce a **coordinate that can be explained and supported by evidence**.

---

# 🏆 Final Project Summary

PATA is an Indian address intelligence platform for last-mile delivery.

It starts with the BharatAddress deterministic parser and extends it with:

```text
Messy Address
      ↓
Indian Address Parsing
      ↓
Pincode Verification
      ↓
Landmark Verification
      ↓
OpenStreetMap Evidence
      ↓
Confidence
      ↓
Verified / Needs Verification
```

This approach is designed for the realities of Indian addresses:

- Landmark-based directions
- Informal localities
- Missing information
- Incorrect information
- Multiple possible locations
- Mixed scripts
- Transliteration
- Delivery-oriented geographic ambiguity

---

# 📣 Hackathon Pitch

> **PATA turns messy Indian delivery addresses into evidence-backed locations. It parses landmarks, localities and administrative information, verifies pincode candidates against reference data, checks real nearby landmarks through OpenStreetMap, and reports confidence instead of silently guessing.**

---

# 📄 License

MIT.

See [`LICENSE`](LICENSE) for the complete license information.

The original BharatAddress project uses public India Post-derived reference data as documented by the project.

---

# 👥 Contributing to the Address Dataset

The most useful improvements are real-world difficult addresses that expose parser or verification weaknesses.

Useful examples include:

```text
Landmark-heavy addresses
Missing-pincode addresses
Wrong-pincode addresses
Mixed-script addresses
Hinglish addresses
Informal colony names
Abbreviated addresses
Transliterated locality names
```

When contributing examples, avoid exposing unnecessary personal information.

---

# ⭐ PATA

### Indian Address Intelligence

**AI Build 2026 · E-Commerce in India · Student Edition**

**Track 1 — Location Intelligence for Last-Mile Delivery**

```text
Parse.
Verify.
Show the evidence.
Don't silently guess.
```