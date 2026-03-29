# iOS App Publisher

Complete iOS app publishing lifecycle — from Xcode project setup through App Store approval and post-launch management.

## What It Does

This skill enables your agent to act as an iOS publishing expert, covering every phase of getting an app to the App Store:

- **Xcode project setup** — Project structure, targets, schemes, build configurations, xcconfig files
- **Code signing** — Automatic vs manual signing, certificates, provisioning profiles, entitlements
- **Swift/SwiftUI best practices** — MVVM architecture, SPM dependencies, project organization
- **App Store Connect** — App records, bundle IDs, metadata, screenshot specs, privacy manifests
- **TestFlight** — Internal testing (100 testers), external testing (10,000 testers), beta review
- **App Review** — Common rejection reasons, preparation checklist, expedited reviews, appeals
- **In-App Purchases** — StoreKit 2 setup, subscription groups, sandbox testing
- **Release management** — Manual/automatic/scheduled releases, phased rollout
- **Post-launch** — Crash reporting, MetricKit, ratings management, App Analytics
- **Automation** — Fastlane (match, gym, deliver, pilot, snapshot), GitHub Actions CI/CD

## When to Use

- Building an iOS app from scratch
- Configuring code signing and provisioning profiles
- Setting up App Store Connect and managing app metadata
- Running TestFlight beta testing
- Preparing for and responding to App Review
- Configuring In-App Purchases and Subscriptions
- Automating builds with Fastlane or GitHub Actions

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/ios-app-publisher ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/ios-app-publisher ~/.openclaw/workspace/skills/ios-app-publisher
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Key Features

- Full xcodebuild command reference (build, test, archive, export)
- ExportOptions.plist examples for App Store distribution
- Privacy manifest (PrivacyInfo.xcprivacy) templates
- Complete Fastlane lane examples for CI pipelines
- GitHub Actions workflow for iOS CI/CD
- Screenshot specifications for all current device sizes (2026)
- StoreKit 2, CloudKit, WidgetKit, and ScreenTime API examples

## License

MIT
