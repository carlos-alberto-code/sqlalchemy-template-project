El repo es una plantilla para incializar proyectos que usan sqlalchemy y alembic. El propósito es evitar la configuración de los archivos de alembic en cada proyecto, sino que en base a esta plantilla pueda comenzar a declarar los modelos y ejecutar tu primer migración en dev.

El proyecto usa poetry para gestionar las dependencias, por lo que es recomendable que estes usando esta herramienta en tus proyectos también; aunque existen formas de usar las herramientas de entorno virtual proporcionadas por Python para hacer uso de esta plantilla, sin embargo, este texto no proporciona un workflow sobre cómo hacerlo.

De forma predeterminada poetry considera que vas a crear un paquete, razón por la cual existe una carpeta llamada ``alembic_template``. Si no desesar crear un paquete que pueda ser publicado en el PyPI, entonces haz uso de poetry para indicar que sólo requieres la herramienta para gestionar las dependencias y puedes eliminar esa carpeta. Si por el contrario el proyecto es un paquete, una vez que hayas nombrado tu proyecto, deberás cambiar el nombre de la carpeta para que coincida con el nombre de tu paquete usando snacke_case (en caso de que hayas creado tu proyecto como this-case).

Las versión de las dependencias se detallan en el archivo ``pyproject.toml``. De forma predeterminada estarán definidas algunas versiones de ``sqlalchemy``, ``alembic`` y ``mysql-connector-python``; aunque puedes actualizar a otras versiones o usar versiones específicas con ayuda de poetry.

# Poner en marcha un proyecto

El workflow para trabajar inmediatamente con un proyecto basado en esta plantilla es el siguiente:

1. Activar el entorno virtual
2. Seleccionar el interprete
3. Configurar las variables de entorno
4. Definir los modelos
5. Ejecutar la migración

Este flujo de trabajo es considerando que ya tienes un entorno de desarrollo listo para trabajar con Python y bases de datos en MySQL. Si no has configurado tu entorno de desarrollo, podrían servirte las siguientes herramientas, aunque puedes usar las de tu preferencia.

## Configuración del entorno de desarrollo

- vscode: Aunque puedes usar el editor de tu preferencia, la plantilla es más eficaz en un entorno vscode ya que hay extensiones que permiten trabajar con MySQL desde el edito sin necesidad de usar el Workbench de MySQL.
- Tener un servidor de MySQL instalado localmente, de preferencia una versión '^8'
- Instalar la siguiente extensión en vscode: https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2. Una vez instalada, es necesario que especifíques tus credenciales. Para ello se da por sentado que ya has hecho la labor de levantar el servidor MySQL y administrar tus credenciales de acceso. Por simpleza, la plantilla está para un usuario con contraseña y con conexión localhost y puerto predeterminado, razón por la que en las variables de entorno no está el puerto.

Dado que SQLAlchemy está para funcionar con cualquier motor de base de datos, es posible que en lugar de MySQL queiras usar PostgreSQL, si levantas el servidor de la misma forma que en MySQL, no habrá problemas en las variables de entorno, pero sí los habrá en la ``DATABASE_URI``. Por lo que en este caso, la plantilla tendría que ser modificada. Esa modificación implica instalar un conector para ese motor de base de datos y modificar la URI de conexión en dos archivos: ``database/connection.py`` y en ``alembic/env.py``. En estos archivos está algo como: ``DATABASE_URI = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"`` que debería ser modificado para adaptarse al conector instalado. Luego puedes eliminar la dependencia que se usa en esta plantilla: ``mysql-connector-python``.

## Activar el entorno virtual y seleccionar el interprete

Una vez que hayas clonado el repositorio, puedes comenzar se activará un entorno virtual gestionado por poetry, en caso de que no lo veas, usa el comando ``poetry shell`` para activar el entorno virtual. Ahora será necesario escoger el interprete, para ello puedes presionar ``ctrl + shift + p`` y buscar *Python: Select interpreter*. Esperas un momento en lo que vscode carga el interprete para este proyecto y lo seleccionas, esto es necesario para que uses el entorno virtual gestionado por poetry y que uses la versión de python definida en el archivo ``.toml``, de otra forma, si tienes más versiones de Python instaladas, podría haber errores.

## Configurar las variables de entorno

Para trabajar adecuadamente con un nuevo proyecto que involucre bases de datos, es necesario que las credenciales se proporcionen con variables de entorno para evitar subir información sencible a los registros de git y de la terminal. Se usa el paquete dotenv para cargar las variables de entorno. Sólo es necesario que crees un archivo ``.env`` en la raíz del proyecto y declarar cuatro variables:

- ``HOST = localhost``
- ``USERNAME = tuUserName``
- ``PASSWORD = tuPassWORD``
- ``DATABASE = data_base_name``

El nombre de la base de datos debe coincidir con la base de datos física. Si usas varias bases de datos, ya sea una para desarrollo y una base de datos estable, tendrás que cambiar el nombre aquí para que la conexión se dirija hacia esa base de datos. Cualquier cambio en las credenciales de tu base de datos física, tendrás que modificar aquí para dirigir la conexión hacia allá. Si usas la extensión que recomendé, podrás crear una nueva base de datos fácilmente. Un uso sobre esa extensión está fuera del propósito de este texto, para saber cómo útilizar esa extensión, te sugiero que experimentes un poco con ella, no romperás nada, y si necesitas usar más características, entonces es preferible ir a la documentación oficial.

## Definición de los modelos

Suponiendo que eres un usaurio activo de Python, entonces tendrás configurado tu entorno de desarrollo para cualquier proyecto. Si es así, entonces notarás que el arranque de un proyecto con estas tecnologías se volverá más rápido con esta plantilla, ya que tú única labor hasta este momento, debería haber sido delcarar tus crendeciales en variables de entorno. Y después de esto comienza el proyecto real.

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

Una vez que hayas terminado de declarar tus modelos es momento de ejecutar una migración. Usa los comandos de alembic para generar la migración, sólo que ahora los añadirás a los comandos de poetry:

``poetry run alembic revision --autogenerate -m 'Mensaje sobre tu migración'``

Un curso de alembic está fuera del alcance del texto.

A partir de aquí, el proceso de desarrollo y migraciones sigue siendo el mismo.