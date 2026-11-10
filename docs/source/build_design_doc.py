"""Generate the shareable design document HTML. Usage: python3 design_doc.py OUT.html"""

import sys
from html import escape

STYLE = {
    "ppl": ("#f5f5f4", "#a8a29e", "#1c1917"),
    "sn": ("#edf6f0", "#2f7d4f", "#2f7d4f"),
    "ag": ("#edf2fb", "#2b5faa", "#2b5faa"),
    "llm": ("#fdf3e4", "#a35c00", "#a35c00"),
}


def box(x, y, w, h, title, sub, st):
    _, stroke, _ = STYLE[st]
    cx = x + w / 2
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#fff" stroke="{stroke}"/>'
        f'<text x="{cx}" y="{y + h / 2 - 2}" text-anchor="middle" font-size="10.5" font-weight="600">{escape(title)}</text>'
        f'<text x="{cx}" y="{y + h / 2 + 11}" text-anchor="middle" font-size="8.5" fill="#57534e">{escape(sub)}</text>'
    )


def zone(x, y, w, h, title, st):
    fill, stroke, ink = STYLE[st]
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}"/>'
        f'<text x="{x + 10}" y="{y + 18}" font-size="11" font-weight="700" fill="{ink}">{escape(title)}</text>'
    )


def architecture():
    o = [
        '<svg viewBox="0 0 760 330" role="img" aria-label="Architecture overview">',
        '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#44403c"/></marker></defs>',
    ]
    o.append(zone(0, 20, 126, 300, "People", "ppl"))
    for y, t, s in [
        (52, "Employee", "submits, reads replies"),
        (122, "HR agent", "works cases, approves"),
        (192, "Policy admin", "owns rules, policies"),
    ]:
        o.append(box(8, y, 110, 46, t, s, "ppl"))
    o.append(zone(140, 20, 330, 300, "ServiceNow platform", "sn"))
    for y, t, s in [
        (52, "Case management", "case table, portal, form"),
        (122, "Routing policy", "HR routing rules"),
        (192, "Knowledge base", "HR policy articles"),
        (262, "Audit", "AI fields, citations, log"),
    ]:
        o.append(box(150, y, 150, 46, t, s, "sn"))
    for y, t, s in [
        (52, "Orchestration", "Business rules, events"),
        (122, "Outbound integration", "REST, key in settings"),
        (192, "Read-only API", "integration user"),
        (262, "Human approval", "UI action for close"),
    ]:
        o.append(box(310, y, 150, 46, t, s, "sn"))
    o.append(zone(485, 20, 170, 300, "AI agent service", "ag"))
    for y, t, s in [
        (46, "API gateway", "TLS, auth, rate limits"),
        (100, "Agent orchestrator", "triage and chat"),
        (154, "Tool server (MCP)", "read-only tools"),
        (208, "Ingestion", "parse, chunk, embed"),
        (262, "Search index", "vectors + keywords"),
    ]:
        o.append(box(495, y, 150, 44, t, s, "ag"))
    o.append(
        '<rect x="668" y="96" width="90" height="56" rx="8" fill="#fdf3e4" stroke="#a35c00"/>'
        '<text x="713" y="120" text-anchor="middle" font-size="10.5" font-weight="700" fill="#a35c00">LLM provider</text>'
        '<text x="713" y="135" text-anchor="middle" font-size="8.5" fill="#57534e">behind an adapter</text>'
    )
    o.append(
        '<g stroke="#44403c" stroke-width="1.4" fill="none">'
        '<line x1="118" y1="75" x2="148" y2="75" marker-end="url(#a)"/>'
        '<line x1="118" y1="145" x2="148" y2="75" marker-end="url(#a)"/>'
        '<line x1="118" y1="215" x2="148" y2="145" marker-end="url(#a)"/>'
        '<line x1="118" y1="215" x2="148" y2="215" marker-end="url(#a)"/>'
        '<line x1="460" y1="145" x2="474" y2="145"/><path d="M474,145 V68 H493" marker-end="url(#a)"/>'
        '<path d="M495,176 H478 V215 H462" marker-end="url(#a)"/>'
        '<path d="M495,230 H478"/>'
        '<line x1="645" y1="122" x2="666" y2="122" marker-start="url(#a)" marker-end="url(#a)"/>'
        "</g>"
    )
    o.append(
        '<g font-size="9" fill="#57534e" text-anchor="middle">'
        '<text x="478" y="14">HTTPS</text></g>'
    )
    o.append("</svg>")
    return "\n".join(o)


