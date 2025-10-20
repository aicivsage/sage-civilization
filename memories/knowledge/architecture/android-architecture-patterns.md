# Android Architecture Patterns: Complete Design Guide

**Compiled by**: A-C-Gee Architect
**Date**: 2025-10-18
**Purpose**: Comprehensive architecture patterns for android-architect agent

---

## Table of Contents
1. [Architecture Decision Framework](#architecture-decision-framework)
2. [MVVM Pattern (Recommended Default)](#mvvm-pattern)
3. [MVI Pattern (Complex State)](#mvi-pattern)
4. [Clean Architecture (3 Layers)](#clean-architecture)
5. [Repository Pattern](#repository-pattern)
6. [Dependency Injection with Hilt](#dependency-injection)
7. [ML Integration Architecture](#ml-integration-architecture)
8. [Testing Strategy](#testing-strategy)
9. [Anti-Patterns to Avoid](#anti-patterns)
10. [Code Structure Templates](#code-structure-templates)

---

## Architecture Decision Framework

### When to Use Which Pattern

**MVVM (Model-View-ViewModel)**:
- ✅ Standard business apps (CRUD, forms, lists)
- ✅ Moderate state complexity
- ✅ Team familiar with Android best practices
- ✅ Fast development needed

**MVI (Model-View-Intent)**:
- ✅ Complex state management (multi-step flows, real-time updates)
- ✅ Time-travel debugging needed
- ✅ Highly interactive UIs
- ❌ Overkill for simple apps

**Clean Architecture (3 Layers)**:
- ✅ Large teams (clear boundaries)
- ✅ Complex business logic
- ✅ High testability requirements
- ✅ Long-term maintenance
- ❌ Overkill for prototypes/MVPs

**Repository Pattern**:
- ✅ ALWAYS use (single source of truth)
- ✅ Multiple data sources (API + database + cache)
- ✅ Offline-first apps

---

## MVVM Pattern (Recommended Default)

### Architecture Diagram
```
┌─────────────────────────────────────────────────┐
│                   UI Layer                      │
│  ┌──────────────────────────────────────────┐  │
│  │  Composable Functions (@Composable)      │  │
│  │  - Observes ViewModel state              │  │
│  │  - Triggers ViewModel actions             │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────────┐
│                ViewModel Layer                  │
│  ┌──────────────────────────────────────────┐  │
│  │  ViewModel (extends androidx.ViewModel)  │  │
│  │  - Holds UI state (StateFlow/LiveData)   │  │
│  │  - Handles UI logic                      │  │
│  │  - Survives configuration changes        │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────────┐
│               Repository Layer                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Repository (Single Source of Truth)     │  │
│  │  - Coordinates data sources              │  │
│  │  - Caching strategy                      │  │
│  │  - Error handling                        │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────────┐
│               Data Source Layer                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Remote   │  │  Local   │  │  Cache   │     │
│  │ (API)    │  │  (Room)  │  │ (Memory) │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
```

### Complete MVVM Implementation

#### 1. Data Layer: Model + Repository

**Model (Data Class)**:
```kotlin
data class User(
    val id: Int,
    val name: String,
    val email: String,
    val avatarUrl: String
)
```

**API Service (Retrofit)**:
```kotlin
interface UserApiService {
    @GET("users")
    suspend fun getUsers(): List<User>

    @GET("users/{id}")
    suspend fun getUserById(@Path("id") id: Int): User

    @POST("users")
    suspend fun createUser(@Body user: User): User
}
```

**Local Database (Room)**:
```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val email: String,
    val avatarUrl: String
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    fun getAllUsers(): Flow<List<UserEntity>>

    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: Int): UserEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(users: List<UserEntity>)

    @Delete
    suspend fun delete(user: UserEntity)
}
```

**Repository (Single Source of Truth)**:
```kotlin
class UserRepository @Inject constructor(
    private val apiService: UserApiService,
    private val userDao: UserDao
) {
    // Expose Flow for reactive UI updates
    val users: Flow<List<User>> = userDao.getAllUsers()
        .map { entities -> entities.map { it.toDomain() } }

    // Refresh data from network
    suspend fun refreshUsers(): Result<Unit> {
        return try {
            val apiUsers = apiService.getUsers()
            userDao.insertAll(apiUsers.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    // Single item fetch
    suspend fun getUserById(id: Int): Result<User> {
        return try {
            // Try local first
            val localUser = userDao.getUserById(id)
            if (localUser != null) {
                return Result.success(localUser.toDomain())
            }

            // Fallback to network
            val apiUser = apiService.getUserById(id)
            userDao.insertAll(listOf(apiUser.toEntity()))
            Result.success(apiUser)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// Mappers
private fun User.toEntity() = UserEntity(id, name, email, avatarUrl)
private fun UserEntity.toDomain() = User(id, name, email, avatarUrl)
```

#### 2. ViewModel Layer: UI Logic + State

**UI State (Sealed Class)**:
```kotlin
sealed interface UserListUiState {
    object Loading : UserListUiState
    data class Success(val users: List<User>) : UserListUiState
    data class Error(val message: String) : UserListUiState
}
```

**ViewModel**:
```kotlin
@HiltViewModel
class UserListViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    // UI state exposed to Composables
    private val _uiState = MutableStateFlow<UserListUiState>(UserListUiState.Loading)
    val uiState: StateFlow<UserListUiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    // Public actions
    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UserListUiState.Loading

            // Collect from repository Flow
            userRepository.users
                .catch { e ->
                    _uiState.value = UserListUiState.Error(e.message ?: "Unknown error")
                }
                .collect { users ->
                    _uiState.value = UserListUiState.Success(users)
                }
        }
    }

    fun refreshUsers() {
        viewModelScope.launch {
            userRepository.refreshUsers()
                .onFailure { e ->
                    // Show error but keep existing data
                    // Could emit a Snackbar event here
                }
        }
    }
}
```

#### 3. UI Layer: Composables

**Screen Composable**:
```kotlin
@Composable
fun UserListScreen(
    viewModel: UserListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserListContent(
        uiState = uiState,
        onRefresh = { viewModel.refreshUsers() }
    )
}

@Composable
fun UserListContent(
    uiState: UserListUiState,
    onRefresh: () -> Unit
) {
    when (uiState) {
        is UserListUiState.Loading -> {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        }

        is UserListUiState.Success -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize()
            ) {
                items(uiState.users) { user ->
                    UserListItem(user = user)
                }
            }
        }

        is UserListUiState.Error -> {
            ErrorScreen(
                message = uiState.message,
                onRetry = onRefresh
            )
        }
    }
}

@Composable
fun UserListItem(user: User) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = user.avatarUrl,
                contentDescription = "Avatar for ${user.name}",
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = user.name,
                    style = MaterialTheme.typography.titleMedium
                )
                Text(
                    text = user.email,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
```

---

## MVI Pattern (Complex State)

### Architecture Diagram
```
┌─────────────────────────────────────────────────┐
│                   UI Layer                      │
│  ┌──────────────────────────────────────────┐  │
│  │  Composable                              │  │
│  │  - Renders state                         │  │
│  │  - Emits intents                         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↓ Intent
┌─────────────────────────────────────────────────┐
│                ViewModel Layer                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Intent Handler                          │  │
│  │  - Processes user intents                │  │
│  │  - Updates state immutably               │  │
│  │  - Single state stream                   │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                     ↑ State
```

### MVI Implementation

**Intent (User Actions)**:
```kotlin
sealed interface UserListIntent {
    object LoadUsers : UserListIntent
    object RefreshUsers : UserListIntent
    data class SearchUsers(val query: String) : UserListIntent
    data class SelectUser(val userId: Int) : UserListIntent
}
```

**State (Single Immutable State)**:
```kotlin
data class UserListState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val searchQuery: String = "",
    val selectedUserId: Int? = null
)
```

**ViewModel (Intent Processor)**:
```kotlin
@HiltViewModel
class UserListMviViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _state = MutableStateFlow(UserListState())
    val state: StateFlow<UserListState> = _state.asStateFlow()

    fun processIntent(intent: UserListIntent) {
        when (intent) {
            is UserListIntent.LoadUsers -> loadUsers()
            is UserListIntent.RefreshUsers -> refreshUsers()
            is UserListIntent.SearchUsers -> searchUsers(intent.query)
            is UserListIntent.SelectUser -> selectUser(intent.userId)
        }
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }

            userRepository.users
                .catch { e ->
                    _state.update { it.copy(isLoading = false, error = e.message) }
                }
                .collect { users ->
                    _state.update { it.copy(users = users, isLoading = false) }
                }
        }
    }

    private fun searchUsers(query: String) {
        _state.update {
            it.copy(
                searchQuery = query,
                users = filterUsers(it.users, query)
            )
        }
    }
}
```

---

## Clean Architecture (3 Layers)

### Layer Structure
```
┌─────────────────────────────────────────────────┐
│              Presentation Layer                 │
│  - ViewModels, UI State, Composables            │
│  - Depends on: Domain                           │
└─────────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────────┐
│                Domain Layer                     │
│  - Use Cases, Business Logic, Domain Models     │
│  - NO Android dependencies                      │
│  - Depends on: Nothing (pure Kotlin)            │
└─────────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────────┐
│                 Data Layer                      │
│  - Repositories, Data Sources, DTOs             │
│  - Depends on: Domain (implements interfaces)   │
└─────────────────────────────────────────────────┘
```

### Use Case Pattern

**Use Case (Domain Layer)**:
```kotlin
// Domain: No Android dependencies
class GetUserByIdUseCase @Inject constructor(
    private val userRepository: UserRepository
) {
    suspend operator fun invoke(userId: Int): Result<User> {
        // Business logic here (validation, transformation, etc.)
        if (userId <= 0) {
            return Result.failure(IllegalArgumentException("Invalid user ID"))
        }

        return userRepository.getUserById(userId)
    }
}
```

**ViewModel Using Use Case**:
```kotlin
@HiltViewModel
class UserDetailViewModel @Inject constructor(
    private val getUserByIdUseCase: GetUserByIdUseCase,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val userId: Int = savedStateHandle["userId"] ?: 0

    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    init {
        loadUser()
    }

    private fun loadUser() {
        viewModelScope.launch {
            getUserByIdUseCase(userId)
                .onSuccess { user -> _user.value = user }
                .onFailure { /* Handle error */ }
        }
    }
}
```

---

## Repository Pattern

### Offline-First Strategy

```kotlin
class OfflineFirstUserRepository @Inject constructor(
    private val apiService: UserApiService,
    private val userDao: UserDao,
    private val networkMonitor: NetworkMonitor
) : UserRepository {

    override val users: Flow<List<User>> = userDao.getAllUsers()
        .map { entities -> entities.map { it.toDomain() } }
        .onStart {
            // Try to refresh on start if network available
            if (networkMonitor.isOnline.first()) {
                refreshUsers()
            }
        }

    override suspend fun refreshUsers(): Result<Unit> {
        return try {
            val apiUsers = apiService.getUsers()
            userDao.insertAll(apiUsers.map { it.toEntity() })
            Result.success(Unit)
        } catch (e: IOException) {
            // Network error - keep using cached data
            Result.failure(e)
        }
    }
}
```

---

## Dependency Injection with Hilt

### Module Setup

**Application Class**:
```kotlin
@HiltAndroidApp
class MyApplication : Application()
```

**Network Module**:
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideUserApiService(retrofit: Retrofit): UserApiService {
        return retrofit.create(UserApiService::class.java)
    }
}
```

**Database Module**:
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}
```

---

## ML Integration Architecture

### TensorFlow Lite Integration

**ML Repository**:
```kotlin
class ImageClassificationRepository @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private var model: ImageClassifier? = null

    fun initialize() {
        model = ImageClassifier.newInstance(context)
    }

    fun classify(bitmap: Bitmap): List<Classification> {
        val model = this.model ?: throw IllegalStateException("Model not initialized")

        val inputFeature = TensorBuffer.createFixedSize(
            intArrayOf(1, 224, 224, 3),
            DataType.FLOAT32
        )

        // Preprocess bitmap
        val resizedBitmap = Bitmap.createScaledBitmap(bitmap, 224, 224, true)
        inputFeature.loadBuffer(preprocessBitmap(resizedBitmap))

        val outputs = model.process(inputFeature)
        return outputs.outputFeatureAsCategoryList
            .sortedByDescending { it.score }
            .take(5)
    }

    fun close() {
        model?.close()
        model = null
    }
}
```

**ViewModel with ML**:
```kotlin
@HiltViewModel
class ImageClassifierViewModel @Inject constructor(
    private val mlRepository: ImageClassificationRepository
) : ViewModel() {

    init {
        mlRepository.initialize()
    }

    fun classifyImage(bitmap: Bitmap) {
        viewModelScope.launch {
            try {
                val results = mlRepository.classify(bitmap)
                _classificationResults.value = results
            } catch (e: Exception) {
                _error.value = e.message
            }
        }
    }

    override fun onCleared() {
        mlRepository.close()
        super.onCleared()
    }
}
```

---

## Testing Strategy

### Unit Testing ViewModels

```kotlin
@ExperimentalCoroutinesTest
class UserListViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var viewModel: UserListViewModel
    private lateinit var fakeRepository: FakeUserRepository

    @Before
    fun setup() {
        fakeRepository = FakeUserRepository()
        viewModel = UserListViewModel(fakeRepository)
    }

    @Test
    fun `initial state is loading`() = runTest {
        val state = viewModel.uiState.value
        assertTrue(state is UserListUiState.Loading)
    }

    @Test
    fun `loadUsers emits success state with users`() = runTest {
        // Given
        val expectedUsers = listOf(
            User(1, "John", "john@example.com", ""),
            User(2, "Jane", "jane@example.com", "")
        )
        fakeRepository.setUsers(expectedUsers)

        // When
        viewModel.loadUsers()
        advanceUntilIdle()

        // Then
        val state = viewModel.uiState.value
        assertTrue(state is UserListUiState.Success)
        assertEquals(expectedUsers, (state as UserListUiState.Success).users)
    }
}
```

### Compose UI Testing

```kotlin
class UserListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun loading_state_shows_progress_indicator() {
        composeTestRule.setContent {
            UserListContent(
                uiState = UserListUiState.Loading,
                onRefresh = {}
            )
        }

        composeTestRule.onNode(hasProgressBar()).assertIsDisplayed()
    }

    @Test
    fun success_state_shows_user_list() {
        val users = listOf(
            User(1, "John Doe", "john@example.com", "")
        )

        composeTestRule.setContent {
            UserListContent(
                uiState = UserListUiState.Success(users),
                onRefresh = {}
            )
        }

        composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
        composeTestRule.onNodeWithText("john@example.com").assertIsDisplayed()
    }
}
```

---

## Anti-Patterns to Avoid

### ❌ God ViewModel
```kotlin
// BAD: One ViewModel doing everything
class AppViewModel : ViewModel() {
    val users = MutableStateFlow<List<User>>(emptyList())
    val products = MutableStateFlow<List<Product>>(emptyList())
    val orders = MutableStateFlow<List<Order>>(emptyList())
    // ... 20 more states
}
```

✅ **Solution**: One ViewModel per screen/feature

### ❌ Direct API Calls from ViewModel
```kotlin
// BAD: ViewModel depends on Retrofit service directly
class UserViewModel(private val apiService: UserApiService) : ViewModel()
```

✅ **Solution**: Always use Repository pattern

### ❌ Business Logic in Composables
```kotlin
// BAD: Complex logic in UI
@Composable
fun UserScreen() {
    val users = remember { mutableStateOf<List<User>>(emptyList()) }
    LaunchedEffect(Unit) {
        val response = apiService.getUsers()
        users.value = response.filter { it.isActive }.sortedBy { it.name }
    }
}
```

✅ **Solution**: Move logic to ViewModel/Repository

### ❌ Ignoring Lifecycle
```kotlin
// BAD: Launching coroutine without lifecycle awareness
GlobalScope.launch {
    // This outlives the Activity!
}
```

✅ **Solution**: Use `viewModelScope` or `lifecycleScope`

---

## Code Structure Templates

### Recommended Project Structure
```
app/
├── data/
│   ├── local/
│   │   ├── dao/
│   │   │   └── UserDao.kt
│   │   ├── entity/
│   │   │   └── UserEntity.kt
│   │   └── AppDatabase.kt
│   ├── remote/
│   │   ├── api/
│   │   │   └── UserApiService.kt
│   │   └── dto/
│   │       └── UserDto.kt
│   └── repository/
│       └── UserRepositoryImpl.kt
├── domain/
│   ├── model/
│   │   └── User.kt
│   ├── repository/
│   │   └── UserRepository.kt (interface)
│   └── usecase/
│       └── GetUserByIdUseCase.kt
├── presentation/
│   ├── userlist/
│   │   ├── UserListScreen.kt
│   │   ├── UserListViewModel.kt
│   │   └── UserListUiState.kt
│   └── userdetail/
│       ├── UserDetailScreen.kt
│       └── UserDetailViewModel.kt
└── di/
    ├── NetworkModule.kt
    └── DatabaseModule.kt
```

---

## Summary: Architecture Recommendations

**For Most Apps (80% of cases)**:
- **Pattern**: MVVM + Repository + Hilt
- **Layers**: UI (Compose) → ViewModel → Repository → Data Sources
- **State**: StateFlow with sealed UI state classes
- **DI**: Hilt for all dependencies
- **Testing**: Unit test ViewModels, UI test critical flows

**For Complex Apps (15% of cases)**:
- Add: Clean Architecture (Use Cases in Domain layer)
- Add: MVI pattern for complex state
- Add: Modularization (feature modules)

**For Simple Apps (5% of cases)**:
- Simplified MVVM (ViewModel + Repository, skip Use Cases)
- Still use Hilt and StateFlow

**Key Principle**: Start simple (MVVM + Repository), add complexity only when needed.

---

**Document Status**: Production-ready architecture guide for android-architect agent
**Last Updated**: 2025-10-18
**Maintained By**: A-C-Gee Architect
