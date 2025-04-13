// Import our custom CSS
import '../scss/styles.scss'
// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

import Alpine from 'alpinejs'
import mammoth from "mammoth";

window.Alpine = Alpine

// Define an Alpine component to manage the game state
Alpine.data('gameManager', () => ({
    // --- Component State ---
    isLoading: false,
    error: null,
    gameData: null,
    // --- Document State (add properties for each document type) ---
    passportSrc: null,      // For PNG data URL
    accountSrc: null,       // For PDF data URL
    profileHtml: null,       // For DOCX data URL
    descriptionText: null,  // For decoded TXT content

    init() {
        console.log('Game manager initializing...');
        this.startNewGame();
    },

    // Helper to convert Base64 to ArrayBuffer (needed for Mammoth)
    base64ToArrayBuffer(base64) {
        try {
            const binary_string = atob(base64);
            const len = binary_string.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return bytes.buffer;
        } catch (e) {
            console.error("Error decoding base64 string:", e);
            return null;
        }
    },

    // --- Helper Function to Process Document Data ---
    async processClientData(clientData) {
        if (!clientData) {
            console.log('No client data to process.');
            this.passportSrc = null;
            this.accountSrc = null;
            this.profileHtml = null;
            this.descriptionText = null;
            return;
        }

        console.log('Processing client data for documents:', clientData);

        // --- Passport (PNG) ---
        if (clientData.passport) {
            this.passportSrc = `data:image/png;base64,${clientData.passport}`;
        } else {
            this.passportSrc = null; // Reset if not provided
            console.log('Passport base64 data not found.');
        }

        // --- Account (PDF) ---
        if (clientData.account) {
            this.accountSrc = `data:application/pdf;base64,${clientData.account}`;
        } else {
            this.accountSrc = null; // Reset if not provided
            console.log('Account base64 data not found.');
        }

        // --- Profile (DOCX) - Create download link ---
        if (clientData.profile) {
            const arrayBuffer = this.base64ToArrayBuffer(clientData.profile);
            const result = await mammoth.convertToHtml({ arrayBuffer: arrayBuffer });
            this.profileHtml = result.value;
        } else {
            this.profileHtml = null; // Reset if not provided
            console.log('Profile base64 data not found.');
        }

        // --- Description (TXT) - Decode base64 ---
        if (clientData.description) {
            try {
                this.descriptionText = atob(clientData.description);
            } catch (e) {
                console.error('Error decoding description base64:', e);
                this.descriptionText = 'Error decoding document content.';
            }
        } else {
            this.descriptionText = null; // Reset if not provided
            console.log('Description base64 data not found.');
        }
    },

    startNewGame() {
        this.isLoading = true;
        this.error = null;
        this.gameData = null;
        // Reset document states
        this.processClientData(null);

        // Use the browser's fetch API
        fetch('http://127.0.0.1:5000/new-game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                   throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
                }).catch(() => {
                   throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('New game data received:', data);
            this.gameData = data;
            // Process documents from the new game data
            this.processClientData(this.gameData.client_data);
        })
        .catch(error => {
            console.error('Error starting new game:', error);
            this.error = error.message || 'Failed to start game. Check console/backend.';
        })
        .finally(() => {
            this.isLoading = false;
        });
    },

    submitDecision(decision) {
        if (!decision || (decision !== 'Accept' && decision !== 'Reject')) {
             this.error = 'Invalid decision provided.';
             console.error('Invalid decision:', decision);
             return;
        }
        if (!this.gameData || !this.gameData.session_id || !this.gameData.client_id) {
            this.error = 'Missing game data (session or client ID). Cannot submit decision.';
            console.error('Missing game data for decision:', this.gameData);
            return;
        }
        if (this.isLoading) {
            console.warn('Already processing a request.');
            return;
        }
        if (this.gameData.status === 'gameover') {
             console.warn('Game is already over.');
             return;
        }

        console.log(`Submitting decision: ${decision} for client: ${this.gameData.client_id}`);
        this.isLoading = true;
        this.error = null;
        // Reset document states before fetching new data
        this.processClientData(null);

        const requestBody = {
            decision: decision,
            session_id: this.gameData.session_id,
            client_id: this.gameData.client_id
        };

        fetch('http://127.0.0.1:5000/next', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
             if (!response.ok) {
                return response.text().then(text => {
                    try {
                        const errData = JSON.parse(text);
                        throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
                    } catch (e) {
                        throw new Error(text || `HTTP error! status: ${response.status}`);
                    }
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Decision response received:', data);
            // Update core game data
            this.gameData.score = data.score;
            this.gameData.status = data.status;
            this.gameData.decision = data.decision;
            this.gameData.bot_reason = data.bot_reason;
            this.gameData.bot_decision = data.bot_decision;

            // Update client_id and client_data only if present and game not over
            if (data.status !== 'gameover') {
                if (data.client_id) {
                    this.gameData.client_id = data.client_id;
                } else {
                     console.warn("Game continues but no new client ID received from /next endpoint.");
                }

                if (data.client_data) {
                     this.gameData.client_data = data.client_data;
                     // Process documents from the new client data
                     this.processClientData(this.gameData.client_data);
                } else {
                     console.warn("Game continues but no new client data received from /next endpoint.");
                     this.gameData.client_data = null; // Clear old client data if none received
                     this.processClientData(null); // Ensure docs are cleared
                }
            } else {
                console.log('Game Over! Final score:', this.gameData.score);
                // Optionally clear client_id and client_data on gameover
                // this.gameData.client_id = null;
                // this.gameData.client_data = null;
                // this.processClientData(null); // Clear docs on game over
            }
        })
        .catch(error => {
            console.error('Error submitting decision:', error);
            this.error = error.message || 'Failed to submit decision.';
        })
        .finally(() => {
            this.isLoading = false;
        });
    }
}));


Alpine.start()