LANES = [70, 250, 450, 650]


def sequence():
    lanes = [
        ("Employee", "ppl"),
        ("ServiceNow", "sn"),
        ("AI agent service", "ag"),
        ("LLM provider", "llm"),
    ]
    steps = [
        ("m", 0, 1, "Submits a case", False),
        ("m", 1, 2, "Triage request: case text, country, employee type", False),
        ("m", 2, 3, "Classify and plan", False),
        ("s", 2, "Searches the policy index (tools)"),
        ("m", 2, 3, "Draft answer from retrieved policy text", False),
        ("m", 3, 2, "Classification + cited draft", True),
        ("s", 2, "Verifies every quote against the source"),
        ("m", 2, 1, "Recommendation (JSON)", True),
        ("s", 1, "Routing rules pick the team; result and citations saved"),
        ("m", 1, 0, "AI suggestion with quotes, if allowed", False),
    ]
    top, step = 66, 27
    bottom = top + step * (len(steps) - 1) + 16
    o = [
        f'<svg viewBox="0 0 720 {bottom + 4}" role="img" aria-label="New case flow">',
        '<defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#44403c"/></marker></defs>',
    ]
    for x, (t, st) in zip(LANES, lanes, strict=False):
        fill, stroke, ink = STYLE[st]
        o.append(
            f'<rect x="{x - 65}" y="6" width="130" height="34" rx="6" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x}" y="27" text-anchor="middle" font-size="10.5" font-weight="700" fill="{ink}">{escape(t)}</text>'
            f'<line x1="{x}" y1="40" x2="{x}" y2="{bottom}" stroke="#a8a29e" stroke-dasharray="3 4"/>'
        )
    for i, s in enumerate(steps):
        y, n = top + step * i, i + 1
        if s[0] == "m":
            _, a, b, text, dashed = s
            xa, xb = LANES[a], LANES[b]
            end = xb - 2 if xb > xa else xb + 2
            d = ' stroke-dasharray="5 3"' if dashed else ""
            o.append(
                f'<line x1="{xa}" y1="{y}" x2="{end}" y2="{y}" stroke="#44403c" stroke-width="1.4" marker-end="url(#s)"{d}/>'
                f'<text x="{(xa + xb) / 2}" y="{y - 5}" text-anchor="middle" font-size="10" class="halo">{n}  {escape(text)}</text>'
            )
        else:
            _, a, text = s
            x = LANES[a]
            fill, stroke, _ = STYLE[lanes[a][1]]
            o.append(
                f'<rect x="{x - 7}" y="{y - 10}" width="14" height="20" rx="2" fill="{fill}" stroke="{stroke}"/>'
                f'<text x="{x + 14}" y="{y + 4}" font-size="10" class="halo">{n}  {escape(text)}</text>'
            )
    o.append("</svg>")
    return "\n".join(o)


def pipeline():
    items = [
        (["Policy published", "or updated"], "sn"),
        (["Ingestion", "triggered"], "sn"),
        (["Parse", "into sections"], "ag"),
        (["Chunk", "by heading and size"], "ag"),
        (["Embed", "and index"], "ag"),
        (["Searchable", "with citations"], "ag"),
    ]
    n, gap = len(items), 18
    w = (720 - gap * (n - 1)) / n
    o = [
        '<svg viewBox="0 0 720 62" role="img" aria-label="Knowledge ingestion pipeline">',
        '<defs><marker id="p" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#44403c"/></marker></defs>',
    ]
    for i, (lines, st) in enumerate(items):
        fill, stroke, _ = STYLE[st]
        x = i * (w + gap)
        o.append(
            f'<rect x="{x + 0.5}" y="4" width="{w - 1}" height="52" rx="6" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + w / 2}" y="26" text-anchor="middle" font-size="10" font-weight="600">{escape(lines[0])}</text>'
            f'<text x="{x + w / 2}" y="41" text-anchor="middle" font-size="9" fill="#57534e">{escape(lines[1])}</text>'
        )
        if i < n - 1:
            o.append(
                f'<line x1="{x + w + 1}" y1="30" x2="{x + w + gap - 2}" y2="30" stroke="#44403c" stroke-width="1.4" marker-end="url(#p)"/>'
            )
    o.append("</svg>")
    return "\n".join(o)


