# AgentsHome - Yashus Digital Agents Landing Page

**Status:** Production Ready ✅  
**Last Updated:** December 14, 2025

---

## What Is This?

Professional Angular SPA (Single Page Application) landing page showcasing the Yashus Digital Agents marketplace.

**Live Features:**
- 🎨 Beautiful Blue & Pink design (Yashus branding)
- 📱 Mobile-first responsive layout
- 🤖 5 AI Agents grid (1 live: The Hunter, 4 coming soon)
- 💳 Pricing section with per-agent pricing
- 📊 ROI metrics showing results vs traditional sales
- ❓ Interactive FAQ (collapsible Q&A)
- 🎬 Demo modal with YouTube video
- 🔐 Login modal with email/password form

---

## Quick Start (3 minutes)

### Prerequisites
- Node.js 18+
- npm or yarn

### Steps

1. **Install Dependencies**
   ```bash
   cd /workspaces/yashus/AgentsHome
   npm install
   ```

2. **Run Development Server**
   ```bash
   npm start
   ```

3. **View in Browser**
   - Opens automatically at http://localhost:4200
   - Auto-reloads on code changes

---

## Structure

```
AgentsHome/
├── README.md                    # ← YOU ARE HERE
├── src/
│   ├── app/
│   │   ├── app.component.*      # Root component
│   │   ├── app.module.ts        # Module declarations
│   │   └── components/          # 10 feature components
│   │       ├── header/          # Navigation + logo
│   │       ├── hero/            # Main headline + CTAs
│   │       ├── carousel/        # Industry selector
│   │       ├── agents/          # 5 agents grid
│   │       ├── how-it-works/    # 4-step process
│   │       ├── results/         # ROI metrics
│   │       ├── pricing/         # Pricing table
│   │       ├── faq/             # FAQ section
│   │       ├── footer/          # Footer links
│   │       ├── login-modal/     # Login form
│   │       └── demo-modal/      # Video embed
│   ├── index.html               # SEO optimized
│   ├── main.ts                  # Bootstrap
│   └── styles.scss              # Global styles
├── angular.json                 # Angular CLI config
├── package.json                 # Dependencies
└── docs/
    ├── DEPLOYMENT_GUIDE.md      # Detailed deployment
    └── SETUP.md                 # Full setup instructions
```

---

## Components

| Component | Purpose | Features |
|-----------|---------|----------|
| **Header** | Navigation bar | Logo, menu, sticky, login button |
| **Hero** | Main headline | 3 CTAs: Demo, Free Trial, Consultation |
| **Carousel** | Industry selector | Auto-rotating, manual controls |
| **Agents** | Agent showcase | 5 agents (1 live, 4 coming soon) with badges |
| **How It Works** | Process guide | 4 steps: Login → Subscribe → Configure → Start |
| **Results** | ROI metrics | Live numbers vs traditional sales comparison |
| **Pricing** | Pricing table | Per-agent + bundle discounts |
| **FAQ** | Q&A | 8 collapsible questions |
| **Footer** | Links | Social, terms, Yashus copyright |
| **Login Modal** | User login | Email/password form with validation |
| **Demo Modal** | Video demo | YouTube embed, closeable |

---

## Development

### Install Dependencies
```bash
npm install
```

### Start Dev Server
```bash
npm start
```
- Runs on `http://localhost:4200`
- Auto-reloads on changes
- Hot Module Replacement enabled

### Build for Production
```bash
npm run build:prod
```
- Creates optimized bundle in `/dist/agents-home/`
- Minified, tree-shaken, lazy-loaded
- Ready for deployment

### Run Tests
```bash
npm test
```
- Runs Jasmine test suite
- Coverage reports

### Lint Code
```bash
npm run lint
```
- Checks TypeScript & template syntax
- Follows Angular style guide

---

## Agents

