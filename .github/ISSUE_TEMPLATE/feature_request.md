---
name: Feature Request
description: Suggest an idea or improvement for this project
title: "[Feature] <short description of the feature>"
labels: ["enhancement"]

body:

- type: markdown
  attributes:
  value: |
  Thank you for suggesting an improvement! Please provide as much context as possible.
- type: dropdown
  id: image-name
  attributes:
  label: Which image or part of the project is this for?
  description: Is your request for a specific image or the project as a whole?
  options: - Project-wide (e.g., build process, documentation) - keycloak - postgres - redis # --- Add more image names here as you add them ---
  multiple: false
  validations:
  required: true
- type: textarea
  id: problem-description
  attributes:
  label: Is your feature request related to a problem? Please describe.
  description: A clear and concise description of what the problem is.
  placeholder: "e.g., I'm always frustrated when I have to manually set..."
  validations:
  required: true
- type: textarea
  id: solution-description
  attributes:
  label: Describe the solution you'd like
  description: A clear and concise description of what you want to happen.
  validations:
  required: true
- type: textarea
  id: alternatives
  attributes:
  label: Describe alternatives you've considered
  description: A clear and concise description of any alternative solutions or features you've considered.
- type: textarea
  id: additional-context
  attributes:
  label: Additional context
  description: Add any other context, mockups, or screenshots about the feature request here.

---
