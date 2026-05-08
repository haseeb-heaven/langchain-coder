"""
miniSWE Agent — Industry-Standard Multi-Language Software Engineering Agent
=============================================================================
Full software development cycle: Plan → Code → Review → Test → Execute → Report
Supports: Python, JavaScript/TypeScript, Go, Rust, Java, C++, C, Ruby, Shell, PHP
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, TypedDict

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from litellm import completion
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.theme import Theme

# ─────────────────────────────────────────────
# Console & Logging
# ─────────────────────────────────────────────

THEME = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "phase.plan": "bold magenta",
        "phase.code": "bold cyan",
        "phase.review": "bold blue",
        "phase.test": "bold orange3",
        "phase.exec": "bold green",
        "muted": "dim white",
        "label": "bold white",
    }
)

console = Console(theme=THEME, highlight=True)


def setup_logging(log_file: str) -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    if root.hasHandlers():
        root.handlers.clear()

    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

    ch = RichHandler(console=console, show_time=False, show_path=False, markup=True)
    ch.setLevel(logging.INFO)

    root.addHandler(fh)
    root.addHandler(ch)

    for noisy in ("LiteLLM", "httpcore", "httpx", "asyncio", "urllib3"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


# ─────────────────────────────────────────────
# Language Registry
# ─────────────────────────────────────────────

@dataclass
class LanguageSpec:
    name: str
    extensions: list[str]
    file_name: str          # default output filename
    test_file_name: str     # default test filename
    run_cmd: list[str]      # command to run the main file
    test_cmd: list[str]     # command to run tests
    compile_cmd: Optional[list[str]] = None   # compile step if needed
    checker: str = ""       # binary to check availability
    test_framework: str = ""


LANGUAGE_REGISTRY: dict[str, LanguageSpec] = {
    "python": LanguageSpec(
        name="Python",
        extensions=[".py"],
        file_name="generated_code.py",
        test_file_name="test_generated_code.py",
        run_cmd=[sys.executable, "{file}"],
        test_cmd=[sys.executable, "-m", "pytest", "{test_file}", "-v", "--tb=short"],
        checker=sys.executable,
        test_framework="pytest",
    ),
    "javascript": LanguageSpec(
        name="JavaScript",
        extensions=[".js", ".mjs"],
        file_name="generated_code.js",
        test_file_name="generated_code.test.js",
        run_cmd=["node", "{file}"],
        test_cmd=["npx", "jest", "{test_file}", "--no-coverage"],
        checker="node",
        test_framework="jest",
    ),
    "typescript": LanguageSpec(
        name="TypeScript",
        extensions=[".ts"],
        file_name="generated_code.ts",
        test_file_name="generated_code.test.ts",
        run_cmd=["npx", "ts-node", "{file}"],
        test_cmd=["npx", "jest", "{test_file}", "--no-coverage"],
        checker="node",
        test_framework="jest",
    ),
    "go": LanguageSpec(
        name="Go",
        extensions=[".go"],
        file_name="generated_code.go",
        test_file_name="generated_code_test.go",
        run_cmd=["go", "run", "{file}"],
        test_cmd=["go", "test", "-v", "./..."],
        checker="go",
        test_framework="go test",
    ),
    "rust": LanguageSpec(
        name="Rust",
        extensions=[".rs"],
        file_name="src/main.rs",
        test_file_name="src/main.rs",   # tests embedded in Rust
        run_cmd=["cargo", "run"],
        test_cmd=["cargo", "test", "--", "--nocapture"],
        checker="cargo",
        test_framework="cargo test",
    ),
    "java": LanguageSpec(
        name="Java",
        extensions=[".java"],
        file_name="GeneratedCode.java",
        test_file_name="GeneratedCodeTest.java",
        run_cmd=["java", "GeneratedCode"],
        compile_cmd=["javac", "{file}"],
        test_cmd=["java", "-cp", ".:junit-platform-console-standalone.jar", "org.junit.platform.console.ConsoleLauncher", "--scan-class-path"],
        checker="java",
        test_framework="junit",
    ),
    "cpp": LanguageSpec(
        name="C++",
        extensions=[".cpp", ".cc"],
        file_name="generated_code.cpp",
        test_file_name="test_generated_code.cpp",
        run_cmd=["./generated_code"],
        compile_cmd=["g++", "-std=c++17", "-o", "generated_code", "{file}"],
        test_cmd=["./test_generated_code"],
        checker="g++",
        test_framework="catch2",
    ),
    "c": LanguageSpec(
        name="C",
        extensions=[".c"],
        file_name="generated_code.c",
        test_file_name="test_generated_code.c",
        run_cmd=["./generated_code"],
        compile_cmd=["gcc", "-o", "generated_code", "{file}"],
        test_cmd=["./test_generated_code"],
        checker="gcc",
        test_framework="unity",
    ),
    "ruby": LanguageSpec(
        name="Ruby",
        extensions=[".rb"],
        file_name="generated_code.rb",
        test_file_name="test_generated_code_spec.rb",
        run_cmd=["ruby", "{file}"],
        test_cmd=["rspec", "{test_file}"],
        checker="ruby",
        test_framework="rspec",
    ),
    "shell": LanguageSpec(
        name="Shell",
        extensions=[".sh"],
        file_name="generated_code.sh",
        test_file_name="test_generated_code.sh",
        run_cmd=["bash", "{file}"],
        test_cmd=["bash", "{test_file}"],
        checker="bash",
        test_framework="bats",
    ),
    "php": LanguageSpec(
        name="PHP",
        extensions=[".php"],
        file_name="generated_code.php",
        test_file_name="test_generated_code.php",
        run_cmd=["php", "{file}"],
        test_cmd=["./vendor/bin/phpunit", "{test_file}"],
        checker="php",
        test_framework="phpunit",
    ),
}


def detect_language(requirement: str, hint: str = "") -> str:
    """Detect target language from requirement text or explicit hint."""
    text = (requirement + " " + hint).lower()

    patterns = {
        "typescript": [r"\btypescript\b", r"\b\.tsx?\b", r"\bts\b"],
        "javascript": [r"\bjavascript\b", r"\bjs\b", r"\bnode\.?js\b", r"\bnpm\b", r"\bdeno\b"],
        "go": [r"\bgolang\b", r"\bgo\b(?!\s+ahead)"],
        "rust": [r"\brust\b", r"\bcargo\b"],
        "java": [r"\bjava\b(?!script)", r"\bspring\b", r"\bmaven\b", r"\bgradle\b"],
        "cpp": [r"\bc\+\+\b", r"\bcpp\b"],
        "c": [r"\blanguage c\b", r"\bwrite in c\b", r"\bin c\b"],
        "ruby": [r"\bruby\b", r"\brails\b", r"\bgemfile\b"],
        "shell": [r"\bbash\b", r"\bshell script\b", r"\bsh script\b"],
        "php": [r"\bphp\b", r"\blaravel\b", r"\bwordpress\b"],
        "python": [r"\bpython\b", r"\bpip\b", r"\bdjango\b", r"\bflask\b", r"\bfastapi\b"],
    }

    for lang, pats in patterns.items():
        for pat in pats:
            if re.search(pat, text):
                return lang

    return "python"  # Default


def check_language_runtime(spec: LanguageSpec) -> bool:
    """Verify the language runtime is available on this system."""
    return bool(shutil.which(spec.checker)) if spec.checker else False


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

@dataclass
class Config:
    model_fleet: list[tuple[str, str]] = field(default_factory=list)
    max_iterations: int = 5
    timeout: int = 60
    log_file: str = "miniswe.log"
    output_dir: str = "output"
    language_hint: str = ""


def load_config() -> Config:
    load_dotenv()

    fleet: list[tuple[str, str]] = []
    primary_model = os.getenv("LLM_MODEL")
    primary_key = os.getenv("GROQ_API_KEY") or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")

    if primary_model and primary_key:
        fleet.append((primary_model, primary_key))

    for i in range(1, 6):
        m = os.getenv(f"LLM_FALLBACK_MODEL{i}" if i > 1 else "LLM_FALLBACK_MODEL")
        k = os.getenv(f"LLM_API_KEY{i}" if i > 1 else "LLM_API_KEY") or primary_key
        if m and k:
            fleet.append((m, k))

    if not fleet:
        raise ValueError(
            "No LLM model configured. Set LLM_MODEL and one of: GROQ_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY in .env"
        )

    return Config(
        model_fleet=fleet,
        max_iterations=int(os.getenv("MAX_ITERATIONS", "5")),
        timeout=int(os.getenv("EXEC_TIMEOUT", "60")),
        output_dir=os.getenv("OUTPUT_DIR", "output"),
        language_hint=os.getenv("LANGUAGE_HINT", ""),
    )


# ─────────────────────────────────────────────
# Agent State
# ─────────────────────────────────────────────

class AgentState(TypedDict):
    requirement: str
    language: str                    # detected/selected language
    plan: str                        # architect's plan
    code: str                        # generated code
    tests: str                       # generated tests
    review_feedback: str             # reviewer feedback
    test_results: str                # raw test output
    exec_results: str                # raw execution output
    iterations: int
    review_passed: bool
    tests_passed: bool
    exec_passed: bool
    success: bool
    errors: list[str]
    artifacts: list[str]             # paths of saved files


# ─────────────────────────────────────────────
# LLM Client
# ─────────────────────────────────────────────

class LLMClient:
    """Robust LLM client with model fleet failover and exponential backoff."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = logging.getLogger("LLM")
        self._fleet_index = 0

    @property
    def current_model(self) -> str:
        return self.config.model_fleet[self._fleet_index][0]

    def _set_api_key(self) -> None:
        _, key = self.config.model_fleet[self._fleet_index]
        os.environ["GROQ_API_KEY"] = key
        os.environ["OPENAI_API_KEY"] = key
        os.environ["ANTHROPIC_API_KEY"] = key

    def complete(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 8192,
        json_mode: bool = False,
    ) -> str:
        max_retries = self.config.max_iterations + 2
        backoff = 2.0

        for attempt in range(max_retries):
            self._set_api_key()
            model = self.current_model
            try:
                self.logger.debug(f"LLM call | model={model} | attempt={attempt + 1}")
                kwargs: dict = dict(
                    model=model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.config.timeout,
                )
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                response = completion(**kwargs)
                content: str = response.choices[0].message.content.strip()
                return self._clean(content)

            except Exception as exc:
                msg = str(exc).lower()
                is_rate_limit = "rate limit" in msg or "429" in msg or "quota" in msg

                if is_rate_limit:
                    wait = backoff * (2**attempt)
                    self.logger.warning(f"Rate-limited on {model}. Waiting {wait:.1f}s …")
                    time.sleep(wait)

                    if attempt >= 1 and len(self.config.model_fleet) > 1:
                        self._fleet_index = (self._fleet_index + 1) % len(self.config.model_fleet)
                        self.logger.warning(f"Switching to fallback model: {self.current_model}")
                else:
                    self.logger.error(f"LLM error ({model}): {exc}")
                    raise RuntimeError(f"LLM call failed: {exc}") from exc

        raise RuntimeError("All models in fleet exhausted or max retries reached.")

    @staticmethod
    def _clean(text: str) -> str:
        """Strip markdown code fences from LLM output."""
        # Try to extract fenced block
        fence_match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
        if fence_match:
            return fence_match.group(1).strip()
        # Remove trailing/leading backtick fences
        text = re.sub(r"^```\w*\n?", "", text.strip())
        text = re.sub(r"\n?```$", "", text.strip())
        return text.strip()


