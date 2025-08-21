const express = require('express');
const path = require('path');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;
const ollamaUrl = process.env.OLLAMA_URL || 'http://localhost:11434/api/generate';

// Middleware
app.use(express.static(path.join(__dirname, 'src', 'frontend')));
app.use(bodyParser.json());

// API endpoints
app.get('/api/modules', (req, res) => {
    res.json({
        registration: {
            title: 'Student Registration',
            description: 'Manage your decentralized identity, link your wallet, and control your learning journey from a single, secure dashboard. Your identity is your own.'
        },
        syllabus: {
            title: 'AI Syllabus Creation',
            description: 'Leverage AI to generate personalized and adaptive learning paths tailored to your goals. Choose from various templates and customize your curriculum.'
        },
        content: {
            title: 'Content Generation',
            description: 'Access a rich library of AI-generated, curriculum-aligned content in various formats. All content is license-aware and ready for remixing.'
        },
        evaluation: {
            title: 'Automated Evaluation',
            description: 'Receive instant, rubric-based feedback on your work. Our AI-powered evaluation service helps you track your progress and identify areas for improvement.'
        },
        credentialing: {
            title: 'NFT Credentialing',
            description: 'Mint your course completions and achievements as verifiable, immutable NFT credentials on the blockchain. Showcase your skills to the world.'
        },
        governance: {
            title: 'Student-Only Governance',
            description: 'Participate in the decentralized governance of the SageEduMint platform. Propose and vote on changes, and help shape the future of education.'
        }
    });
});

app.post('/api/prompt', async (req, res) => {
    const { prompt, model } = req.body;

    if (!prompt || !model) {
        return res.status(400).json({ error: 'Prompt and model are required.' });
    }

    try {
        const response = await axios.post(ollamaUrl, {
            model: model,
            prompt: prompt,
            stream: false
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error contacting Ollama:', error.message);
        res.status(500).json({ error: 'Failed to get response from Ollama server.' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});