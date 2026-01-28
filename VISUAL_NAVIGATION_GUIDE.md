# Peer Analyst Feature - Visual & Navigation Guide

## 🗺️ NAVIGATION MAP

```
┌─────────────────────────────────────────────────────────────┐
│                    DASHBOARD HOME                           │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │Market Hub    │  │  Compare     │  │Peer Analysts ← NEW│ │
│  │📊            │  │  ⚖️          │  │👥                │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │                  PROJECT PORTFOLIO                      ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ ││
│  │  │iPhone        │  │Dress Reviews │  │Smart Watch   │ ││
│  │  │📊            │  │📊            │  │📊            │ ││
│  │  │View Report ──────> Report Page                   │ ││
│  │  └──────────────┘  └──────────────┘  └──────────────┘ ││
│  └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
         │
         └─────────> Peer Analysts Button (NEW)
                      │
                      ▼
         ┌─────────────────────────────────────┐
         │  /peer_analyses PAGE                │
         │                                     │
         │  👥 Peer Analyst Network            │
         │  [Search Bar]                       │
         │                                     │
         │  ┌─────────────┐ ┌─────────────┐   │
         │  │ J           │ │ S           │   │
         │  │John Analyst │ │Sarah Analyst│   │
         │  │View Profile ─────────────────┐  │
         │  └─────────────┘ └─────────────┘   │
         │                                     │
         └─────────────────────────────────────┘
                      │
                      └─────────> View Profile Button
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ /analyst/<id> PAGE           │
                    │                              │
                    │ John Analyst Profile         │
                    │ ├─ 5 Shared Analyses        │
                    │ ├─ 2500 Total Reviews       │
                    │ ├─ 73% Avg Sentiment        │
                    │ ├─ Expertise: [iPhone]      │
                    │ │                            │
                    │ ├─ ┌──────────────────────┐ │
                    │ │  │iPhone 15 Pro         │ │
                    │ │  │73% Pos | 15% Neg     │ │
                    │ │  │View Full Analysis ────┼─┼──> Analysis Report
                    │ │  └──────────────────────┘ │     (Existing Page)
                    │ └─ ┌──────────────────────┐ │
                    │    │Dress Pants            │ │     └─> Share Toggle (NEW)
                    │    │68% Pos | 20% Neg     │ │
                    │    │View Full Analysis    │ │
                    │    └──────────────────────┘ │
                    │                              │
                    └──────────────────────────────┘
```

---

## 🎨 PAGE LAYOUTS

### PEER ANALYSES PAGE (`/peer_analyses`)

```
┌────────────────────────────────────────────────────────────┐
│                  👥 PEER ANALYST NETWORK                   │
│      Discover insights from your analyst peers             │
│                                                            │
│ [Header with gradient background - #667eea → #764ba2]     │
└────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ STAT CARD    │ STAT CARD    │ STAT CARD    │ STAT CARD    │
│              │              │              │              │
│ 5            │ 3            │ 12           │ [Reserved]   │
│ Active       │ Sharing      │ Shared       │              │
│ Analysts     │ Analysts     │ Projects     │              │
└──────────────┴──────────────┴──────────────┴──────────────┘

Search: [🔍 Search analysts by name...]

┌──────────────────┬──────────────────┬──────────────────┐
│  ANALYST CARD    │  ANALYST CARD    │  ANALYST CARD    │
│  ┌────────────┐  │  ┌────────────┐  │  ┌────────────┐  │
│  │  J         │  │  │  S         │  │  │  M         │  │
│  │(avatar)    │  │  │(avatar)    │  │  │(avatar)    │  │
│  │John A.     │  │  │Sarah A.    │  │  │Mike A.     │  │
│  │(gradient)  │  │  │(gradient)  │  │  │(gradient)  │  │
│  └────────────┘  │  └────────────┘  │  └────────────┘  │
│                  │                  │                  │
│  📊 5 Analyses   │  📊 3 Analyses   │  📊 4 Analyses   │
│  ⭐ 73% Avg      │  ⭐ 68% Avg      │  ⭐ 71% Avg      │
│                  │                  │                  │
│  [iPhone]        │  [Dress]         │  [Watch]         │
│  [Dress]         │  [Watch]         │  [Phone]         │
│                  │                  │                  │
│  [View Profile] │  [View Profile] │  [View Profile] │
└──────────────────┴──────────────────┴──────────────────┘

[More cards following same pattern...]
```

---

### ANALYST PROFILE PAGE (`/analyst/<id>`)

