import psycopg2
import uuid

# Configuración de conexión a PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "zodipair",
    "user": "postgres",
    "password": "13Ha7ka713",
}
"""
os.system("cls")
path = 'app/images/users/fbc9cb8fd12d4a7a8abb3e9e86d14d3d/'                                             
url = '/'.join(path.split('/')[-2:-1]) + '/'
print('\n'.join(['"'+url+img+'",' for img in os.listdir('app/images/users/86b3fb32981740efbceb15e44036e988')]))

"""

# Datos a insertar
users_data = [
    {
        "name": "Leo Messi", 
        "age": 36, 
        "gender": "male", 
        "target_gender": "female",
        "zodiac": "cancer", 
        "img": "86b3fb32981740efbceb15e44036e988/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hi, I’m Leo! I’ve spent my life playing football and chasing dreams. Family is everything to me, and I enjoy quiet moments at home with my loved ones. I also love a good Argentine barbecue—simple joys make life amazing!", 
        "imgs": [
            "86b3fb32981740efbceb15e44036e988/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "86b3fb32981740efbceb15e44036e988/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "86b3fb32981740efbceb15e44036e988/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "86b3fb32981740efbceb15e44036e988/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "86b3fb32981740efbceb15e44036e988/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Scarlett Johansson",
        "age": 38, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "sagittarius", 
        "img": "5479ed10e41742d5a82e9e919a5125e0/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hey there! I’m Scarlett, an actress with a passion for art and storytelling. You might know me from my Marvel adventures as Black Widow. When I’m not working, I enjoy spending time with my family and exploring new creative projects.", 
        "imgs": [
            "5479ed10e41742d5a82e9e919a5125e0/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Dwayne Johnson", 
        "age": 51, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "taurus", 
        "img": "9101d5c205974d7a9285237c9bd14ceb/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "What’s up? I’m Dwayne, but you can call me The Rock. I’m all about hard work, family, and a good gym session. Whether I’m acting, producing, or sipping my Teremana tequila, I live for big dreams and even bigger laughs.", 
        "imgs": [
            "9101d5c205974d7a9285237c9bd14ceb/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Tom Cruise", 
        "age": 61, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "cancer", 
        "img": "18139f8d2b0b4e86a69d2a20919c6d91/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hi, I’m Tom! I live for adventure, whether it’s performing my own stunts or pushing boundaries on and off screen. I love extreme sports, action movies, and chasing the next big thrill. Let’s make every moment an adventure!", 
        "imgs": [
            "18139f8d2b0b4e86a69d2a20919c6d91/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Ariana Grande", 
        "age": 30, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "cancer", 
        "img": "286937237eb64e1b9594910ca07c33e2/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hey, I’m Ariana! Singing and performing are my passions, but I also love connecting with people and spreading positivity. Whether I’m in the studio or on stage, I pour my heart into everything I do. Music is my happy place.", 
        "imgs": [
            "286937237eb64e1b9594910ca07c33e2/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "286937237eb64e1b9594910ca07c33e2/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "286937237eb64e1b9594910ca07c33e2/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "286937237eb64e1b9594910ca07c33e2/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "286937237eb64e1b9594910ca07c33e2/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Zendaya", 
        "age": 27, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "virgo", 
        "img": "c3b2b5dde4b1481c8a98e2433936fc9e/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hi, I’m Zendaya! I’m an actress and fashion lover who’s passionate about making a difference. When I’m not on set, I enjoy experimenting with style, standing up for what I believe in, and spending time with the people I care about.", 
        "imgs": [
            "c3b2b5dde4b1481c8a98e2433936fc9e/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Beyoncé", 
        "age": 42, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "virgo", 
        "img": "c4d1a44616744074b079999966775527/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
        "description": "Hello, I’m Beyoncé! Music is my soul, and I love creating empowering art that moves people. I’m a proud mom and a performer at heart. Life is about balancing passion, family, and spreading love wherever I go.", 
        "imgs": [
            "c4d1a44616744074b079999966775527/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "c4d1a44616744074b079999966775527/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "c4d1a44616744074b079999966775527/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "c4d1a44616744074b079999966775527/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "c4d1a44616744074b079999966775527/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Selena Gomez", 
        "age": 31, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "cancer", 
        "img": "d72e584223d24924af75b7294f3953e0/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hi, I’m Selena! I’m all about kindness, creativity, and living authentically. Whether I’m singing, acting, or working on my charity projects, I strive to make a difference. Mental health and meaningful connections are my priorities.", 
        "imgs": [
            "d72e584223d24924af75b7294f3953e0/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "d72e584223d24924af75b7294f3953e0/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "d72e584223d24924af75b7294f3953e0/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "d72e584223d24924af75b7294f3953e0/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "d72e584223d24924af75b7294f3953e0/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Leonardo DiCaprio", 
        "age": 49, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "scorpio", 
        "img": "edca788023af4dbb8e270e2c4caf523d/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hi, I’m Leo! Acting is my craft, but environmental activism is my mission. I’m passionate about sustainability and preserving our planet. When I’m not on set, I’m probably working on ways to make a positive impact on the world.", 
        "imgs": [
            "edca788023af4dbb8e270e2c4caf523d/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "edca788023af4dbb8e270e2c4caf523d/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "edca788023af4dbb8e270e2c4caf523d/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "edca788023af4dbb8e270e2c4caf523d/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "edca788023af4dbb8e270e2c4caf523d/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
    {
        "name": "Cristiano Ronaldo", 
        "age": 38, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "aquarius", 
        "img": "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg", 
        "description": "Hello, I’m Cristiano! Football is my life, but I’m also a proud father and a big believer in hard work. I love challenging myself, staying disciplined, and making every moment count, both on and off the field.", 
        "imgs": [
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/5bffe5ef-92e7-4dfe-912f-24ea8fe4ad5d.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/6d68dafb-628e-4558-952d-77aa35ee4346.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/b69b11be-9c21-43f4-86a3-c0979e9bc679.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/ddf6257e-42ed-465a-a760-872311226639.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/f98ffd18-a574-4ba5-b98d-e28600d7dca4.jpg",
        ]},
]

# Función para insertar datos
def insert_data():
    # try:
    # Conectar a la base de datos
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for user in users_data:
        # Insertar en la tabla Profile
        cursor.execute(
            """
            INSERT INTO profile (img, description, age, gender, target_gender, zodiac_symbol, imgs)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (user["img"], user["description"], user["age"], user["gender"], user["target_gender"], user["zodiac"], user["imgs"]),
        )
        profile_id = cursor.fetchone()[0]  # Obtener el ID generado para Profile

        # Insertar en la tabla User
        print((user['img'].split('/')[-2] , user["name"], "password", profile_id))
        cursor.execute(
            """
            INSERT INTO "users" (id, user_name, password, profile_id, requests_id)
            VALUES (%s, %s, %s, %s, NULL);
            """,
            (user['img'].split('/')[-2] , user["name"], "password", profile_id),
        )

    # Confirmar transacciones
    conn.commit()
    print("Datos insertados correctamente.")
    try:
        pass
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Ejecutar la función
if __name__ == "__main__":
    insert_data()
