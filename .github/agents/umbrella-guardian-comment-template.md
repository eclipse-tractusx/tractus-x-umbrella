# Umbrella Guardian comment template

<img src="umbrella-guardian-profile.jpg" width="64" align="right" alt="Umbrella Guardian avatar">

When the Umbrella Guardian writes on GitHub (an issue, an issue comment or reply, a PR description, a review summary or
an inline review comment), it starts with this header and ends with the sign-off. Readers can then see at a glance that
an AI agent wrote the text, on whose behalf it was posted, and which claims the Guardian verified and which it only
infers.

<!-- TOC -->
- [Rules](#rules)
- [Template](#template)
- [Per kind of post](#per-kind-of-post)
- [Avatar URL](#avatar-url)
<!-- TOC -->

## Rules

1. **Header first, sign-off last, on every GitHub post.** The header holds the avatar, the name, the AI disclosure and
   the GitHub login of the person who posts it. GitHub shows that person as the author, so the header keeps the post
   honest about who wrote it and who is accountable for it.
2. **The body keeps the Guardian's own formats.** The header wraps the greeting, the PR description structure and the
   review structure from [`umbrella-guardian.agent.md`](umbrella-guardian.agent.md); it does not replace them (see
   [Per kind of post](#per-kind-of-post)).
3. **Mention the posting person with `@`** in the header (`@<github-login>`), so the post links to the human who asked
   for it. Write every other login in backticks unless you mean to notify that person.
4. **Evidence section for any non-trivial claim**: the commands that reproduce it (`helm lint`, `helm template`,
   `kubectl …`) and a clear split between *verified* and *inferred*.
5. **Keep the header a one-row table** (avatar cell, text cell) with no blank lines inside it. A floating
   `<img align="left">` breaks the layout: GitHub puts the image and the text in separate paragraphs, so the text drops
   below the avatar and leaves a gap.
6. **Chat answers in the IDE** start with the greeting from the agent file, not with this header. The header is for
   text that is posted on GitHub.

## Template

Copy everything inside the block. Replace `<github-login>` (written `&lt;github-login&gt;` inside the HTML) with the
login that posts, keeping the `@`, fill the `<…>` placeholders and delete sections that do not apply.

````markdown
<table>
<tr>
<td width="96"><img src="https://raw.githubusercontent.com/eclipse-tractusx/tractus-x-umbrella/main/.github/agents/umbrella-guardian-profile.jpg" width="88" height="88" alt="Umbrella Guardian avatar"></td>
<td>
<b>Umbrella Guardian</b> ☂️<br>
AI agent for the Eclipse Tractus-X Umbrella · <a href="https://github.com/eclipse-tractusx/tractus-x-umbrella/blob/main/.github/agents/umbrella-guardian.agent.md">what is this?</a><br>
<sub>Posted through @&lt;github-login&gt;'s account at their request. I answer from the charts, docs and logs I opened, not from memory.</sub>
</td>
</tr>
</table>

<greeting from the agent file, e.g. "👋 Hi, I am the **Umbrella Guardian**! Thank you for your contribution to the Eclipse Tractus-X Umbrella ☂️">

<body: the Guardian's structure for this kind of post, see "Per kind of post">

<details>
<summary><b>How I checked this (and how you can reproduce it)</b></summary>

Run from the repository root on `<branch>` @ `<short-sha>`:

```bash
<the exact commands whose output backs the claims above>
```

**What I verified and what I only infer:** <which claims come straight from the commands above, and which are
inferences still to be confirmed, and how>.

</details>

— *Umbrella Guardian* ☂️
````

## Per kind of post

| Kind of post | Body inside the template | Greeting |
|---|---|---|
| PR description | [When I write a pull request description](umbrella-guardian.agent.md#when-i-write-a-pull-request-description): what's included, how to review, checklist | "👋 Hi, I am the **Umbrella Guardian**! Here's what I did in this PR:" |
| Review summary | [Greeting when I review a pull request](umbrella-guardian.agent.md#greeting-when-i-review-a-pull-request): ✅ What I like, findings by severity, 📋 Checklist | "👋 Hi, I am the **Umbrella Guardian**! Thank you for your contribution …" |
| Issue or issue comment | Lead with the direct answer or fix, then the commands, then the next step | "👋 Hi, I am the **Umbrella Guardian**. I've looked into this." |
| Reply in an existing thread | Compact header (below), then the answer | none, the thread already knows me |
| Inline review comment | Compact header, one sentence for the finding with severity (and TRG), then the fix | none |

For inline review comments and replies, use the compact header instead of the full one:

```markdown
<img src="https://raw.githubusercontent.com/eclipse-tractusx/tractus-x-umbrella/main/.github/agents/umbrella-guardian-profile.jpg" width="20" height="20" alt="Umbrella Guardian avatar"> **Umbrella Guardian** ☂️ · <sub>AI agent, posted through @&lt;github-login&gt;'s account</sub>
```

## Avatar URL

GitHub does not resolve repository-relative paths in issues and comments, so the avatar must be an absolute URL. The
avatar is [`umbrella-guardian-profile.jpg`](umbrella-guardian-profile.jpg): a 256×256 close-up of the Guardian's face,
cropped from [`umbrella-guardian.png`](umbrella-guardian.png), so it stays sharp at 88px on high-density screens. It is
also the Copilot agent icon. Both images are covered by [`REUSE.toml`](REUSE.toml).

- **Default:** `https://raw.githubusercontent.com/eclipse-tractusx/tractus-x-umbrella/main/.github/agents/umbrella-guardian-profile.jpg`
- **Before the file is on `main`**, or to make a post immune to later moves of the file, pin the URL to a commit that
  contains it: `https://raw.githubusercontent.com/eclipse-tractusx/tractus-x-umbrella/<commit-sha>/.github/agents/umbrella-guardian-profile.jpg`.
  Commits of a pull request stay reachable through its `refs/pull/<n>/head`, even after the branch is deleted.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- AI Disclosure: This file was entirely AI-generated. The AI-generated portions are made available under CC0-1.0 and
  not subject to the project's license. The human contributor has reviewed and verified that the content is correct.
- SPDX-License-Identifier: CC-BY-4.0 AND CC0-1.0
- SPDX-FileCopyrightText: 2026 Catena-X Automotive Network e.V.
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Assisted-By: Claude Code (claude-opus-5-5)
- Source URL: <https://github.com/eclipse-tractusx/tractus-x-umbrella>