# ─────────────────────────────────────────────
# Agents
# ─────────────────────────────────────────────

class BaseAgent:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.llm = LLMClient(config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def _run_cmd(
        self,
        cmd: list[str],
        *,
        cwd: Optional[str] = None,
        stdin_data: Optional[str] = None,
    ) -> subprocess.CompletedProcess:
        """Shared helper to run shell commands safely."""
        try:
            return subprocess.run(
                cmd,
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                cwd=cwd,
            )
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="Process timed out.")
        except Exception as exc:
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr=str(exc))


class LanguageDetectorAgent(BaseAgent):
    """Detects the target programming language from the requirement."""

    def run(self, state: AgentState) -> dict:
        self.logger.info("[phase.plan]Phase 0 · Language Detection[/phase.plan]")

        hint = self.config.language_hint
        lang = detect_language(state["requirement"], hint)
        spec = LANGUAGE_REGISTRY[lang]

        if not check_language_runtime(spec):
            self.logger.warning(
                f"Runtime for {spec.name} not found on PATH. Defaulting to Python."
            )
            lang = "python"
            spec = LANGUAGE_REGISTRY[lang]

        console.print(
            Panel(
                f"[bold]Language:[/bold] {spec.name}\n"
                f"[bold]Test Framework:[/bold] {spec.test_framework}\n"
                f"[bold]Runtime available:[/bold] {'✓' if check_language_runtime(spec) else '✗'}",
                title="[phase.plan]Language Detection[/phase.plan]",
                border_style="magenta",
            )
        )

        return {"language": lang, "errors": []}


