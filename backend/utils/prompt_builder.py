def build_travel_context(flights=None, rides=None, hostels=None) -> str:
    sections = []

    if flights:
        lines = ["Available flights:"]
        for f in flights[:5]:
            lines.append(
                f"  - {f['carrier']}: {f['departure']} → {f['arrival']}, "
                f"{f['stops']} stop(s), {f['duration']}min, {f['price']} {f['currency']}"
            )
        sections.append("\n".join(lines))

    if rides:
        sections.append("Available rides:\n  (coming soon)")

    if hostels:
        sections.append("Available hostels:\n  (coming soon)")

    if not sections:
        return ""

    return "Here is real travel data for the user's query:\n\n" + "\n\n".join(sections)