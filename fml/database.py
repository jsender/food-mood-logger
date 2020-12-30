from importlib import resources
from pathlib import Path

__all__ = ['execute_schema', 'check_schema', 'queries']


# Get traversable object with files from fml/resources/queries
directory = (resources.files('fml')/'resources/queries').iterdir()


def read(filepath: Path):
    # Helper function for queries dictionary filling
    with open(filepath, 'r') as fp:
        return fp.read()


# `queries` dictionary stores all static queries from the
# fml/resources/queries/ directory
queries = {filepath.stem: read(filepath)
           for filepath in directory if filepath.is_file()}


def execute_schema(connection):
    # Read schema creation sql queries from the resource/schema folder
    food_table_schema = resources.read_text('fml.resources.schema', 'food.sql')
    mood_table_schema = resources.read_text('fml.resources.schema', 'mood.sql')

    connection.executescript(food_table_schema)
    connection.executescript(mood_table_schema)


def check_schema(connection):
    food_table = 'CREATE TABLE food('
    mood_table = 'CREATE TABLE mood('
    food_present = mood_present = False

    # List all table schemas in the database
    dbschema = connection.executescript(queries['schema'])
    for dbs in dbschema:
        # Check for presence of "food" and "mood" tables:
        if dbs[0].startswith(food_table):
            food_present = True
        if dbs[0].startswith(mood_table):
            mood_present = True

    return food_present and mood_present


def insert_food(connection, *parameters):
    if len(parameters) not in [2, 3]:
        raise Exception(f'Insufficient amount of parameters for "INSERT INTO '
                        f'food" statement: {parameters}')
    columns = ['type', 'amount', 'consumption_time'][:len(parameters)]
    insert_statement = f"""
    INSERT INTO food({', '.join(columns)})
    VALUES ({', '.join(['?']*len(columns))});
    """
    connection.execute(insert_statement, parameters)


def insert_mood(connection, *parameters):
    if len(parameters) not in [2, 3]:
        raise Exception(f'Insufficient amount of parameters for "INSERT INTO'
                        f'mood" statement: {parameters}')
    columns = ['type', 'score', 'mood_time'][:len(parameters)]
    insert_statement = f"""
    INSERT INTO mood({', '.join(columns)})
    VALUES ({', '.join(['?']*len(columns))});
    """
    connection.execute(insert_statement, parameters)
