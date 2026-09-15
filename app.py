from flask import Flask, jsonify, send_file
from flask_cors import CORS
import pymssql
import os

app = Flask(__name__)
CORS(app)

# Configuracion para produccion
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Configuración de la base de datos
DB_CONFIG = {
    'server': 'senerspte.database.windows.net',
    'database': 'senerspte',
    'username': 'senerspte',
    'password': 'S3n3rspt3'
}

def get_connection():
    return pymssql.connect(
        server=DB_CONFIG['server'],
        user=DB_CONFIG['username'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

@app.route('/')
def index():
    return send_file('PLADESHI.html')

@app.route('/PLADESHI_ER.html')
def pladeshi_er():
    return send_file('PLADESHI_ER.html')

@app.route('/api/series')
def get_series():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PLADESHI.Serie')
        columns = [column[0] for column in cursor.description]
        rows = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[str(col)] = row[i]
            rows.append(row_dict)
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cuadros')
def get_cuadros():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PLADESHI.Cuadros')
        rows = [{'CuadrosId': row[0], 'Descripcion': row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cuadro-serie')
def get_cuadro_serie():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT cs.CuadroSerieId, cs.CuadrosId, cs.SerieId, s.MMPCD
            FROM PLADESHI.CuadroSerie cs
            INNER JOIN PLADESHI.Serie s ON cs.SerieId = s.SerieId
        ''')
        rows = [{'CuadroSerieId': row[0], 'CuadrosId': row[1], 'SerieId': row[2], 'NombreSerie': row[3]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadatos')
def get_metadatos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PLADESHI.Metadatos')
        rows = [{'MetadatoId': row[0], 'SerieId': row[1], 'Campo': row[2], 'Valor': row[3]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/metadatos/<int:serie_id>')
def get_metadatos_by_serie(serie_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM PLADESHI.Metadatos WHERE SerieId = %s', (serie_id,))
        rows = [{'MetadatoId': row[0], 'SerieId': row[1], 'Campo': row[2], 'Valor': row[3]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/utiles/relaciones')
def get_relaciones_utiles():
    """Endpoint para verificar las foreign keys del esquema utiles"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                fk.name AS fk_name,
                tp.name AS tabla_origen,
                cp.name AS columna_origen,
                tr.name AS tabla_destino,
                cr.name AS columna_destino
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
            INNER JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
            INNER JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
            INNER JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
            INNER JOIN sys.schemas s ON tp.schema_id = s.schema_id
            WHERE s.name = 'utiles'
        ''')

        relaciones = []
        for row in cursor.fetchall():
            relaciones.append({
                'fk_name': row[0],
                'tabla_origen': row[1],
                'columna_origen': row[2],
                'tabla_destino': row[3],
                'columna_destino': row[4]
            })

        conn.close()
        return jsonify(relaciones)
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/api/utiles/estructura')
def get_estructura_utiles():
    """Endpoint que devuelve la estructura de las tablas del esquema utiles"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        tablas = [
            'CAT_ENTIDAD_FEDERATIVA',
            'CAT_LOCALIDAD',
            'CAT_MUNICIPIO',
            'CAT_TECNOLOGIA',
            'CAT_TEMA',
            'CAT_UNIDAD',
            'CAT_UNIDAD_RESPONSABLE'
        ]

        resultado = {}

        for tabla in tablas:
            # Obtener columnas basicas
            cursor.execute('''
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'utiles' AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            ''', (tabla,))

            columnas_raw = cursor.fetchall()

            # Obtener PKs
            cursor.execute('''
                SELECT ku.COLUMN_NAME
                FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE ku
                    ON tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
                    AND tc.TABLE_SCHEMA = ku.TABLE_SCHEMA
                    AND tc.TABLE_NAME = ku.TABLE_NAME
                WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                    AND tc.TABLE_SCHEMA = 'utiles'
                    AND tc.TABLE_NAME = %s
            ''', (tabla,))
            pks = [row[0] for row in cursor.fetchall()]

            # Obtener FKs
            cursor.execute('''
                SELECT
                    COL_NAME(fc.parent_object_id, fc.parent_column_id) as columna,
                    OBJECT_NAME(fc.referenced_object_id) as tabla_ref,
                    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) as columna_ref
                FROM sys.foreign_key_columns fc
                JOIN sys.tables t ON fc.parent_object_id = t.object_id
                JOIN sys.schemas s ON t.schema_id = s.schema_id
                WHERE s.name = 'utiles' AND t.name = %s
            ''', (tabla,))
            fks = {row[0]: {'tabla': row[1], 'columna': row[2]} for row in cursor.fetchall()}

            columnas = []
            for row in columnas_raw:
                col = {
                    'nombre': row[0],
                    'tipo': row[1],
                    'longitud': row[2],
                    'nullable': row[3] == 'YES',
                    'es_pk': row[0] in pks,
                    'es_fk': row[0] in fks,
                    'tabla_referencia': fks.get(row[0], {}).get('tabla'),
                    'columna_referencia': fks.get(row[0], {}).get('columna')
                }
                columnas.append(col)

            resultado[tabla] = columnas

        conn.close()
        return jsonify(resultado)
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/api/dashboard')
def get_dashboard():
    """Endpoint que devuelve todos los datos necesarios para el dashboard"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Series
        cursor.execute('SELECT * FROM PLADESHI.Serie')
        columns = [column[0] for column in cursor.description]
        series = []
        for row in cursor.fetchall():
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[str(col)] = row[i]
            series.append(row_dict)

        # Cuadros
        cursor.execute('SELECT * FROM PLADESHI.Cuadros')
        cuadros = [{'CuadrosId': row[0], 'Descripcion': row[1]} for row in cursor.fetchall()]

        # CuadroSerie
        cursor.execute('''
            SELECT cs.CuadroSerieId, cs.CuadrosId, cs.SerieId, s.MMPCD
            FROM PLADESHI.CuadroSerie cs
            INNER JOIN PLADESHI.Serie s ON cs.SerieId = s.SerieId
        ''')
        cuadro_serie = [{'CuadroSerieId': row[0], 'CuadrosId': row[1], 'SerieId': row[2], 'NombreSerie': row[3]} for row in cursor.fetchall()]

        # Metadatos
        cursor.execute('SELECT * FROM PLADESHI.Metadatos')
        metadatos = [{'MetadatoId': row[0], 'SerieId': row[1], 'Campo': row[2], 'Valor': row[3]} for row in cursor.fetchall()]

        # Series con metadatos
        cursor.execute('SELECT DISTINCT SerieId FROM PLADESHI.Metadatos')
        series_con_metadatos = [row[0] for row in cursor.fetchall()]

        # Datos de pozos por operador (vista v_PLADESHI_SIH_POZ_DESA_X_OPERA)
        cursor.execute('''
            SELECT fecha, operador, num_pozos_perforados, CuadrosId
            FROM [PLADESHI].[v_PLADESHI_SIH_POZ_DESA_X_OPERA]
            ORDER BY fecha, operador
        ''')
        pozos_operador = [{'fecha': row[0], 'operador': row[1], 'num_pozos': row[2], 'CuadrosId': row[3]} for row in cursor.fetchall()]

        conn.close()

        return jsonify({
            'series': series,
            'cuadros': cuadros,
            'cuadroSerie': cuadro_serie,
            'metadatos': metadatos,
            'seriesConMetadatos': series_con_metadatos,
            'pozosOperador': pozos_operador
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("PLADESHI - Servidor iniciado")
    print(f"Abre tu navegador en: http://localhost:{port}")
    print("=" * 50)
    app.run(debug=DEBUG, host='0.0.0.0', port=port)
