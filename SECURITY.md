# Security Policy

## Supported versions

Deliberator is in active development (Alpha per `pyproject.toml` classifiers).
We support the latest tagged release on `main` for security fixes. Older
release candidates and dev builds will not receive security updates —
upgrade to the latest tag for any security-relevant change.

| Version | Supported |
|---|---|
| Latest release (`main`) | ✅ |
| Older tags / dev branches | ❌ |

## Reporting a vulnerability

**Please do not file public GitHub issues for security reports.** Public
issues are visible to everyone and may put users at risk before a fix lands.

### How to report

Use one of these channels in preference order:

1. **GitHub private vulnerability reporting** (preferred). Open
   https://github.com/Build-Fractal/deliberator/security/advisories/new and
   submit a private advisory. This routes directly to maintainers without
   public exposure.
2. **Email:** `security@buildfractal.com`. Include a clear description of
   the issue, reproduction steps, and any proof-of-concept code. Encrypted
   reports welcome — request a PGP key in your first message.

### What to include

A good report has:

- A clear description of the issue and its impact.
- A reproduction recipe (config file, command sequence, expected vs actual
  behavior).
- The deliberator version and Python version where you observed it.
- Whether the issue is in deliberator itself or a dependency.
- Any mitigations you've identified (workarounds, configuration changes).

### What to expect

- **Acknowledgement:** within 5 business days of receipt.
- **Initial assessment:** within 10 business days — severity, scope,
  whether a fix is planned, expected timeline.
- **Coordinated disclosure:** we'll work with you on a disclosure timeline.
  We aim for fix-and-release within 30 days for critical issues, 90 days
  for high-severity, longer for lower-severity. Public advisory is
  published alongside the fix release.
- **Credit:** if you'd like recognition, we'll credit you in the
  advisory and CHANGELOG. If you prefer anonymity, we'll respect that.

## Threat model

Deliberator is a developer tool that orchestrates LLM-driven deliberations
and runs on the user's local machine. Security concerns we care about,
in priority order:

### In-scope

1. **Code execution from untrusted config.** A `deliberator.yml` file
   should not be able to execute arbitrary code on the host beyond what
   the documented configuration surface allows. Report any path where a
   malformed or hostile config triggers code execution outside the
   documented surface.
2. **Prompt-injection escapes from deliberation output.** A hostile
   target document (the document being deliberated on) should not be
   able to escape the agent prompt boundary and exfiltrate data,
   subvert the deliberation verdict, or trigger destructive operations
   via tool calls. Report any path you find.
3. **Credential exfiltration.** API keys and OAuth tokens stored in
   `~/.deliberator/credentials/` should never be transmitted anywhere
   except the legitimate provider endpoint. Report any path where
   credentials leak to logs, error messages, deliberation outputs,
   or third-party services.
4. **Path traversal in persistence.** `engine/persistence.py` should
   never read or write outside its sanctioned directories. The existing
   `read_deliberation_file` path-traversal check is one such guard;
   bypasses qualify.
5. **Supply-chain integrity.** Plugin marketplace manifests should not
   be able to install code from arbitrary sources without explicit user
   consent. Report any path that bypasses the documented manifest
   validation surface.

### Out-of-scope

These are known limitations, not vulnerabilities — please don't report
them as security issues:

- **LLM outputs are not authoritative.** Deliberator orchestrates deliberations;
  it does not validate the *content* of agent outputs against ground truth.
  An agent producing incorrect or misleading text is a product concern, not
  a security one.
- **API credentials are stored in plain JSON files** at
  `~/.deliberator/credentials/`. We use file-permission protection
  (`chmod 600`) but not OS keychain integration. If your threat model
  requires keychain storage, file a feature request rather than a security
  advisory.
- **Deliberation cost is unbounded by default.** Without a `max_launches`
  or `max_budget_usd` cap, a deliberation can spend more LLM credits than
  intended. Configure the caps; we treat unbounded cost as a UX issue.
- **The snap-gate prototype's failure mode is ASK, not DENY.** When the LLM
  is unreachable, snap-gate returns ASK (escalate to user) rather than DENY
  (block). This is by design (Principle V: malformed output better than no
  output) but a stricter shop may want DENY semantics — file a feature
  request.

## Acknowledgements

Security reporters who help us improve deliberator will be credited here
(with permission). No reports yet.

## Constitutional anchor

The discipline behind this policy is anchored in Tier 2 (Suite) Principle
XXIV — *Safety-Critical Defense-in-Depth*. See `SAFETY.md` for the
enumerated safety perimeters and their independent guards. Security
vulnerabilities that bypass a documented perimeter or guard receive
priority.