CSS = """
  @page { size: Letter; margin: 0.65in 0.7in; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1c1917; font-size: 10.5pt; line-height: 1.5; margin: 0; background: #fff; }
  h1 { font-size: 21pt; margin: 0 0 4px; letter-spacing: -0.01em; }
  h2 { font-size: 14pt; margin: 22px 0 6px; padding-top: 4px; border-top: 1px solid #e7e5e4; }
  h3 { font-size: 11pt; margin: 14px 0 4px; }
  p { margin: 0 0 8px; }
  .meta { color: #57534e; font-size: 9.5pt; margin-bottom: 18px; }
  .brk { break-before: page; }
  .brk > h2:first-child { border-top: none; margin-top: 0; }
  h2, h3 { break-after: avoid; }
  svg, .callout { break-inside: avoid; }
  ul, ol { break-inside: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 9.5pt; margin: 6px 0 8px; }
  th, td { text-align: left; vertical-align: top; padding: 5px 8px; border-bottom: 1px solid #e7e5e4; }
  th { background: #f5f5f4; font-weight: 600; }
  tr, .avoid { break-inside: avoid; }
  ol, ul { margin: 4px 0 8px; padding-left: 22px; }
  li { margin-bottom: 3px; }
  .callout { background: #f5f5f4; border-radius: 6px; padding: 10px 14px; margin: 10px 0; }
  code { font-size: 0.92em; }
  svg { width: 100%; height: auto; display: block; margin: 6px 0; }
  svg text { font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; fill: #1c1917; }
  svg .halo { paint-order: stroke; stroke: #fff; stroke-width: 4px; stroke-linejoin: round; }
"""

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>HR Case Orchestration Design</title><style>{CSS}</style></head>
<body>

<h1>Policy-driven HR case orchestration</h1>
<div class="meta">Design overview for the ServiceNow take-home &middot; Raghav Munjal &middot; November 2026 &middot; Draft for discussion</div>

<h2>Summary</h2>
<p>HR teams receive a steady flow of questions about leave, benefits and payroll. Most of them are answered by a policy document that already exists, but finding the right policy, routing the case to the right team and writing a reply still takes people time.</p>
<p>This prototype handles HR cases with rules that HR can change without code, and uses an AI agent to help at each step. The agent reads the case, classifies it, finds the relevant policy text, and drafts a reply that quotes the policy word for word. ServiceNow stays in charge: it applies the routing rules, writes every change, keeps the audit trail, and asks a person to approve anything critical, such as closing a case.</p>

<h2>Goals</h2>
<ul>
  <li>Route cases with configurable policy: an HR-owned rules table, so HR can change routing by editing a row.</li>
  <li>Use AI to classify cases, search policies and draft answers, with every factual claim backed by an exact quote.</li>
  <li>Let HR staff ask the AI for help inside a case, pointing it at a specific document.</li>
  <li>Keep a person in control of critical actions, and record who approved what.</li>
  <li>Design for a realistic policy library: hundreds of long documents, not a handful of short ones.</li>
</ul>

<h3>Not in scope for the prototype</h3>
<p>Sensitive case handling (for example harassment or medical cases), personal data redaction, production hosting, multi-language support, and a dedicated chat panel. Each is covered in "Future work" so the path forward is clear.</p>

<h2>How people use it</h2>
<ol>
  <li><b>An employee submits a case</b> on the portal with a title and description.</li>
  <li><b>The AI classifies it</b>: department, topics, priority and severity. Routing rules then pick the assignment group and assignee.</li>
  <li><b>The AI searches HR policies</b> using retrieval over the knowledge base.</li>
  <li><b>The employee gets an AI suggestion</b> on the case that quotes the exact policy text, as long as the AI is confident and can cite every claim. Otherwise no suggestion is posted and the case goes to people as usual.</li>
  <li><b>HR staff can tag <code>@ai</code></b> in a comment or work note, point it at a document, and get a cited answer.</li>
  <li><b>A person approves critical actions.</b> The AI can propose closing a case, but only an HR agent can approve it.</li>
</ol>

