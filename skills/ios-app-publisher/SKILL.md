---
name: ios-app-publisher
description: Comprehensive iOS app publishing skill covering Xcode project setup, code signing, App Store Connect configuration, TestFlight testing, App Store submission, and post-launch management. Use when building, testing, and publishing iOS apps to the App Store.
---

# iOS App Publisher

## Overview

This skill enables an agent to act as a Subject Matter Expert for building and publishing iOS applications to the App Store. It covers the complete lifecycle from project setup through App Store approval and post-launch management.

**When to use this skill:**
- Building an iOS app from scratch
- Configuring code signing and provisioning profiles
- Setting up App Store Connect accounts and app records
- Managing TestFlight beta testing
- Submitting apps for App Review
- Configuring In-App Purchases and Subscriptions
- Automating builds with Fastlane or GitHub Actions

---

## Quick Start

### Complete Workflow Overview

```
1. Development → 2. Code Signing → 3. App Store Connect → 4. TestFlight → 5. Submission → 6. Release
```

**Minimum Required Steps:**
1. Create Xcode project with proper bundle ID
2. Configure code signing (automatic recommended)
3. Create App Store Connect app record
4. Build and archive in Xcode
5. Upload via Xcode Organizer or Transporter
6. Submit for App Review
7. Release (manual or automatic)

---

## Part 1: Development Phase

### 1.1 Xcode Project Setup

#### Creating a New Project

```bash
# Open Xcode and create new project
open -a Xcode
# Or use command line to list templates (limited)
xcodebuild -list
```

#### Project Structure Best Practices

```
MyApp/
├── MyApp/                      # Main app target
│   ├── App/
│   │   ├── MyAppApp.swift     # App entry point (SwiftUI)
│   │   └── AppDelegate.swift  # UIKit lifecycle
│   ├── Views/                 # SwiftUI Views
│   ├── ViewModels/            # MVVM ViewModels
│   ├── Models/                # Data models
│   ├── Services/              # API, Database, etc.
│   ├── Resources/
│   │   ├── Assets.xcassets
│   │   └── LaunchScreen.storyboard
│   └── Info.plist
├── MyAppTests/                # Unit test target
├── MyAppUITests/              # UI test target
└── MyApp.xcodeproj/
```

#### Understanding Targets, Schemes, and Build Configurations

**Targets:** A target specifies a product to build and contains instructions for building that product.

**Schemes:** A scheme identifies which targets to build, what configuration to use, and how to execute tests.

```bash
# List all schemes in a project
xcodebuild -list -project MyApp.xcodeproj

# List schemes in a workspace
xcodebuild -list -workspace MyApp.xcworkspace

# Show all available destinations
xcodebuild -showdestinations -project MyApp.xcodeproj -scheme MyScheme
```

**Build Configurations:**
- **Debug:** Development build with debugging symbols, no optimization
- **Release:** Production build with optimizations, symbols stripped
- **Configuration files (.xcconfig):** Override build settings

```ruby
# Example .xcconfig for App Store release
PRODUCT_NAME = $(TARGET_NAME)
SWIFT_VERSION = 5.9
IPHONEOS_DEPLOYMENT_TARGET = 16.0
CODE_SIGN_STYLE = Automatic
```

Run with configuration:
```bash
xcodebuild -project MyApp.xcodeproj -scheme MyScheme -xcconfig Release.xcconfig build
```

### 1.2 Swift/SwiftUI Best Practices

#### Architecture Patterns

**MVVM (Model-View-ViewModel):**
```swift
import SwiftUI

// Model
struct TodoItem: Identifiable, Codable {
    let id: UUID
    var title: String
    var isCompleted: Bool
}

// ViewModel
@MainActor
class TodoViewModel: ObservableObject {
    @Published var items: [TodoItem] = []
    
    func addItem(_ title: String) {
        items.append(TodoItem(id: UUID(), title: title, isCompleted: false))
    }
}

// View
struct TodoListView: View {
    @StateObject private var viewModel = TodoViewModel()
    
    var body: some View {
        List {
            ForEach(viewModel.items) { item in
                Text(item.title)
            }
        }
    }
}
```

**TCA (The Composable Architecture):**
- More complex but excellent for large apps
- Built-in support for dependency injection
- Composable and testable

