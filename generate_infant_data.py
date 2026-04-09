"""
Generate JSON data files for the Standard Infant Formula Market dashboard.
Produces:
  - public/data/value.json   (USD Million)
  - public/data/volume.json  (Million Units)
  - public/data/segmentation_analysis.json

Top-level segment types (yellow in images):
  By Product Type            -> 3-level (product type -> system -> item)
  By Feeding Stage           -> flat (3 leaves)
  By Ingredient Category     -> 2-level (category -> ingredient)
  By Functional Enrichment Profile -> flat (6 leaves)
  By Distribution Channel    -> flat (6 leaves)
"""

import json
import os
import random

BASE = os.path.dirname(os.path.abspath(__file__))
VALUE_JSON = os.path.join(BASE, "public", "data", "value.json")
VOLUME_JSON = os.path.join(BASE, "public", "data", "volume.json")
SEG_JSON = os.path.join(BASE, "public", "data", "segmentation_analysis.json")

YEARS = [str(y) for y in range(2020, 2037)]

GEO_HIERARCHY = {
    "North America": ["U.S.", "Canada"],
    "Europe": [
        "Germany", "France", "UK", "Italy", "Spain",
        "Rest of Western Europe", "Eastern Europe",
    ],
    "Asia Pacific": [
        "China", "Vietnam", "Singapore", "Japan", "South Korea",
        "Thailand", "Indonesia", "Malaysia", "India", "Pakistan",
        "Rest of Asia Pacific",
    ],
    "Latin America": ["Brazil", "Mexico", "Rest of Latin America"],
}
REGIONS = list(GEO_HIERARCHY.keys())
ALL_COUNTRIES = [c for cs in GEO_HIERARCHY.values() for c in cs]

COUNTRY_VALUE_2026 = {
    "U.S.": 5400, "Canada": 620,
    "Germany": 980, "France": 870, "UK": 760, "Italy": 540, "Spain": 410,
    "Rest of Western Europe": 690, "Eastern Europe": 880,
    "China": 9200, "Vietnam": 520, "Singapore": 140, "Japan": 1850,
    "South Korea": 690, "Thailand": 430, "Indonesia": 1280,
    "Malaysia": 360, "India": 2150, "Pakistan": 540,
    "Rest of Asia Pacific": 720,
    "Brazil": 880, "Mexico": 640, "Rest of Latin America": 510,
}
COUNTRY_CAGR = {
    "U.S.": 0.052, "Canada": 0.048,
    "Germany": 0.045, "France": 0.044, "UK": 0.046, "Italy": 0.041,
    "Spain": 0.043, "Rest of Western Europe": 0.044, "Eastern Europe": 0.057,
    "China": 0.071, "Vietnam": 0.082, "Singapore": 0.062, "Japan": 0.034,
    "South Korea": 0.052, "Thailand": 0.066, "Indonesia": 0.078,
    "Malaysia": 0.069, "India": 0.094, "Pakistan": 0.087,
    "Rest of Asia Pacific": 0.063,
    "Brazil": 0.058, "Mexico": 0.061, "Rest of Latin America": 0.055,
}

