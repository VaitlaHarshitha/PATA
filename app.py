import streamlit as st
import pandas as pd
import re
import requests
import math
from difflib import SequenceMatcher
from bharataddress import parse

st.set_page_config(page_title="PATA", page_icon="📍")


# ---------------- PINCODE DATA ----------------

@st.cache_data
def load_pincodes():
    return pd.read_csv(
        "data/pincodes.csv",
        dtype={"pincode": str}
    )


pincode_df = load_pincodes()


# ---------------- TEXT NORMALIZATION ----------------

def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


pincode_df["office_normalized"] = (
    pincode_df["officename"].apply(normalize)
)


# ---------------- PINCODE SEARCH ----------------

def find_pincode_candidates(locality):

    if not locality:
        return pd.DataFrame()

    locality = normalize(locality)

    matches = pincode_df[
        pincode_df["office_normalized"] == locality
    ]

    if matches.empty:
        matches = pincode_df[
            pincode_df["office_normalized"].str.contains(
                locality,
                na=False,
                regex=False
            )
        ]

    return matches[
        [
            "officename",
            "pincode",
            "district",
            "statename",
            "latitude",
            "longitude"
        ]
    ].drop_duplicates()


# ---------------- DISTANCE ----------------

def distance_km(lat1, lon1, lat2, lon2):

    try:
        R = 6371

        p1 = math.radians(float(lat1))
        p2 = math.radians(float(lat2))

        dp = math.radians(float(lat2) - float(lat1))
        dl = math.radians(float(lon2) - float(lon1))

        a = (
            math.sin(dp / 2) ** 2
            + math.cos(p1)
            * math.cos(p2)
            * math.sin(dl / 2) ** 2
        )

        return 2 * R * math.asin(math.sqrt(a))

    except:
        return None


# ---------------- FAST OSM SEARCH ----------------

def search_osm(landmarks, candidates):

    if not landmarks or candidates.empty:
        return []

    # Use the first candidate as search centre
    candidate = candidates.iloc[0]

    lat = candidate["latitude"]
    lon = candidate["longitude"]

    if pd.isna(lat) or pd.isna(lon):
        return []

    # Search all landmark names in ONE query
    regex = "|".join(
        re.escape(x)
        for x in landmarks
    )

    query = f"""
    [out:json][timeout:5];

    nwr
      ["name"~"{regex}",i]
      (around:5000,{lat},{lon});

    out center;
    """

    try:

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            headers={
                "User-Agent": "PATA-Student-Hackathon"
            },
            timeout=8
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for element in data.get("elements", []):

            tags = element.get("tags", {})
            name = tags.get("name")

            if not name:
                continue

            if "lat" in element:
                osm_lat = element["lat"]
                osm_lon = element["lon"]

            elif "center" in element:
                osm_lat = element["center"]["lat"]
                osm_lon = element["center"]["lon"]

            else:
                continue

            best_match = max(
                SequenceMatcher(
                    None,
                    normalize(landmark),
                    normalize(name)
                ).ratio()
                for landmark in landmarks
            )

            distance = distance_km(
                lat,
                lon,
                osm_lat,
                osm_lon
            )

            results.append({
                "OSM Name": name,
                "Latitude": osm_lat,
                "Longitude": osm_lon,
                "Distance (km)": round(distance, 2)
                if distance is not None else None,
                "Name Match (%)": round(best_match * 100)
            })

        results.sort(
            key=lambda x: (
                -x["Name Match (%)"],
                x["Distance (km)"]
                if x["Distance (km)"] is not None
                else 999
            )
        )

        return results[:10]

    except Exception:
        return []


# ---------------- UI ----------------

st.title("PATA 📍")
st.subheader("Indian Address Intelligence")

address = st.text_area(
    "Enter a messy Indian address",
    placeholder=(
        "Opposite Ganesh temple, near Sai bakery, "
        "Ramalingapuram, Tenali"
    )
)


if st.button("Find Location"):

    if not address.strip():

        st.warning("Please enter an address.")

    else:

        try:

            # ADDRESS PARSER
            result = parse(address)

            st.success("Address parsed successfully!")

            # ORIGINAL
            st.subheader("Original Address")
            st.write(result.raw)

            # PARSED
            st.subheader("AI Parsed Address")

            col1, col2 = st.columns(2)

            with col1:

                st.write("🏛️ **Landmark**")
                st.write(result.landmark or "Not found")

                st.write("📍 **Locality**")
                st.write(result.locality or "Not found")

                st.write("🏙️ **City**")
                st.write(result.city or "Not found")

            with col2:

                st.write("📮 **Pincode**")
                st.write(result.pincode or "Not found")

                st.write("🗺️ **Latitude**")
                st.write(result.latitude or "Not available")

                st.write("🗺️ **Longitude**")
                st.write(result.longitude or "Not available")


            # PINCODE
            st.subheader("📮 Pincode Verification")

            candidates = find_pincode_candidates(
                result.locality
            )

            if candidates.empty:

                st.warning(
                    "No pincode candidates found."
                )

            else:

                st.info(
                    f"Found {len(candidates)} "
                    "possible pincode record(s)."
                )

                st.dataframe(
                    candidates,
                    use_container_width=True,
                    hide_index=True
                )


                # OSM
                st.subheader(
                    "🗺️ OpenStreetMap Landmark Evidence"
                )

                landmarks = []

                if result.landmark:

                    landmarks = [
                        x.strip()
                        for x in result.landmark.split(";")
                        if x.strip()
                    ]

                if landmarks:

                    st.write(
                        "Searching OpenStreetMap..."
                    )

                    osm_results = search_osm(
                        landmarks,
                        candidates
                    )

                    if osm_results:

                        st.success(
                            "✓ Landmark evidence found."
                        )

                        st.dataframe(
                            pd.DataFrame(osm_results),
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.warning(
                            "⚠️ No matching landmark "
                            "was found on OpenStreetMap."
                        )

                else:

                    st.warning(
                        "No landmark extracted."
                    )


            # CONFIDENCE
            confidence = result.confidence * 100

            st.subheader("Confidence")

            st.progress(int(confidence))

            st.write(
                f"🎯 **{confidence:.0f}%**"
            )


            # SAFETY
            if (
                result.pincode is None
                or result.latitude is None
            ):

                st.warning(
                    "⚠️ Final coordinates are not "
                    "verified yet. PATA will not guess."
                )


        except Exception as e:

            st.error("Unable to process the address.")
            st.exception(e)