#### Project Organization Guidelines

1. **Use Swift Package Manager** for dependencies (preferred over CocoaPods)
2. **Group by feature** rather than by file type for large projects
3. **Keep AppDelegate/App minimal** - delegate to other objects
4. **Use @MainActor** for UI-related code

### 1.3 Code Signing

#### Understanding Code Signing

Code signing verifies app identity and ensures code hasn't been modified. Components:
- **Certificates:** Identity documents (Development, Distribution)
- **Provisioning Profiles:** Permissions and device whitelist
- **App ID:** Unique identifier (bundle ID + capabilities)

#### Automatic vs Manual Signing

**Automatic Signing (Recommended):**
```bash
# In Xcode:
# Project → Signing & Capabilities → Enable "Automatically manage signing"

# Or via xcodebuild:
xcodebuild -project MyApp.xcodeproj -scheme MyScheme \
    -allowProvisioningUpdates \
    CODE_SIGN_IDENTITY=- CODE_SIGNING_REQUIRED=NO CODE_SIGNING_ALLOWED=NO
```

**Manual Signing:**
```bash
# Download certificates and profiles from Developer Portal
# Set in Xcode: Signing → Uncheck "Automatically manage signing"

# Export manually signed archive
xcodebuild -exportArchive \
    -archivePath ./MyApp.xcarchive \
    -exportPath ./Export \
    -exportOptionsPlist ExportOptions.plist
```

#### Distribution Certificate Types

From Apple Developer documentation:
- **Apple Development:** For development/testing on devices
- **Apple Distribution:** For App Store distribution (replaces iOS Distribution)
- **iOS Development / iOS Distribution:** Legacy certificates

**Certificate Limits:**
- Maximum 2 iOS Development certificates per team member
- 1 Distribution certificate per team

### 1.4 Entitlements

Entitlements grant specific app capabilities. Key entitlements:

```xml
<!-- MyApp.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- App Groups for data sharing -->
    <key>com.apple.security.application-groups</key>
    <array>
        <string>group.com.example.myapp</string>
    </array>
    
    <!-- Push Notifications -->
    <key>aps-environment</key>
    <string>development</string>
    
    <!-- HealthKit -->
    <key>com.apple.developer.healthkit</key>
    <true/>
    <key>com.apple.developer.healthkit.access</key>
    <array/>
    
    <!-- HomeKit -->
    <key>com.apple.developer.homekit</key>
    <true/>
    
    <!-- CloudKit -->
    <key>com.apple.developer.icloud-container-identifiers</key>
    <array>
        <string>iCloud.com.example.myapp</string>
    </array>
    <key>com.apple.developer.icloud-services</key>
    <array>
        <string>CloudKit</string>
    </array>
    
    <!-- Family Controls (ScreenTime API) -->
    <key>com.apple.developer.family-controls</key>
    <true/>
</dict>
</plist>
```

**To add capabilities in Xcode:**
1. Select target → Signing & Capabilities
2. Click "+" to add capability
3. Select required entitlements

### 1.5 Frameworks

#### ScreenTime API (Family Controls)

Required for parental control apps:

```swift
import FamilyControls
import DeviceActivity
import ManagedSettings

// Authorization
AuthorizationCenter.shared.requestAuthorization(for: .individual) { result in
    switch result {
    case .success:
        print("Authorized")
    case .failure(let error):
        print(error)
    }
}

// DeviceActivityMonitor (App Extension)
class DeviceActivityMonitorExtension: DeviceActivityMonitor {
    override func intervalDidStart(for activity: DeviceActivityName) {
        super.intervalDidStart(for: activity)
    }
    
    override func eventDidReachThreshold(_ event: DeviceActivityEvent.Name, activity: DeviceActivityName) {
        super.eventDidReachThreshold(event, activity: activity)
    }
}
```

**Note:** Requires special entitlement request from Apple.

#### StoreKit 2 (In-App Purchases)

