# Infrastructure Layer

This module describes the infrastructure components for SageEduMint, focusing on minimal, scalable, and remixable foundations.

## Components:

- **Static Hosting**: Utilizes platforms like GitHub Pages, Netlify, or Cloudflare Pages for passive, Markdown-first content delivery. This ensures high availability and low operational costs.

- **DNS & Routing**: Cloudflare DNS is preferred for robust domain name resolution and traffic management. Ethereum Name Service (ENS) can be integrated for decentralized identity and domain resolution, supporting decentralized identity for learners and content.

- **Version Control**: Git and platforms like GitHub or Gitea are central to content management and governance. All educational content, syllabus definitions, and governance proposals are version-controlled, enabling transparent auditing and collaborative development.

- **Containerization (optional)**: Docker or Podman can be used for encapsulating local AI models (like Ollama) or specific microservices that require isolated environments. This provides flexibility for deploying specialized components without affecting the core static infrastructure.

This layer emphasizes a static-first approach to ensure scalability, transparency, and cost-effectiveness, aligning with the decentralized and modular principles of SageEduMint.