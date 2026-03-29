---
name: ios-ui-design
description: iOS UI/UX design in SwiftUI and UIKit, Human Interface Guidelines compliance, App Store visual optimization, and accessibility. Use when designing screens, building UI components, reviewing layouts, creating App Store screenshots or preview assets, improving accessibility, or optimizing an app’s visual presentation and App Store listing.
---

# iOS UI Design

## Overview

Design native-feeling iPhone and iPad interfaces that survive real shipping constraints: HIG compliance, accessibility, performance, and App Store conversion. Default to SwiftUI for new interface work. Translate the same principles to UIKit when the app already uses `UIViewController`, `UINavigationController`, `UITabBarController`, `UICollectionView`, or custom legacy components.

## Operating Workflow

1. Identify the product goal, target devices, minimum iOS version, and whether the codebase is SwiftUI, UIKit, or hybrid.
2. Choose the navigation model before polishing visuals.
3. Establish design tokens first: spacing, typography, colors, radii, shadows, icon treatment, and states.
4. Compose the UI from small reusable views instead of one giant screen body.
5. Validate on the smallest supported iPhone, a large iPhone, and an iPad in both light and dark mode.
6. Test Dynamic Type, VoiceOver, Reduce Motion, loading/error/empty states, and keyboard interaction.
7. If the request includes App Store optimization, produce screenshot concepts, metadata recommendations, and icon/video guidance.

## Human Interface Guidelines Non-Negotiables

### Core principles

- **Clarity**: Make content legible, controls obvious, and hierarchy immediate.
- **Deference**: Let content lead. Use chrome, decoration, and motion to support comprehension, not compete with it.
- **Depth**: Use layering, motion, and transitions to communicate structure and cause/effect.

### Platform conventions to follow

- Prefer standard controls before inventing custom ones.
- Respect iOS-safe areas; do not tuck important controls under the notch, home indicator, or rounded corners.
- Use standard gestures only when users already expect them.
- Keep primary actions reachable and visually obvious.
- Match system behavior for destructive actions, edit modes, swipe actions, and sheets.
- Support both **Dynamic Type** and **Dark Mode**. Treat both as required, not optional polish.
- Keep interactive targets at **44x44pt minimum**.
- Use **16pt horizontal margins** as the default content edge on iPhone and align to an **8pt spacing grid**.

### Navigation decision rules

- Use **`TabView`** for 3-5 top-level peer destinations that users switch between frequently.
- Use **`NavigationStack`** for hierarchical drill-down flows: list -> detail -> subdetail.
- Use **`.sheet`** for temporary or secondary tasks that should dismiss back to the prior context: filters, editors, pickers, compose flows, confirmation details.
- Use **`.fullScreenCover`** for immersive or mode-switching experiences: onboarding, authentication gates, media capture, focused creation flows.
- Use **popover-style UI** for contextual detail and lightweight controls, primarily on iPad. Expect compact-width iPhone presentations to adapt into a sheet.

### Safe areas, layout margins, and dark mode

- Respect `safeAreaInset`, `safeAreaPadding`, and default navigation/tab bar behavior before forcing custom offsets.
- Let scrollable content extend under bars only when gradients/materials make the content readable.
- Use semantic foreground/background colors so the interface holds up in dark mode.
- Never assume white backgrounds or black text.

## Design System Baseline

Start with reusable tokens and semantic naming. Avoid raw hex literals spread across feature views.

```swift
import SwiftUI

enum AppSpacing {
    static let xxs: CGFloat = 4
    static let xs: CGFloat = 8
    static let sm: CGFloat = 12
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
}

enum AppRadius {
    static let card: CGFloat = 16
    static let control: CGFloat = 12
}

enum AppShadow {
    static let card = Color.black.opacity(0.08)
}

extension Color {
    static let brandPrimary = Color("BrandPrimary")
    static let brandSecondary = Color("BrandSecondary")
    static let surface = Color("Surface")
    static let card = Color("Card")
    static let textPrimary = Color("TextPrimary")
    static let textSecondary = Color("TextSecondary")
}
```

Asset catalog guidance:

- Create color assets with **light and dark variants**.
- Define at least: `BrandPrimary`, `BrandSecondary`, `Surface`, `Card`, `TextPrimary`, `TextSecondary`, `TextTertiary`, `Success`, `Warning`, `Danger`.
- Prefer semantic SwiftUI colors such as `Color.primary`, `Color.secondary`, `.background`, and `.tint` when they fit. Use brand tokens where the product needs distinct personality.
- Use `.tint()` to theme controls. Treat `Color.accentColor` as legacy-compatible shorthand; prefer explicit `tint` in modern SwiftUI.

## SwiftUI Design Patterns

### Compose small, reusable views

Split screens into sections, rows, cards, and action bars. Keep bodies readable.

```swift
struct AppCard<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .padding(AppSpacing.md)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.card)
            .clipShape(RoundedRectangle(cornerRadius: AppRadius.card, style: .continuous))
            .shadow(color: AppShadow.card, radius: 10, y: 4)
    }
}
```

Use `@ViewBuilder` for containers that should accept arbitrary child content while keeping consistent styling.

### Build reusable control styles

```swift
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.headline)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(Color.brandPrimary)
            .foregroundStyle(.white)
            .clipShape(RoundedRectangle(cornerRadius: AppRadius.control, style: .continuous))
            .opacity(configuration.isPressed ? 0.88 : 1)
            .scaleEffect(configuration.isPressed ? 0.98 : 1)
            .animation(.easeOut(duration: 0.15), value: configuration.isPressed)
    }
}

struct BrandedToggleStyle: ToggleStyle {
    func makeBody(configuration: Configuration) -> some View {
        HStack {
            configuration.label
            Spacer()
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(configuration.isOn ? Color.brandPrimary : Color.secondary.opacity(0.25))
                .frame(width: 52, height: 32)
                .overlay(alignment: configuration.isOn ? .trailing : .leading) {
                    Circle()
                        .fill(.white)
                        .frame(width: 28, height: 28)
                        .padding(2)
                }
                .onTapGesture { configuration.isOn.toggle() }
                .animation(.spring(response: 0.25, dampingFraction: 0.8), value: configuration.isOn)
        }
    }
}

struct BrandedTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding(14)
            .background(Color.card)
            .overlay(
                RoundedRectangle(cornerRadius: AppRadius.control, style: .continuous)
                    .stroke(Color.secondary.opacity(0.16), lineWidth: 1)
            )
    }
}
```

### Use layout tools intentionally

- Use `VStack`/`HStack` for small, always-present groups.
- Use `LazyVStack`/`LazyHStack` inside scroll views for larger or dynamic collections.
- Use `GeometryReader` sparingly for proportional layouts, scroll effects, or size-aware arrangements. Do not use it as a default wrapper around every screen.
- Use `ScrollView` for custom layouts; use `List` or `Form` when you want native behaviors, separators, edit actions, and accessibility conventions.
- Keep scroll content padded and visually sectioned; avoid a giant unstructured scroll column.

### Use shapes, animation, symbols, and typography deliberately

- Use custom `Shape` or `Path` when the brand actually needs a distinctive silhouette.
- Prefer subtle motion: `withAnimation`, `.transition`, and `matchedGeometryEffect` should clarify state changes, not distract.
- Honor Reduce Motion for large transforms or springy transitions.
- Use SF Symbols for common metaphors. Prefer semantic icons before custom artwork.
- Choose symbol rendering modes intentionally:
  - `.monochrome` for neutral UI
  - `.hierarchical` for depth with one tint
  - `.palette` for multitone brand usage
  - `.multicolor` sparingly for delight or system-like emphasis
- Size symbols relative to text: `.imageScale(.medium)` for inline usage, or apply `.font(.title3)` / `.font(.largeTitle)`.
- Prefer text styles such as `.font(.title)`, `.font(.headline)`, `.font(.body)`, `.font(.caption)`.
- For custom fonts, scale them correctly:

```swift
Text("Premium")
    .font(.custom("Inter-SemiBold", size: 17, relativeTo: .headline))

Image(systemName: "chart.line.uptrend.xyaxis")
    .symbolRenderingMode(.hierarchical)
    .font(.title3)
    .foregroundStyle(Color.brandPrimary)
```