```swift
import StoreKit

// Product request
func loadProducts() async {
    do {
        let products = try await Product.products(for: ["com.example.premium", "com.example.subscription"])
        for product in products {
            print("\(product.displayName): \(product.price)")
        }
    } catch {
        print("Failed: \(error)")
    }
}

// Purchase
func purchase(_ product: Product) async {
    do {
        let result = try await product.purchase()
        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await transaction.finish()
        case .userCancelled:
            break
        default:
            break
        }
    } catch {
        print("Purchase failed: \(error)")
    }
}

// Check entitlements
func checkEntitlements() async {
    for await result in Transaction.currentEntitlements {
        if result.revocationDate == nil {
            print("Entitled: \(result.productID)")
        }
    }
}
```

#### CloudKit

```swift
import CloudKit

let container = CKContainer(identifier: "iCloud.com.example.myapp")

// Private database (user's iCloud)
let privateDB = container.privateCloudDatabase

// Public database
let publicDB = container.publicCloudDatabase

// Save record
let record = CKRecord(recordType: "MyType")
record["name"] = "Example" as CKRecordValue
privateDB.save(record) { savedRecord, error in
    if let error = error {
        print(error)
    }
}
```

#### WidgetKit

```swift
import WidgetKit
import SwiftUI

struct MyWidgetEntry: TimelineEntry {
    let date: Date
    let data: String
}

struct MyWidgetProvider: TimelineProvider {
    func placeholder(in context: Context) -> MyWidgetEntry {
        MyWidgetEntry(date: Date(), data: "Loading...")
    }
    
    func getSnapshot(in context: Context, completion: @escaping (MyWidgetEntry) -> Void) {
        completion(MyWidgetEntry(date: Date(), data: "Snapshot"))
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<MyWidgetEntry>) -> Void) {
        let entry = MyWidgetEntry(date: Date(), data: Date().description)
        let timeline = Timeline(entries: [entry], policy: .atEnd)
        completion(timeline)
    }
}

struct MyWidget: Widget {
    let kind: String = "MyWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: MyWidgetProvider()) { entry in
            Text(entry.data)
        }
    }
}
```

### 1.6 Testing

#### Running Tests with xcodebuild

```bash
# Build and run tests
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -destination 'platform=iOS Simulator,name=iPhone 17'

# Build tests without running
xcodebuild build-for-testing \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -destination 'platform=iOS Simulator,name=iPhone 17'

# Run pre-built tests
xcodebuild test-without-building \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -destination 'platform=iOS Simulator,name=iPhone 17' \
    -xctestrun ./Build/Products/Test.xctestrun

# Test specific target or class
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -destination 'platform=iOS Simulator,name=iPhone 17' \
    -only-testing:MyAppTests/MyTestClass

# Skip specific tests
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -destination 'platform=iOS Simulator,name=iPhone 17' \
    -skip-testing:MyAppUITests
```

#### Test Plans

```bash
# Show available test plans
xcodebuild -showTestPlans -project MyApp.xcodeproj -scheme MyScheme

# Run specific test plan
xcodebuild test \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -testPlan SmokeTests \
    -destination 'platform=iOS Simulator,name=iPhone 17'
```

#### Key Testing Flags

| Flag | Description |
|------|-------------|
| `-destination` | Specify device/simulator (required for test) |
| `-only-testing` | Include specific tests |
| `-skip-testing` | Exclude specific tests |
| `-testPlan` | Use specific test plan configuration |
| `-parallel-testing-enabled` | Enable parallel test execution |
| `-retry-tests-on-failure` | Retry failed tests |
| `-enableCodeCoverage` | Generate code coverage report |

### 1.7 Build Commands

#### Archive

```bash
# Archive for App Store
xcodebuild archive \
    -project MyApp.xcodeproj \
    -scheme MyScheme \
    -configuration Release \
    -archivePath ./MyApp.xcarchive

# Archive with specific destination
xcodebuild archive \
    -workspace MyApp.xcworkspace \
    -scheme MyScheme \
    -configuration Release \
    -sdk iphoneos \
    -archivePath ./Build/MyApp.xcarchive
```

#### Export

```bash
# Export archive for App Store distribution
xcodebuild -exportArchive \
    -archivePath ./MyApp.xcarchive \
    -exportPath ./Export \
    -exportOptionsPlist ExportOptions.plist
```

**ExportOptions.plist example:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>signingCertificate</key>
    <string>Apple Distribution</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>uploadSymbols</key>
    <true/>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>manageAppVersionAndBuildNumber</key>
    <true/>
