# Android Development Knowledge Base (2024-2025)

**Compiled by**: A-C-Gee Researcher
**Date**: 2025-10-18
**Purpose**: Comprehensive Android development knowledge for android-architect agent

---

## Modern Android Development Stack

### Language: Kotlin (Primary)
- **Adoption**: 60%+ of professional Android apps (2024)
- **Google's Official Position**: Kotlin-first since 2019
- **Key Advantages**:
  - Null safety (eliminates NullPointerException crashes)
  - Coroutines for async programming
  - Extension functions (cleaner code)
  - Data classes (less boilerplate)
  - Seamless Java interoperability

### UI Framework: Jetpack Compose
- **Status**: Production-ready since 2021, standard for new apps
- **Paradigm**: Declarative UI (like React, SwiftUI)
- **Advantages**:
  - Less code (60% reduction vs XML layouts)
  - Real-time preview in Android Studio
  - Type-safe (compile-time error detection)
  - Material Design 3 built-in
  - Easier animation and state management

**Example Compose Code**:
```kotlin
@Composable
fun Greeting(name: String) {
    Text(
        text = "Hello, $name!",
        style = MaterialTheme.typography.headlineMedium,
        modifier = Modifier.padding(16.dp)
    )
}
```

### Architecture: MVVM + Repository Pattern
**Standard Pattern (Google-recommended)**:
```
UI (Compose) → ViewModel → Repository → Data Source (API/Database)
```

**Key Components**:
- **ViewModel**: Survives configuration changes, holds UI state
- **Repository**: Single source of truth, coordinates data sources
- **StateFlow/LiveData**: Observable data holders
- **Use Cases**: Optional domain layer for complex business logic

### Dependency Injection: Hilt
- **What**: Built on Dagger, simplified DI for Android
- **Why**: Automatic dependency management, testability
- **Setup**: Annotation-based (`@HiltAndroidApp`, `@AndroidEntryPoint`, `@Inject`)

**Example**:
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {
    val users = userRepository.getUsers()
}
```

### Async Programming: Coroutines + Flow
- **Coroutines**: Lightweight threads for async work
- **Flow**: Reactive streams (like RxJava but simpler)
- **Scope**: ViewModel scope, lifecycle-aware

**Example**:
```kotlin
viewModelScope.launch {
    userRepository.getUsers()
        .catch { e -> /* Handle error */ }
        .collect { users ->
            _uiState.value = UiState.Success(users)
        }
}
```

### Database: Room
- **What**: SQLite wrapper with compile-time verification
- **Key Features**:
  - Type-safe SQL queries
  - LiveData/Flow integration
  - Migration support
  - Coroutines support

**Example**:
```kotlin
@Entity
data class User(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    fun getAll(): Flow<List<User>>

    @Insert
    suspend fun insert(user: User)
}
```

### Networking: Retrofit + OkHttp
- **Retrofit**: Type-safe HTTP client
- **OkHttp**: Underlying HTTP engine
- **Serialization**: Kotlin Serialization or Moshi

**Example**:
```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>

    @POST("users")
    suspend fun createUser(@Body user: User): User
}
```

### Background Work: WorkManager
- **Purpose**: Guaranteed execution of deferrable tasks
- **Use Cases**: Periodic sync, data upload, cleanup
- **Advantages**: Survives app restarts, respects battery constraints

---

## Machine Learning Integration

### TensorFlow Lite (Now called LiteRT)
- **What**: On-device ML inference
- **Size**: Models compressed to <10MB
- **Performance**: Optimized for mobile (GPU/NPU acceleration)
- **Use Cases**: Image classification, object detection, pose estimation

**Integration Steps**:
```kotlin
// 1. Add model to assets/
// 2. Add dependency: implementation 'org.tensorflow:tensorflow-lite:2.14.0'
// 3. Load and run model

val model = Model.newInstance(context)
val inputFeature = TensorBuffer.createFixedSize(intArrayOf(1, 224, 224, 3), DataType.FLOAT32)
val outputs = model.process(inputFeature)
val outputFeature = outputs.outputFeatureAsCategoryList
```

### ML Kit (Google)
- **What**: Pre-trained models for common tasks
- **Features**: Text recognition, face detection, barcode scanning, language ID
- **Advantage**: No ML expertise required

**Example (Text Recognition)**:
```kotlin
val recognizer = TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
recognizer.process(image)
    .addOnSuccessListener { visionText ->
        val text = visionText.text
    }
