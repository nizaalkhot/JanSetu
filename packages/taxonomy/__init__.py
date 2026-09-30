"""JanSetu UN SDG-aligned development taxonomy."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SubCategory(BaseModel):
    id: str
    name: str
    description: str
    keywords: List[str] = Field(default_factory=list)


class TaxonomyCategory(BaseModel):
    id: str
    sdg_goal: int
    name: str
    description: str
    subcategories: List[SubCategory] = Field(default_factory=list)
    multilingual_names: Dict[str, str] = Field(default_factory=dict)


# Unified taxonomy aligned with UN Sustainable Development Goals (SDGs)
TAXONOMY_CATEGORIES: Dict[str, TaxonomyCategory] = {
    "water_sanitation": TaxonomyCategory(
        id="water_sanitation",
        sdg_goal=6,
        name="Clean Water & Sanitation",
        description="Drinking water supply, borewells, pipeline leaks, contamination, sewage and sanitation facilities.",
        multilingual_names={
            "en": "Clean Water & Sanitation",
            "hi": "स्वच्छ जल एवं स्वच्छता",
            "pt": "Água Limpa e Saneamento",
            "ru": "Чистая вода и санитария",
            "zh": "清洁饮水和卫生设施",
        },
        subcategories=[
            SubCategory(
                id="drinking_water",
                name="Drinking Water Shortage",
                description="Lack of potable drinking water, dry borewells, delayed water tankers",
                keywords=["water", "pani", "tanker", "borewell", "handpump", "tap water", "água", "вода"],
            ),
            SubCategory(
                id="water_quality",
                name="Water Contamination",
                description="Dirty water, fluorosis, chemical runoff, sickness from tap water",
                keywords=["dirty water", "smell", "poisonous", "yellow water", "turbid", "fluoride"],
            ),
            SubCategory(
                id="drainage_sanitation",
                name="Drainage & Public Toilets",
                description="Overflowing sewers, lack of public community toilets, open defecation",
                keywords=["drain", "sewer", "gutter", "toilet", "nallah", "esgoto", "latrine"],
            ),
        ],
    ),
    "healthcare": TaxonomyCategory(
        id="healthcare",
        sdg_goal=3,
        name="Good Health & Well-being",
        description="Primary health centres (PHC), medicine availability, emergency ambulances, doctors.",
        multilingual_names={
            "en": "Healthcare & Clinics",
            "hi": "स्वास्थ्य एवं प्राथमिक चिकित्सा",
            "pt": "Saúde e Bem-Estar",
            "ru": "Здравоохранение и медицина",
            "zh": "良好健康与福祉",
        },
        subcategories=[
            SubCategory(
                id="primary_clinic",
                name="Primary Health Centre (PHC) Access",
                description="Closed clinic, absent doctor or nurse, lack of essential medicines",
                keywords=["doctor", "hospital", "phc", "clinic", "dispensary", "dawa", "médico", "врач"],
            ),
            SubCategory(
                id="emergency_services",
                name="Maternal & Emergency Services",
                description="No ambulance access, lack of maternity ward, emergency delays",
                keywords=["ambulance", "pregnant", "delivery", "emergency", "108", "ambulância"],
            ),
        ],
    ),
    "transport_roads": TaxonomyCategory(
        id="transport_roads",
        sdg_goal=9,
        name="Roads & Rural Connectivity",
        description="Potholes, all-weather rural roads, broken bridges, public bus transport.",
        multilingual_names={
            "en": "Roads & Rural Connectivity",
            "hi": "सड़कें एवं ग्रामीण संपर्क",
            "pt": "Estradas e Mobilidade Rural",
            "ru": "Дороги и транспортная связность",
            "zh": "产业、创新和基础设施",
        },
        subcategories=[
            SubCategory(
                id="rural_roads",
                name="All-Weather Road Connectivity",
                description="Muddy roads unpassable during monsoon, village cut off from highways",
                keywords=["road", "sadak", "pothole", "gaddha", "bridge", "pul", "estrada", "дорога"],
            ),
            SubCategory(
                id="public_transit",
                name="Public Bus / Transport Frequency",
                description="Infrequent buses for school children and workers, lack of stops",
                keywords=["bus", "transport", "bus stand", "auto", "onibus", "автобус"],
            ),
        ],
    ),
    "education": TaxonomyCategory(
        id="education",
        sdg_goal=4,
        name="Quality Education",
        description="Government schools, teacher absenteeism, classroom infrastructure, girls toilets.",
        multilingual_names={
            "en": "Quality Education",
            "hi": "गुणवत्तापूर्ण शिक्षा एवं विद्यालय",
            "pt": "Educação de Qualidade",
            "ru": "Качественное образование",
            "zh": "优质教育",
        },
        subcategories=[
            SubCategory(
                id="school_infrastructure",
                name="School Facilities & Toilets",
                description="Broken roofs, lack of separate girls toilets, electricity in school",
                keywords=["school", "vidyalaya", "classroom", "desk", "escuela", "школа"],
            ),
            SubCategory(
                id="teacher_availability",
                name="Teacher Shortage",
                description="Single teacher for entire primary school, unstaffed STEM subjects",
                keywords=["teacher", "adhyapak", "shikshak", "professor", "учитель"],
            ),
        ],
    ),
    "electricity_energy": TaxonomyCategory(
        id="electricity_energy",
        sdg_goal=7,
        name="Affordable & Clean Energy",
        description="Frequent power outages, low voltage, transformer breakdown, solar microgrids.",
        multilingual_names={
            "en": "Electricity & Energy",
            "hi": "विद्युत एवं स्वच्छ ऊर्जा",
            "pt": "Energia Acessível e Limpa",
            "ru": "Доступная и чистая энергия",
            "zh": "经济适用的清洁能源",
        },
        subcategories=[
            SubCategory(
                id="power_outages",
                name="Frequent Outages & Transformer Burnout",
                description="Daily 10+ hours load shedding, burnt transformer unrepaired for weeks",
                keywords=["power cut", "bijli", "transformer", "load shedding", "energia", "свет"],
            ),
        ],
    ),
    "digital_connectivity": TaxonomyCategory(
        id="digital_connectivity",
        sdg_goal=9,
        name="Digital Public Infrastructure (DPI)",
        description="Mobile cellular coverage, optical fibre (BharatNet), Common Service Centres (CSC).",
        multilingual_names={
            "en": "Digital Connectivity & DPI",
            "hi": "डिजिटल कनेक्टिविटी एवं इंटरनेट",
            "pt": "Conectividade Digital e DPI",
            "ru": "Цифровая связь и инфраструктура",
            "zh": "数字基础设施",
        },
        subcategories=[
            SubCategory(
                id="cellular_broadband",
                name="Mobile Signal & Last-Mile Internet",
                description="Zero network towers, students climbing hills for mobile reception",
                keywords=["internet", "mobile network", "tower", "signal", "range", "conexao", "сеть"],
            ),
            SubCategory(
                id="csc_ration_services",
                name="E-Gov CSC / Biometric Ration Issues",
                description="Biometric fingerprint failure at ration shop, e-governance kiosk offline",
                keywords=["ration", "aadhaar", "fingerprint", "csc", "kiosk", "biometric"],
            ),
        ],
    ),
}


def get_all_categories() -> List[TaxonomyCategory]:
    return list(TAXONOMY_CATEGORIES.values())


def match_category_by_keywords(text: str) -> Optional[str]:
    """Simple keyword matching fallback when LLM is unavailable."""
    text_lower = text.lower()
    for cat_id, cat in TAXONOMY_CATEGORIES.items():
        for sub in cat.subcategories:
            for kw in sub.keywords:
                if kw.lower() in text_lower:
                    return cat_id
    return "water_sanitation"  # default fallback
