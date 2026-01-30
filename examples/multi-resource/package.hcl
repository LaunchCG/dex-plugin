package {
  name        = "dev-workflow"
  version     = "1.0.0"
  description = "Development workflow tools"
  author      = "DevTeam"
  license     = "MIT"
  platforms   = ["claude-code"]
}

claude_skill "dev-workflow" {
  description = "Development workflow best practices"
  content     = file("skills/dev-workflow.md")
}

claude_command "test" {
  description = "Run project tests"
  content     = file("commands/test.md")
}

claude_rule "code-style" {
  description = "Code style guidelines"
  content     = file("rules/code-style.md")
}

claude_settings "dev" {
  allow = [
    "Bash(npm:*)",
    "Bash(pytest:*)",
    "Bash(go test:*)",
  ]
}