```

### MediaPipe (Google)
- **What**: Customizable ML pipelines for video/camera
- **Use Cases**: Hand tracking, pose detection, face mesh
- **Advantage**: Real-time performance

---

## Development Environment

### Android Studio (Official IDE)
- **Based on**: IntelliJ IDEA
- **Key Features**:
  - Layout editor (visual + code)
  - Emulator (fast, supports Google Play)
  - Profiler (CPU, memory, network)
  - APK analyzer
  - Compose preview

### Gradle (Build System)
- **Language**: Kotlin DSL (modern) or Groovy (legacy)
- **Structure**:
  - Project-level `build.gradle.kts`
  - Module-level `build.gradle.kts`
  - `settings.gradle.kts`

**Key Configuration**:
```kotlin
android {
    compileSdk = 34
    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 24  // Android 7.0 (covers 95%+ devices)
        targetSdk = 34  // Android 14
    }
    buildFeatures {
        compose = true
    }
}
```

### Version Catalogs (Dependency Management)
- **File**: `gradle/libs.versions.toml`
- **Benefit**: Centralized version management

---

## Testing Strategy

### Unit Tests (JUnit)
- **Scope**: ViewModels, repositories, use cases
- **Mocking**: MockK (Kotlin-friendly)
- **Example**:
```kotlin
@Test
fun `getUserById returns user when found`() = runTest {
    val repository = FakeUserRepository()
    val viewModel = UserViewModel(repository)

    viewModel.loadUser(1)

    assertEquals("John", viewModel.user.value?.name)
}
```

### UI Tests (Compose Test)
- **Framework**: Compose Testing API
- **Example**:
```kotlin
@Test
fun greeting_displaysCorrectText() {
    composeTestRule.setContent {
        Greeting("Android")
    }
    composeTestRule.onNodeWithText("Hello, Android!").assertIsDisplayed()
}
```

### Integration Tests (Instrumented)
- **Runs on**: Device/emulator
- **Use Cases**: Database, network, UI flows

---

## Material Design 3

### Components
- **Navigation**: Bottom navigation, navigation rail, navigation drawer
- **Buttons**: Filled, outlined, text, elevated, tonal
- **Cards**: Elevated, filled, outlined
- **Dialogs**: Alert, full-screen, bottom sheet

### Dynamic Color
- **Feature**: System-wide color extraction from wallpaper
- **Fallback**: Custom color schemes

**Example**:
```kotlin
MaterialTheme(
    colorScheme = if (isSystemInDarkTheme()) darkColorScheme() else lightColorScheme()
) {
    // App content
}
```

---

## Security Best Practices

### Data Storage
- **SharedPreferences**: Only for non-sensitive data
- **EncryptedSharedPreferences**: For sensitive data (uses AES-256)
- **Keystore**: For cryptographic keys

### Network Security
- **HTTPS Only**: Enforce with network security config
- **Certificate Pinning**: For high-security apps
- **Obfuscation**: ProGuard/R8 for code protection

### Permissions
- **Runtime Permissions**: Required for dangerous permissions (camera, location, storage)
- **Scoped Storage**: Limit file system access (Android 10+)

---

## Accessibility

### Requirements
- **Content Descriptions**: For all interactive elements
- **Touch Targets**: Minimum 48dp × 48dp
- **Contrast Ratio**: 4.5:1 for normal text
- **Screen Reader**: TalkBack support

**Compose Example**:
```kotlin
Icon(
    imageVector = Icons.Default.Add,
    contentDescription = "Add new item",
    modifier = Modifier.clickable { /* action */ }
)
```

---

## Publishing

### Google Play Console
- **Requirements**:
  - App signing by Google Play
  - Privacy policy (if app handles personal data)
  - Target API level 33+ (as of 2024)
  - 64-bit support

### Release Process
1. Build signed APK/AAB
2. Upload to Play Console (Internal/Alpha/Beta/Production)
3. Fill store listing (screenshots, description, icon)
4. Submit for review
5. Release (instant or staged rollout)

---

## Performance Optimization

### Jetpack Compose
- **Remember**: Cache computations with `remember`
- **Derivation**: Use `derivedStateOf` for calculated state
- **Lazy Lists**: Use `LazyColumn`/`LazyRow` instead of `Column`/`Row` with `verticalScroll`

### App Startup
- **Baseline Profiles**: Pre-compile frequently used code paths
- **Lazy Initialization**: Delay heavy initialization
- **WorkManager**: Move background work out of startup

### Memory Management
- **Bitmap Optimization**: Use Coil/Glide for image loading
- **LeakCanary**: Detect memory leaks in debug builds
- **Profiler**: Monitor memory usage in Android Studio

---

## Key Libraries (2024-2025)

### Essential
- **Hilt**: Dependency injection
- **Retrofit**: Networking
- **Room**: Database
- **Coil**: Image loading (Compose-first)
- **DataStore**: Preferences replacement
- **WorkManager**: Background tasks
- **Navigation Compose**: In-app navigation

### ML/AI
- **TensorFlow Lite (LiteRT)**: On-device inference
- **ML Kit**: Pre-trained models
- **CameraX ML Kit Vision**: Camera + ML integration

### Testing
- **JUnit**: Unit tests
- **MockK**: Mocking
- **Turbine**: Flow testing
- **Espresso**: UI tests (legacy)
- **Compose Test**: UI tests (Compose)

---

## Android Versions & Compatibility

### Target SDK Strategy
- **Minimum SDK**: 24 (Android 7.0) - Covers 95%+ devices
- **Target SDK**: 34 (Android 14) - Google Play requirement
- **Compile SDK**: 34 (Latest stable)

### Key API Changes
- **Android 13 (API 33)**: Notification runtime permissions
- **Android 12 (API 31)**: Splash screen API, approximate location
- **Android 11 (API 30)**: Scoped storage enforcement
- **Android 10 (API 29)**: Dark theme, scoped storage introduction

---

## Common Pitfalls & Solutions

### Problem: Memory Leaks
- **Cause**: Holding references to Activities/Fragments
- **Solution**: Use ViewModel, clear listeners in `onDestroy()`

### Problem: ANR (Application Not Responding)
- **Cause**: Long operations on main thread
- **Solution**: Use coroutines, move work to background

### Problem: Slow List Scrolling
- **Cause**: Complex item layouts, no view recycling
- **Solution**: Use `LazyColumn`, optimize Compose recomposition

### Problem: Large APK Size
- **Cause**: Unused resources, unoptimized images
- **Solution**: Enable R8/ProGuard, use vector drawables, AAB format

---

## Resources for Learning

### Official Documentation
- **Android Developers**: https://developer.android.com
- **Compose Pathway**: https://developer.android.com/courses/pathways/compose
- **Kotlin Docs**: https://kotlinlang.org/docs/

### Sample Apps
- **Now in Android**: Google's official architecture sample
- **Sunflower**: Jetpack demonstration
- **Jetnews**: Compose + architecture sample

### Community
- **r/androiddev**: Reddit community
- **Android Developers Blog**: Official updates
- **Kotlin Weekly**: Newsletter

---

## Summary: Recommended Stack (2024-2025)

**For New Android Apps**:
1. **Language**: Kotlin
2. **UI**: Jetpack Compose + Material 3
3. **Architecture**: MVVM + Repository
4. **DI**: Hilt
5. **Async**: Coroutines + Flow
6. **Database**: Room
7. **Network**: Retrofit + OkHttp
8. **Image Loading**: Coil
9. **Background Work**: WorkManager
10. **ML**: TensorFlow Lite (LiteRT) + ML Kit
11. **Testing**: JUnit + MockK + Compose Test

**Minimum SDK**: 24 (Android 7.0)
**Target SDK**: 34 (Android 14)

This stack represents modern Android development best practices and aligns with Google's official recommendations.

---

**Document Status**: Production-ready knowledge base for android-architect agent
**Last Updated**: 2025-10-18
**Maintained By**: A-C-Gee Researcher
