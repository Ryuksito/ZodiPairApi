import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from typing import List

from app.config import HOST, PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASS
from app.models import (
    UserValidationModel,
    UserListModel,
    GetUserModel,
    GetRandomUsersModel,
    CreateUserModel,
    GetProfileModel,
    CreateProfileModel
)

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": HOST,
    "port": PORT,
    "database": DATABASE_NAME,
    "user": DATABASE_USER,
    "password": DATABASE_PASS,
}

class ZodiPairDB:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        """Implementación del patrón Singleton"""
        if not cls._instance:
            cls._instance = super(ZodiPairDB, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión a la base de datos"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Connected to the database successfully.")
        except psycopg2.Error as e:
            print(f"Failed to connect to the database: {e}")
            raise

    def create_profile(self, profile_data: CreateProfileModel) -> GetProfileModel:
        """Crea un perfil y retorna el perfil creado"""
        query = """
        INSERT INTO profile (img, description, age, gender, target_gender, zodiac_symbol, imgs)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
        """
        self.cursor.execute(
            query,
            (
                profile_data.img,
                profile_data.description,
                profile_data.age,
                profile_data.gender,
                profile_data.target_gender,
                profile_data.zodiac_symbol,
                profile_data.imgs,
            ),
        )
        self.connection.commit()
        result = self.cursor.fetchone()
        return GetProfileModel(**result)

    def create_user(self, user_data: CreateUserModel) -> GetUserModel:
        """Crea un usuario asociado a un perfil y retorna el usuario creado"""
        user_id = str(uuid.uuid4())
        query = """
        INSERT INTO "users" (id, user_name, password, profile_id, requests_id, chats_id)
        VALUES (%s, %s, %s, %s, NULL, NULL)
        RETURNING *;
        """
        self.cursor.execute(
            query,
            (user_id, user_data.user_name, user_data.password, user_data.profile_id),
        )
        self.connection.commit()
        result = self.cursor.fetchone()
        return GetUserModel(**result)

    def get_users(self) -> UserListModel:
        """Obtiene todos los usuarios"""
        query = "SELECT * FROM \"users\";"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        users = [GetUserModel(**user) for user in results]
        return UserListModel(users=users)

    def get_user(self, validation_data: UserValidationModel) -> GetUserModel:
        """Obtiene un usuario específico basado en el nombre de usuario y la contraseña"""
        query = """
        SELECT * 
        FROM "users"
        WHERE user_name = %s AND password = %s;
        """
        self.cursor.execute(
            query, (validation_data.user_name, validation_data.password)
        )
        result = self.cursor.fetchone()
        if not result:
            raise ValueError("Invalid username or password.")
        return GetUserModel(**result)

    def get_random_users(self, get_random_users: GetRandomUsersModel) -> UserListModel:
        """Obtiene n usuarios aleatorios excluyendo al usuario con el ID especificado"""
        query = """
        SELECT * FROM "users"
        WHERE id != %s
        ORDER BY RANDOM()
        LIMIT %s;
        """
        self.cursor.execute(query, (get_random_users.id, get_random_users.count))
        results = self.cursor.fetchall()
        users = [GetUserModel(**user) for user in results]
        return UserListModel(users=users)

    def get_profile(self, user_id: str) -> GetProfileModel:
        """Obtiene el perfil de un usuario específico por UUID"""
        query = """
        SELECT p.*
        FROM profile p
        JOIN "users" u ON u.profile_id = p.id
        WHERE u.id = %s;
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"No profile found for user_id: {user_id}")
        return GetProfileModel(**result)

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")