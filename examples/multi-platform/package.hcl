package {
  name        = "code-reviewer"
  version     = "1.0.0"
  description = "Code review across platforms"
  platforms   = ["claude-code", "github-copilot", "cursor"]
}

# Shared content - same file for all platforms
claude_skill "review" {
  description = "Perform code reviews"
  content     = file("content/shared-skill.md")
}

copilot_skill "review" {
  description = "Perform code reviews"
  content     = file("content/shared-skill.md")
}

# Platform-specific commands using templates
claude_command "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "Read"
  })
}

copilot_prompt "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "fetch"
  })
}

cursor_command "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "read_file"
  })
}
