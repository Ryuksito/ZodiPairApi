import json
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
from typing import List
import ast

from app.config import HOST, PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASS
from app.models import (
    UserValidationModel,
    UserListModel,
    GetUserModel,
    GetRandomUsersModel,
    CreateUserModel,
    GetProfileModel,
    CreateProfileModel,
    UpdateRequestModel,
    UpdateRequestResponseModel,
    GetRequestModel,
    GetUserRequestModel,
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
    
    def find_user(self, user_id: str) -> GetUserModel:
        """
        Busca un usuario en la base de datos por su user_id y devuelve un objeto GetUserModel,
        excluyendo la contraseña.

        :param user_id: El ID del usuario a buscar.
        :return: Una instancia de GetUserModel si se encuentra el usuario, None si no se encuentra.
        """
        query = """
        SELECT u.id, u.user_name, u.profile_id, u.requests_id
        FROM users u
        WHERE u.id = %s;
        """
        self.cursor.execute(query, (user_id,))
        user_data = self.cursor.fetchone()

        if user_data is None:
            return None  # Usuario no encontrado

        # Convertir los datos en un modelo GetUserModel
        return GetUserModel(
            id=user_data["id"],
            user_name=user_data["user_name"],
            profile_id=user_data["profile_id"],
            requests_id=user_data["requests_id"],
        )

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
        """Obtiene n usuarios aleatorios excluyendo al usuario con el ID especificado y asegurando coincidencia de géneros"""
        query = """
        SELECT u.*
        FROM "users" u
        JOIN "profile" p ON u.profile_id = p.id
        WHERE u.id != %s
        AND p.gender = (
            SELECT target_gender
            FROM "profile"
            WHERE id = (
                SELECT profile_id
                FROM "users"
                WHERE id = %s
            )
        )
        ORDER BY RANDOM()
        LIMIT %s;
        """
        self.cursor.execute(query, (get_random_users.id, get_random_users.id, get_random_users.count))
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
    
    def add_request(self, update_request: UpdateRequestModel) -> bool:
        """
        Agrega un 'love' o 'hot love' a la lista de requests de un usuario.
        Si el usuario no tiene un request asociado, se crea uno nuevo.

        :param update_request: Datos de la solicitud (user_id, sender_id, is_hot_love)
        :return: True si se realiza la operación con éxito, False en caso de error
        """
        try:
            # Verificar si el usuario tiene un requests_id asociado
            self.cursor.execute("""
                SELECT requests_id FROM users WHERE id = %s
            """, (update_request.user_id,))
            user_data = self.cursor.fetchone()

            if not user_data:
                print(f"User with ID {update_request.user_id} does not exist.")
                return UpdateRequestResponseModel(status=False)

            requests_id = user_data.get("requests_id")

            if requests_id is None:
                # Crear un nuevo registro en la tabla requests si no existe
                self.cursor.execute("""
                    INSERT INTO requests (hearts, hot_hearts)
                    VALUES (%s, %s)
                    RETURNING id
                """, ([], []))
                requests_id = self.cursor.fetchone()["id"]

                # Asociar el nuevo requests_id al usuario
                self.cursor.execute("""
                    UPDATE users
                    SET requests_id = %s
                    WHERE id = %s
                """, (requests_id, update_request.user_id))
                self.connection.commit()

            # Determinar si es un 'love' o 'hot love' y actualizar la lista correspondiente
            if update_request.is_hot_love:
                self.cursor.execute("""
                    UPDATE requests
                    SET hot_hearts = array_append(hot_hearts, %s)
                    WHERE id = %s
                """, (update_request.sender_id, requests_id))
            else:
                self.cursor.execute("""
                    UPDATE requests
                    SET hearts = array_append(hearts, %s)
                    WHERE id = %s
                """, (update_request.sender_id, requests_id))

            self.connection.commit()
            return UpdateRequestResponseModel(status=True)

        except psycopg2.Error as e:
            print(f"Database error while adding request: {e}")
            self.connection.rollback()
            return UpdateRequestResponseModel(status=True)

    import ast

    def get_user_request(self, user_request: GetUserRequestModel) -> GetRequestModel:
        """
        Obtiene los datos de la request de un usuario (hearts y hot_hearts).
        Si no existe una request asociada, devuelve un resultado vacío.

        :param user_request: Modelo con el ID del usuario para buscar su request.
        :return: Modelo GetRequestModel con los datos de la request.
        """
        try:
            # Obtener el requests_id del usuario
            self.cursor.execute("""
                SELECT requests_id FROM users WHERE id = %s
            """, (user_request.user_id,))
            user_data = self.cursor.fetchone()

            if not user_data or user_data["requests_id"] is None:
                return GetRequestModel(id=-1, hearts=[], hot_hearts=[])

            requests_id = user_data["requests_id"]

            # Obtener los datos de la request con conversión de arrays a JSON
            self.cursor.execute("""
                SELECT 
                    id, 
                    array_to_json(hearts) AS hearts, 
                    array_to_json(hot_hearts) AS hot_hearts
                FROM requests
                WHERE id = %s
            """, (requests_id,))
            request_data = self.cursor.fetchone()

            if not request_data:
                return GetRequestModel(id=requests_id, hearts=[], hot_hearts=[])

            # Convertir los campos JSON a listas reales
            hearts = request_data["hearts"] if request_data["hearts"] else []
            hot_hearts = request_data["hot_hearts"] if request_data["hot_hearts"] else []

            return GetRequestModel(
                id=request_data["id"],
                hearts=hearts,
                hot_hearts=hot_hearts
            )

        except psycopg2.Error as e:
            print(f"Database error while retrieving user request: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from PostgreSQL array: {e}")
            raise



    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