<div class="brk">
<h2>Architecture</h2>
{architecture()}
<p>The design has three parts.</p>
<p><b>ServiceNow</b> is the system of record. It holds the cases, the routing rules, the HR policy knowledge base and the audit trail. Business rules and events call the AI agent service, apply its recommendation through the routing rules, and post replies. A UI action gives HR agents the approval step for closing a case.</p>
<p><b>The AI agent service</b> is a small, containerized service outside ServiceNow. It runs the agent loop, exposes read-only tools over the Model Context Protocol (MCP), and keeps a search index of the policy library. It reads from ServiceNow with a read-only integration user and never writes to a case. It returns a recommendation, and ServiceNow decides what to do with it.</p>
<p><b>The LLM provider</b> is accessed through an adapter, so the model can be swapped without changing the rest of the system. A hosted model with tool calling and citation support is the default. Moving to Now Assist on a licensed instance would replace this adapter, not the design.</p>

<h3>Why an external service</h3>
<p>Personal developer instances don't include Now Assist or AI Agent Studio, and good retrieval over hundreds of long documents needs a proper search index. Keeping that work in a separate service also keeps the ServiceNow app small and upgrade-safe. The integration uses standard patterns (outbound REST with the key kept out of source, and the Table API with a least-privilege user), so it could be pointed at a different AI backend later.</p>
</div>

<div>
<h2>Key design decisions</h2>
<table>
  <tr><th style="width:30%">Decision</th><th style="width:38%">Why</th><th>Trade-off</th></tr>
  <tr><td>The AI recommends; ServiceNow decides and writes</td><td>Keeps control, audit and permissions in the platform. The AI service needs no write access</td><td>Every action needs logic in ServiceNow to apply the recommendation</td></tr>
  <tr><td>Routing lives in an HR-owned rules table</td><td>HR changes routing in the UI without code, and deployments never overwrite their edits</td><td>Not Decision Builder, which the build tooling cannot define as code; switching later changes one script</td></tr>
  <tr><td>Every factual claim must quote the policy exactly</td><td>Employees and HR can check the answer, and hallucinated policy never reaches an employee</td><td>Some questions get no suggestion when the policy can't be quoted</td></tr>
  <tr><td>The knowledge base is the source of truth; the search index is a copy</td><td>Policy owners keep using ServiceNow Knowledge; the index can be rebuilt any time</td><td>Ingestion has to keep the index in sync</td></tr>
  <tr><td>Hybrid search with reranking</td><td>Keywords catch exact terms and form names, while vector search catches paraphrases</td><td>More components than keyword search alone</td></tr>
  <tr><td>Human approval for closing</td><td>Closing affects the employee directly and is hard to undo</td><td>One more click for HR</td></tr>
  <tr><td>Fail safe to people</td><td>Any AI failure sends the case to manual triage instead of blocking it</td><td>Cases can reach people without AI help during an outage</td></tr>
  <tr><td>Provider-neutral LLM access</td><td>Avoids lock-in and keeps a clear path to Now Assist</td><td>Provider-specific features sit behind the adapter</td></tr>
</table>

<h2>Flow of a new case</h2>
{sequence()}
<p>If the service is unreachable, times out or returns something invalid, the case goes to a Manual Triage group and the failure is noted on the case. If the AI isn't confident, or any claim lacks a citation, routing still happens but no suggestion is posted.</p>
</div>

<div>
<h2>Knowledge and retrieval</h2>
{pipeline()}
<p>When a policy article is published, updated or retired in ServiceNow, the AI service re-ingests it. A nightly check compares versions to catch anything missed. Retired articles are kept for audit but never searched.</p>

<h3>Chunking</h3>
<p>Articles are split along their headings first, so a chunk never mixes two sections, and then into pieces of a few hundred words with a small overlap, cut only at sentence boundaries. Tables are kept whole where possible, and the section path ("Parental leave > Germany > Eligibility") travels with each chunk so it keeps its context. Each chunk remembers exactly where it came from in which version of the article.</p>

<h3>Search</h3>
<p>Searches always filter to active policies for the employee's country (or global ones). The service runs a vector search and a keyword search, merges the results, reranks them and keeps the best few. If nothing is relevant enough, the agent says it couldn't find a policy instead of guessing.</p>

