package {
  name        = "hello-world"
  version     = "1.0.0"
  description = "Simple greeting skill"
  license     = "MIT"
}

claude_skill "greeter" {
  description = "Greets users warmly"
  content     = file("skills/greeter.md")
}
