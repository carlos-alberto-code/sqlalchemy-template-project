# Plantilla de Inicio Rápido para SQLAlchemy y Alembic

Iniciar un proyecto que involucre bases de datos en Python con SQLAlchemy a menudo requiere configurar Alembic para manejar las migraciones de la base de datos. Este proceso incluye ajustar archivos de configuración y establecer conexiones adecuadas con la base de datos, lo cual puede ser tedioso y consumir algo de tiempo.

Esta plantilla preconfigurada elimina la carga inicial de configuración, permitiéndote enfocarte en lo esencial desde el principio: modelar y manipular tus datos. Con esta plantilla, puedes saltar directamente a definir tus modelos de datos y ejecutar tu primera migración en minutos.

### Cómo Empezar

1. **Usa la plantilla proporcionada en GitHub:** En lugar de clonar el repositorio directamente, da clic en 'use this template' y crea un nuevo repositorio para tu proyecto basado en esta plantilla (llama a tu proyecto como desees).
2. **Clona el nuevo repositorio:** En cuanto tengas listo tu repositorio remoto, clonalo en local.
3. **Modificación del nombre del proyecto:** En el archivo ``pyproject.toml`` modifica el ``name`` del proyecto y cambialo por el nombre que diste al tu repositorio.
4. **Modifica el nombre de la carpeta interna:** Una vez clonado y que estés dentro del proyecto, notarás que existe una carpeta llamada ``alembic_template``. Modifica el nombre de esa carpeta para que coincida con el nombre de tu proyecto. Cuida de usar el estilo ``snake_case`` aunque tu proyecto haya sido nombrado con el estilo ``project-name``.

    *Nota: Se sugiere que siempre nombres tus proyectos como: 'point-of-sale', 'punto-de-venta', 'my-app', etc.*

---

El proyecto usa poetry para gestionar las dependencias, por lo que es recomendable que estes usando esta herramienta en tus proyectos también; aunque existen formas de usar las herramientas de entorno virtual proporcionadas por Python para hacer uso de esta plantilla, sin embargo, este texto no proporciona un workflow sobre cómo hacerlo.

De forma predeterminada poetry considera que vas a crear un paquete, razón por la cual existe una carpeta llamada ``alembic_template``. Si no desesar crear un paquete que pueda ser publicado en el PyPI, entonces haz uso de poetry para indicar que sólo requieres la herramienta para gestionar las dependencias y puedes eliminar esa carpeta.

Si no estas familiarizado con poetry es preferible que leas un poco la cdocumentación en la página oficial; No es necesario que leas toda la información, con que puedas usar los comandos básicos es sufienciente para poner en marcha un proyecto.

### Poner en marcha un proyecto

El workflow para trabajar inmediatamente con un proyecto basado en esta plantilla es el siguiente:

1. Tener configurado el entorno de desarrollo
2. Activar el entorno virtual y seleccionar el interprete
3. Instalas las dependencias
4. Configurar las variables de entorno
5. Ejecutar la migración inicial
6. Definir modelos y ejecución migraciones

Este flujo de trabajo es considerando que ya tienes un entorno de desarrollo listo para trabajar con Python y bases de datos en MySQL. Si no has configurado tu entorno de desarrollo, podrían servirte las siguientes herramientas, aunque puedes usar las de tu preferencia.

#### 1. Configuración del entorno de desarrollo

- vscode: Aunque puedes usar el editor de tu preferencia, todo lo que se hace aquí está hecho en vscode ya que hay extensiones que permiten trabajar con MySQL desde el edito sin necesidad de usar el Workbench de MySQL.
- Tener un servidor de MySQL instalado localmente, de preferencia una versión '^8'
- Instalar la siguiente extensión en vscode: https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2. Una vez instalada, es necesario que especifíques tus credenciales. Para ello se da por sentado que ya has hecho la labor de levantar el servidor MySQL y administrar tus credenciales de acceso. Por simpleza, la plantilla está para un usuario con contraseña y con conexión localhost y puerto predeterminado, razón por la que en las variables de entorno no está el puerto.

Dado que SQLAlchemy está para funcionar con cualquier motor de base de datos, es posible que en lugar de MySQL queiras usar PostgreSQL, si levantas el servidor de la misma forma que en MySQL, no habrá problemas en las variables de entorno, pero sí los habrá en la ``DATABASE_URI``. Por lo que en este caso, la plantilla tendría que ser modificada. Esa modificación implica instalar un conector para ese motor de base de datos y modificar la URI de conexión en dos archivos: ``database/connection.py`` y en ``alembic/env.py``. En estos archivos está algo como: ``DATABASE_URI = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"`` que debería ser modificado para adaptarse al conector instalado para el motor de base de datos que estés utilizando. Luego puedes eliminar la dependencia que se usa en esta plantilla: ``mysql-connector-python``.

#### 2. Activar el entorno virtual y seleccionar el interprete

Una vez que hayas clonado el repositorio, puedes comenzar se activará un entorno virtual gestionado por poetry, si estás usando vscode, a veces las cosas pueden demorar un poco en cargarse o no actualizarse. Lo recomendable es abrir siempre una nueva terminal cada que hagas algo importante como instalaciones o cosas por el estilo. Una vez en la nueva terminal,  usa el comando ``poetry shell`` para activar el entorno virtual. Ahora será necesario escoger el interprete, para ello puedes presionar ``ctrl + shift + p`` y buscar *Python: Select interpreter*. Esperas un momento en lo que vscode carga el interprete para este proyecto y lo seleccionas. Esto es necesario para que uses el entorno virtual gestionado por poetry y que uses la versión de python definida en el archivo ``.toml``, de otra forma, si tienes más versiones de Python instaladas, podría haber errores, y en un caso extremo, podrías instalar todas las dependencias en tu máquina y eso no es algo deseable.