### Example: animated state swap

```swift
struct FavoriteChip: View {
    @State private var isSelected = false
    @Namespace private var namespace
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Button {
            if reduceMotion {
                isSelected.toggle()
            } else {
                withAnimation(.spring(response: 0.28, dampingFraction: 0.8)) {
                    isSelected.toggle()
                }
            }
        } label: {
            HStack(spacing: 8) {
                Image(systemName: isSelected ? "heart.fill" : "heart")
                    .matchedGeometryEffect(id: "icon", in: namespace)
                Text(isSelected ? "Saved" : "Save")
            }
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
            .background(isSelected ? Color.brandPrimary.opacity(0.12) : Color.card)
            .clipShape(Capsule())
        }
        .buttonStyle(.plain)
    }
}
```

## Layout and Responsive Design

Design for the full range from **iPhone SE** to **Pro Max** and **iPad**.

- Prefer flexible frames over hardcoded widths/heights.
- Use `.frame(maxWidth: .infinity, alignment: .leading)` to let content grow naturally.
- Use `@Environment(\.horizontalSizeClass)` to switch between compact and regular layouts.
- Use `ViewThatFits` for content that should gracefully collapse from horizontal to vertical.
- Use `LazyVGrid` / `LazyHGrid` for dashboards, galleries, settings tiles, and metric cards.
- Plan for landscape: toolbars, side-by-side content, and keyboard overlap change quickly in short-height layouts.
- Test long localized strings and large Dynamic Type on the narrowest width.

```swift
struct AdaptiveDashboard: View {
    @Environment(\.horizontalSizeClass) private var sizeClass

    private var columns: [GridItem] {
        let count = sizeClass == .regular ? 3 : 2
        return Array(repeating: GridItem(.flexible(), spacing: AppSpacing.md), count: count)
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: AppSpacing.lg) {
                ViewThatFits {
                    HStack {
                        Text("Overview").font(.largeTitle.bold())
                        Spacer()
                        Button("Export") {}
                    }

                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Overview").font(.largeTitle.bold())
                        Button("Export") {}
                    }
                }

                LazyVGrid(columns: columns, spacing: AppSpacing.md) {
                    ForEach(0..<6, id: \.self) { _ in
                        AppCard {
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Revenue").font(.subheadline).foregroundStyle(.secondary)
                                Text("$24.8K").font(.title2.bold())
                            }
                        }
                    }
                }
            }
            .padding(AppSpacing.md)
        }
    }
}
```

UIKit equivalents:

- Use size classes via `traitCollection.horizontalSizeClass`.
- Use `UICollectionViewCompositionalLayout` for adaptive grids.
- Use `UIFont.preferredFont(forTextStyle:)` plus `UIFontMetrics` for scalable type.
- Use dynamic `UIColor` assets or `UIColor { trait in ... }` for light/dark variants.

## Accessibility Requirements

Treat accessibility as part of the design system.

- Label every meaningful interactive element with `.accessibilityLabel()` when the visible text is insufficient.
- Add `.accessibilityHint()` only when the outcome is not already obvious.
- Add `.accessibilityValue()` for dynamic state such as progress, counts, selected filters, and ratings.
- Mark structure with traits like `.isHeader`, `.isSelected`, and button behavior.
- Group compound rows with `.accessibilityElement(children: .combine)`.
- Support all Dynamic Type sizes. Prefer text styles over fixed point sizes.
- Respect `@Environment(\.accessibilityReduceMotion)`.
- Maintain contrast of at least **4.5:1 for normal text** and **3:1 for large text**.
- Add `.accessibilityAction` for custom swipe, archive, favorite, or reorder actions that otherwise rely on gestures alone.
- Test with **Xcode Accessibility Inspector** and **VoiceOver on a physical device**.

```swift
struct AccessibleStatCard: View {
    let title: String
    let value: String
    let trend: String

    var body: some View {
        AppCard {
            VStack(alignment: .leading, spacing: 8) {
                Text(title).font(.headline)
                Text(value).font(.title.bold())
                Text(trend).font(.subheadline).foregroundStyle(.secondary)
            }
            .accessibilityElement(children: .combine)
            .accessibilityLabel(title)
            .accessibilityValue("\(value), \(trend)")
            .accessibilityAddTraits(.isHeader)
        }
    }
}
```