```
┌────────────────────────────────────────────────────────────┐
│ ← Back to Peer Network                                    │
├────────────────────────────────────────────────────────────┤
│           [PROFILE HEADER - GRADIENT]                      │
│     J               │                                      │
│  (avatar)           │  John Analyst                        │
│                     │  💼 Data Analyst                     │
│                     │  🎯 Specializing in PR Analysis      │
│                                                            │
│ [Background: Linear gradient]                             │
└────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ STAT BOX     │ STAT BOX     │ STAT BOX     │ STAT BOX     │
│              │              │              │              │
│ 5            │ 2500         │ 73%          │ 4            │
│ Shared       │ Total        │ Avg          │ High-Quality │
│ Analyses     │ Reviews      │ Positive     │ Analyses     │
└──────────────┴──────────────┴──────────────┴──────────────┘

🏆 Areas of Expertise
┌───────┬───────┬───────┬───────┬───────┐
│iPhone │ Dress │ Watch │Phone  │Search │
└───────┴───────┴───────┴───────┴───────┘

📈 Recent Analyses

┌──────────────────┬──────────────────┬──────────────────┐
│  ANALYSIS CARD   │  ANALYSIS CARD   │  ANALYSIS CARD   │
│  ┌────────────┐  │  ┌────────────┐  │  ┌────────────┐  │
│  │iPhone 15Pro│  │  │Dress Pants │  │  │Smart Watch │  │
│  │(gradient)  │  │  │(gradient)  │  │  │(gradient)  │  │
│  │📅 Jan 20   │  │  │📅 Jan 18   │  │  │📅 Jan 15   │  │
│  └────────────┘  │  └────────────┘  │  └────────────┘  │
│                  │                  │                  │
│  73% | 15% | 12% │  68% | 20% | 12% │  71% | 18% | 11% │
│  Pos  Neg  Neu   │  Pos  Neg  Neu   │  Pos  Neg  Neu   │
│                  │                  │                  │
│  ✅ Excellent    │  👍 Good         │  ✅ Excellent    │
│                  │                  │                  │
│  [View Full →]   │  [View Full →]   │  [View Full →]   │
└──────────────────┴──────────────────┴──────────────────┘

[More analysis cards...]
```

---

### ANALYSIS REPORT PAGE (EXISTING - WITH NEW FEATURE)

```
┌─────────────────────────────────────────────────────────┐
│              REPORT - iPhone 15 Pro                      │
├─────────────────┬───────────────────────────────────────┤
│                 │                                       │
│   SIDEBAR       │       MAIN CONTENT                   │
│                 │                                       │
│ ┌─────────────┐ │ ┌─────────────────────────────────┐  │
│ │Overall      │ │ │AI Executive Summary             │  │
│ │Score        │ │ │[Verdict text...]                │  │
│ │73% Positive │ │ └─────────────────────────────────┘  │
│ │ [Pie Chart] │ │                                      │
│ └─────────────┘ │ ┌─────────────┬─────────────────┐    │
│                 │ │ Aspect      │ Word Cloud      │    │
│ [PDF Download]  │ │ Analysis    │ [Cloud Image]   │    │
│ [CSV Download]  │ │ [Bars...]   │                 │    │
│ [Back to Dash]  │ └─────────────┴─────────────────┘    │
│                 │                                      │
│ ┌─────────────┐ │ ┌─────────────┐ ┌─────────────┐    │
│ │AI Trend     │ │ │Pie Chart    │ │Trend Chart  │    │
│ │Forecast:   │ │ │[Canvas]     │ │[Canvas]     │    │
│ │📈 Improving │ │ │             │ │             │    │
│ └─────────────┘ │ └─────────────┘ └─────────────┘    │
│                 │                                      │
│ ┌─────────────┐ │ [Sentiment Breakdown with Filters]  │
│ │Share with   │ │                                      │
│ │Peers:   ← NEW│ │ ┌──────────────────────────────┐   │
│ │📤 Share     │ │ │ [Review List - 100 reviews]  │   │
│ │Analysis     │ │ │ ├─ Review 1... [SUSPICIOUS]   │   │
│ │             │ │ │ ├─ Review 2...                │   │
│ │[✅ Shared]  │ │ │ └─ Review 3...                │   │
│ │[✓ with      │ │ │                               │   │
│ │ peer        │ │ └──────────────────────────────┘   │
│ │ analysts]   │ │                                      │
│ └─────────────┘ │                                      │
│                 │                                      │
└─────────────────┴───────────────────────────────────────┘
```

---

## 🎯 COLOR SCHEME

```
PRIMARY COLORS:
┌─────────────────────────────────────────────────┐
│ Purple/Violet Gradient                          │
│ ├─ #667eea (Light Purple)                       │
│ ├─ #764ba2 (Dark Purple)                        │
│ └─ Used for: Headers, Buttons, Accents          │
└─────────────────────────────────────────────────┘

ACCENT COLORS:
┌─────────────────────────────────────────────────┐
│ Sentiment Indicators                            │
│ ├─ #00b894 (Green) - Positive/Success           │
│ ├─ #d63031 (Red) - Negative/Warning             │
│ ├─ #fdcb6e (Yellow) - Neutral/Info              │
│ └─ #2d3436 (Dark) - Text/Headers                │
└─────────────────────────────────────────────────┘

BACKGROUND COLORS:
┌─────────────────────────────────────────────────┐
│ Neutral Tones                                   │
│ ├─ #ffffff (White) - Cards, Content             │
│ ├─ #f1f2f6 (Light Gray) - Secondary BG          │
│ ├─ #dfe6e9 (Medium Gray) - Borders              │
│ └─ #b2bec3 (Gray) - Secondary Text              │
└─────────────────────────────────────────────────┘
```

