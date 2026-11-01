-- Una fila guarda el progreso JSON de una ranura, identificada por jugador y número.
CREATE TABLE IF NOT EXISTS save_slots (
    player_id VARCHAR(64) NOT NULL, -- Identificador del perfil del jugador.
    slot_number TINYINT UNSIGNED NOT NULL, -- La interfaz permite las ranuras 1, 2 y 3.
    payload JSON NOT NULL, -- Estado serializado de la partida.
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Fecha de la última escritura.
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (player_id, slot_number), -- Impide duplicados por jugador y ranura.
    CONSTRAINT chk_save_slots_number CHECK (slot_number BETWEEN 1 AND 3) -- Valida el rango permitido.
);
