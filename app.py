import requests
import streamlit as st

API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BACK = "https://image.tmdb.org/t/p/w1280"

st.set_page_config(
    page_title="FRAME",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

section[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMainBlockContainer"],
.block-container {
    background: #f5f0e8 !important;
    font-family: 'Outfit', sans-serif !important;
    color: #1a1714 !important;
    padding: 0 !important;
    max-width: 100% !important;
}

.block-container { padding: 0 !important; max-width: 100% !important; }

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 3rem;
    border-bottom: 1px solid #e0d9ce;
    background: #f5f0e8;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-style: italic;
    letter-spacing: -0.01em;
    color: #1a1714;
}
.topbar-logo span { color: #c0392b; }
.topbar-nav {
    display: flex;
    gap: 2.5rem;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7a7269;
}

.hero { padding: 5rem 3rem 3rem; max-width: 780px; }
.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c0392b;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 1.02;
    letter-spacing: -0.02em;
    color: #1a1714;
    margin-bottom: 1.5rem;
}
.hero-title em { font-style: italic; color: #c0392b; }

[data-testid="stTextInput"] { margin: 0 !important; }
[data-testid="stTextInput"] > div { background: transparent !important; border: none !important; padding: 0 !important; }
[data-testid="stTextInput"] input {
    background: #fff !important;
    border: 1.5px solid #1a1714 !important;
    border-radius: 0 !important;
    color: #1a1714 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.9rem 1.2rem !important;
    width: 100% !important;
    transition: box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus { box-shadow: 4px 4px 0 #1a1714 !important; outline: none !important; }
[data-testid="stTextInput"] input::placeholder { color: #b5aea3 !important; }

[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1.5px solid #1a1714 !important;
    border-radius: 0 !important;
    color: #1a1714 !important;
    font-family: 'Outfit', sans-serif !important;
}

[data-testid="stButton"] > button {
    background: #fff !important;
    border: 1.5px solid #1a1714 !important;
    border-radius: 0 !important;
    color: #1a1714 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    transition: background 0.15s, color 0.15s, box-shadow 0.15s !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    background: #1a1714 !important;
    color: #f5f0e8 !important;
    box-shadow: 3px 3px 0 #c0392b !important;
}

.cat-strip {
    display: flex;
    gap: 0.5rem;
    padding: 1.5rem 3rem 0;
    border-top: 1px solid #e0d9ce;
    margin-top: 0.5rem;
    overflow-x: auto;
}
.cat-pill {
    white-space: nowrap;
    padding: 0.35rem 1rem;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid #c8bfb2;
    background: transparent;
    color: #7a7269;
}
.cat-pill.active { background: #1a1714; border-color: #1a1714; color: #f5f0e8; }

.section-label {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    padding: 2.5rem 3rem 1.2rem;
}
.section-label-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    letter-spacing: -0.01em;
    color: #1a1714;
}
.section-label-line { flex: 1; height: 1px; background: #e0d9ce; }
.section-label-count { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #b5aea3; }

.grid-wrap { padding: 0 3rem 3rem; }

[data-testid="stImage"] img {
    border-radius: 2px !important;
    display: block;
    transition: transform 0.22s cubic-bezier(.25,.46,.45,.94), filter 0.22s;
    filter: saturate(0.9);
}
[data-testid="stImage"] img:hover { transform: translateY(-6px); filter: saturate(1.1); }

.film-label {
    font-size: 0.73rem;
    color: #7a7269;
    margin-top: 0.35rem;
    line-height: 1.25;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    letter-spacing: 0.02em;
}

.detail-backdrop {
    width: 100%;
    height: 52vh;
    min-height: 300px;
    object-fit: cover;
    display: block;
    filter: brightness(0.6) saturate(0.8);
}
.detail-backdrop-wrap {
    position: relative;
    overflow: hidden;
    background: #1a1714;
}
.detail-backdrop-wrap::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, transparent 40%, #f5f0e8 100%);
}

.detail-info-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c0392b;
    margin-bottom: 0.5rem;
}
.detail-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 4vw, 3.5rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #1a1714;
    margin-bottom: 0.8rem;
}
.genre-tag {
    display: inline-block;
    border: 1px solid #c8bfb2;
    padding: 0.25rem 0.7rem;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7a7269;
    margin: 0 0.3rem 0.4rem 0;
}
.detail-overview {
    font-size: 1rem;
    line-height: 1.8;
    color: #4a4540;
    font-weight: 300;
    margin-top: 1rem;
    max-width: 620px;
}
.back-btn-wrap { padding: 1.2rem 3rem 0; }

hr { border: none !important; border-top: 1px solid #e0d9ce !important; margin: 0 !important; }

[data-testid="stAlert"] {
    background: #fff !important;
    border: 1px solid #e0d9ce !important;
    border-radius: 0 !important;
    color: #7a7269 !important;
    font-family: 'Outfit', sans-serif !important;
    margin: 0 3rem !important;
}

.no-poster {
    background: #ede8df;
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #c8bfb2;
    font-size: 1.8rem;
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

CATEGORIES = ["trending", "popular", "top_rated", "now_playing", "upcoming"]
CAT_LABELS  = ["Trending", "Popular", "Top Rated", "Now Playing", "Upcoming"]

for key, val in [("view","home"), ("selected_tmdb_id",None), ("category","trending")]:
    if key not in st.session_state:
        st.session_state[key] = val

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
qp_cat  = st.query_params.get("cat")
if qp_view in ("home","details"): st.session_state.view = qp_view
if qp_id:
    try: st.session_state.selected_tmdb_id = int(qp_id); st.session_state.view = "details"
    except: pass
if qp_cat in CATEGORIES: st.session_state.category = qp_cat


def goto_home(cat=None):
    st.session_state.view = "home"
    if cat: st.session_state.category = cat
    st.query_params["view"] = "home"
    st.query_params["cat"] = st.session_state.category
    if "id" in st.query_params: del st.query_params["id"]
    st.rerun()

def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()

@st.cache_data(ttl=30)
def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400: return None, f"HTTP {r.status_code}"
        return r.json(), None
    except Exception as e:
        return None, str(e)

def poster_grid(cards, cols=7, key_prefix="g"):
    if not cards: st.info("Nothing to show here."); return
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards): break
            m = cards[idx]; idx += 1
            tid = m.get("tmdb_id")
            with colset[c]:
                if m.get("poster_url"): st.image(m["poster_url"], use_column_width=True)
                else: st.markdown("<div class='no-poster'>🎞</div>", unsafe_allow_html=True)
                if st.button("View", key=f"{key_prefix}_{r}_{c}_{tid}"):
                    if tid: goto_details(tid)
                st.markdown(f"<div class='film-label'>{m.get('title','')}</div>", unsafe_allow_html=True)

def tfidf_to_cards(items):
    out = []
    for x in items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            out.append({"tmdb_id": tmdb["tmdb_id"], "title": tmdb.get("title") or x.get("title",""), "poster_url": tmdb.get("poster_url")})
    return out

def parse_search(data, kw, limit=24):
    kl = kw.strip().lower(); raw = []
    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            t = (m.get("title") or "").strip(); tid = m.get("id"); pp = m.get("poster_path")
            if t and tid: raw.append({"tmdb_id": int(tid), "title": t, "poster_url": f"{TMDB_IMG}{pp}" if pp else None, "release_date": m.get("release_date","")})
    elif isinstance(data, list):
        for m in data:
            tid = m.get("tmdb_id") or m.get("id"); t = (m.get("title") or "").strip()
            if t and tid: raw.append({"tmdb_id": int(tid), "title": t, "poster_url": m.get("poster_url"), "release_date": m.get("release_date","")})
    matched = [x for x in raw if kl in x["title"].lower()]
    final = matched if matched else raw
    suggestions = [(f"{x['title']} ({(x.get('release_date') or '')[:4]})" if (x.get('release_date') or '')[:4] else x['title'], x["tmdb_id"]) for x in final[:10]]
    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]} for x in final[:limit]]
    return suggestions, cards


# ── TOP NAV ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='topbar'>
  <div class='topbar-logo'><em>Frame</em><span>.</span></div>
  <div class='topbar-nav'>
    <span>Discover</span><span>Collections</span><span>About</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.view == "home":

    st.markdown("""
    <div class='hero'>
      <div class='hero-eyebrow'>Your personal film guide</div>
      <div class='hero-title'>Find your next<br><em>obsession.</em></div>
    </div>
    """, unsafe_allow_html=True)

    _, sc, __ = st.columns([3, 6, 3])
    with sc:
        typed = st.text_input("Search", placeholder="Search — inception, parasite, dune…", label_visibility="collapsed")

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get("/tmdb/search", {"query": typed.strip()})
            if err or data is None:
                st.error(f"Search error: {err}")
            else:
                suggestions, cards = parse_search(data, typed.strip(), 24)
                if suggestions:
                    labels = ["— pick a title —"] + [s[0] for s in suggestions]
                    _, selc, __ = st.columns([3, 6, 3])
                    with selc:
                        sel = st.selectbox("Suggestions", labels, index=0, label_visibility="collapsed")
                    if sel != "— pick a title —":
                        goto_details({s[0]: s[1] for s in suggestions}[sel])

                st.markdown(f"""
                <div class='section-label'>
                  <div class='section-label-text'>Results for "{typed}"</div>
                  <div class='section-label-line'></div>
                  <div class='section-label-count'>{len(cards)} films</div>
                </div>""", unsafe_allow_html=True)
                st.markdown("<div class='grid-wrap'>", unsafe_allow_html=True)
                poster_grid(cards, cols=7, key_prefix="sr")
                st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    current_cat = st.session_state.category
    pills = "<div class='cat-strip'>" + "".join(
        f"<div class='cat-pill {'active' if s == current_cat else ''}'>{l}</div>"
        for s, l in zip(CATEGORIES, CAT_LABELS)
    ) + "</div><div style='height:0.5rem'></div>"
    st.markdown(pills, unsafe_allow_html=True)

    btn_cols = st.columns(len(CATEGORIES))
    for i, (s, l) in enumerate(zip(CATEGORIES, CAT_LABELS)):
        with btn_cols[i]:
            if st.button(l, key=f"cat_{s}"): goto_home(cat=s)

    st.markdown(f"""
    <div class='section-label'>
      <div class='section-label-text'>{CAT_LABELS[CATEGORIES.index(current_cat)]}</div>
      <div class='section-label-line'></div>
    </div>""", unsafe_allow_html=True)

    home_cards, err = api_get("/home", {"category": current_cat, "limit": 28})
    if err or not home_cards: st.error(f"Feed error: {err or 'unknown'}"); st.stop()

    st.markdown("<div class='grid-wrap'>", unsafe_allow_html=True)
    poster_grid(home_cards, cols=7, key_prefix="hf")
    st.markdown("</div>", unsafe_allow_html=True)


elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No film selected.")
        if st.button("← Back"): goto_home()
        st.stop()

    data, err = api_get(f"/movie/id/{tmdb_id}")
    if err or not data: st.error(f"Could not load: {err or 'unknown'}"); st.stop()

    if data.get("backdrop_url"):
        st.markdown(f"<div class='detail-backdrop-wrap'><img class='detail-backdrop' src='{data['backdrop_url']}' /></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='height:6rem;background:#1a1714'></div>", unsafe_allow_html=True)

    st.markdown("<div class='back-btn-wrap'>", unsafe_allow_html=True)
    bc, _ = st.columns([1, 9])
    with bc:
        if st.button("← Back"): goto_home()
    st.markdown("</div>", unsafe_allow_html=True)

    genres = data.get("genres", [])
    release_yr = (data.get("release_date") or "")[:4]
    genre_tags = "".join(f"<span class='genre-tag'>{g['name']}</span>" for g in genres)

    pc, ic = st.columns([1, 3], gap="large")
    with pc:
        if data.get("poster_url"): st.image(data["poster_url"], use_column_width=True)
        else: st.markdown("<div class='no-poster' style='height:330px'>🎞</div>", unsafe_allow_html=True)
    with ic:
        st.markdown(f"""
        <div style='padding-top:2rem'>
          <div class='detail-info-eyebrow'>{release_yr}</div>
          <div class='detail-title'>{data.get('title','')}</div>
          <div>{genre_tags}</div>
          <div class='detail-overview'>{data.get('overview') or 'No overview available.'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin:2.5rem 0'>", unsafe_allow_html=True)

    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get("/movie/search", {"query": title, "tfidf_top_n": 14, "genre_limit": 14})
        if not err2 and bundle:
            tfc = tfidf_to_cards(bundle.get("tfidf_recommendations"))
            gc  = bundle.get("genre_recommendations", [])
            if tfc:
                st.markdown("<div class='section-label'><div class='section-label-text'>Similar films</div><div class='section-label-line'></div></div>", unsafe_allow_html=True)
                st.markdown("<div class='grid-wrap'>", unsafe_allow_html=True)
                poster_grid(tfc, cols=7, key_prefix="dt")
                st.markdown("</div>", unsafe_allow_html=True)
            if gc:
                st.markdown("<div class='section-label'><div class='section-label-text'>More in genre</div><div class='section-label-line'></div></div>", unsafe_allow_html=True)
                st.markdown("<div class='grid-wrap'>", unsafe_allow_html=True)
                poster_grid(gc, cols=7, key_prefix="dg")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            gonly, err3 = api_get("/recommend/genre", {"tmdb_id": tmdb_id, "limit": 14})
            if not err3 and gonly:
                st.markdown("<div class='section-label'><div class='section-label-text'>You might also like</div><div class='section-label-line'></div></div>", unsafe_allow_html=True)
                st.markdown("<div class='grid-wrap'>", unsafe_allow_html=True)
                poster_grid(gonly, cols=7, key_prefix="dfb")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No recommendations available right now.")
