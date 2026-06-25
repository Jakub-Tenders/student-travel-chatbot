const state = {
  activeTab: "flights",
  history: [],
};

const els = {
  apiBase: document.querySelector("#apiBase"),
  chatMessages: document.querySelector("#chatMessages"),
  chatForm: document.querySelector("#chatForm"),
  chatInput: document.querySelector("#chatInput"),
  clearChat: document.querySelector("#clearChat"),
  tabs: document.querySelectorAll(".tab"),
  transportForm: document.querySelector("#transportForm"),
  hostelForm: document.querySelector("#hostelForm"),
  transportSubmit: document.querySelector("#transportSubmit"),
  results: document.querySelector("#results"),
  status: document.querySelector("#status"),
};

const samplePrompts = [
  "I can help turn a rough trip idea into transport and hostel searches.",
  "Try asking: cheapest way from Paris to Barcelona next Friday.",
];

function apiBase() {
  return els.apiBase.value.replace(/\/$/, "");
}

function setStatus(message, type = "") {
  els.status.textContent = message;
  els.status.className = `status ${type}`.trim();
}

function addMessage(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `message ${role}`;
  bubble.textContent = text;
  els.chatMessages.appendChild(bubble);
  els.chatMessages.scrollTop = els.chatMessages.scrollHeight;
}

function remember(role, content) {
  state.history.push({ role, content });
  if (state.history.length > 12) {
    state.history = state.history.slice(-12);
  }
}

async function requestJson(path, options = {}) {
  const response = await fetch(`${apiBase()}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.error || `Request failed with status ${response.status}`);
  }

  return data;
}

function buildQuery(params) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, value);
    }
  });
  return query.toString();
}

function formatKey(key) {
  return key
    .replace(/_/g, " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function valueToText(value) {
  if (value === null || value === undefined || value === "") {
    return "N/A";
  }
  if (Array.isArray(value)) {
    return value.map(valueToText).join(", ");
  }
  if (typeof value === "object") {
    return Object.entries(value)
      .map(([key, item]) => `${formatKey(key)}: ${valueToText(item)}`)
      .join("; ");
  }
  return String(value);
}

function renderResults(type, items) {
  els.results.innerHTML = "";

  if (!Array.isArray(items) || items.length === 0) {
    setStatus(`No ${type} found for this search.`);
    return;
  }

  setStatus(`Showing ${items.length} ${type}.`);

  items.forEach((item, index) => {
    const card = document.createElement("article");
    card.className = "result-card";

    const title = document.createElement("h3");
    title.textContent = item.title || item.name || item.company || `${formatKey(type)} ${index + 1}`;
    card.appendChild(title);

    const list = document.createElement("ul");
    list.className = "meta-list";

    Object.entries(item)
      .filter(([key]) => !["title", "name"].includes(key))
      .slice(0, 8)
      .forEach(([key, value]) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${formatKey(key)}:</strong> ${escapeHtml(valueToText(value))}`;
        list.appendChild(li);
      });

    card.appendChild(list);
    els.results.appendChild(card);
  });
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setActiveTab(tab) {
  state.activeTab = tab;
  els.tabs.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.tab === tab);
  });

  const isHostels = tab === "hostels";
  els.hostelForm.classList.toggle("hidden", !isHostels);
  els.transportForm.classList.toggle("hidden", isHostels);
  els.transportSubmit.textContent = tab === "rides" ? "Search rides" : "Search flights";
}

async function handleChatSubmit(event) {
  event.preventDefault();
  const message = els.chatInput.value.trim();
  if (!message) return;

  els.chatInput.value = "";
  addMessage("user", message);
  remember("user", message);

  const button = els.chatForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Sending";

  try {
    const data = await requestJson("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message, history: state.history }),
    });
    const reply = data.reply || "No reply returned.";
    addMessage("assistant", reply);
    remember("assistant", reply);
  } catch (error) {
    addMessage("error", error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Send";
  }
}

async function handleTransportSubmit(event) {
  event.preventDefault();
  const origin = document.querySelector("#origin").value.trim();
  const destination = document.querySelector("#destination").value.trim();
  const date = document.querySelector("#date").value;
  const endpoint = state.activeTab === "rides" ? "/api/search/rides" : "/api/search/flights";
  const resultKey = state.activeTab === "rides" ? "rides" : "flights";

  setStatus(`Searching ${resultKey}...`, "loading");
  els.results.innerHTML = "";

  try {
    const query = buildQuery({ origin, destination, date });
    const data = await requestJson(`${endpoint}?${query}`);
    renderResults(resultKey, data[resultKey]);
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function handleHostelSubmit(event) {
  event.preventDefault();
  const city = document.querySelector("#city").value.trim();
  const maxPrice = document.querySelector("#maxPrice").value;

  setStatus("Searching hostels...", "loading");
  els.results.innerHTML = "";

  try {
    const query = buildQuery({ city, max_price: maxPrice });
    const data = await requestJson(`/api/search/hostels?${query}`);
    renderResults("hostels", data.hostels);
  } catch (error) {
    setStatus(error.message, "error");
  }
}

function init() {
  samplePrompts.forEach((prompt) => addMessage("assistant", prompt));

  els.chatForm.addEventListener("submit", handleChatSubmit);
  els.transportForm.addEventListener("submit", handleTransportSubmit);
  els.hostelForm.addEventListener("submit", handleHostelSubmit);
  els.clearChat.addEventListener("click", () => {
    state.history = [];
    els.chatMessages.innerHTML = "";
    samplePrompts.forEach((prompt) => addMessage("assistant", prompt));
  });

  els.tabs.forEach((button) => {
    button.addEventListener("click", () => setActiveTab(button.dataset.tab));
  });

  const today = new Date().toISOString().slice(0, 10);
  document.querySelector("#date").value = today;
}

init();