---

## 📱 RESPONSIVE BREAKPOINTS

```
MOBILE (≤ 480px)
├─ Single column grid
├─ Full-width buttons
├─ Stack all elements vertically
└─ Touch-friendly spacing (48px min-height)

TABLET (481px - 768px)
├─ 2-column grid for analyst cards
├─ Sidebar moves above content
├─ Optimized spacing
└─ Readable font sizes

DESKTOP (769px+)
├─ 3-column grid for analyst cards
├─ Side-by-side layouts
├─ Full feature width
└─ Optimized white space
```

---

## 🔄 USER FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│ ANALYST ACTION FLOW                                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 1. Login/Dashboard                                  │
│    │                                                │
│    └──> Create Analysis (Existing Flow)             │
│         │                                           │
│         └──> View Report                            │
│              │                                      │
│              └──> See "Share with Peers" Button    │
│                   │                                 │
│              ┌────┴────┐                            │
│              │          │                           │
│              ▼          ▼                           │
│         [SHARE]    [HIDE]                          │
│              │          │                           │
│              │          └──> Appears in Network    │
│              │                                      │
│              └──> Removed from Peer View           │
│                                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ PEER ANALYST DISCOVERY FLOW                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 1. Login/Dashboard                                  │
│    │                                                │
│    └──> Click "Peer Analysts" Button               │
│         │                                           │
│         └──> View Peer Network                     │
│              │                                      │
│              ├──> Search Analyst by Name            │
│              │                                      │
│              └──> Click Analyst Card               │
│                   │                                 │
│                   └──> View Analyst Profile        │
│                        │                            │
│                        └──> View Their Analyses    │
│                             │                       │
│                             └──> Full Analysis     │
│                                  (Existing Page)   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎤 KEY INTERACTION POINTS

### Share Toggle Button
```
[INACTIVE STATE]                [ACTIVE STATE]
┌────────────────────┐         ┌────────────────────┐
│ 📤 Share Analysis  │  ──────>│ 📤 Shared with     │
│ (Gray background)  │         │    Peers           │
│                    │         │ (Green gradient)   │
│ Loading...         │         │                    │
│                    │         │ ✅ Shared with     │
└────────────────────┘         │    peer analysts   │
                               └────────────────────┘
```

### Search Input
```
┌─────────────────────────────────────────┐
│ 🔍 Search analysts by name...           │
│  ↓ Type here                            │
│  John → [Shows "John Analyst" card]     │
│  Sarah → [Shows "Sarah Analyst" card]   │
│  Mike → [Shows "Mike Analyst" card]     │
│  (No match) → [Shows empty state]       │
└─────────────────────────────────────────┘
```

### Analyst Card Hover
```
BEFORE HOVER:              AFTER HOVER:
┌──────────────┐          ┌──────────────┐
│ J            │   ──────>│ J            │
│(flat)        │          │(elevated)    │
│John Analyst  │          │John Analyst  │
│5 Analyses    │          │5 Analyses    │
│73% Avg       │          │73% Avg       │
│[View Profile]│          │[View Profile]│
└──────────────┘          └──────────────┘
(shadow: 0 5px)          (shadow: 0 15px)
                         (transform: up)
```

---

## 📋 ELEMENT REFERENCE

### BUTTONS

**Primary Button** (Purple Gradient)
```
Background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Padding: 12px 22px
Border-radius: 12px
Hover: Transform up 2px, Enhanced shadow
```

**Secondary Button** (Dark)
```
Background: #2d3436
Padding: 12px 22px
Border-radius: 12px
Hover: Transform up, Enhanced shadow
```

### CARDS

**Analyst Card**
```
Background: white
Border-radius: 15px
Padding: 0
Shadow: 0 5px 20px rgba(0,0,0,0.08)
Header: Gradient (667eea → 764ba2)
Hover: -8px transform, enhanced shadow
```

**Stat Card**
```
Background: white
Border-radius: 15px
Padding: 25px
Shadow: 0 5px 20px rgba(0,0,0,0.08)
Text-align: center
```

### INPUT

**Search Box**
```
Padding: 12px 20px
Border: 2px solid #dfe6e9
Border-radius: 10px
Focus: Border becomes #667eea, shadow with color
```

---

## ✅ VISUAL CHECKLIST

- [ ] Gradient backgrounds apply correctly
- [ ] Hover animations smooth and visible
- [ ] Responsive grid adjusts to screen size
- [ ] Search filters work in real-time
- [ ] Buttons have proper states (normal/hover/active)
- [ ] Colors consistent across pages
- [ ] Icons load properly (Font Awesome)
- [ ] Text is readable (contrast OK)
- [ ] Touch targets are 48px+ on mobile
- [ ] No broken images or missing elements

---

**End of Visual & Navigation Guide**