# ----- Hierarchical: By Product Type -> System -> Items -----
# NOTE: System-level names must be unique per product type (the dashboard's
# hierarchy is keyed by segment name, not full path), so each system label
# is suffixed with its product-type short name.
PRODUCT_TYPE_TREE = {
    "Conventional Standard Infant Formula": {
        "By Protein System (Conventional)": [
            "Whey-dominant formula",
            "Whey-casein blend formula",
            "Casein-adjusted formula",
            "Demineralised whey-based formula",
        ],
        "By Lipid System (Conventional)": [
            "DHA-fortified formula",
            "DHA + ARA fortified formula",
            "Fish oil-derived DHA formula",
            "Algal DHA formula",
            "Algal DHA + fungal ARA formula",
        ],
        "By Functional Ingredient Enrichment (Conventional)": [
            "Formula with probiotics",
            "Formula with prebiotics",
            "Formula with HMOs",
            "Formula with synbiotics",
            "Formula with combined functional ingredients",
        ],
    },
    "Organic / Clean-Label Standard Infant Formula": {
        "By Protein System (Organic)": [
            "Organic whey-based formula",
            "Organic whey-casein blend formula",
            "Organic demineralised whey-based formula",
        ],
        "By Lipid System (Organic)": [
            "Organic DHA-fortified formula",
            "Organic DHA + ARA fortified formula",
            "Organic algal DHA formula",
        ],
        "By Functional Ingredient Enrichment (Organic)": [
            "Organic formula with probiotics",
            "Organic formula with prebiotics",
            "Organic formula with HMOs",
            "Organic formula with synbiotics",
            "Organic formula with combined functional ingredients",
        ],
    },
    "Plant-Based Standard Infant Formula": {
        "By Protein System (Plant-Based)": [
            "Soy-based formula",
            "Soy protein isolate-based formula",
            "Rice-based formula",
            "Other plant protein-based formula",
        ],
        "By Lipid System (Plant-Based)": [
            "Plant-based formula with algal DHA",
            "Plant-based formula with DHA + ARA alternatives",
            "Vegan omega-fortified formula",
        ],
        "By Functional Ingredient Enrichment (Plant-Based)": [
            "Plant-based formula with probiotics",
            "Plant-based formula with prebiotics",
            "Plant-based formula with HMOs",
            "Plant-based formula with synbiotics",
            "Plant-based formula with combined functional ingredients",
        ],
    },
    "Comfort / Partially Hydrolysed Standard Infant Formula": {
        "By Protein System (Comfort)": [
            "Partially hydrolysed whey protein formula",
            "Partially hydrolysed whey-dominant blend formula",
        ],
        "By Lipid System (Comfort)": [
            "Comfort formula with DHA",
            "Comfort formula with DHA + ARA",
            "Comfort formula with algal DHA",
        ],
        "By Functional Ingredient Enrichment (Comfort)": [
            "Comfort formula with probiotics",
            "Comfort formula with prebiotics",
            "Comfort formula with HMOs",
            "Comfort formula with synbiotics",
            "Comfort formula with combined digestive-support ingredients",
        ],
    },
}

# Top-level Product Type proportions (sum = 1.0)
PRODUCT_TYPE_PROPS = {
    "Conventional Standard Infant Formula": 0.46,
    "Organic / Clean-Label Standard Infant Formula": 0.22,
    "Plant-Based Standard Infant Formula": 0.14,
    "Comfort / Partially Hydrolysed Standard Infant Formula": 0.18,
}
# Within a product type, split between the 3 systems (sum = 1.0)
# Keyed by short prefix (everything before the " (" suffix).
SYSTEM_SPLIT = {
    "By Protein System": 0.40,
    "By Lipid System": 0.30,
    "By Functional Ingredient Enrichment": 0.30,
}


def system_base_name(name):
    return name.split(" (")[0]

# ----- Hierarchical: By Ingredient Category -> Ingredient -----
INGREDIENT_TREE = {
    "Proteins": [
        "Whey protein",
        "Whey protein isolate",
        "Casein",
        "Demineralised whey",
        "Partially hydrolysed whey protein",
        "Soy protein",
        "Rice protein",
        "Other plant proteins",
    ],
    "Lipids": [
        "DHA",
        "ARA",
        "DHA + ARA blends",
    ],
    "Probiotics": [
        "Bifidobacterium species",
        "Lactobacillus species",
        "Other probiotic species",
    ],
    "Prebiotics": [
        "GOS",
        "FOS",
        "Inulin",
        "GOS/FOS blends",
        "Other prebiotic fibres",
    ],
    "HMOs": [
        "2'FL",
        "LnNT",
        "2'FL + LnNT blends",
        "Other single HMOs",
        "Multi-HMO systems",
    ],
}
INGREDIENT_CATEGORY_PROPS = {
    "Proteins": 0.45,
    "Lipids": 0.20,
    "Probiotics": 0.10,
    "Prebiotics": 0.12,
    "HMOs": 0.13,
}