class ArchitectAgent(BaseAgent):
    """Creates a detailed technical plan before writing any code."""

    def run(self, state: AgentState) -> dict:
        iteration = state.get("iterations", 0)
        self.logger.info(f"[phase.plan]Phase 1 · Architecture (iteration {iteration + 1})[/phase.plan]")

        spec = LANGUAGE_REGISTRY[state["language"]]

        context = f"Requirement:\n{state['requirement']}\n\nTarget Language: {spec.name}"
        if state.get("review_feedback") and not state.get("review_passed"):
            context += f"\n\nPrevious Review Feedback:\n{state['review_feedback']}"
        if state.get("test_results") and not state.get("tests_passed"):
            context += f"\n\nPrevious Test Failures:\n{state['test_results']}"
        if state.get("exec_results") and not state.get("exec_passed"):
            context += f"\n\nPrevious Execution Errors:\n{state['exec_results']}"

        system = (
            "You are a Principal Software Architect with 20+ years of experience. "
            "Produce a precise, structured technical plan in the following format:\n\n"
            "## Problem Analysis\n"
            "## Architecture Design\n"
            "## Data Structures & Algorithms\n"
            "## Edge Cases & Error Handling\n"
            "## Implementation Steps\n"
            "## Testing Strategy\n\n"
            "Be concise but thorough. Focus on correctness, efficiency, and maintainability."
        )

        plan = self.llm.complete(system, context, temperature=0.1, max_tokens=2048)

        console.print(
            Panel(
                plan,
                title=f"[phase.plan]Architect Plan (iteration {iteration + 1})[/phase.plan]",
                border_style="magenta",
            )
        )

        return {"plan": plan}