</dict>
</plist>
```

#### Key xcodebuild Options

| Option | Description |
|--------|-------------|
| `-project` | Xcode project name |
| `-workspace` | Xcode workspace name |
| `-scheme` | Build scheme name |
| `-configuration` | Debug or Release |
| `-sdk` | Target SDK (iphoneos, iphonesimulator) |
| `-destination` | Device/simulator destination |
| `-derivedDataPath` | Build output directory |
| `-archivePath` | Archive output path |
| `-allowProvisioningUpdates` | Allow automatic signing |

---

## Part 2: App Store Connect

### 2.1 App Store Connect Setup

#### Creating App Record

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Sign in with Apple Developer account
3. Navigate to Apps → "+" → New App

**Required fields:**
- **Platform:** iOS, macOS, tvOS, visionOS, watchOS
- **Name:** App name (max 30 characters)
- **Primary Language:** Default language
- **Bundle ID:** Must match Xcode project (e.g., com.example.myapp)
- **SKU:** Unique ID (not visible to users)

#### Bundle ID and App ID

**Register Bundle ID:**
1. Go to [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources)
2. Identifiers → "+" → App IDs
3. Select type: App (not App Clip)
4. Enable required capabilities
5. Register

**Note:** Bundle ID cannot be changed after app creation.

### 2.2 Certificates and Profiles

#### Creating Distribution Certificate

**Method 1: Xcode (Automatic)**
- Xcode → Settings → Accounts → Add Apple Developer account
- Project → Signing & Capabilities → Check "Automatically manage signing"

**Method 2: Developer Portal (Manual)**

1. Certificate → "+" → Apple Distribution
2. Create CSR via Keychain Access:
```bash
# Create CSR
openssl req -new -key mykey.key -out CertificateSigningRequest.certSigningRequest \
    -subj "/emailAddress=developer@example.com/CN=Developer Name/C=US"
```
3. Upload CSR to Apple
4. Download and install certificate

#### Creating Provisioning Profile

1. Profiles → "+" → App Store Connect
2. Select App ID (bundle ID)
3. Select Distribution certificate
4. Name and generate profile
5. Download and install (or let Xcode handle)

### 2.3 App Metadata

#### Required Metadata

| Field | Limit | Notes |
|-------|-------|-------|
| App Name | 30 chars | Key for discoverability |
| Subtitle | 30 chars | Appears below name |
| Description | 4000 chars | Detailed app info |
| Keywords | 100 bytes | Comma-separated |
| Support URL | Required | Must be valid |
| Privacy Policy URL | Required | For all apps |

#### Screenshot Specifications (2026)

**iPhone:**
| Display | Devices | Size (portrait) |
|---------|---------|-----------------|
| 6.9" | iPhone 17 Pro Max | 1260 × 2736 |
| 6.5" | iPhone 14 Plus, 13 Pro Max | 1242 × 2688 |
| 6.3" | iPhone 17 Pro, 16 Pro | 1206 × 2622 |
| 6.1" | iPhone 17, 14, 13 | 1170 × 2532 |

**iPad:**
| Display | Size |
|---------|------|
| 13" (portrait) | 2064 × 2752 |
| 11" (portrait) | 1488 × 2266 |

- Format: JPEG, PNG
- Minimum 1, maximum 10 screenshots
- App previews: Optional, .mov/.m4v/.mp4 (H.264), up to 30 seconds

### 2.4 App Store Review Guidelines

#### Common Rejection Reasons

1. **Missing demo account:** Provide working test credentials
2. **Incomplete app info:** Fill all metadata fields
3. **Broken links:** Check all URLs in metadata
4. **Privacy issues:** Proper data collection disclosures
5. **Misleading content:** App must match descriptions/screenshots
6. **In-app purchase issues:** Not clearly explained

#### Preparation Checklist

- [ ] Test on physical device (not just simulator)
- [ ] Complete all metadata fields
- [ ] Provide demo account if login required
- [ ] Include App Review notes for complex features
- [ ] Verify privacy manifest (required since Nov 2024)
- [ ] Complete App Privacy answers in App Store Connect

### 2.5 Privacy

#### Privacy Manifest (PrivacyInfo.xcprivacy)

Required since November 12, 2024. Add to target:

```xml
<!-- PrivacyInfo.xcprivacy -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>C617.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategorySystemBootTime</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>35F9.1</string>
            </array>
        </dict>
    </array>
    <key>NSPrivacyCollectedDataTypes</key>
    <array/>
    <key>NSPrivacyTracking</key>
    <false/>
    <key>NSPrivacyTrackingDomains</key>
    <array/>