# ----- Flat segment types -----
FLAT_SEGMENTS = {
    "By Feeding Stage": [
        "Stage 1 / First Infant Formula (0–6 months)",
        "Stage 2 / Follow-On Formula (6–12 months)",
        "Stage 3 / Toddler Formula / Growing-Up Milk (12–36 months)",
    ],
    "By Functional Enrichment Profile": [
        "Core nutrition formula",
        "Probiotic-enriched formula",
        "Prebiotic-enriched formula",
        "HMO-enriched formula",
        "Synbiotic formula",
        "Advanced functional formula",
    ],
    "By Distribution Channel": [
        "Hospital / Institutional",
        "Pharmacy / Drug Store",
        "Supermarket / Hypermarket",
        "Specialty Baby Stores",
        "E-Commerce / Online Retail",
        "Direct-to-Consumer",
    ],
}


def make_props(items, seed):
    rng = random.Random(seed)
    raw = [rng.uniform(0.6, 1.4) for _ in items]
    s = sum(raw)
    return [r / s for r in raw]


FLAT_PROPS = {st: make_props(items, hash(st) & 0xFFFFFFFF) for st, items in FLAT_SEGMENTS.items()}

# Per-system leaf proportions, normalized within each system
SYSTEM_LEAF_PROPS = {}
for pt, systems in PRODUCT_TYPE_TREE.items():
    SYSTEM_LEAF_PROPS[pt] = {}
    for sys_name, items in systems.items():
        SYSTEM_LEAF_PROPS[pt][sys_name] = make_props(items, hash(pt + sys_name) & 0xFFFFFFFF)

# Ingredient category leaf proportions
INGREDIENT_LEAF_PROPS = {
    cat: make_props(items, hash("ingr-" + cat) & 0xFFFFFFFF)
    for cat, items in INGREDIENT_TREE.items()
}


def project_series(value_2026, cagr):
    base_idx = YEARS.index("2026")
    return {
        y: round(value_2026 * ((1 + cagr) ** (i - base_idx)), 2)
        for i, y in enumerate(YEARS)
    }


def scale_series(series, factor, decimals=1):
    return {y: round(v * factor, decimals) for y, v in series.items()}


def with_aggregated(series, children):
    """Return a node mixing year totals (with _aggregated flag) and child nodes."""
    node = dict(series)
    node["_aggregated"] = True
    node.update(children)
    return node


def build_geo_segments(value_2026, cagr, decimals=1):
    """Return nested {segment_type: ...} block for one geography."""
    total = project_series(value_2026, cagr)
    out = {}

    # By Product Type (3-level, with parent aggregations)
    pt_block = {}
    for pt, sys_dict in PRODUCT_TYPE_TREE.items():
        pt_total = scale_series(total, PRODUCT_TYPE_PROPS[pt], decimals)
        sys_children = {}
        for sys_name, items in sys_dict.items():
            sys_total = scale_series(pt_total, SYSTEM_SPLIT[system_base_name(sys_name)], decimals)
            leaves = {}
            for item, p in zip(items, SYSTEM_LEAF_PROPS[pt][sys_name]):
                leaves[item] = scale_series(sys_total, p, decimals)
            sys_children[sys_name] = with_aggregated(sys_total, leaves)
        pt_block[pt] = with_aggregated(pt_total, sys_children)
    out["By Product Type"] = pt_block

    # By Ingredient Category (2-level, with parent aggregations)
    ing_block = {}
    for cat, items in INGREDIENT_TREE.items():
        cat_total = scale_series(total, INGREDIENT_CATEGORY_PROPS[cat], decimals)
        leaves = {}
        for item, p in zip(items, INGREDIENT_LEAF_PROPS[cat]):
            leaves[item] = scale_series(cat_total, p, decimals)
        ing_block[cat] = with_aggregated(cat_total, leaves)
    out["By Ingredient Category"] = ing_block

    # Flat segments (no aggregation needed - leaves are level 1)
    for seg_type, items in FLAT_SEGMENTS.items():
        node = {}
        for item, p in zip(items, FLAT_PROPS[seg_type]):
            node[item] = scale_series(total, p, decimals)
        out[seg_type] = node

    return out


