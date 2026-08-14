#!/usr/bin/env python3
"""Run one prompt template over a test set and collect the outputs.

Usage:
    python3 run_eval.py eval-config.json
    python3 run_eval.py eval-config.json --out results-v2.md
    python3 run_eval.py eval-config.json --repeat 3

Writes a Markdown file with one section per test case, ready for manual
scoring against your success criteria. Requires the `anthropic` package
and ANTHROPIC_API_KEY.
"""

import argparse
import json
import sys

try:
    import anthropic
except ImportError:
    sys.exit("This script needs the SDK. Run: pip install anthropic")

DEFAULT_MODEL = "claude-opus-5"
DEFAULT_MAX_TOKENS = 4000

# Built rather than written literally so this file stays safe to paste inside
# a Markdown fenced code block.
FENCE = "`" * 3


def load_config(path: str) -> dict:
    """Load and validate the eval config."""
    try:
        with open(path, encoding="utf-8") as handle:
            config = json.load(handle)
    except FileNotFoundError:
        sys.exit(f"Config file not found: {path}")
    except json.JSONDecodeError as error:
        sys.exit(f"Config file is not valid JSON: {error}")

    if "prompt_template" not in config:
        sys.exit("Config must contain 'prompt_template'.")
    if "{input}" not in config["prompt_template"]:
        sys.exit("'prompt_template' must contain the placeholder {input}.")

    cases = config.get("cases")
    if not isinstance(cases, list) or not cases:
        sys.exit("Config must contain a non-empty 'cases' list.")
    for index, case in enumerate(cases):
        if "input" not in case:
            sys.exit(f"Case at position {index} is missing an 'input' field.")

    return config


def extract_text(response) -> str:
    """Pull the text out of a response, ignoring non-text blocks.

    Content is a list of blocks; on models with thinking enabled there may
    be thinking blocks before the text, so filter by type rather than
    reading content[0] blindly.
    """
    parts = [block.text for block in response.content if block.type == "text"]
    return "\n".join(parts).strip()


def run_case(client, config: dict, case_input: str) -> tuple[str, dict]:
    """Send one case and return its text output plus token usage."""
    prompt = config["prompt_template"].replace("{input}", case_input)

    request = {
        "model": config.get("model", DEFAULT_MODEL),
        "max_tokens": config.get("max_tokens", DEFAULT_MAX_TOKENS),
        "messages": [{"role": "user", "content": prompt}],
    }

    if config.get("system"):
        request["system"] = config["system"]

    # `effort` trades thoroughness against tokens and latency. Low is a good
    # default for evaluation runs. Set "effort": null in the config to omit it
    # entirely — older models (for example Haiku 4.5) reject the parameter.
    #
    # Note there is deliberately no `temperature` here: current frontier models
    # reject sampling parameters. Control consistency through the prompt itself,
    # which is what this course teaches anyway.
    effort = config.get("effort", "low")
    if effort:
        request["output_config"] = {"effort": effort}

    response = client.messages.create(**request)

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }

    # A refusal returns a normal 200 with an empty or partial content list, so
    # check stop_reason before treating the output as a real answer.
    if response.stop_reason == "refusal":
        return "[MODEL REFUSED — stop_reason: refusal]", usage

    return extract_text(response), usage


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a prompt template over a test set."
    )
    parser.add_argument("config", help="path to the JSON eval config")
    parser.add_argument(
        "--out", default="eval-results.md", help="output Markdown file"
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="runs per case, for observing run-to-run variation (default: 1)",
    )
    args = parser.parse_args()

    if args.repeat < 1:
        sys.exit("--repeat must be at least 1.")

    config = load_config(args.config)
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    model = config.get("model", DEFAULT_MODEL)
    lines = [
        f"# Eval results — {config.get('version', 'unnamed version')}",
        "",
        f"- Model: `{model}`",
        f"- Config: `{args.config}`",
        f"- Runs per case: {args.repeat}",
        "",
        "Score each output against your success criteria by hand.",
        "",
    ]

    total_in = 0
    total_out = 0

    for case in config["cases"]:
        case_id = case.get("id", "unnamed")
        print(f"Running {case_id} ...", file=sys.stderr)

        lines.append(f"## {case_id}")
        lines.append("")
        if case.get("expected"):
            lines.append(f"**Expected behavior:** {case['expected']}")
            lines.append("")
        lines.append("**Input:**")
        lines.append("")
        lines.append(FENCE)
        lines.append(case["input"])
        lines.append(FENCE)
        lines.append("")

        for run_number in range(1, args.repeat + 1):
            try:
                output, usage = run_case(client, config, case["input"])
            except anthropic.AuthenticationError:
                sys.exit("Authentication failed. Is ANTHROPIC_API_KEY set?")
            except anthropic.RateLimitError:
                sys.exit("Rate limited. Wait and rerun.")
            except anthropic.APIError as error:
                output = f"[API ERROR: {error}]"
                usage = {"input_tokens": 0, "output_tokens": 0}

            total_in += usage["input_tokens"]
            total_out += usage["output_tokens"]

            heading = "**Output:**" if args.repeat == 1 else f"**Run {run_number}:**"
            lines.append(heading)
            lines.append("")
            lines.append(FENCE)
            lines.append(output)
            lines.append(FENCE)
            lines.append("")

        lines.append("**Score:** (fill in by hand)")
        lines.append("")
        lines.append("| C1 | C2 | C3 | C4 | C5 | Pass? |")
        lines.append("|---|---|---|---|---|---|")
        lines.append("|  |  |  |  |  |  |")
        lines.append("")

    lines.append("## Token usage")
    lines.append("")
    lines.append(f"- Input tokens: {total_in:,}")
    lines.append(f"- Output tokens: {total_out:,}")
    lines.append("")

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    print(f"Wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()