</dict>
</plist>
```

#### App Tracking Transparency (ATT)

To track users or access IDFA:

```swift
import AppTrackingTransparency
import AdSupport

// Request permission
func requestTrackingPermission() {
    ATTrackingManager.requestTrackingAuthorization { status in
        switch status {
        case .authorized:
            let idfa = ASIdentifierManager.shared().advertisingIdentifier
        case .denied, .restricted, .notDetermined:
            break
        @unknown default:
            break
        }
    }
}
```

**Note:** Include NSUserTrackingUsageDescription in Info.plist.

#### App Privacy in App Store Connect

1. Go to App → App Privacy
2. Answer questions about data collection:
   - Data types collected
   - Third-party data collection
   - Tracking usage
3. Provide Privacy Policy URL

### 2.6 In-App Purchases & Subscriptions

#### StoreKit 2 Setup

1. App Store Connect → Your App → In-App Purchases
2. Create products ( Consumable, Non-Consumable, Subscription)
3. For subscriptions: Create subscription group first

#### Product Types

**Consumable:** Credits, gems, one-time use items
**Non-Con consumable:** Premium features, one-time purchase
**Auto-renewable:** Subscriptions that renew automatically
**Non-renewing:** Time-limited subscriptions (manually managed)

#### Subscription Groups

```swift
// In App Store Connect:
//
// Subscription Group: Premium
//   ├── Weekly Premium ($4.99/week)
//   ├── Monthly Premium ($9.99/month)
//   └── Yearly Premium ($49.99/year)
```

**Requirements for review:**
- Review screenshot for each subscription level
- Subscription demo account (if features are content)
- Review notes describing features

#### Testing In-App Purchases

- **Simulator:** Use StoreKit Testing in Xcode
- **Sandbox:** Create sandbox tester account in App Store Connect
- **Production:** Real purchases (requires approved app)

---

## Part 3: Submission & Release

### 3.1 Archive and Upload

#### Using Xcode Organizer

1. Product → Archive (Cmd+Shift+B)
2. Wait for completion
3. Window → Organizer → Archives
4. Select archive → Distribute App
5. Follow wizard for App Store Connect

#### Using altool (Command Line)

```bash
# Upload .ipa to App Store Connect
xcrun altool --upload-app -f ./MyApp.ipa \
    --api-key "API_KEY_ID" \
    --api-issuer "ISSUER_ID"

# Or with username/password
xcrun altool --upload-app -f ./MyApp.ipa \
    -u "developer@apple.com" \
    -p "@keychain:APPLE_PASSWORD"

# Check upload status
xcrun altool --build-status \
    --apple-id "123456789" \
    --bundle-version "1.0" \
    --bundle-short-version-string "1.0.0" \
    --platform ios
```

#### Using Transporter App

1. Download Transporter from Mac App Store
2. Sign in with Apple Developer account
3. Add .ipa or .xcarchive file
4. Click Deliver

### 3.2 TestFlight

#### Internal Testing

- **Limit:** Up to 100 internal testers
- **Setup:** App Store Connect → TestFlight → Internal Testing
- **Access:** Add team members in Users and Access

#### External Testing

- **Limit:** Up to 10,000 external testers
- **Beta App Review:** Required for first external build
- **Setup:** App Store Connect → TestFlight → External Testing

```bash
# Using pilot (Fastlane) to manage TestFlight
fastlane pilot add
fastlane pilot list
fastlane pilot distribute --ipa ./MyApp.ipa
```

#### TestFlight Workflow

1. Upload build
2. Wait for processing (can take hours)
3. For external: Build becomes available after beta review (usually 24-48h)
4. Testers install via TestFlight app
5. Submit feedback via TestFlight

### 3.3 App Review Process

#### Timeline

- **Average:** 24-48 hours
- **Complex apps:** May take longer
- **Expedited review:** Available for critical bugs or time-sensitive releases

#### Expedited Review Request

Request at: App Store Connect → App → Activity → Expedited Review

**Valid reasons:**
- Critical bug fix
- Security vulnerability
- Time-sensitive event
- Legal requirement

#### Responding to Rejection

1. Read rejection reason in App Store Connect
2. Address issues in code/metadata
3. Reply with resolution notes in App Store Connect
4. Re-submit

#### Appeal Process

If you believe rejection was incorrect:
1. App Store Connect → App → Activity → Resolution Center
2. Submit appeal explaining why the rejection should be overturned
3. Wait for App Review Board response (1-2 weeks typical)

### 3.4 Release Management

#### Version Release Options

| Option | Description |
|--------|-------------|
| Manual | Developer releases after approval |
| Automatic | Goes live immediately after approval |
| Automatic (No earlier than) | Scheduled release |

#### Phased Release

Available for automatic updates (iOS 14+):

- 1 day: 1%
- 2 days: 2%
- 3 days: 5%
- 4 days: 20%
- 5 days: 50%
- 6 days: 75%
- 7 days: 100%

Users can opt out in Settings.

### 3.5 Post-Launch

#### Crash Reporting

**Xcode Organizer:**
- Window → Organizer → Crashes
- View crash logs and statistics

**MetricKit:**
```swift
import MetricKit

