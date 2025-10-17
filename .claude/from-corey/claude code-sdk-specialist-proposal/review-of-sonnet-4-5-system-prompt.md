A Guide to Building Long-Horizon Agentic Systems
(Synthesized from the Leaked Claude System Architecture)

This guide translates the observed principles into an actionable blueprint for designing agents that can perform complex, multi-step tasks over extended periods without losing state or coherence.

The core insight is that sustained autonomy is not achieved by a single, clever prompt. It's an emergent property of a holistic system comprising the Model, the Orchestrator, a Sandboxed Environment, and a well-defined set of Tools and Protocols.

Part 1: The Foundation - State and Artifact Management
This is the most critical component for overcoming the limitations of context windows and inherent model statelessness. The agent must have a reliable external memory and a structured way to interact with it.

Principle 1: Durable, Granular Artifacts

What it is: Forcing the model to externalize any significant output (code, text, data) into a discrete, manageable file or "artifact." The prompt enforces strict rules: one artifact per response, with clear size limits (~20 lines or 1500 chars).

Why it works: This converts the model's ephemeral generation into a persistent, append-only file system. It prevents context window truncation from "losing" code and creates a tangible project structure that can be reviewed, versioned, and tested programmatically.

Implementation Guide:

Create an emit_artifact(filename: str, content: str) tool.

In your system prompt, add a hard constraint: "For any code block, configuration, or text exceeding 20 lines, you MUST use the emit_artifact tool. You may only call this tool once per turn. All code must be written to artifacts before execution."

Principle 2: Explicit Iterative Workflow (Update vs. Rewrite)

What it is: The system defines two distinct modes for changing an artifact: minor patching (update) and full replacement (rewrite). The prompt provides clear heuristics for when to use each (e.g., update for diffs under 20 lines in less than 5 locations).

Why it works: This mimics a professional developer's workflow (a small commit vs. a major refactor). It dramatically reduces the risk of the model accidentally destroying a large, working file when asked to make a small change. It conserves tokens and processing time.

Implementation Guide:

Provide two distinct tools: update_artifact(filename: str, diffs: list[dict]) and rewrite_artifact(filename: str, new_content: str).

System Prompt Instruction: "To modify an existing artifact, first state your intention. For minor changes, use update_artifact. For major structural changes or refactoring, use rewrite_artifact. Do not generate the entire file content if you only need to change a few lines."

Principle 3: Uncompromising State Persistence

What it is: The full conversational history and the current state of all artifacts (e.g., a file tree or a manifest) are sent with every single API call.

Why it works: The LLM is fundamentally stateless. This technique makes it stateful from the user's perspective. It ensures the model has perfect, up-to-the-moment context of the entire project, preventing state drift and "forgetting" what it has already built.

Implementation Guide:

Your orchestrator (the code wrapping the LLM API calls) must be responsible for maintaining a project_state.json.

Before each call to the model, serialize this state and prepend it to the user's prompt, e.g., "<project_state>\n{...file tree and status...}\n</project_state>".

Part 2: The Logic - Planning, Research, and Execution
This layer governs the agent's cognitive cycle, moving it from a reactive respondent to a proactive problem-solver.

Principle 4: Deliberation-Action Split

What it is: The agent is forced to separate "thinking" from "doing." It must first output a plan (deliberation) which is then approved (by the user or an automated check) before it generates the code or tool calls to execute that plan (action).

Why it works: This prevents the model from rushing into half-baked solutions. It makes the agent's behavior auditable, steerable, and far less prone to catastrophic errors.

Implementation Guide:

Enforce a two-stage response protocol, perhaps using XML tags.

Stage 1 Prompt: "First, think. In a <plan> tag, describe your goal, the steps you will take, and the tools you will use. Stop after the plan."

Your orchestrator parses the <plan>, approves it, and then sends a new call.

Stage 2 Prompt: "Your plan has been approved. Now, execute the steps you outlined."

Principle 5: Governed Tool Use and Research Cadence

