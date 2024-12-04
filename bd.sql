-- Database: zodipair

-- DROP DATABASE IF EXISTS zodipair;

CREATE DATABASE zodipair
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Panama.1252'
    LC_CTYPE = 'Spanish_Panama.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE profile (
    id SERIAL PRIMARY KEY, -- ID autoincremental para referencia desde User
    img TEXT NOT NULL, -- URL de la imagen de perfil
    description TEXT, -- Descripción del perfil
    age INT NOT NULL CHECK (age > 0), -- Años, debe ser mayor a 0
    gender VARCHAR(10) CHECK (gender IN ('male', 'female')), -- Género del usuario
    target_gender VARCHAR(10) CHECK (target_gender IN ('male', 'female')), -- Género objetivo
    zodiac_symbol VARCHAR(20) CHECK (zodiac_symbol IN ('aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces')), -- Signo zodiacal
    imgs TEXT[] -- Lista de URLs de fotos del perfil
);

CREATE TABLE requests (
    id SERIAL PRIMARY KEY, -- ID autoincremental para referencia desde User
    hearts UUID[], -- Lista de IDs de usuarios que enviaron "hearts"
    hot_hearts UUID[] -- Lista de IDs de usuarios que enviaron "hot hearts"
);


CREATE TABLE users (
    id UUID PRIMARY KEY, -- ID único, proporcionado en el query
    user_name TEXT NOT NULL, -- Nombre de usuario
    password TEXT NOT NULL, -- Contraseña del usuario
    profile_id INT REFERENCES Profile(id) ON DELETE CASCADE, -- Clave foránea hacia Profile
    requests_id INT REFERENCES Requests(id) ON DELETE CASCADE -- Clave foránea hacia Requests
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY, -- ID único autoincremental del chat
    user_1_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Primer participante
    user_2_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Segundo participante
    created_at TIMESTAMP DEFAULT NOW(), -- Fecha de creación del chat
    UNIQUE (user_1_id, user_2_id) -- Garantiza que no haya duplicados
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY, -- ID único autoincremental del mensaje
    chat_id INT REFERENCES chats(id) ON DELETE CASCADE, -- Relación con el chat
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Usuario que envió el mensaje
    content TEXT NOT NULL, -- Contenido del mensaje
    status VARCHAR(10) CHECK (status IN ('sended', 'received')), -- Estado del mensaje
    created_at TIMESTAMP DEFAULT NOW() -- Marca de tiempo para ordenar mensajes
);


SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';


SELECT * FROM "profile";

SELECT * FROM "user";