<h3>Citations</h3>
<p>The agent drafts its answer only from the retrieved text. Every factual sentence must carry a quote, and the service checks each quote word for word against the stored source before anything is returned. ServiceNow saves each citation with the article version, so you can always see what the AI relied on, even after the policy changes. An AI suggestion looks like this:</p>
<div class="callout"><p style="margin:0">You can take up to three years of parental leave per child, and you need to request it in writing at least seven weeks before it starts. [1][2]</p>
<p style="margin:6px 0 0; font-size:9.5pt; color:#57534e">[1] Parental leave (Germany), Eligibility: "Employees in Germany are entitled to up to 3 years of parental leave per child."<br>[2] Parental leave (Germany), Eligibility: "Leave must be requested in writing at least 7 weeks before it starts."</p></div>

<h2>What the AI can and can't do</h2>
<table>
  <tr><th style="width:50%">The AI agent can</th><th>The AI agent can't</th></tr>
  <tr><td>Classify a case and explain its reasoning</td><td>Write to a case, assign it or close it</td></tr>
  <tr><td>Search policies and read a specific section</td><td>Choose the assignment group (the routing rules do)</td></tr>
  <tr><td>Draft a reply in which every claim is quoted</td><td>State a policy it can't quote</td></tr>
  <tr><td>Answer <code>@ai</code> questions from HR staff</td><td>Change routing rules or policy articles</td></tr>
  <tr><td>Propose closing a case, with a resolution</td><td>Act on instructions written inside a case</td></tr>
</table>
</div>

<div>
<h2>Technology choices</h2>
<table>
  <tr><th style="width:24%">Area</th><th style="width:36%">Choice</th><th>Why</th></tr>
  <tr><td>ServiceNow app</td><td>Scoped application built with the ServiceNow SDK, kept in Git</td><td>Upgrade-safe and under source control</td></tr>
  <tr><td>Orchestration and policy</td><td>Business rules, events and script actions; HR-owned routing rules table</td><td>Runs off the user's transaction; routing is data HR edits</td></tr>
  <tr><td>Platform logic</td><td>Script Includes, Business Rules, <code>RESTMessageV2</code>; service URL and key in admin-only system properties</td><td>Standard, reusable integration pattern</td></tr>
  <tr><td>User interface</td><td>Service Portal record producer, case form, UI action for approval</td><td>Out-of-the-box experiences</td></tr>
  <tr><td>Service language</td><td>Python</td><td>Strongest ecosystem for agents, retrieval and evaluation</td></tr>
  <tr><td>API server</td><td>FastAPI with Pydantic models</td><td>Typed request and response contracts, async, automatic API docs</td></tr>
  <tr><td>Agent loop</td><td>LangGraph</td><td>An explicit graph (classify, retrieve, draft, verify) with bounded tool calls, easy to test and reason about</td></tr>
  <tr><td>LLM access</td><td>Provider adapter over the provider's official SDK</td><td>Model can be swapped by configuration</td></tr>
  <tr><td>Tools</td><td>Model Context Protocol, official Python SDK</td><td>Standard tool interface the agent and other clients can share</td></tr>
  <tr><td>Search index</td><td>PostgreSQL with pgvector and built-in full-text search</td><td>Vectors and keywords in one database</td></tr>
  <tr><td>Embeddings and reranking</td><td>Open-source ONNX models run inside the service (FastEmbed): an embedding model and a cross-encoder reranker</td><td>No extra vendor, policy text stays in our infrastructure</td></tr>
  <tr><td>Parsing and chunking</td><td>BeautifulSoup and a heading-aware splitter</td><td>Keeps policy structure intact</td></tr>
  <tr><td>Gateway</td><td>Caddy reverse proxy</td><td>Automatic TLS, routing and rate limits</td></tr>
  <tr><td>Packaging</td><td>Docker Compose</td><td>One command to run the whole service</td></tr>
  <tr><td>Testing</td><td>pytest, a retrieval evaluation set, ServiceNow ATF where time allows</td><td>Covers code, retrieval quality and platform behaviour</td></tr>
</table>

<h2>Security and governance</h2>
<ul>
  <li><b>Least privilege.</b> The AI service reads cases and HR articles through a read-only integration user. It can't write anything in ServiceNow.</li>
  <li><b>Authenticated calls.</b> ServiceNow calls the service over HTTPS with an API key kept in an admin-only system property, optionally with signed, time-stamped requests to prevent replays.</li>
  <li><b>Small surface.</b> Only the gateway is exposed, and only for the endpoints ServiceNow needs. The index, models and tools stay internal.</li>
  <li><b>Prompt injection.</b> Case text is treated as data, not instructions. Even a successful injection can't change a case, because the agent has no write access and closing needs approval.</li>
  <li><b>Audit.</b> Every AI result, citation and approval is stored on the case in ServiceNow.</li>
  <li><b>Data.</b> The prototype uses synthetic employees, cases and policies only.</li>
