# Umbrella Guardian

<img src="umbrella-guardian-profile.jpg" width="96" align="right" alt="Umbrella Guardian avatar">

The **Umbrella Guardian** is the AI agent of this repository: a first-person guide and reviewer for the Tractus-X
umbrella Helm chart, its bundles, profiles, docs and the Tractus-X Release Guidelines. It works with **Claude Code** and
**GitHub Copilot**.

| File | Purpose |
|---|---|
| [`.claude/agents/umbrella-guardian.md`](../../.claude/agents/umbrella-guardian.md) | The agent for Claude Code |
| [`CLAUDE.md`](../../CLAUDE.md) | Claude Code session instructions: loads `AGENTS.md` and the Copilot instructions |
| [`umbrella-guardian.agent.md`](umbrella-guardian.agent.md) | The same agent for GitHub Copilot |
| [`../copilot-instructions.md`](../copilot-instructions.md) | Repository-wide Copilot instructions (chat and code review) |
| [`../skills/`](../skills/) | The skills (procedures and scripts), shared by both |
| [`umbrella-guardian-comment-template.md`](umbrella-guardian-comment-template.md) | The avatar header it uses on GitHub |

## Start a chat in Claude Code from the command line

Install Claude Code once (`npm install -g @anthropic-ai/claude-code`) and run `claude` once to sign in. Then, from the
repository root or a worktree of it:

```bash
# Chat with the Guardian: the whole session runs as the agent
claude --agent umbrella-guardian

# The same, with your first question already asked
claude --agent umbrella-guardian "My EDC pods are Pending on Minikube, what do I check first?"

# One answer printed to the terminal, then exit (quick lookups, scripts)
claude --agent umbrella-guardian -p "Which profile deploys the decentralized IdentityHub flow?"

# Continue your last chat in this directory
claude --agent umbrella-guardian --continue
```

Plain `claude` works too: `CLAUDE.md` makes Claude speak as the Guardian and hand deep work to the `umbrella-guardian`
subagent (`/agents` lists it). With `--agent`, the Guardian answers every message itself, with its full persona and
rules from the first line. To make it your default in this repository, put `{"agent": "umbrella-guardian"}` in
`.claude/settings.local.json` (personal settings, keep them out of commits).

## Use it in GitHub Copilot

- **VS Code (Copilot Chat, agent mode):** open the repository, open the chat and select **Eclipse Tractus-X Umbrella
  Guardian** in the agent picker. Reload the window if it does not appear yet.
- **Copilot code review on github.com:** follows [`../copilot-instructions.md`](../copilot-instructions.md), so reviews
  come from the Guardian without selecting anything.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- AI Disclosure: This file was entirely AI-generated. The AI-generated portions are made available under CC0-1.0 and
  not subject to the project's license. The human contributor has reviewed and verified that the content is correct.
- SPDX-License-Identifier: CC-BY-4.0 AND CC0-1.0
- SPDX-FileCopyrightText: 2026 Catena-X Automotive Network e.V.
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Assisted-By: Claude Code (claude-opus-5-5)
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