// In AppDelegate
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions...) {
    MXMetricManager.shared().add(self)
}

extension AppDelegate: MXMetricManagerSubscriber {
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            // Process crash/anr metrics
        }
    }
}
```

#### Ratings and Reviews

- Respond to reviews in App Store Connect
- Use SKStoreReviewController to prompt (max 3 times per 365 days)
- Reset overview rating with each major version update

#### App Analytics

Access via App Store Connect → Analytics:
- Impressions, Product Page Views
- Conversion Rate
- Downloads, Proceeds
- Retention, Engagement metrics

---

## Part 4: Automation

### 4.1 Fastlane

#### Installation

```bash
# Install Fastlane
sudo gem install fastlane

# Or via Homebrew
brew install fastlane
```

#### Key Fastlane Actions

**match (Code Signing):**
```ruby
# Fastfile
lane :certificates do
    match(type: "appstore", appIdentifier: "com.example.myapp")
end
```

**gym (Build):**
```ruby
lane :build do
    gym(
        scheme: "MyApp",
        configuration: "Release",
        export_method: "app-store",
        output_name: "MyApp"
    )
end
```

**deliver (Upload to App Store Connect):**
```ruby
lane :upload do
    deliver(
        skip_screenshots: false,
        skip_metadata: false,
        force: true
    )
end
```

**pilot (TestFlight):**
```ruby
lane :testflight do
    pilot(
        app_identifier: "com.example.myapp",
        distribute_external: true,
        groups: ["External Testers"]
    )
end
```

**scan (Testing):**
```ruby
lane :test do
    scan(
        scheme: "MyApp",
        devices: ["iPhone 17"]
    )
end
```

**snapshot (Screenshots):**
```ruby
lane :screenshots do
    snapshot(
        scheme: "MyApp",
        devices: ["iPhone 17", "iPad Pro 13"],
        languages: ["en-US", "en-GB"]
    )
end
```

#### Example Complete CI Pipeline

```ruby
# Fastfile
default_platform(:ios)

platform :ios do
    lane :ci do
        match(app_identifier: "com.example.myapp", type: "appstore")
        
        gym(
            scheme: "MyApp",
            configuration: "Release",
            export_method: "app-store"
        )
        
        deliver(skip_screenshots: true, skip_metadata: true)
    end
