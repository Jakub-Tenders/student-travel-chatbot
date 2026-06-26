# Roam — Student Travel Chatbot

An AI chatbot that helps students find the cheapest way to travel, sleep, and explore on a tight budget. Built for the EPITA "Generative AIs & Chatbots" project.

Ask it things like *"I have €50 and want to go somewhere from Paris this weekend"* and it suggests flights, carpooling rides, and hostels, then reasons about them with an LLM.

## Tech stack

- **Backend:** Python + Flask
- **Frontend:** Vanilla JS, HTML, CSS (no framework)
- **AI:** Groq (`llama-3.1-8b-instant`, OpenAI-compatible API)
- **Flights:** Sky-Scrapper (RapidAPI) — currently running in mock mode
- **Rides:** BlaBlaCar-style carpooling — mock data (see note below)
- **Hostels:** Mock data, seeded per city for consistent results

## Why mock data for rides and hostels?

BlaBlaCar's real API requires partner approval (not self-serve), and free hostel-specific APIs (Hostelworld, Hostelz) don't offer public access either. Rather than block the project on third-party approval timelines, we built mock services with the **same function signatures and return shapes** a real API would have. Swapping in real data later means changing one internal function, not the routes or frontend. This trade-off is documented further in our `B-conception.docx` and `C-privacy.docx`.

Flights currently also default to mock data (`USE_MOCK = True` in `services/sky_scrapper.py`) while we finish testing the real RapidAPI integration.

## Project structure

```
backend/
  app.py                    Flask app entry point, registers routes
  routes/
    chat.py                 POST /api/chat — main chatbot endpoint
    search.py               GET /api/search/flights, /api/search/rides
    hostels.py              GET /api/search/hostels
  services/
    llm.py                  Groq API calls + system prompt
    sky_scrapper.py         Flight search (mock + real RapidAPI logic)
    blablacar.py             Carpooling search (mock)
    hostels.py              Hostel search (mock)
  utils/
    prompt_builder.py        Formats flights/rides/hostels into LLM context
  requirements.txt
  .env.example

frontend/
  index.html                 Single page: chat + search panel + results
  src/
    app.js                   All frontend logic (fetch calls, rendering)
    styles.css

docs/
  A-innovation.docx
  B-conception.docx
  C-privacy.docx
  D-security.docx
  collaboration-log.md
  GenAI-log.docx
```

## Setup

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
GROQ_API_KEY=your_groq_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
```

Get a free Groq key at [console.groq.com](https://console.groq.com) (no credit card needed).

Run the server:

```bash
python app.py
```

Server runs at `http://127.0.0.1:5001`. Confirm it's alive:

```bash
curl http://127.0.0.1:5001/
```

### 2. Frontend

No build step needed. Just open `frontend/index.html` in a browser, or serve it locally:

```bash
cd frontend
python3 -m http.server 8000
```

Then visit `http://localhost:8000`. The frontend talks to the backend at the URL shown in the **API** field at the top of the page (defaults to `http://localhost:5001`).

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Main chatbot endpoint. Body: `{ message, history, origin?, destination?, date? }` |
| `GET` | `/api/search/flights` | Query params: `origin`, `destination`, `date` |
| `GET` | `/api/search/rides` | Query params: `origin`, `destination`, `date` |
| `GET` | `/api/search/hostels` | Query params: `city`, `max_price?` |

## Known limitations

- Flight and ride data are currently mocked — see "Why mock data" above
- No authentication / user accounts yet (see `D-security.docx` for planned approach)
- Single-session chat history only (not persisted between page reloads)

## Team

See `docs/collaboration-log.md` for individual contributions and decision history.