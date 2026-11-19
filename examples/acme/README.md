# Example: Acme Route Analytics (fictional)

A made-up company, to show what the setup produces for a non-healthcare
business. Acme sells software that finds late and failed deliveries in a
logistics company's own data. Only the parts that differ from the templates
are shown.

## config.yaml (excerpt)

```yaml
owner:
  name: "Jane Doe"
  first_name: "Jane"
  sender_email: "jane@acme-route.example"
  timezone: "Europe/Amsterdam"
company:
  name: "Acme Route Analytics"
  website: "acme-route.example"
  product: "software that finds late and failed deliveries in a carrier's own data, per depot, every day"
email:
  default_language: "English"
  language_by_market: {nl: English, de: German}
  greeting: "Dear <First name>"
  default_subject: "Depot-level delivery data"
  follow_ups: 1
```

## markets.md

| code | market | tier | last_run | total_added |
|---|---|---|---|---|
| nl | Netherlands | core |  | 0 |
| de | Germany | core |  | 0 |
| be | Belgium | expansion |  | 0 |

## playbook.md (excerpt)

Facts we may state:
- Running at two Dutch parcel carriers since 2025 (names may not be used).
- Works from the carrier's existing data warehouse; no new scanners or apps.

What the customer gets:
> Each depot sees its own late and failed deliveries, updated every day, and
> can follow how they change. Management sees the same for all depots and
> can compare them.

Objection: "Our IT team is busy with a new TMS."
> "It runs on the data warehouse you already have, so it doesn't depend on
> your TMS vendor."

Reference draft:

    Subject: Depot-level delivery data

    Dear Pieter,

    We have built software that finds late and failed deliveries directly
    in a carrier's own data, with no manual reporting.

    It already runs every day at two Dutch parcel carriers.

    Each depot sees its own figures, updated every day, and can follow how
    they change over time. Management sees the same for all depots and can
    compare them.

    It runs on the data warehouse you already have, so it doesn't depend on
    your TMS vendor.

    I'm curious whether it could be useful at Example Logistics. Would you
    be open to a short call where I show you how it works?

## criteria/criteria-nl.md (excerpt)

| Bucket | Example titles |
|---|---|
| Operations leadership (most important) | COO, Directeur Operations, Head of Last Mile |
| Depot / network management | Regiomanager, Netwerkmanager, Depotmanager (large hubs only) |
| Customer experience | Head of Customer Service, Manager Klantenservice |

Segments: `parcel`, `freight`, `3pl`. Excluded: IT, finance, procurement.