end
```

### 4.2 GitHub Actions

#### iOS CI/CD Workflow

```yaml
name: iOS CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: macos-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Select Xcode
      uses: maxim-lobanov/setup-xcode@v1
      with:
        xcode-version: '26.4'
    
    - name: Cache CocoaPods
      uses: actions/cache@v3
      with:
        path: Pods
        key: ${{ runner.os }}-pods-${{ hashFiles('Podfile.lock') }}
    
    - name: Install dependencies
      run: pod install
    
    - name: Build
      run: |
        xcodebuild build-for-testing \
          -workspace MyApp.xcworkspace \
          -scheme MyApp \
          -destination 'platform=iOS Simulator,name=iPhone 17' \
          -derivedDataPath ./DerivedData
    
    - name: Run tests
      run: |
        xcodebuild test \
          -workspace MyApp.xcworkspace \
          -scheme MyApp \
          -destination 'platform=iOS Simulator,name=iPhone 17'
    
  deploy:
    needs: build
    runs-on: macos-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Import Apple Certificate
      env:
        APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
        APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
        KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
      run: |
        # Create keychain
        security create-keychain -p "$KEYCHAIN_PASSWORD" ios-build.keychain
        security set-keychain-settings ios-build.keychain
        security unlock-keychain -p "$KEYCHAIN_PASSWORD" ios-build.keychain
        
        # Import certificate
        echo -n "$APPLE_CERTIFICATE" | base64 --decode -o certificate.p12
        security import certificate.p12 -P "$APPLE_CERTIFICATE_PASSWORD" -A -t cert -f pkcs12 -k ios-build.keychain
        security set-key-partition-list -S apple-tool:,apple: -k "$KEYCHAIN_PASSWORD" ios-build.keychain
    
    - name: Build and Upload
      env:
        APPLE_API_KEY: ${{ secrets.APPLE_API_KEY }}
        APPLE_API_ISSUER: ${{ secrets.APPLE_API_ISSUER }}
      run: |
        xcodebuild archive \
          -workspace MyApp.xcworkspace \
          -scheme MyApp \
          -configuration Release \
          -archivePath ./MyApp.xcarchive
        
        xcodebuild -exportArchive \
          -archivePath ./MyApp.xcarchive \
          -exportPath ./Export \
          -exportOptionsPlist ExportOptions.plist
        
        # Upload via altool or Transporter
        xcrun altool --upload-app -f ./Export/MyApp.ipa \
          --api-key "$APPLE_API_KEY" \
          --api-issuer "$APPLE_API_ISSUER"
```

#### Prerequisites

1. **Apple Developer Certificate:** Create .p12 certificate
2. **App Store Connect API Key:** Create in Users and Access
3. **GitHub Secrets:** Store sensitive values

### 4.3 Command-Line Tools

#### altool

```bash
# Upload
xcrun altool --upload-app -f /path/to/app.ipa \
    --api-key "KEY_ID" --api-issuer "ISSUER_ID"

# Validate without uploading
xcrun altool --validate-app /path/to/app.ipa \
    -u "user@apple.com" -p "password"

# List providers
xcrun altool --list-providers --api-key "KEY_ID" --api-issuer "ISSUER_ID"

# Build status
xcrun altool --build-status --apple-id "123456789" \
    --bundle-version "1" --platform ios
```

#### simctl

```bash
# List available simulators
xcrun simctl list devices available

# Boot simulator
xcrun simctl boot "iPhone 17"

# Install app
xcrun simctl install booted /path/to/app.app

# Launch app
xcrun simctl launch booted com.example.myapp

# Open URL
xcrun simctl openurl booted "myapp://action"

# Erase device
xcrun simctl erase booted
```

#### notarytool (macOS Notarization)

```bash
# Submit for notarization
xcrun notarytool submit MyApp.zip \
    --apple-id "user@apple.com" \
    --password "@keychain:APPLE_PASSWORD" \
    --team-id "TEAM_ID"

# Wait for completion
xcrun notarytool wait --uuid "UUID" \
    --apple-id "user@apple.com" \
    --password "password"

# Staple (attach notarization)
xcrun notarytool staple MyApp.app
```

---

## Resources

### Key URLs

- **App Store Connect:** https://appstoreconnect.apple.com
- **Developer Portal:** https://developer.apple.com/account
- **App Store Review Guidelines:** https://developer.apple.com/app-store/review/guidelines/
- **Certificate Types:** https://developer.apple.com/help/account/reference/certificate-types
- **Screenshot Specs:** https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications

### Version Compatibility Notes (2025-2026)

From App Store Connect Release Notes (March 2026):
- Xcode 26.4 upload support for all platforms
- New devices: iPhone 17e, iPad Air 13" (M4), iPad Air 11" (M4)
- Multiple draft submissions now supported
- Build upload status tracking enhanced with webhooks
- Offer codes now available for consumable and non-consumable IAPs
- Managed Apple Accounts can now use TestFlight (except Student roles)

---

*Skill Version: 1.0 | Last Updated: March 2026 | Xcode: 26.4*
