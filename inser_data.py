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
path = 'app/images/users/86b3fb32981740efbceb15e44036e988/'
url = '/'.join(path.split('/')[-2:-1]) + '/'
print('\n'.join(['"'+url+img+'",' for img in os.listdir(path)]))                                              

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
        "img": "5479ed10e41742d5a82e9e919a5125e0/0a5c2b9e-9b6f-4fd2-8a3d-5dfd39c32983.jpg", 
        "description": "Hey there! I’m Scarlett, an actress with a passion for art and storytelling. You might know me from my Marvel adventures as Black Widow. When I’m not working, I enjoy spending time with my family and exploring new creative projects.", 
        "imgs": [
            "5479ed10e41742d5a82e9e919a5125e0/0a5c2b9e-9b6f-4fd2-8a3d-5dfd39c32983.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/15ff670c-8862-4639-9598-c2c74b1dd1a7.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/6f818e58-aba1-4030-b49e-cd43d6188c2e.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/b661dd34-55f1-47be-9ad4-03e68dc8e199.jpg",
            "5479ed10e41742d5a82e9e919a5125e0/dcdb4992-1854-4c1d-87eb-1e770faae872.jpg",
        ]},
    {
        "name": "Dwayne Johnson", 
        "age": 51, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "taurus", 
        "img": "9101d5c205974d7a9285237c9bd14ceb/3790b84e-e1a0-4b05-a3d0-624826942726.jpg",
        "description": "What’s up? I’m Dwayne, but you can call me The Rock. I’m all about hard work, family, and a good gym session. Whether I’m acting, producing, or sipping my Teremana tequila, I live for big dreams and even bigger laughs.", 
        "imgs": [
            "9101d5c205974d7a9285237c9bd14ceb/3790b84e-e1a0-4b05-a3d0-624826942726.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/3918f929-0507-40f4-9927-2b8a7c1cdb18.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/75ebcab4-ad7c-4ab3-b0a9-44f44bd28ef6.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/c107dadb-b90d-47d9-a472-a135b838722f.jpg",
            "9101d5c205974d7a9285237c9bd14ceb/c818e545-31b9-4220-b650-994be39b4188.jpg",
        ]},
    {
        "name": "Tom Cruise", 
        "age": 61, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "cancer", 
        "img": "18139f8d2b0b4e86a69d2a20919c6d91/14cea8aa-5ee3-43db-829e-d2d6b8fb69dd.jpg",
        "description": "Hi, I’m Tom! I live for adventure, whether it’s performing my own stunts or pushing boundaries on and off screen. I love extreme sports, action movies, and chasing the next big thrill. Let’s make every moment an adventure!", 
        "imgs": [
            "18139f8d2b0b4e86a69d2a20919c6d91/14cea8aa-5ee3-43db-829e-d2d6b8fb69dd.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/26092d02-fdd3-427e-8a29-7566da5442ee.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/3eec1d6a-f836-4f17-82ac-ee86948f5450.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/9907e32a-3abb-4fef-84f2-4e3126b9624d.jpg",
            "18139f8d2b0b4e86a69d2a20919c6d91/d68cf79c-f875-4a03-8667-2f968f1e52be.jpg",
        ]},
    {
        "name": "Ariana Grande", 
        "age": 30, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "cancer", 
        "img": "286937237eb64e1b9594910ca07c33e2/63313d2f-d7ac-492c-8ea9-c82c8bf736dc.jpg",
        "description": "Hey, I’m Ariana! Singing and performing are my passions, but I also love connecting with people and spreading positivity. Whether I’m in the studio or on stage, I pour my heart into everything I do. Music is my happy place.", 
        "imgs": [
            "286937237eb64e1b9594910ca07c33e2/63313d2f-d7ac-492c-8ea9-c82c8bf736dc.jpg",
            "286937237eb64e1b9594910ca07c33e2/8a3cee4e-a5f3-433a-8bd9-cf3be21e671c.jpg",
            "286937237eb64e1b9594910ca07c33e2/d70aa6a5-1d10-4246-9f53-dbdb0faa40f4.jpg",
            "286937237eb64e1b9594910ca07c33e2/ddf767d7-68ce-4fb5-a838-04f41a3d6e3e.jpg",
            "286937237eb64e1b9594910ca07c33e2/df97c0c5-2b8d-4df8-950d-605e8cf1738b.jpg",
        ]},
    {
        "name": "Zendaya", 
        "age": 27, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "virgo", 
        "img": "c3b2b5dde4b1481c8a98e2433936fc9e/6be50d32-4d89-4742-a2de-13ab8c8acf1c.jpg",
        "description": "Hi, I’m Zendaya! I’m an actress and fashion lover who’s passionate about making a difference. When I’m not on set, I enjoy experimenting with style, standing up for what I believe in, and spending time with the people I care about.", 
        "imgs": [
            "c3b2b5dde4b1481c8a98e2433936fc9e/6be50d32-4d89-4742-a2de-13ab8c8acf1c.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/8964609f-e3f6-430a-b67e-5d06b28f7fed.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/d45cdfff-e0b9-4fb9-8928-c19c5d31342d.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/f426c387-83e2-4135-bcde-afadc21cb8bc.jpg",
            "c3b2b5dde4b1481c8a98e2433936fc9e/f4b919cc-a00f-42ab-b443-70be8a876c0f.jpg",
        ]},
    {
        "name": "Beyoncé", 
        "age": 42, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "virgo", 
        "img": "c4d1a44616744074b079999966775527/1fc57985-aa26-4d7e-9e9c-d4de6cbb4c69.jpg",
        "description": "Hello, I’m Beyoncé! Music is my soul, and I love creating empowering art that moves people. I’m a proud mom and a performer at heart. Life is about balancing passion, family, and spreading love wherever I go.", 
        "imgs": [
            "c4d1a44616744074b079999966775527/1fc57985-aa26-4d7e-9e9c-d4de6cbb4c69.jpg",
            "c4d1a44616744074b079999966775527/6607ea0f-cfa7-420b-89ae-f91446ca1de1.jpg",
            "c4d1a44616744074b079999966775527/68ae2960-b17e-4254-99e5-89bfa50c8ad4.jpg",
            "c4d1a44616744074b079999966775527/979956a7-7918-4c21-87c2-5d054b4545bf.jpg",
            "c4d1a44616744074b079999966775527/ec8f426d-92cb-4ebd-a2fa-92d9f7a45c6b.jpg",
        ]},
    {
        "name": "Selena Gomez", 
        "age": 31, 
        "gender": "female", 
        "target_gender": "male", 
        "zodiac": "cancer", 
        "img": "d72e584223d24924af75b7294f3953e0/4d34957c-30a7-4647-8f71-29f9d8a74eaf.jpg",
        "description": "Hi, I’m Selena! I’m all about kindness, creativity, and living authentically. Whether I’m singing, acting, or working on my charity projects, I strive to make a difference. Mental health and meaningful connections are my priorities.", 
        "imgs": [
            "d72e584223d24924af75b7294f3953e0/4d34957c-30a7-4647-8f71-29f9d8a74eaf.jpg",
            "d72e584223d24924af75b7294f3953e0/5aeca19d-6b93-4e7a-96f9-5403ffb3db57.jpg",
            "d72e584223d24924af75b7294f3953e0/61eeb21e-ef69-4e02-85e5-9a4c7398fd07.jpg",
            "d72e584223d24924af75b7294f3953e0/b9789607-795b-49e8-8ff9-08316d1adf17.jpg",
            "d72e584223d24924af75b7294f3953e0/e0f5fa7b-7b56-4a79-8128-0ee690e5291f.jpg",
        ]},
    {
        "name": "Leonardo DiCaprio", 
        "age": 49, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "scorpio", 
        "img": "edca788023af4dbb8e270e2c4caf523d/109c77f7-cd24-4df6-843d-eb1edc64e458.jpg",
        "description": "Hi, I’m Leo! Acting is my craft, but environmental activism is my mission. I’m passionate about sustainability and preserving our planet. When I’m not on set, I’m probably working on ways to make a positive impact on the world.", 
        "imgs": [
            "edca788023af4dbb8e270e2c4caf523d/109c77f7-cd24-4df6-843d-eb1edc64e458.jpg",
            "edca788023af4dbb8e270e2c4caf523d/5c2370c4-04ed-4263-a7c1-560969ba03c0.jpg",
            "edca788023af4dbb8e270e2c4caf523d/ae991962-a40d-497e-8f91-d485ef36983a.jpg",
            "edca788023af4dbb8e270e2c4caf523d/c3005fe1-8843-4783-8c55-4d66ade26f50.jpg",
            "edca788023af4dbb8e270e2c4caf523d/ec792c12-57aa-4497-9360-ca42d51b105f.jpg",
            "edca788023af4dbb8e270e2c4caf523d/f3c8f295-c7db-46e9-a9fe-bc8cd7f5ad5f.jpg",
        ]},
    {
        "name": "Cristiano Ronaldo", 
        "age": 38, 
        "gender": "male", 
        "target_gender": "female", 
        "zodiac": "aquarius", 
        "img": "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/75dc43da-7674-4c9b-bab2-5853a473a35c.jpg",
        "description": "Hello, I’m Cristiano! Football is my life, but I’m also a proud father and a big believer in hard work. I love challenging myself, staying disciplined, and making every moment count, both on and off the field.", 
        "imgs": [
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/75dc43da-7674-4c9b-bab2-5853a473a35c.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/cb763415-a6e2-4f7e-9825-2680285d2622.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/d6349bf2-c8fb-42b3-9931-085ad10cfc95.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/e5c68dcf-a738-48ab-86e1-0b2b8fed7076.jpg",
            "fbc9cb8fd12d4a7a8abb3e9e86d14d3d/eeb1ef19-2b84-4e0a-97cb-b2cb76fe6007.jpg",
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
