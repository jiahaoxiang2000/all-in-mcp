#import "@preview/touying:0.6.1": *
#import themes.simple: *
#import "@preview/cetz:0.3.2"
#import "@preview/fletcher:0.5.5" as fletcher: edge, node
#import "@preview/numbly:0.1.0": numbly
#import "@preview/theorion:0.3.2": *
#import cosmos.clouds: *
#show: show-theorion

// cetz and fletcher bindings for touying
#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))
#let fletcher-diagram = touying-reducer.with(reduce: fletcher.diagram, cover: fletcher.hide)

// Set Chinese fonts for the presentation
// If the fonts are not installed, you can find new fonts to replace them. by the `typst fonts`.
// #set text(
//   font: (
//     "Noto Sans CJK SC", // Primary Chinese font
//     "Noto Serif CJK SC", // Alternative Chinese serif font
//     "WenQuanYi Micro Hei", // Chinese fallback font
//     "FZShuSong-Z01", // Traditional Chinese font
//     "HYZhongSongJ", // Another Chinese font option
//     "Noto Sans", // Latin fallback
//     "Roboto", // Final fallback
//   ),
//   // lang: "zh",
//   // region: "cn",
// )

// Color shorthand functions
#let redt(content) = text(fill: red, content)
#let bluet(content) = text(fill: blue, content)
#let greent(content) = text(fill: green, content)
#let yellowt(content) = text(fill: yellow, content)
#let oranget(content) = text(fill: orange, content)
#let purplet(content) = text(fill: purple, content)
#let greyt(content) = text(fill: gray, content)
#let grayt(content) = text(fill: gray, content)

// Additional font customization options:
// For headings, you can use a different font:
#show heading: set text(font: "Noto Serif CJK SC", weight: "bold")
// For code blocks, you can use a monospace font:
#show raw: set text(font: "Noto Sans Mono CJK SC")

#show: simple-theme.with(aspect-ratio: "16-9", footer: [All-in-MCP - v0.3.\*])

#title-slide[
  = All-in-MCP: A Comprehensive MCP Collection
  #v(0.5em)

  _FastMCP-based Model Context Protocol server providing  paper search and more_

  #v(0.5em)

  isomo #footnote[github/jiahaoxiang2000]

  #v(1em)
  #datetime.today().display()
]

= Why All-in-MCP?

== Our Mission & Goals

*Goal:* Maintain a comprehensive collection of great MCP tools for specific tasks

#pause

*Our Approach:*
- 🛠️ Some MCPs created by us (e.g., APaper academic research tools)
- 🌟 Some MCPs curated from the community (e.g., GitHub-Repo-MCP)
- 🔧 Unified proxy server with modular architecture

#pagebreak()

*Problem We Solve:*
- Scattered MCP tools across different repositories
- Difficulty discovering and integrating specialized MCPs

#pause

#redt[*Result:*] One-stop shop for curated, tested, and integrated MCP collections!


= Architecture Overview

== FastMCP Proxy Design

// The All-in-MCP architecture: LLM clients connect to the All-in-MCP Proxy Server, which routes requests to specialized MCP modules (APaper for academic tools, GitHub-Repo-MCP for repository tools, and other MCP servers). This design provides better modularity, performance, and scalability.
#fletcher-diagram(
  node-stroke: .1em,
  spacing: 1.5em,
  // Nodes with three-layer vertical stack on the right
  node((-4, 0), `LLM Client`, radius: 1.8em),
  edge((-4, 0), (0, 0), `requests `, "--|>"),
  pause,
  node((0, 0), `All-in-MCP Proxy`, radius: 2em, fill: blue),
  pause,
  node((4, 0.8), `APaper Module`, radius: 2em, fill: green),
  node((4, 0), `GitHub-Repo MCP`, radius: 2em, fill: yellow),
  node((4, -0.8), `Other Servers`, radius: 2em, fill: gray),
  edge((0, 0), (4, 0.8), ``, "-|>"),
  edge((0, 0), (4, 0), ``, "-|>"),
  edge((0, 0), (4, -0.8), ``, "-|>"),
)


= Simple Usage

== One-Line Installation & Running

*Installation & Run:* Just use pipx - no complex setup required!

#pause

```bash
# Install and run directly
pipx run all-in-mcp

# With specific tool modules enabled
APAPER=true GITHUB_REPO_MCP=true pipx run all-in-mcp
```


== MCP Client Configuration

#alternatives[
  _VSCode (.vscode/mcp.json)_
  ```json
  {
    "servers": {
      "all-in-mcp": {
        "command": "pipx", "args": ["run", "all-in-mcp"],
        "env": {"APAPER": "true", "GITHUB_REPO_MCP": "true"}
      }
    }
  }
  ```][
  _Claude Code (.mcp.json)_
  ```json
  {
    "mcpServers": {
      "all-in-mcp": {
        "command": "pipx", "args": ["run", "all-in-mcp"],
        "env": {"APAPER": "true", "GITHUB_REPO_MCP": "true"}
      }
    }
  }
  ```
]

= Development Journey

== Key Milestones from CHANGELOG

*v0.1.0* (June 2025): 🌱 Initial IACR paper tools and search functionality

#pause

*v0.2.x* (June-August 2025): 📚 Added multiple academic platforms
- DBLP, Google Scholar integration
- PDF processing and year filtering capabilities

#pause

*v0.3.0* (August 2025): 🚀 *Major Migration to FastMCP Architecture*
- Modular APaper design with proxy server

#pause

*Evolution:* From single-purpose IACR tools → comprehensive MCP collection

= Future Plans

== Vision & Community

*More Great Tools:*
- Expand beyond academic research

#pause

*Awesome MCP Collections:*
- Curate the best MCPs for specific workflows

#pause

*Community Contributions:*
- 🎯 *We welcome PRs!* If you have great MCP tools or ideas

#pause

*Goal:* Become the go-to hub for discovering, using, and contributing quality MCP tools! 🚀

= Thanks Everyone

Enjoy *_All-in-MCP_* and happy Coding! 🎉

#v(2em)

🔗 *Repository:* https://github.com/jiahaoxiang2000/all-in-mcp

#v(1em)

_Star ⭐ the repo if you find it useful!_
