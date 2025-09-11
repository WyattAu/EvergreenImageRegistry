---
name: New Image Proposal
description: Propose a new image to be added to the Evergreen Image Registry
title: "Proposal: Add image for <Image Name>"
labels: ["enhancement", "new-image"]
body:

- type: input
  id: iamge-name
  attributes:
  label: Image Name
  description: "What is the name of the image you'd like to see added?"
  validations:
  required: true
- type: input
  id: image-link
  attributes:
  label: Link to Official Image Repository or Website
  description: "Where can we find the official source code or documentation?"
  validations:
  required: true
- type: textarea
  id: justification
  attributes:
  label: Justification
  description: "Why does this image belong in the Evergreen Image Registry? How does it align with the project's philosophy?"
  validations:
  required: true
- type: checkboxes
  id: standards-checklist
  attributes:
  label: Standards Checklist
  description: "Please confirm that an image for this image can meet our project standards."
  options: - label: Can it be run from a distroless or minimal Alpine base image?
  required: true - label: Does the application support running as a non-root user?
  required: true - label: Does the application provide a healthcheck endpoint (e.g., an HTTP endpoint or a command)?
  required: true - label: Is its configuration manageable via environment variables?
  required: true
---