## Color, Theming, Materials, and Blur

- Build a consistent palette with roles, not random per-screen colors.
- Define at minimum:
  - primary, secondary, accent/brand
  - background, surface, card
  - text primary, secondary, tertiary
  - semantic success, warning, error
- Use gradients to emphasize hero zones or onboarding moments, not every card.
- Prefer restrained gradients:

```swift
LinearGradient(
    colors: [Color.brandPrimary, Color.brandSecondary],
    startPoint: .topLeading,
    endPoint: .bottomTrailing
)
```

- Use `RadialGradient` for highlights and focus; use `AngularGradient` only when the circular color sweep supports the concept.
- Use materials for layering over rich content:
  - `.ultraThinMaterial` for light overlays
  - `.regularMaterial` for cards, floating controls, and contextual surfaces
- Combine materials with saturation, shadow, and stroke carefully so text remains readable.
- Treat vibrancy and blur as support for hierarchy, not decoration.

## Common UI Patterns with SwiftUI Code

### Card-style list item

```swift
struct MessageRow: View {
    let title: String
    let subtitle: String

    var body: some View {
        AppCard {
            HStack(spacing: AppSpacing.md) {
                Image(systemName: "bubble.left.and.bubble.right.fill")
                    .font(.title3)
                    .foregroundStyle(Color.brandPrimary)
                VStack(alignment: .leading, spacing: 4) {
                    Text(title).font(.headline)
                    Text(subtitle).font(.subheadline).foregroundStyle(.secondary)
                }
                Spacer()
                Image(systemName: "chevron.right")
                    .foregroundStyle(.tertiary)
            }
        }
        .contentShape(Rectangle())
    }
}
```

### Onboarding flow with `PageTabViewStyle`

```swift
struct OnboardingPage: Identifiable {
    let id = UUID()
    let title: String
    let detail: String
    let systemImage: String
}

struct OnboardingView: View {
    @State private var selection = 0
    let pages: [OnboardingPage]

    var body: some View {
        VStack(spacing: AppSpacing.lg) {
            TabView(selection: $selection) {
                ForEach(Array(pages.enumerated()), id: \.element.id) { index, page in
                    VStack(spacing: AppSpacing.md) {
                        Image(systemName: page.systemImage)
                            .font(.system(size: 56))
                            .foregroundStyle(Color.brandPrimary)
                        Text(page.title).font(.title.bold())
                        Text(page.detail)
                            .font(.body)
                            .multilineTextAlignment(.center)
                            .foregroundStyle(.secondary)
                    }
                    .padding(AppSpacing.xl)
                    .tag(index)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .always))

            Button(selection == pages.count - 1 ? "Get Started" : "Next") {
                if selection < pages.count - 1 { selection += 1 }
            }
            .buttonStyle(PrimaryButtonStyle())
        }
        .padding(AppSpacing.md)
    }
}
```

### Settings screen with `Form`, `List`, and `Section`

```swift
struct SettingsView: View {
    @State private var notificationsEnabled = true
    @State private var username = "Jarvis"

    var body: some View {
        NavigationStack {
            Form {
                Section("Profile") {
                    TextField("Display name", text: $username)
                        .textFieldStyle(.roundedBorder)
                }

                Section("Preferences") {
                    Toggle("Notifications", isOn: $notificationsEnabled)
                    NavigationLink("Appearance") { Text("Appearance Settings") }
                }

                Section {
                    Button("Sign Out", role: .destructive) {}
                }
            }
            .navigationTitle("Settings")
        }
    }
}
```

### Dashboard with stats cards

```swift
struct DashboardView: View {
    let metrics = [("Active Users", "12.4K"), ("Conversion", "8.1%"), ("Revenue", "$24.8K")]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: AppSpacing.md) {
                ForEach(metrics, id: \.0) { metric in
                    AccessibleStatCard(title: metric.0, value: metric.1, trend: "Up 12% this week")
                }
            }
            .padding(AppSpacing.md)
        }
    }
}
```