class CoderAgent(BaseAgent):
    """Generates production-quality code from the architect's plan."""

    def run(self, state: AgentState) -> dict:
        iteration = state.get("iterations", 0)
        self.logger.info(f"[phase.code]Phase 2 · Code Generation (iteration {iteration + 1})[/phase.code]")

        spec = LANGUAGE_REGISTRY[state["language"]]

        user_prompt = (
            f"Requirement:\n{state['requirement']}\n\n"
            f"Architecture Plan:\n{state['plan']}\n\n"
        )

        if state.get("code") and iteration > 0:
            user_prompt += f"Previous Code (needs fixing):\n{state['code']}\n\n"
        if state.get("review_feedback") and not state.get("review_passed"):
            user_prompt += f"Review Feedback to Address:\n{state['review_feedback']}\n\n"
        if state.get("test_results") and not state.get("tests_passed"):
            user_prompt += f"Test Failures to Fix:\n{state['test_results']}\n\n"
        if state.get("exec_results") and not state.get("exec_passed"):
            user_prompt += f"Runtime Errors to Fix:\n{state['exec_results']}\n\n"

        user_prompt += (
            "Write the complete, production-ready implementation. "
            "Output ONLY raw source code with no markdown fences, no explanations."
        )

        system = (
            f"You are a senior {spec.name} engineer writing production-grade code. "
            "Rules:\n"
            "1. Output ONLY raw source code — no markdown, no explanations, no comments like 'here is the code'.\n"
            "2. Code must be complete and runnable as-is.\n"
            "3. Include comprehensive inline documentation (docstrings/comments).\n"
            "4. Handle all error cases explicitly — no silent failures.\n"
            "5. Use idiomatic patterns and best practices for the language.\n"
            "6. Include a main entry point / example usage at the bottom.\n"
            f"7. The test framework used will be: {spec.test_framework}."
        )

        code = self.llm.complete(system, user_prompt, temperature=0.15, max_tokens=8192)

        if not code or len(code) < 10:
            raise RuntimeError("Coder returned empty or trivial output.")

        # Display with syntax highlighting
        syntax = Syntax(code[:3000], state["language"], theme="monokai", line_numbers=True)
        console.print(
            Panel(
                syntax,
                title=f"[phase.code]Generated Code · {spec.name} (iteration {iteration + 1})[/phase.code]",
                border_style="cyan",
            )
        )

        return {
            "code": code,
            "iterations": iteration + 1,
            "review_passed": False,
            "tests_passed": False,
            "exec_passed": False,
        }


