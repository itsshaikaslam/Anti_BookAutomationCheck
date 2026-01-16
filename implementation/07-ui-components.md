# UI Components & Design System

## Design Aesthetic: Neo-Brutalisim
- **High Contrast**: Black `#000000` on white or vibrant backgrounds.
- **Bold Borders**: 4px-8px solid black borders on all cards and buttons.
- **Vibrant Highlights**: Neo-yellow, Neo-pink, and Neo-cyan for active states.
- **Hard Shadows**: Box shadows with no blur (e.g., `box-shadow: 8px 8px 0px 0px #000;`).

## Reusable Components

### 1. Neo-Card
A container component with a thick border and hard shadow. Used for agent status and ebook previews.

### 2. Progress Swarm
A collective progress bar showing the status of parallel agents. Each agent in the swarm has a mini-indicator (Color-coded: Green=Done, Yellow=Working, Red=Error).

### 3. Agent Log Terminal
A retro-styled terminal component for viewing real-time logs from the 13 agents. Uses a monospace font and minimal styling.

### 4. Interactive Config Slider
A custom slider for chapter structure that visually balances Basic/One-Level/Two-Level chapters within the total limit.

### 5. PDF Previewer
Integrated viewer for checking the generated PDF structure before download.

### 6. Fact-Check Result Tile
A high-contrast card for displaying verified claims.
- **Header**: The claim text in bold.
- **Status Badge**: Neo-Brutalist green (Verified) or red (Corrected/Flagged).
- **Source Link**: Clickable link to the verification source.
- **Confidence Slider**: A 0-100% bar showing the agent's confidence in the verification.