### Empty state and loading/skeleton state

```swift
struct EmptyStateView: View {
    let title: String
    let message: String
    let action: () -> Void

    var body: some View {
        ContentUnavailableView {
            Label(title, systemImage: "tray")
        } description: {
            Text(message)
        } actions: {
            Button("Create Item", action: action)
                .buttonStyle(PrimaryButtonStyle())
        }
    }
}

struct SkeletonCard: View {
    var body: some View {
        RoundedRectangle(cornerRadius: AppRadius.card, style: .continuous)
            .fill(Color.secondary.opacity(0.12))
            .frame(height: 100)
            .redacted(reason: .placeholder)
            .shimmeringIfAvailable()
    }
}
```

If a shimmer modifier is unavailable, keep placeholders simple and stable instead of inventing a noisy animation.

### Pull-to-refresh and search

```swift
struct SearchableListView: View {
    @State private var query = ""
    @State private var items = ["Alpha", "Beta", "Gamma"]

    var filteredItems: [String] {
        query.isEmpty ? items : items.filter { $0.localizedCaseInsensitiveContains(query) }
    }

    var body: some View {
        NavigationStack {
            List(filteredItems, id: \.self) { item in
                Text(item)
            }
            .refreshable {
                try? await Task.sleep(for: .seconds(1))
                items.shuffle()
            }
            .searchable(text: $query, placement: .navigationBarDrawer(displayMode: .always))
            .navigationTitle("Library")
        }
    }
}
```

### Custom tab bar

Use a custom tab bar only when the standard tab bar cannot express the brand or behavior. Preserve the same semantics: clear selected state, large tap targets, and stable destination count.

```swift
struct CustomTabBar: View {
    @Binding var selection: Int
    let items: [(title: String, icon: String)]

    var body: some View {
        HStack {
            ForEach(items.indices, id: \.self) { index in
                Button {
                    selection = index
                } label: {
                    VStack(spacing: 4) {
                        Image(systemName: items[index].icon)
                        Text(items[index].title).font(.caption2)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 10)
                    .foregroundStyle(selection == index ? Color.brandPrimary : .secondary)
                }
                .accessibilityAddTraits(selection == index ? .isSelected : [])
            }
        }
        .padding(8)
        .background(.regularMaterial, in: Capsule())
        .padding()
    }
}
```

### Bottom sheet with `.presentationDetents`

```swift
struct FiltersView: View {
    @State private var showingFilters = false

    var body: some View {
        Button("Show Filters") { showingFilters = true }
            .sheet(isPresented: $showingFilters) {
                NavigationStack {
                    Form {
                        Toggle("Favorites only", isOn: .constant(false))
                    }
                    .navigationTitle("Filters")
                    .navigationBarTitleDisplayMode(.inline)
                }
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
            }
    }
}
```

### Toast or snackbar notification

```swift
struct ToastModifier: ViewModifier {
    let isPresented: Bool
    let message: String

    func body(content: Content) -> some View {
        content
            .overlay(alignment: .bottom) {
                if isPresented {
                    Text(message)
                        .font(.subheadline.weight(.semibold))
                        .padding(.horizontal, 16)
                        .padding(.vertical, 12)
                        .background(.regularMaterial, in: Capsule())
                        .padding(.bottom, 24)
                        .transition(.move(edge: .bottom).combined(with: .opacity))
                }
            }
            .animation(.easeInOut(duration: 0.2), value: isPresented)
    }
}
```

## Performance Guidance

- Use `LazyVStack` with stable identifiers for long or dynamic lists:

```swift
LazyVStack(spacing: AppSpacing.md) {
    ForEach(viewModel.items, id: \.id) { item in
        MessageRow(title: item.title, subtitle: item.subtitle)
    }
}
```

- Use `AsyncImage` for straightforward remote images. For production feeds, add caching via `URLCache`, `NSCache`, or an image pipeline library when flicker/reload cost matters.
- Place `@State` at the narrowest view that owns the interaction. Pass `@Binding` downward instead of duplicating mutable state across the hierarchy.
- Break giant `body` implementations into subviews or computed view sections to reduce diffing complexity and improve maintainability.
- Use `.drawingGroup()` only for genuinely complex vector compositions when profiling shows a benefit.
- Profile with **Instruments**:
  - **Core Animation** for FPS and overdraw
  - **Hangs** for main-thread stalls
  - **Time Profiler** for expensive layouts, image decoding, and repeated work
