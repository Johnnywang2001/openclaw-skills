# iOS UI Design

iOS UI/UX design with SwiftUI and UIKit — Human Interface Guidelines compliance, design systems, accessibility, and App Store visual optimization.

## What It Does

This skill makes your agent a capable iOS design partner that produces production-ready SwiftUI code following Apple's Human Interface Guidelines:

- **HIG compliance** — Core principles (clarity, deference, depth), safe areas, navigation decision rules
- **Design system baseline** — Reusable spacing, radius, shadow, and color tokens with semantic naming
- **SwiftUI patterns** — Composable views, custom button/toggle/text field styles, layout tools
- **Responsive design** — Adaptive layouts from iPhone SE to iPad with size classes and `ViewThatFits`
- **Accessibility** — Dynamic Type, VoiceOver labels/hints/values, contrast requirements, Reduce Motion
- **Color and theming** — Palette roles, gradients, materials, blur, dark mode support
- **Common UI patterns** — Cards, onboarding, settings, dashboards, empty/loading states, toasts, sheets, custom tab bars, pull-to-refresh, search
- **Performance** — LazyVStack, state management, profiling with Instruments
- **App Store visuals** — Screenshot specs, design rules, icon guidance, preview video guidance, metadata optimization

## When to Use

- Designing new iOS screens or components
- Reviewing layouts for HIG compliance
- Building reusable design systems in SwiftUI
- Creating App Store screenshots and preview assets
- Improving accessibility (Dynamic Type, VoiceOver, contrast)
- Optimizing an app's App Store listing visuals and metadata

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/ios-ui-design ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/ios-ui-design ~/.openclaw/workspace/skills/ios-ui-design
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Key Features

- Complete design system template with tokens (spacing, radius, shadow, colors)
- 10+ production-ready SwiftUI component examples
- Navigation decision tree (TabView vs NavigationStack vs sheet vs fullScreenCover)
- Responsive layout patterns with `LazyVGrid`, `ViewThatFits`, and size classes
- Design review checklist for shipping
- App Store screenshot specifications and optimization strategy

## License

MIT