#### 3. Instalas las dependencias

Poetry es una herramienta muy poderosa, en muy diferente a la gestión de entornos virtuale oficial de Python. Pienso que en algún momento Python adoptará poetry como herramienta oficial en lugar de la creción del entorno con pip.

Instalar las dependencias es sencillo, tan sólo escribe en la consola ``poetry install``, este leerá las dependencias en el archivo ``.toml`` y las instalará en el entorno virtual que este ha creado por ti. Las dependencias necesarias son ``alembic``, ``sqlalchemy``, ``python-dotenv`` y por supuesto ``python``. Más adelante si deseas mejorar las versiones de estas, será necesario que sepas usar poetry para este fin.

#### 4. Configurar las variables de entorno

Para trabajar adecuadamente con un nuevo proyecto que involucre bases de datos, es necesario que las credenciales se proporcionen con variables de entorno para evitar subir información sencible a los registros de git y de la terminal. Se usa el módulo dotenv para cargar las variables de entorno. Sólo es necesario que crees un archivo ``.env`` en la raíz del proyecto y declarar cuatro variables:

- ``HOST = localhost``
- ``USERNAME = tuUserName``
- ``PASSWORD = tuPassWORD``
- ``DATABASE = data_base_name``

El nombre de la base de datos debe coincidir con la base de datos física. Si usas varias bases de datos, ya sea una para desarrollo y una base de datos estables, tendrás que cambiar el nombre aquí para que la conexión se dirija hacia esa base de datos. Cualquier cambio en las credenciales de tu base de datos física, tendrás que modificar aquí para dirigir la conexión. Si usas la extensión que recomendé, podrás crear una nueva base de datos fácilmente.

Un uso sobre esa extensión está fuera del propósito de este texto, para saber cómo útilizar esa extensión, te sugiero que experimentes un poco con ella, no romperás nada, y si necesitas usar más características, entonces es preferible ir a la documentación oficial.

#### 5. Ejecutar la migración inicial

Ya que tienes tus variables de entorno listas para la conexión, será necesario que abras una nueva terminal y ejecutes el siguiente comando: ``poetry run alembic upgrade head``. Esto hará que tu base de datos tenga una tabla de demostración incial.

*Cautela:* Si no tenías una base de datos creada, esto no funcionará. Será necesario que tengas una base de datos creada, de preferencia usa las herramientas recomendadas, y nombra a tu base de datos para que coincida con la variable de entorno ``DATABASE``.

Si has todo ha salido bien, en este momento ya tendrías una tabla de demostración. Y como notarás no fue necesario ejecutar ningún comando DDL para crear esa tabla, sino que alembic gestiona eso por nosotros.

#### 6. Definición de los modelos y ejecución de migraciones

Definir tus modelos implica saber cómo declarar modelos para usar SQLAlchemy. Aprender sobre SQLAlchemy está fuera del propósito de este texto, por lo que se da por hecho que sabes cómo manejar esa herramienta.

Puedes comenzar a definir tus modelos de la siguiente forma en el archivo que está en ``database/models.py`` Si tu aplicación no es excesivamente grande, puedes estar seguro que todos los modelos pueden ser declarados en este archivo. Un ejemplo de cómo sería esto es:

```python
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Heredar de la clase Base definida en el archivo

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)


class Book(Base):
    # Se declará está entidad
    pass
```

A manera de ejemplo se definió un modelo, si ya has ejecutado la migración del paso anterior, entonces ahora puedes eliminar ese código y comenzar a declarar tus propios modelos. Una vez que hayas terminado de declarar tus modelos es momento de ejecutar tus migraciones. Usa los comandos de alembic para generar la migraciones:
- ``poetry run alembic revision --autogenerate -m 'Mensaje sobre tu migración'``: Para una revisión autogenerada
- ``poetry run alembic upgrade head``: Para actualizar la base de datos física

Errores en la definición de modelos y problemas con las migraciones que hagas a partir de aquí pueden deberse a un mal uso. Para ello lee la documentación de sqlalchemy y alembic. Por ejemplo, puede sucederte que en la declaración de un modelo no hayas colocado el tipo de dato. La revisión podría generarse correctamente pero cuando ejecutes el comando de acualización, tendrás problemas en la base de datos física, ya que comúnmente cualquier motor, requiere de que específiques el tipo de dato de esa columna.

Un curso de alembic y sqlalchemy están fuera del alcance del texto.
A partir de aquí, el proceso de desarrollo y migraciones sigue siendo el mismo. Declaara modelos y ejecuta migraciones con esta plantilla de arranque rápido. Si eres nuevo, esto no te parecerá prometedor ya que configurar tu entorno de desarrollo es lo que podría quitarte algo de tiempo. Pero una vez que tengas un buen entorno de desarrollo, en 2 minutos puedes estár trabajando en un proyecto con ayuda de esta plantilla.

Espero que la plantilla te sirva, si detectas algún error o mejora no dudes en mandarme mensaje. Puedes hacerlo a través de LinkedIn: www.linkedin.com/in/carlos-alberto-code. En algún momento esta plantilla se extendera para trbajar con múltiples bases de datos para los casos de sistemas distribuidos y planeo crear algunos scrips para que evites modificar las cosas manualmente. El objetivo es llegar a una declaración de tus variables de entorno y ejecutar inmediatamente la migración inicial.