- Avoid unnecessary `.onAppear` network refetches during scrolling.
- Avoid stacking multiple heavy blur, shadow, and mask effects in repeated cells.

## App Store Visual Optimization

### Screenshot specifications

Prepare export-ready screenshots at these sizes when requested:

- **6.9" (iPhone 16 Pro Max):** 1320 x 2868
- **6.7" (iPhone 15 Pro Max):** 1290 x 2796
- **6.5" (iPhone 14 Plus):** 1284 x 2778
- **5.5" (iPhone 8 Plus):** 1242 x 2208
- **iPad Pro 13":** 2064 x 2752

### Screenshot design rules

- Lead with strong feature callouts in large text that stays readable on small previews.
- Prioritize the **first 3 screenshots**; they often determine whether the user keeps scrolling.
- Show **real app UI**, not disconnected marketing art.
- Keep one visual language across the full set: consistent typography, brand colors, spacing, and overlay style.
- Use device frames only if they improve clarity and stay visually clean.
- One screenshot should communicate one message. Do not cram five benefits into one frame.
- Favor benefit-led captions: “Track expenses instantly” beats “Finance dashboard screen”.
- Use portrait sets unless the app is truly landscape-first.

Recommended screenshot sequence:

1. Core value proposition
2. Main workflow or hero screen
3. Differentiator or trust builder
4. Secondary feature
5. Personalization / integrations / social proof

### App icon guidance

- Deliver the App Store icon at **1024x1024**.
- Remove transparency and alpha.
- Keep the silhouette simple and recognizable at small sizes.
- Follow Apple’s icon grid proportions and corner behavior.
- Avoid text in the icon unless the brand is already universally recognized by a single letterform.
- Prefer one dominant metaphor over a busy collage.

### App Preview video guidance

- Keep videos **15-30 seconds**.
- Show the core functionality in the **first 5 seconds**.
- Record at native resolution.
- Do not include hands or fingers.
- Use Xcode Simulator recording for clean capture.
- Sequence the video like a product demo, not a cinematic trailer.

## App Store Listing Optimization

- Keep the **title** within **30 characters** and include the primary keyword if it still reads naturally.
- Keep the **subtitle** within **30 characters** and use complementary keywords or value props.
- Use the **keywords** field up to **100 characters**, comma-separated, no spaces after commas, and no duplicates already present in the title.
- Front-load the **description** with the value proposition because the first 3 lines matter before the user taps “more”.
- Choose a primary category that matches user intent and a secondary category only when it clarifies discoverability.
- Write **What’s New** notes that are brief, scannable, and centered on user-visible improvements.

Example metadata pattern:

- Title: `BudgetFlow: Expense Tracker`
- Subtitle: `Shared budgets and insights`
- Keywords: `budget,expense,tracker,shared finance,savings,spending`
- Description opening: `Track spending, plan budgets, and share progress with your household in seconds.`

## Design Review Checklist

Run this review before calling a design production-ready:

- [ ] All text supports Dynamic Type.
- [ ] Dark Mode looks correct and intentional.
- [ ] Touch targets are at least 44x44pt.
- [ ] VoiceOver reads all interactive elements correctly.
- [ ] Loading states exist for async content.
- [ ] Error states exist for failures.
- [ ] Empty states exist for no-data scenarios.
- [ ] Text inputs avoid the keyboard and remain reachable.
- [ ] Safe areas are respected on all target devices.
- [ ] No content clips on the smallest supported device, especially iPhone SE.

## Final Operating Rules

- Prefer native patterns over clever ones.
- Prefer semantic colors and text styles over hardcoded values.
- Prefer reusable components over repeated modifier chains.
- Prefer clarity over visual noise.
- Treat accessibility, dark mode, and small-screen support as release criteria.
- When asked to critique or redesign a screen, explain the tradeoffs, recommend the layout pattern, and provide implementation-ready SwiftUI structure.