</ul>
</div>

<div>
<h2>Testing</h2>
<table>
  <tr><th style="width:42%">Scenario</th><th>Expected result</th></tr>
  <tr><td>Routine benefits question</td><td>Routed to Benefits, with a suggestion that quotes the benefits policy exactly</td></tr>
  <tr><td>Same leave question from two countries</td><td>Each answer cites its own country's policy</td></tr>
  <tr><td>Vague request</td><td>Low confidence: no suggestion, routed to Manual Triage</td></tr>
  <tr><td>HR edits a routing rule</td><td>The next case routes differently, with no code change</td></tr>
  <tr><td>A policy article is updated</td><td>New answers quote the new text; older citations keep the old version</td></tr>
  <tr><td>HR tags <code>@ai</code> and points at an article</td><td>The reply cites that article</td></tr>
  <tr><td>The AI proposes closing a case</td><td>The case stays open until an HR agent approves</td></tr>
  <tr><td>AI service unavailable</td><td>Manual Triage, with the failure noted on the case</td></tr>
  <tr><td>Case text tries to override the AI's instructions</td><td>No effect</td></tr>
</table>
<p>Retrieval quality is measured separately with a set of 30 to 50 questions, each with a known correct policy section. The target is that the right section appears in the top five results and that every quote matches its source.</p>

<h2>Delivery plan</h2>
<ol>
  <li><b>Foundations.</b> Confirm instance capabilities and connectivity between ServiceNow and the AI service.</li>
  <li><b>ServiceNow app.</b> Case model, portal form, roles, groups and the routing rules.</li>
  <li><b>Policy library.</b> A synthetic set of 50 to 100 long policies across several countries.</li>
  <li><b>Retrieval.</b> Ingestion, chunking, the search index and the retrieval evaluation.</li>
  <li><b>Triage end to end.</b> Classification, routing and cited suggestions.</li>
  <li><b><code>@ai</code> assistance and close approval.</b></li>
  <li><b>Hardening.</b> Failure paths and injection tests.</li>
  <li><b>Hand-off.</b> This document finalized, a recorded walkthrough and test evidence.</li>
</ol>

<h2>Future work</h2>
<ul>
  <li><b>Sensitive case handling.</b> A configurable sensitivity check before any AI call, with a restricted queue and access controls. This is the first step before any real data.</li>
  <li><b>Personal data redaction</b> before case text leaves the platform.</li>
  <li><b>Now Assist and AI Agent Studio.</b> On a licensed instance, replace the provider adapter with Now Assist skills and agents, and consider ServiceNow AI Search for retrieval.</li>
  <li><b>Richer policy governance:</b> versioned routing policies with owners and effective dates, and per-category limits on what the AI may do automatically.</li>
  <li><b>Production operations:</b> managed hosting, tracing dashboards, a full ATF suite and CI/CD.</li>
</ul>
</div>

<div class="brk">
<h2>Assumptions</h2>
<ul>
  <li>The prototype is built on a personal developer instance. That instance doesn't include HR Service Delivery, Now Assist or AI Agent Studio.</li>
  <li>Because HR Service Delivery isn't available, cases live in a custom table modeled on the HR case fields. In production this would be the standard HR case table.</li>
  <li>Calling an external LLM provider is acceptable, because all data is synthetic.</li>
  <li>A small service outside ServiceNow is acceptable for the AI and retrieval work, reachable from the instance over HTTPS.</li>
  <li>The prototype's hosting is for demonstration only and isn't meant to reflect production hosting.</li>
  <li>A synthetic library of 50 to 100 long policies across a few countries is a fair stand-in for a real policy library.</li>
  <li>English only.</li>
  <li>Closing a case is the only action that needs human approval in the prototype. The same pattern extends to others.</li>
  <li>Sensitive cases are out of scope for the prototype and handled by the future-work design above.</li>
</ul>

</div>

</body></html>
"""

open(sys.argv[1], "w").write(HTML)