### Live Now ✅
- **The Hunter** - AI Lead Generation
  - Autonomous discovery and enrichment
  - ML scoring for conversion prediction
  - REST API + Dashboard
  - Status: Live at The Hunter section

### Coming Soon 🚧
- **The Enricher** - Data Enrichment
- **The Messenger** - Email Outreach
- **The Amplifier** - Social Media Management
- **The Analyst** - Analytics & Reporting

---

## Pricing Model

| Agent | Monthly | Annual | Discount |
|-------|---------|--------|----------|
| Single Agent | $99 | $990 | 17% |
| 3 Agents | $247 | $2,470 | 17% |
| All 5 Agents | $399 | $3,990 | 17% |

---

## Environment & Styling

### CSS Variables
Defined in `styles.scss`:

```scss
// Primary Colors
--primary-blue: #0a5dff
--primary-pink: #ff3b6d
--accent-orange: #ff8c42

// Neutral Colors
--dark-bg: #1a1a1a
--light-text: #ffffff
--border-color: #333333

// Spacing
--spacing-unit: 16px
--border-radius: 8px
```

### Responsive Breakpoints
- Mobile: < 576px
- Tablet: 576px - 768px
- Desktop: 768px - 1024px
- Large: > 1024px

---

## Deployment

### Deploy to Vercel (Recommended)
```bash
npm install -g vercel
vercel
```
- Auto-detects Angular project
- Sets build command to `npm run build:prod`
- Deploys to `https://agentshome.vercel.app`

### Deploy to Netlify
```bash
npm run build:prod
# Drag /dist/agents-home/ to Netlify
```

### Deploy to Azure
- See [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)

---

## Common Issues

### Port 4200 Already in Use
```bash
ng serve --port 4300
```

### Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Fails
```bash
npm run lint
npm run build:prod --verbose
```

---

## File Structure

```
AgentsHome/
├── README.md                    # ← YOU ARE HERE
├── src/
│   ├── app/
│   │   ├── components/
│   │   ├── app.component.*
│   │   ├── app.module.ts
│   ├── assets/
│   ├── index.html
│   ├── main.ts
│   └── styles.scss
├── angular.json
├── package.json
├── tsconfig.json
└── docs/
    ├── DEPLOYMENT_GUIDE.md
    └── SETUP.md
```

---

## Next Steps

1. Run `npm install && npm start`
2. View at http://localhost:4200
3. Edit components in `src/app/components/`
4. Deploy with `npm run build:prod`
5. See [docs/DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) for production deployment

---

**Version:** 1.0 (December 14, 2025)  
**Status:** Production Ready ✅
| Results | ROI metrics and comparison dashboard |
| Pricing | Per-agent pricing with bundle discount info |
| FAQ | 8 common questions with collapsible answers |
| Footer | Links and copyright (Yashus.in) |
| LoginModal | Email/password form |
| DemoModal | YouTube embedded video |

## Color Scheme

```
Primary Blue: #1e40af
Secondary Pink: #ec4899
White: #ffffff
Light Gray: #f8fafc
Dark Text: #1f2937
Gray Accent: #6b7280
```

## Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## Features Implemented

✅ Hero section with 3 CTA buttons
✅ Auto-rotating carousel with manual navigation
✅ Agent cards with live/coming-soon badges
✅ How It Works step-by-step guide
✅ Results & ROI comparison
✅ Pricing per agent with bundle info
✅ FAQ with expand/collapse
✅ Login modal with form validation
✅ Demo modal with YouTube embed
✅ Mobile-responsive design
✅ Yashus.in branding and colors
✅ Smooth animations and transitions

## Next Steps

1. Replace YouTube placeholder URL with actual demo video
2. Connect "Subscribe Now" buttons to payment gateway
3. Add backend API integration for lead capture
4. Implement email verification for free trial
5. Add analytics tracking
6. Set up CDN for assets
7. Configure custom domain (agents.yashus.in)

## Author

Created for Yashus.in - Digital Marketing Agency