class ReviewerAgent(BaseAgent):
    """Senior code review with Shadow Execution: Static Analysis + Dynamic Sanity Check."""

    PASS_SIGNAL = "APPROVED"

    def run(self, state: AgentState) -> dict:
        self.logger.info("[phase.review]Phase 3 · Code Review & Shadow Execution[/phase.review]")
        spec = LANGUAGE_REGISTRY[state["language"]]

        # ── Step 1: Static Analysis ───────────────────────────────────────
        system = (
            f"You are a Principal {spec.name} Engineer conducting a rigorous code review.\n"
            f"Respond with exactly '{self.PASS_SIGNAL}' if the code is perfect. "
            "Otherwise, provide a brutal, detailed critique."
        )
        user = f"Requirement:\n{state['requirement']}\n\nCode:\n{state['code']}"
        static_feedback = self.llm.complete(system, user, temperature=0.1)

        if not static_feedback.strip().startswith(self.PASS_SIGNAL):
            return self._format_review(static_feedback, False)

        # ── Step 2: Shadow Execution (Dynamic Sanity Check) ──────────────
        self.logger.info("[phase.review]Running Shadow Sanity Check...[/phase.review]")
        sanity_test_sys = (
            f"You are a Senior QA Automation Engineer. Generate a SINGLE {spec.test_framework} "
            "test file that checks the most complex edge case of the requirement. "
            "Output ONLY raw code. No markdown."
        )
        sanity_test_user = f"Requirement:\n{state['requirement']}\nCode:\n{state['code']}"
        sanity_test_code = self.llm.complete(sanity_test_sys, sanity_test_user, temperature=0.1)

        # Write and Execute
        out_dir = Path(self.config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        temp_code = out_dir / spec.file_name
        temp_test = out_dir / f"shadow_sanity_{spec.test_file_name}"
        temp_code.write_text(state["code"], encoding="utf-8")
        temp_test.write_text(sanity_test_code, encoding="utf-8")

        # Resolve command (use basename since we use cwd)
        test_cmd = [c.replace("{file}", spec.file_name).replace("{test_file}", temp_test.name) for c in spec.run_cmd if "{file}" in c]
        # If no specific run command for test, try test_cmd
        if not test_cmd:
            test_cmd = [c.replace("{file}", spec.file_name).replace("{test_file}", temp_test.name) for c in spec.test_cmd]

        result = self._run_cmd(test_cmd, cwd=str(out_dir))

        if result.returncode != 0:
            err_msg = (result.stderr or result.stdout).strip()
            self.logger.warning(f"Shadow Execution failed:\n{err_msg}")
            feedback = f"✗ SHADOW EXECUTION FAILED\n\nThe code looks okay but failed a dynamic sanity check:\n\n{err_msg}"
            return self._format_review(feedback, False)

        return self._format_review(f"✓ {self.PASS_SIGNAL} (Static + Dynamic checks passed)", True)

    def _format_review(self, feedback: str, passed: bool) -> dict:
        status = "[success]✓ APPROVED[/success]" if passed else "[error]✗ CHANGES REQUIRED[/error]"
        console.print(Panel(f"{status}\n\n{feedback}", title="[phase.review]Code Review[/phase.review]", border_style="blue"))
        return {"review_feedback": feedback, "review_passed": passed}


class TestGeneratorAgent(BaseAgent):
    """Generates a comprehensive, stable test suite (generated once, reused across iterations)."""

    def run(self, state: AgentState) -> dict:
        # Tests are generated once and reused for consistency
        if state.get("tests"):
            self.logger.info("[phase.test]Reusing existing test suite (stable reference).[/phase.test]")
            return {}

        self.logger.info("[phase.test]Phase 4 · Test Generation[/phase.test]")
        spec = LANGUAGE_REGISTRY[state["language"]]

        system = (
            f"You are a Senior QA Engineer specializing in {spec.name}.\n"
            f"Generate a comprehensive test suite using {spec.test_framework}.\n"
            "Rules:\n"
            "1. Output ONLY raw test code — no markdown, no explanations.\n"
            "2. Tests must be INDEPENDENT of implementation details (black-box).\n"
            "3. Cover: happy paths, edge cases, boundary values, error conditions.\n"
            "4. Each test must be isolated and idempotent.\n"
            f"5. Import/reference the main module from '{spec.file_name}'.\n"
            "6. Include at minimum: 5 unit tests, 2 integration tests, 2 edge case tests."
        )

        user = (
            f"Requirement:\n{state['requirement']}\n\n"
            f"Generate the full {spec.test_framework} test suite."
        )

        tests = self.llm.complete(system, user, temperature=0.1, max_tokens=4096)

        syntax = Syntax(tests[:2000], state["language"], theme="monokai", line_numbers=True)
        console.print(
            Panel(syntax, title="[phase.test]Generated Test Suite[/phase.test]", border_style="orange3")
        )

        return {"tests": tests}


class ExecutorAgent(BaseAgent):
    """Executes code and tests, captures all output."""

    def run(self, state: AgentState) -> dict:
        self.logger.info("[phase.exec]Phase 5 · Execution & Testing[/phase.exec]")
        spec = LANGUAGE_REGISTRY[state["language"]]

        output_dir = Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        code_path = output_dir / spec.file_name
        test_path = output_dir / spec.test_file_name
        code_path.parent.mkdir(parents=True, exist_ok=True)

        # Write files
        code_path.write_text(state["code"], encoding="utf-8")
        if state.get("tests"):
            test_path.write_text(state["tests"], encoding="utf-8")

        artifacts = [str(code_path), str(test_path)]

        # ── Step 1: Compile (if needed) ──────────────────────────────────
        if spec.compile_cmd:
            cmd = [c.replace("{file}", spec.file_name) for c in spec.compile_cmd]
            self.logger.info(f"[phase.exec]Compiling: {' '.join(cmd)}[/phase.exec]")
            result = self._run_cmd(cmd, cwd=str(output_dir))
            if result.returncode != 0:
                err = result.stderr or result.stdout
                self.logger.warning(f"Compilation failed:\n{err}")
                return self._fail_state(
                    exec_results=err,
                    feedback=f"Compilation failed:\n{err}",
                    artifacts=artifacts,
                )

        # ── Step 2: Run standalone ────────────────────────────────────────
        run_cmd = self._resolve_cmd(spec.run_cmd, spec.file_name, spec.test_file_name)
        self.logger.info(f"[phase.exec]Running: {' '.join(run_cmd)}[/phase.exec]")

        mock_input = self._generate_mock_input(state["code"], state["language"])
        run_result = self._run_cmd(run_cmd, cwd=str(output_dir), stdin_data=mock_input)

        exec_output = (run_result.stdout + run_result.stderr).strip()
        exec_passed = run_result.returncode == 0

        if not exec_passed:
            self.logger.warning(f"Standalone execution failed:\n{exec_output}")
            return self._fail_state(
                exec_results=exec_output,
                feedback=f"Standalone execution failed (rc={run_result.returncode}):\n{exec_output}",
                artifacts=artifacts,
            )

        console.print(
            Panel(
                exec_output or "(no output)",
                title="[phase.exec]Execution Output[/phase.exec]",
                border_style="green",
            )
        )

        # ── Step 3: Run tests ─────────────────────────────────────────────
        if not state.get("tests"):
            self.logger.info("[phase.exec]No tests generated — skipping test run.[/phase.exec]")
            return {
                "exec_results": exec_output,
                "test_results": "No tests available.",
                "exec_passed": True,
                "tests_passed": True,
                "success": True,
                "artifacts": artifacts,
            }

        test_cmd = self._resolve_cmd(spec.test_cmd, spec.file_name, spec.test_file_name)
        self.logger.info(f"[phase.exec]Testing: {' '.join(test_cmd)}[/phase.exec]")

        test_result = self._run_cmd(test_cmd, cwd=str(output_dir))
        test_output = (test_result.stdout + test_result.stderr).strip()
        tests_passed = test_result.returncode == 0

        status = "[success]✓ ALL TESTS PASSED[/success]" if tests_passed else "[error]✗ TEST FAILURES[/error]"
        console.print(
            Panel(
                f"{status}\n\n{test_output[:3000]}",
                title="[phase.test]Test Results[/phase.test]",
                border_style="green" if tests_passed else "red",
            )
        )

        if tests_passed:
            return {
                "exec_results": exec_output,
                "test_results": test_output,
                "exec_passed": True,
                "tests_passed": True,
                "success": True,
                "artifacts": artifacts,
            }
        else:
            return {
                "exec_results": exec_output,
                "test_results": test_output,
                "exec_passed": True,
                "tests_passed": False,
                "success": False,
                "artifacts": artifacts,
                "review_feedback": f"Tests failed:\n{test_output}",
            }

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _resolve_cmd(template: list[str], file: str, test_file: str) -> list[str]:
        return [c.replace("{file}", file).replace("{test_file}", test_file) for c in template]

    @staticmethod
    def _generate_mock_input(code: str, language: str) -> Optional[str]:
        """Generate basic mock stdin if the code reads from stdin."""
        if language == "python" and "input(" in code:
            return "test_input\n5\nyes\n"
        if language in ("c", "cpp") and "scanf" in code:
            return "5\n"
        if language == "ruby" and "gets" in code:
            return "test\n"
        return None

    @staticmethod
    def _fail_state(**kwargs) -> dict:
        return {"exec_passed": False, "tests_passed": False, "success": False, **kwargs}


# ─────────────────────────────────────────────
# Orchestrator & Graph
# ─────────────────────────────────────────────

class AgentOrchestrator:
    """Wires all agents into a LangGraph workflow."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.detector = LanguageDetectorAgent(config)
        self.architect = ArchitectAgent(config)
        self.coder = CoderAgent(config)
        self.reviewer = ReviewerAgent(config)
        self.test_gen = TestGeneratorAgent(config)
        self.executor = ExecutorAgent(config)
        self.logger = logging.getLogger("Orchestrator")

    # ── Node wrappers ─────────────────────────────────────────────────────

    def detect_node(self, state: AgentState) -> dict:
        return self.detector.run(state)

    def architect_node(self, state: AgentState) -> dict:
        return self.architect.run(state)

    def coder_node(self, state: AgentState) -> dict:
        return self.coder.run(state)

    def reviewer_node(self, state: AgentState) -> dict:
        return self.reviewer.run(state)

    def test_gen_node(self, state: AgentState) -> dict:
        return self.test_gen.run(state)

    def executor_node(self, state: AgentState) -> dict:
        return self.executor.run(state)

    # ── Routing ───────────────────────────────────────────────────────────

    def route_after_review(self, state: AgentState) -> Literal["coder", "test_gen"]:
        if state.get("review_passed"):
            return "test_gen"
        if state.get("iterations", 0) >= self.config.max_iterations:
            self.logger.warning("Max iterations reached. Proceeding past review anyway.")
            return "test_gen"
        return "coder"

    def route_after_executor(self, state: AgentState) -> Literal["coder", "__end__"]:
        if state.get("success"):
            return END
        if state.get("iterations", 0) >= self.config.max_iterations:
            self.logger.warning("Max iterations reached. Stopping.")
            return END
        return "architect"

    def build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)

        builder.add_node("detect", self.detect_node)
        builder.add_node("architect", self.architect_node)
        builder.add_node("coder", self.coder_node)
        builder.add_node("reviewer", self.reviewer_node)
        builder.add_node("test_gen", self.test_gen_node)
        builder.add_node("executor", self.executor_node)

        builder.add_edge(START, "detect")
        builder.add_edge("detect", "architect")
        builder.add_edge("architect", "coder")
        builder.add_edge("coder", "reviewer")
        builder.add_conditional_edges("reviewer", self.route_after_review, {"coder": "coder", "test_gen": "test_gen"})
        builder.add_edge("test_gen", "executor")
        builder.add_conditional_edges("executor", self.route_after_executor, {"architect": "architect", END: END})

        return builder


# ─────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────

def print_final_report(state: Optional[AgentState], start_time: float) -> None:
    elapsed = time.time() - start_time

    if not state:
        console.print(Panel("[error]No final state captured.[/error]", title="Report"))
        return

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold white")
    table.add_column("Value")

    spec = LANGUAGE_REGISTRY.get(state.get("language", "python"), LANGUAGE_REGISTRY["python"])

    table.add_row("Language", spec.name)
    table.add_row("Iterations", str(state.get("iterations", 0)))
    table.add_row("Duration", f"{elapsed:.1f}s")
    table.add_row("Review", "[success]PASSED[/success]" if state.get("review_passed") else "[error]FAILED[/error]")
    table.add_row("Tests", "[success]PASSED[/success]" if state.get("tests_passed") else "[error]FAILED[/error]")
    table.add_row("Execution", "[success]PASSED[/success]" if state.get("exec_passed") else "[error]FAILED[/error]")

    artifacts = state.get("artifacts", [])
    if artifacts:
        table.add_row("Artifacts", "\n".join(artifacts))

    border = "green" if state.get("success") else "red"
    title = "[success]✓ TASK COMPLETE[/success]" if state.get("success") else "[error]✗ TASK INCOMPLETE[/error]"

    console.print(Rule())
    console.print(Panel(table, title=title, border_style=border))

    if not state.get("success"):
        last_err = (
            state.get("review_feedback")
            or state.get("test_results")
            or state.get("exec_results")
            or "Unknown failure"
        )
        console.print(
            Panel(
                last_err[:1000],
                title="[error]Last Known Error[/error]",
                border_style="red",
            )
        )


# ─────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────

def run(requirement: str, config: Config) -> AgentState | None:
    """Run the full SWE cycle for a given requirement. Returns final state."""
    orchestrator = AgentOrchestrator(config)
    graph = orchestrator.build_graph()

    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)

    thread_cfg = {"configurable": {"thread_id": f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}}

    initial_state: AgentState = {
        "requirement": requirement,
        "language": "python",
        "plan": "",
        "code": "",
        "tests": "",
        "review_feedback": "",
        "test_results": "",
        "exec_results": "",
        "iterations": 0,
        "review_passed": False,
        "tests_passed": False,
        "exec_passed": False,
        "success": False,
        "errors": [],
        "artifacts": [],
    }

    final_state: Optional[AgentState] = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Running miniSWE Agent …", total=None)
        for event in app.stream(initial_state, thread_cfg):
            for _node, state_data in event.items():
                if state_data:
                    final_state = state_data  # type: ignore[assignment]
                    progress.update(task, description=f"Active node: [bold]{_node}[/bold]")

    return final_state


def main() -> None:
    try:
        cfg = load_config()
    except ValueError as exc:
        console.print(f"[error]Configuration Error:[/error] {exc}")
        sys.exit(1)

    setup_logging(cfg.log_file)
    logger = logging.getLogger("miniSWE")

    console.print(
        Panel.fit(
            "[bold cyan]miniSWE Agent[/bold cyan]  [dim]v2.0[/dim]\n"
            "[dim]Industry-Standard Multi-Language AI Software Engineer[/dim]",
            border_style="cyan",
        )
    )

    # ── Load requirement ──────────────────────────────────────────────────
    if Path("prompt.txt").exists():
        requirement = Path("prompt.txt").read_text(encoding="utf-8").strip()
        logger.info(f"Loaded requirement from prompt.txt ({len(requirement)} chars)")
    else:
        console.print("[warning]prompt.txt not found. Falling back to interactive input.[/warning]")
        requirement = console.input("\n[bold cyan]Enter your requirement:[/bold cyan] ").strip()

    if not requirement:
        logger.error("No requirement provided. Exiting.")
        sys.exit(1)

    console.print(
        Panel(requirement, title="[label]Requirement[/label]", border_style="dim")
    )

    start = time.time()
    try:
        final = run(requirement, cfg)
        print_final_report(final, start)
        sys.exit(0 if final and final.get("success") else 1)
    except KeyboardInterrupt:
        console.print("\n[warning]Interrupted by user.[/warning]")
        sys.exit(130)
    except Exception as exc:
        logger.exception(f"Unexpected crash: {exc}")
        console.print(f"\n[error]CRITICAL CRASH:[/error] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
