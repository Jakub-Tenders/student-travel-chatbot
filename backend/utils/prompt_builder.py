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
        lines = ["Available carpooling rides:"]
        for r in rides[:5]:
            lines.append(
                f"  - {r['driver_name']} ({r['car_model']}): {r['origin']} → {r['destination']}, "
                f"departs {r['departure_time']}, {r['seats_available']} seat(s), "
                f"€{r['price_eur']} — rated {r['rating']}/5"
            )
        sections.append("\n".join(lines))

    if hostels:
        lines = ["Available hostels:"]
        for h in hostels[:5]:
            lines.append(
                f"  - {h['name']} ({h['city']}): €{h['price_per_night_eur']}/night, "
                f"rated {h['rating']}/10 ({h['reviews_count']} reviews), "
                f"amenities: {', '.join(h['amenities'])}"
            )
        sections.append("\n".join(lines))

    if not sections:
        return ""

    return "Here is real travel data for the user's query:\n\n" + "\n\n".join(sections)