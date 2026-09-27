// ws.js — Client WebSocket global de la plateforme IoT
// Utilisé pour connecter les pages qui ont besoin de données temps réel
// Le script de chaque page appelle connectWS() avec ses propres handlers

/**
 * Connexion WebSocket avec reconnexion automatique
 * @param {string} path - chemin WebSocket (ex: /ws/telemetry)
 * @param {function} onMessage - callback appelé à chaque message reçu
 * @param {function} onStatusChange - callback appelé au changement d'état (open/close)
 */
function connectWS(path, onMessage, onStatusChange) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const url = `${protocol}//${window.location.host}${path}`;

    let ws;
    let reconnectTimer;

    function connect() {
        ws = new WebSocket(url);

        ws.onopen = () => {
            if (onStatusChange) onStatusChange('connected');
            clearTimeout(reconnectTimer);
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (onMessage) onMessage(data);
            } catch (e) {
                console.warn('[WS] Message non JSON ignoré:', event.data);
            }
        };

        ws.onclose = () => {
            if (onStatusChange) onStatusChange('disconnected');
            // Reconnexion automatique après 3 secondes
            reconnectTimer = setTimeout(connect, 3000);
        };

        ws.onerror = (err) => {
            console.error('[WS] Erreur:', err);
            ws.close();
        };
    }

    connect();
}
