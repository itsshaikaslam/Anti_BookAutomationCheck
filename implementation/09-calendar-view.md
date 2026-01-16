# Calendar View (History & Scheduling)

## Overview
A visual calendar to track generation trends, historical volumes, and scheduled batch tasks.

## Key Features
- **Day View**: List of all ebooks generated on a specific day with quick-access links.
- **Heatmap**: Visualization of system load over the month (identifying peak generation times).
- **Audit Logs**: clicking a date shows system errors or agent maintenance periods.

## Implementation
- **Calendar Engine**: `FullCalendar` or `react-calendar`.
- **Styling**: Integrated with Neo-Brutalist design (thick grid lines, bold date numbers).
- **Data Source**: Fetches from `ebook_generations` table grouped by `started_at` date.
- **Interactive Details**: Clicking an event opens the Ebook Details side panel.