What it is: The agent is explicitly told not to guess. When faced with uncertainty (e.g., an unfamiliar API, a design pattern choice), it must use a research tool. The prompt defines a structured loop: plan -> research -> synthesize -> answer.

Why it works: This grounds the model's outputs in factual, up-to-date information, drastically reducing API or method hallucinations. It mimics how a human expert works: they look things up.

Implementation Guide:

Provide a robust web_search(query: str) tool.

System Prompt Instruction: "If you are uncertain about any technical detail, library, or best practice, you MUST use the web_search tool to investigate before proceeding. Do not invent answers. State your research findings before using them in your plan."

Principle 6: Long-Horizon Autonomy via Planning/Feedback Loops

What it is: The system prompt explicitly references proven agent architectures like Voyager (propose -> execute -> learn) and Generative Agents (memory -> reflect -> plan).

Why it works: By framing the task in terms of these known successful patterns, the model is guided to adopt a cyclical process of self-correction and reflection, which is the key to sustained progress over dozens or hundreds of steps.

Implementation Guide:

Structure your master prompt around a core loop: "Your objective is to build a Slack clone. You will operate in a continuous loop: 1. Observe: Review the current project state. 2. Reflect: Analyze the results and errors from your last action. 3. Plan: Formulate a detailed plan for the next logical feature. 4. Execute: Carry out the plan by writing to artifacts."

Part 3: The Sandbox - Environment and Resilience
This layer defines the "rules of physics" for the agent's world, ensuring its actions are safe, predictable, and productive.

Principle 7: Enforce Strict Runtime and Dependency Constraints

What it is: The prompt whitelists exactly what the agent can do in its execution environment (e.g., single-file HTML, React from specific CDNs, no localStorage).

Why it works: This creates a "padded room" for the agent. It prevents it from writing code that the sandbox can't run, or using unstable patterns that could break the long-running session. It drastically simplifies the problem space for the model.

Implementation Guide:

In the system prompt, be explicit about the environment: "Your execution environment is a sandboxed browser iframe. You may only use React and ReactDOM loaded from the Skypack CDN. All code must be self-contained in a single HTML file. localStorage and sessionStorage are disabled. All state must be managed in memory."

Principle 8: Bake-in Error Rituals and Guardrails

What it is: The agent is given a specific protocol for handling errors, rather than just retrying. It must analyze the error, form a hypothesis, and propose a specific fix. This also includes "Ghost Context Removal" (cleaning stale or incorrect assumptions).

Why it works: This transforms errors from dead-ends into learning opportunities. The agent becomes more robust over time by building a "mental model" of what causes failures.

Implementation Guide:

System Prompt Instruction: "If you encounter an error during execution: 1. Stop immediately. 2. Analyze the full error traceback. 3. Re-read the code in the artifact that caused the error. 4. In your next response, provide a <diagnosis> of the cause and a <fix> with the specific code change. Do not retry without this process."

Principle 9: Enable "Claude-in-Claude" Self-Orchestration

What it is: The most advanced concept. The agent's generated artifacts are allowed to call an LLM API themselves (via a provided fetch wrapper).

Why it works: This is a recursive form of intelligence amplification. The agent can build tools for itself. For example, it could build a component that uses an LLM to generate placeholder text, or a dev tool that helps it refactor its own code.

Implementation Guide:

In your execution sandbox, provide a global function: async function call_llm(prompt).

System Prompt Instruction: "You have access to an LLM via the call_llm(prompt) function from within your generated artifacts. You can use this to build intelligent features into the application itself or to create helper tools for your development process."

Conclusion: From Prompt to System
The key takeaway is that achieving complex, long-horizon autonomy is an architectural challenge, not just a prompting one. By implementing these principles, you are building a complete system where the LLM is the intelligent core, but its power is harnessed and disciplined by a robust framework of state management, planning loops, and environmental guardrails. This is the "phase change" you're experiencing—the shift from conversational AI to agentic AI.