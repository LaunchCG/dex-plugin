package {
  name        = "dex-builder"
  version     = "2.0.0"
  description = "Build dex packages and registries using the latest dex format"
  author      = "LaunchCG"
  license     = "MIT"
  repository  = "https://github.com/LaunchCG/dex-plugin"
  platforms   = ["claude-code", "cursor", "github-copilot"]
}

claude_skill "dex-builder" {
  description = "Build dex packages and registries using HCL, Go templates, and modern dex CLI"
  content     = file("skills/dex-builder.md")
}

copilot_skill "dex-builder" {
  description = "Build dex packages and registries using HCL, Go templates, and modern dex CLI"
  content     = file("skills/dex-builder.md")
}
