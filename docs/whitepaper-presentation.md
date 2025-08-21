---
marp: true
theme: default
paginate: true
title: SageEduMint: Modular AI-Powered, Student-Only Education Services
---

## 🔍 Abstract

- For-profit, modular AI-powered education services  
- **Faculty-less, admin-less, instructor-less**  
- Only students—no other roles  
- Services: AI syllabus creation, content generation, automated evaluation  
- Self-serve, scalable, verifiable credentials  
- License-aware, blockchain-enabled

---

## 🎯 Vision

- Empower self-driven learners  
- Scalable, adaptive, verifiable learning  
- No faculty, admins, or instructors  
- Students are the only users and beneficiaries

---

## 🧱 Architectural Principles

- **Student-Only**: No other roles exist  
- **Service-Oriented**: APIs and managed services  
- **Modular**: Customizable, version-controlled  
- **Passive Infrastructure**: Static-first, scalable  
- **Local AI**: On-premises or managed cloud  
- **License-Aware**: PUCL-1.0, Creative Commons

---

## 🗺️ Project & University-as-a-Service Structure

<div class="mermaid">
graph TD
  A[Student] --> B[Self-Service Dashboard]
  B --> C[AI Syllabus Creation Service]
  B --> D[Content Generation Service]
  B --> E[Automated Evaluation Service]
  B --> F[NFT Credentialing Optional]
  B --> G[Student Feedback & Support]
  C --> H[Ollama AI Engine]
  D --> H
  E --> H
  F --> I[Blockchain / IPFS]
</div>

---

## 🧠 Core Service Modules

- **Student Registration**: API onboarding, wallet/email identity  
- **AI Syllabus Creation**: Adaptive, per-student, SaaS/API  
- **Content Generation**: AI-generated, customizable  
- **Automated Evaluation**: Rubric-based, AI feedback  
- **NFT Credentialing**: Verifiable, optional

---

## 🏛️ Governance & Engagement

- **Student-Only Governance**: No admins, faculty, or staff  
- **Self-Service**: Students manage learning, credentials, usage  
- **License Governance**: Students select license tiers

---

## 📚 Licensing Stack

| Tier    | License      | Use Case                        |
|---------|--------------|---------------------------------|
| Tier 1  | PUCL-1.0     | Copyleft remixing with attribution |
| Tier 2  | CC BY-NC-SA  | Non-commercial remixing         |
| Tier 3  | CC BY-NC-ND  | Protected, non-remixable content|

---

## 🧩 Tech Stack Overview

| Layer         | Stack                                   |
|---------------|-----------------------------------------|
| Hosting       | GitHub Pages / Cloudflare / SaaS        |
| AI            | Ollama (LLaMA, Mistral)                |
| Content       | Markdown + Hugo/Zola                    |
| Credentialing | OpenSea / Thirdweb / ERC-721            |
| Governance    | Self-service dashboard                  |
| Licensing     | PUCL-1.0 + CC tiers                     |

---

## 🚀 Roadmap

| Phase   | Milestone                                      |
|---------|------------------------------------------------|
| Q3 2025 | Launch AI syllabus/content APIs                |
| Q4 2025 | Automated evaluation, NFT credentialing        |
| Q1 2026 | Custom branding, compliance features           |
| Q2 2026 | Global expansion, analytics modules            |

---

## 🌐 Impact & Philosophy

- **No gatekeepers**: Students are fully autonomous  
- **AI-powered learning, assessment, credentialing**  
- **Continuous innovation, robust support**  
- **Every asset is verifiable and customizable**

---

## 🏛️ Platform Map (Detailed)

<div class="mermaid">
flowchart TD
  subgraph Student
    S1(Student)
  end
  S1 --> S2[Self-Service Dashboard]
  S2 --> S3[AI Syllabus Creation]
  S2 --> S4[Content Generation]
  S2 --> S5[Automated Evaluation]
  S2 --> S6[NFT Credentialing]
  S2 --> S7[Feedback & Support]
  S3 --> S8[Ollama AI Engine]
  S4 --> S8
  S5 --> S8
  S6 --> S9[Blockchain/IPFS]
  S2 -.-> S10[License Selection]
</div>

---

## Thank You

- Questions?  
- [sageedumint.com](https://sageedumint.com)  
- Student-Only, AI-Powered, Modular Education
