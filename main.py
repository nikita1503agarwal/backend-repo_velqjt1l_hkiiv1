import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

app = FastAPI(title="UMAR SAJID • Jarvis Design Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Models ----------
class Brief(BaseModel):
    client: Optional[str] = Field(None, description="Client or brand name")
    project_type: Literal[
        "logo", "poster", "banner", "branding", "thumbnail", "reel", "ad", "packaging", "social"
    ]
    goals: Optional[str] = None
    audience: Optional[str] = None
    tone: Optional[str] = None
    deliverables: Optional[str] = None
    constraints: Optional[str] = None
    references: Optional[str] = None


class IdeaRequest(BaseModel):
    category: Literal[
        "logo", "poster", "banner", "branding", "thumbnail", "reel", "ad", "packaging", "social"
    ]
    keywords: Optional[str] = None
    style: Optional[str] = None


class ResourceRequest(BaseModel):
    topic: str
    kind: Literal["icons", "mockups", "inspiration", "palettes", "references", "ui", "templates"]


class PaletteRequest(BaseModel):
    vibe: Literal[
        "minimal", "bold", "luxury", "playful", "tech", "retro", "nature", "pastel", "high-contrast"
    ]
    accent: Optional[str] = None


class FontsRequest(BaseModel):
    mood: Literal[
        "modern", "classic", "friendly", "tech", "luxury", "editorial", "playful", "serif+sans", "display+body"
    ]


# ---------- Helpers ----------

def lines(items: List[str]) -> List[str]:
    return [f"• {i}" for i in items]


def suggest_palettes(vibe: str, accent: Optional[str]) -> List[dict]:
    presets = {
        "minimal": [
            ["#0F172A", "#334155", "#94A3B8", "#E2E8F0", "#FFFFFF"],
            ["#111827", "#374151", "#9CA3AF", "#F3F4F6", "#FFFFFF"],
        ],
        "bold": [
            ["#0A0A0A", "#E11D48", "#22D3EE", "#F59E0B", "#F5F3FF"],
            ["#111111", "#7C3AED", "#10B981", "#F43F5E", "#F3F4F6"],
        ],
        "luxury": [
            ["#0B0B0C", "#1F2937", "#D4AF37", "#F1F5F9", "#FFFFFF"],
            ["#111827", "#4B5563", "#B08D57", "#E5E7EB", "#FAFAF9"],
        ],
        "playful": [
            ["#0EA5E9", "#F97316", "#22C55E", "#EAB308", "#FDE68A"],
            ["#A78BFA", "#F472B6", "#34D399", "#60A5FA", "#FDE68A"],
        ],
        "tech": [
            ["#0B1020", "#1F2937", "#22D3EE", "#A78BFA", "#F8FAFC"],
            ["#020617", "#0F172A", "#38BDF8", "#7DD3FC", "#E2E8F0"],
        ],
        "retro": [
            ["#2A1A1F", "#D97706", "#059669", "#B91C1C", "#FDE68A"],
            ["#1F2937", "#BE185D", "#065F46", "#CA8A04", "#FEF3C7"],
        ],
        "nature": [
            ["#0B3D2E", "#065F46", "#34D399", "#A7F3D0", "#F0FDF4"],
            ["#1B4332", "#2D6A4F", "#95D5B2", "#CEEAD6", "#FAFAF9"],
        ],
        "pastel": [
            ["#FEE2E2", "#E9D5FF", "#DBEAFE", "#D1FAE5", "#FEF3C7"],
            ["#FDE2F3", "#CDE8E5", "#EEF5FF", "#D9EDBF", "#FFF6E0"],
        ],
        "high-contrast": [
            ["#0A0A0A", "#FFFFFF", "#FF1F1F", "#1F51FF", "#FFD400"],
            ["#000000", "#FFFFFF", "#00E5FF", "#FF3D00", "#D1D5DB"],
        ],
    }
    out = [{"name": f"{vibe.title()} {i+1}", "colors": p} for i, p in enumerate(presets.get(vibe, []))]
    if accent:
        out.insert(0, {"name": f"Custom with {accent}", "colors": ["#0F172A", "#1F2937", accent, "#E2E8F0", "#FFFFFF"]})
    return out


def font_pairs(mood: str) -> List[dict]:
    pairs = {
        "modern": [
            {"heading": "Poppins", "body": "Inter"},
            {"heading": "Montserrat", "body": "Roboto"},
        ],
        "classic": [
            {"heading": "Merriweather", "body": "Source Sans Pro"},
            {"heading": "Playfair Display", "body": "Lato"},
        ],
        "friendly": [
            {"heading": "Nunito", "body": "Rubik"},
            {"heading": "Quicksand", "body": "Inter"},
        ],
        "tech": [
            {"heading": "IBM Plex Sans", "body": "Inter"},
            {"heading": "Space Grotesk", "body": "Manrope"},
        ],
        "luxury": [
            {"heading": "Cormorant Garamond", "body": "Source Serif Pro"},
            {"heading": "Canela", "body": "Inter"},
        ],
        "editorial": [
            {"heading": "Fraunces", "body": "Inter"},
            {"heading": "Georgia", "body": "Helvetica Neue"},
        ],
        "playful": [
            {"heading": "Baloo 2", "body": "Poppins"},
            {"heading": "Chewy", "body": "Nunito"},
        ],
        "serif+sans": [
            {"heading": "Merriweather", "body": "Inter"},
            {"heading": "Playfair Display", "body": "Work Sans"},
        ],
        "display+body": [
            {"heading": "Bebas Neue", "body": "Inter"},
            {"heading": "Oswald", "body": "Open Sans"},
        ],
    }
    return pairs.get(mood, pairs["modern"])


def category_ideas(category: str, keywords: Optional[str], style: Optional[str]) -> List[str]:
    k = (keywords or "").lower()
    s = (style or "").lower()
    if category == "logo":
        return [
            f"Monogram mark combining initials with {s or 'geometric'} rhythm",
            f"Negative-space symbol referencing {k or 'core brand metaphor'}",
            f"Wordmark with custom ligatures and {s or 'optical kerning'}",
            f"Badge logo adaptable to square avatars and dark mode",
        ]
    if category == "poster":
        return [
            f"Type-led layout with oversized {s or 'grotesk'} headline",
            f"Grid-based collage mixing {k or 'brand'} textures and duotones",
            "Depth via layered shadows, gradients, and subtle noise",
            "QR focal point with motion blur trail for energy",
        ]
    if category == "banner":
        return [
            f"Asymmetrical split with product on {s or 'right'} and CTA on left",
            "Diagonal energy line guiding eyes to CTA",
            f"Contrast pair: muted background + {k or 'vibrant'} accent",
            "System of 3 sizes sharing one modular grid",
        ]
    if category == "branding":
        return [
            f"Core logo + icon set + color system using {s or '60/30/10'} rule",
            f"Tone of voice lines distilled from {k or 'brand story'}",
            "Packaging mockups and social system for rollout",
            "Motion spec for reveal and micro-interactions",
        ]
    if category == "thumbnail":
        return [
            f"High-contrast face crop + {k or 'bold'} keyword banner",
            "Triadic color stripe for brand recognition",
            f"Depth with cutout subject and {s or 'soft'} drop shadows",
            "Iterate 3 variants and A/B in analytics",
        ]
    if category == "reel":
        return [
            f"Hook in first 1s with animated {k or 'headline'}",
            "Beat-synced transitions; keep text < 8 words/frame",
            f"End card with {s or 'clean'} CTA and logo loop",
            "Use masked gradients for futuristic aura",
        ]
    if category == "ad":
        return [
            f"Problem → Solution → Proof → CTA using {s or 'minimal'} layout",
            f"Showcase {k or 'benefit'} with animated before/after",
            "One focal point, ruthless whitespace",
            "Test 3 headlines, 2 visuals, 2 CTAs",
        ]
    if category == "packaging":
        return [
            f"Front hero zone + {s or 'structured'} info stack",
            f"Color blocking inspired by {k or 'ingredients/origin'}",
            "Shelf impact via bold type and tactile pattern",
            "Die-line friendly vector motifs",
        ]
    if category == "social":
        return [
            f"Carousel narrative: Hook → Value → Proof → CTA in {s or '5'} slides",
            f"Template system using {k or 'brand'} modules",
            "Stories: vertical rhythm with sticker moments",
            "ALT text crafted for accessibility",
        ]
    return ["Simple, clear, on-brand."]


def resource_suggestions(topic: str, kind: str) -> List[str]:
    t = topic.title()
    catalogs = {
        "icons": ["Phosphor Icons", "Lucide", "Feather", "Heroicons", "Material Symbols"],
        "mockups": ["Device mockups (Figma)", "Smart object PSDs", "Artboard Studio", "Rotato"],
        "inspiration": ["Behance moodboards", "Dribbble shots", "Awwwards galleries", "Mobbin"],
        "palettes": ["Coolors schemes", "Adobe Color", "Happy Hues", "Color Hunt"],
        "references": ["Pinterest board", "Brand book PDFs", "Campaign tear-sheets"],
        "ui": ["Mobbin patterns", "UI Coach", "Figma Community kits", "Refactoring UI"],
        "templates": ["Canva set", "Figma templates", "Creative Market", "Envato Elements"],
    }
    base = catalogs.get(kind, [])
    return [f"{i} — tuned for {t}" for i in base]


# ---------- Routes ----------

@app.get("/")
def read_root():
    return {"message": "UMAR SAJID • Jarvis Design Agent API"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.post("/api/brief/analyze")
def analyze_brief(brief: Brief):
    tasks = [
        f"Research audience: {brief.audience or 'define segments, needs, channels'}",
        f"Define tone: {brief.tone or '3 adjectives + do/don\'t list'}",
        f"Core message + CTA aligned to goals: {brief.goals or 'clarify business outcome'}",
        f"Deliverables: {brief.deliverables or 'sizes, formats, platforms'}",
        f"Constraints: {brief.constraints or 'brand rules, deadlines, budget'}",
        "Moodboard: 12 refs across type, color, layout, motion",
        "Creative directions: 3 distinct routes with rationale",
        "Production plan + timeline",
    ]
    risks = [
        "Scope creep without clear deliverables",
        "Low contrast harming accessibility",
        "Over-stylized type reducing legibility",
    ]
    return {
        "client": brief.client or "Unknown",
        "project_type": brief.project_type,
        "summary": lines([
            "Clarify success metrics",
            "Align tone and audience",
            "Design system before assets",
        ]),
        "tasks": lines(tasks),
        "risks": lines(risks),
    }


@app.post("/api/ideas")
def ideas(req: IdeaRequest):
    return {"category": req.category, "ideas": lines(category_ideas(req.category, req.keywords, req.style))}


@app.post("/api/resources")
def resources(req: ResourceRequest):
    return {"topic": req.topic, "kind": req.kind, "results": lines(resource_suggestions(req.topic, req.kind))}


@app.post("/api/palettes")
def palettes(req: PaletteRequest):
    return {"vibe": req.vibe, "palettes": suggest_palettes(req.vibe, req.accent)}


@app.post("/api/fonts")
def fonts(req: FontsRequest):
    return {"mood": req.mood, "pairs": font_pairs(req.mood)}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
