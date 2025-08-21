// SageEduMint Dashboard JavaScript
console.log('SageEduMint frontend loaded.');

document.addEventListener('DOMContentLoaded', () => {
    const moduleList = document.getElementById('module-list');
    const governanceList = document.getElementById('governance-list');

    fetch('/api/modules')
        .then(response => response.json())
        .then(data => {
            for (const moduleKey in data) {
                if (data.hasOwnProperty(moduleKey)) {
                    const module = data[moduleKey];
                    const moduleItem = document.createElement('div');
                    moduleItem.classList.add('module-item');
                    moduleItem.dataset.module = moduleKey;

                    const moduleTitle = document.createElement('h3');
                    moduleTitle.textContent = module.title;

                    const moduleDescription = document.createElement('p');
                    moduleDescription.textContent = module.description;

                    moduleItem.appendChild(moduleTitle);
                    moduleItem.appendChild(moduleDescription);

                    if (moduleKey === 'governance') {
                        governanceList.appendChild(moduleItem);
                    } else {
                        moduleList.appendChild(moduleItem);
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error fetching modules:', error);
            moduleList.innerHTML = '<p>Error loading modules. Please try again later.</p>';
        });

    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    const modelInput = document.getElementById('model-input');
    const promptResponse = document.getElementById('prompt-response');

    promptForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const prompt = promptInput.value;
        const model = modelInput.value;

        if (!prompt || !model) {
            promptResponse.textContent = 'Please enter a prompt and a model name.';
            return;
        }

        promptResponse.textContent = 'Loading...';

        fetch('/api/prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt, model })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                promptResponse.textContent = `Error: ${data.error}`;
            } else {
                promptResponse.textContent = data.response;
            }
        })
        .catch(error => {
            console.error('Error sending prompt:', error);
            promptResponse.textContent = 'Error sending prompt. Please try again later.';
        });
    });
});