def aggregate_segments(country_blocks):
    """Sum nested segment blocks across a list of country blocks."""
    def add(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            out = {}
            for k in a:
                if k == "_aggregated":
                    out[k] = True
                    continue
                out[k] = add(a[k], b[k])
            return out
        if isinstance(a, bool) or isinstance(b, bool):
            return True
        return round(a + b, 2)

    result = country_blocks[0]
    for blk in country_blocks[1:]:
        result = add(result, blk)
    return result


def build_data(is_volume=False):
    data = {}
    decimals = 2 if is_volume else 1
    for country in ALL_COUNTRIES:
        v2026 = COUNTRY_VALUE_2026[country]
        if is_volume:
            v2026 = v2026 / 22.0
        data[country] = build_geo_segments(v2026, COUNTRY_CAGR[country], decimals)

    # Aggregate to regions
    for region, countries in GEO_HIERARCHY.items():
        region_block = aggregate_segments([data[c] for c in countries])
        # Add "By Country" sub-listing
        by_country = {}
        for c in countries:
            # Use the aggregated totals on each product-type node
            year_totals = {y: 0.0 for y in YEARS}
            for pt_node in data[c]["By Product Type"].values():
                for y in YEARS:
                    year_totals[y] += pt_node[y]
            by_country[c] = {y: round(year_totals[y], decimals) for y in YEARS}
        region_block["By Country"] = by_country
        data[region] = region_block
    return data


def build_segmentation_analysis():
    analysis = {"Global": {}}

    # By Product Type (3-level)
    pt_node = {}
    for pt, sys_dict in PRODUCT_TYPE_TREE.items():
        sys_node = {}
        for sys_name, items in sys_dict.items():
            sys_node[sys_name] = {item: {} for item in items}
        pt_node[pt] = sys_node
    analysis["Global"]["By Product Type"] = pt_node

    # By Ingredient Category (2-level)
    ing_node = {}
    for cat, items in INGREDIENT_TREE.items():
        ing_node[cat] = {item: {} for item in items}
    analysis["Global"]["By Ingredient Category"] = ing_node

    # Flat segments
    for seg_type, items in FLAT_SEGMENTS.items():
        analysis["Global"][seg_type] = {item: {} for item in items}

    # By Region geography hierarchy
    analysis["Global"]["By Region"] = {}
    for region, countries in GEO_HIERARCHY.items():
        analysis["Global"]["By Region"][region] = {c: {} for c in countries}

    return analysis


def main():
    print("Generating value data...")
    value_data = build_data(is_volume=False)
    print("Generating volume data...")
    volume_data = build_data(is_volume=True)
    seg_analysis = build_segmentation_analysis()

    os.makedirs(os.path.dirname(VALUE_JSON), exist_ok=True)
    with open(VALUE_JSON, "w", encoding="utf-8") as f:
        json.dump(value_data, f, indent=2)
    with open(VOLUME_JSON, "w", encoding="utf-8") as f:
        json.dump(volume_data, f, indent=2)
    with open(SEG_JSON, "w", encoding="utf-8") as f:
        json.dump(seg_analysis, f, indent=2)

    print(f"Wrote {VALUE_JSON}")
    print(f"Wrote {VOLUME_JSON}")
    print(f"Wrote {SEG_JSON}")
    print(f"Top-level segment types: {list(value_data['North America'].keys())}")


if __name__ == "__main__":
    main()
