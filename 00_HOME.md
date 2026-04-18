# Civic Accountability Toolkit — Home

## Start here
- [[dashboards/DAILY_ACTION_BOARD]]
- [[dashboards/PEOPLE_INDEX]]
- [[dashboards/INCIDENT_INDEX]]
- [[dashboards/ISSUE_INDEX]]
- [[dashboards/EVIDENCE_INDEX]]
- [[dashboards/OUTREACH_QUEUE]]
- [[timelines/master-timeline]]

## Core method
1. Start with a source note.
2. Extract facts into an incident note.
3. Link the incident to people, issues, statutes, and agencies.
4. Mark what is established, alleged, disputed, and missing.
5. Draft a neutral outreach note using the template.

## Daily use
- Review one well-sourced incident.
- Check the linked evidence tier.
- Send one respectful fact-based message to an official channel.
- Record unanswered questions for future research.

## Administration roster
See [[dashboards/PEOPLE_INDEX]] for the full current roster seeded from official White House sources.
## Dataview starter queries

```dataview
TABLE role, group, office_status
FROM "people"
SORT file.name ASC
```

```dataview
TABLE status, source_tier
FROM "incidents"
SORT file.name ASC
```

```dataview
TABLE from, to, status
FROM "relationships"
SORT file.name ASC
```
