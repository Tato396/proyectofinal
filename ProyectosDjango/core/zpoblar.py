import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='carlos',
        tipo='Cliente', 
        nombre='carlos', 
        apellido='carrillo', 
        correo=test_user_email if test_user_email else 'carlos@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/user6.png')

    crear_usuario(
        username='joa',
        tipo='Cliente', 
        nombre='joaquin', 
        apellido='lagos', 
        correo=test_user_email if test_user_email else 'joaquin@marvels.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/user4.png')

    crear_usuario(
        username='eme',
        tipo='Cliente', 
        nombre='Emerson', 
        apellido='Lemunao', 
        correo=test_user_email if test_user_email else 'emerson@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user2.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo=test_user_email if test_user_email else 'sjohansson@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user7.jpg')

    crear_usuario(
        username='marcelo',
        tipo='Administrador', 
        nombre='marcelo', 
        apellido='delchuce', 
        correo=test_user_email if test_user_email else 'delchuce@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user3.jpg')
    
    crear_usuario(
        username='tauro',
        tipo='Administrador', 
        nombre='alde', 
        apellido='baran', 
        correo=test_user_email if test_user_email else 'aldebaran@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/user5.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='clark',
        apellido='kent',
        correo=test_user_email if test_user_email else 'superman@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/user1.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Grand Theft Auto V',
            'descripcion': 'Grand Theft AutoV te sumerge en la soleada ciudad de Los Santos y sus alrededores, donde seguirás las historias entrelazadas de tres criminales muy diferentes mientras planean y ejecutan audaces atracos para sobrevivir en una ciudad despiadada. Disfruta de un mundo abierto enorme y detallado, con una gran variedad de misiones, actividades y desafíos, además de un modo online multijugador en constante evolución.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/GTA5.png'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Red Dead Redemption 2',
            'descripcion': 'Red Dead Redemption 2 es una épica historia sobre la vida en el despiadado corazón de América. El vasto y evocador mundo del juego también proporcionará la base para una nueva experiencia multijugador online.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/rdr2.png'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Call of Duty: Modern Warfare II',
            'descripcion': 'Call of Duty: Modern Warfare II es la secuela de Modern Warfare (2019) y la decimonovena entrega de la serie Call of Duty. La campaña de Modern Warfare II sigue a la Fuerza Operativa 141 mientras persiguen a un terrorista iraní llamado Hassan Zyani, quien adquirió un misil balístico estadounidense.',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/modernw2.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Mortal Kombat 1',
            'descripcion': 'Descubre el nuevo universo de Mortal Kombat, creado por el Dios del Fuego Liu Kang. ¡Mortal Kombat™ 1 marca el comienzo de una nueva era para la icónica franquicia, con un sistema de lucha, modos de juego y Fatalities nuevos!',
            'precio': 40000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/Mortal_1.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Dead Island 2',
            'descripcion': 'Un virus mortal se extiende por Los Ángeles y está convirtiendo a sus habitantes en zombis. Te mordieron y te infectaron, pero tu cuerpo es inmune. Descubre la verdad tras el brote y quién (o qué) eres. Sobrevive, evoluciona y conviértete en el matazombis supremo.',
            'precio': 21990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/DeadIsalnd2.png'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Elden Ring',
            'descripcion': 'Elden Ring es un juego de rol de acción desarrollado por FromSoftware y publicado por Bandai Namco Entertainment. El juego se desarrolla en un mundo abierto llamado las Tierras Intermedias, donde los jugadores controlan a un personaje conocido como el Sinluz, que debe viajar por el mundo para restaurar el Elden Ring, un poderoso artefacto que ha sido destruido.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/elden-ring-ps5.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Jujutsu Kaisen Cursed Clash',
            'descripcion': '¡Domina el poder de tus hechiceros y espíritus malditos favoritos! ¡Únete a tu colega y sumérgete en el mundo de JUJUTSU KAISEN en este juego de lucha de 2 contra 2 lleno de acción!',
            'precio': 69990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/JuJuTsu.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Metro 2033 Redux',
            'descripcion': 'In 2013 the world was devastated by an apocalyptic event, annihilating almost all mankind and turning the Earths surface into a poisonous wasteland. A handful of survivors took refuge in the depths of the Moscow underground, and human civilization entered a new Dark Age. The year is 2033.',
            'precio': 14990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Metro_Redux.png'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'The Legend of Zelda: Breath of the Wild',
            'descripcion': 'The Legend of Zelda: Breath of the Wild es un videojuego de acción-aventura desarrollado y publicado por Nintendo para las consolas Nintendo Switch y Wii U. El juego es la decimonovena entrega de la serie The Legend of Zelda y fue lanzado mundialmente en marzo de 2017. Breath of the Wild es un juego de mundo abierto que permite a los jugadores explorar libremente el reino de Hyrule.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Zelda Switch.png'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'art of rally',
            'descripcion': 'Corre en la era dorada del Rally. Maneja icónicos carros que van desde los 60s hasta el Grupo B a través de etapas desafiantes en ambientes estilizados inspirados en ubicaciones reales. ¿Serás tú el maestro del art del rally?',
            'precio': 12990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/ArtOfRally.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Rides',
            'descripcion': '¡Todo listo para vivir la mejor experiencia de juego que los fanáticos de las motocicletas merecen! RIDE 4 encenderá tu alma competitiva con cientos de motos, docenas de circuitos y un inigualable nivel de realismo.',
            'precio': 35990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/RIDE5_PS5.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sonic Racing',
            'descripcion': 'Team Sonic Racing combina los mejores elementos de arcade y carreras de estilo competitivo de ritmo rápido mientras te enfrentas a amigos en intensas carreras multijugador.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Sonic_Racing.jpeg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Civilization VI',
            'descripcion': 'Civilization VI es un juego de estrategia por turnos en el que los jugadores intentan construir un imperio que resista el paso del tiempo. Explora un nuevo mundo, investiga tecnologías, conquista a tus enemigos y enfréntate a los líderes más famosos de la historia mientras intentas construir la civilización más grande jamás conocida.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/cv6.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'XCOM 2',
            'descripcion': 'XCOM 2 es la secuela del galardonado juego de estrategia XCOM: Enemy Unknown. La Tierra ha cambiado y ahora está bajo control alienígena. Como líder de XCOM, una organización militar secreta, debes reconstruir la base de operaciones, reclutar nuevos soldados y liderar la resistencia para liberar a la humanidad del yugo alienígena.',
            'precio': 19990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/xcom-2.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Fifa 2023',
            'descripcion': 'FIFA 23 te trae todo el realismo del Juego de Todos con la tecnología HyperMotion2, la FIFA World Cup™ masculina y femenil, equipos de clubes femeniles, funciones de Cross-Play** y mucho más.',
            'precio': 54990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Fifa2023.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Just Dance 2023',
            'descripcion': '¡Bienvenido a la nueva era del baile con Just Dance® 2023 Edition! ¡Baila por primera vez al ritmo de «Dynamite», de BTS, y otros temazos del momento! Disfruta de una fiesta sin fin con el nuevo modo multijugador* Online, personalización, mundos 3D inmersivos y canciones y modos nuevos durante todo el año.',
            'precio': 30990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/JustDance2023.png'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Witcher 3: Wild Hunt',
            'descripcion': 'The Witcher 3: Wild Hunt es un juego de rol de acción de mundo abierto desarrollado y publicado por CD Projekt Red. El juego sigue a Geralt de Rivia, un cazador de monstruos profesional conocido como brujo, mientras busca a su hija adoptiva, Ciri, quien está siendo perseguida por la Cacería Salvaje, una fuerza espectral que busca usar sus poderes para sus propios fines.',
            'precio': 29990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/thewitcher3.jpeg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Forza Motorsport',
            'descripcion': 'Supera a la competencia en la nueva carrera. Compite con tus amigos en eventos multijugador adjudicados. Compite en más de 500 autos en pistas de fama mundial con IA de vanguardia, física avanzada y estrategia de llantas y combustible.',
            'precio': 53990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/Forza_Motorsport.webp'
        },
        {
            'id': 19,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'The Last of Us™ Part I',
            'descripcion': 'Experimenta la emocionante historia y los inolvidables personajes de The Last of Us, ganador de más de 200 premios Juego del Año.',
            'precio': 41990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/TLOUP1.png'
        },
        {
            'id': 20,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Saints Row',
            'descripcion': 'Te damos la bienvenida a Santo Ileso, una dinámica ciudad ficticia en el suroeste estadounidense. En un mundo plagado de delincuencia, en el que facciones sin ley luchan por el poder, un grupo de jóvenes emprende su propio negocio criminal, en el camino a la cima de su propio éxito.',
            'precio': 22990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/SaintsRow.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

