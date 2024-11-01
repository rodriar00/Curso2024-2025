from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph


g = Graph()
g.parse("../rdf/output-with-links.ttl", format="turtle")

def main_query(request):
    distrito = request.form.get("distrito", "None")
    fecha_desde = request.form.get("fecha-desde", "")
    fecha_hasta = request.form.get("fecha-hasta", "")
    tipo_accidente = request.form.get("tipo-accidente", "None")
    tipo_vehiculo = request.form.get("vehiculo", "None")
    edad_min = request.form.get("edad-min", "")
    edad_max = request.form.get("edad-max", "")
    lesividad = request.form.get("lesividad", "None")
    estado_metereologico = request.form.get("estado-meteorologico", "None")
    alcohol = request.form.get("alcohol", "None")
    droga = request.form.get("droga", "None")

    query = """
        SELECT ?x ?y ?num_expediente ?fecha ?tipo_accidente
        WHERE {
            ?accident a <http://smartcity.linkeddata.es/accidentes/ontologia/Accidente> ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/num_expediente> ?num_expediente ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/coordenada_x_utm> ?x ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/coordenada_y_utm> ?y .
            
            OPTIONAL { 
                ?accident <http://smartcity.linkeddata.es/accidentes/ontologia/estaEnDistrito> ?distrito .
                OPTIONAL { ?distrito <http://smartcity.linkeddata.es/accidentes/ontologia/distrito> ?distrito_nombre }
            }
            OPTIONAL { ?accident <http://smartcity.linkeddata.es/accidentes/ontologia/fecha> ?fecha }
            OPTIONAL { ?accident <http://smartcity.linkeddata.es/accidentes/ontologia/tipo_accidente> ?tipo_accidente }
            OPTIONAL { ?accident <http://smartcity.linkeddata.es/accidentes/ontologia/estado_meteorologico> ?estado }
            
            OPTIONAL {
                ?accident <http://smartcity.linkeddata.es/accidentes/ontologia/personaInvolucrada> ?persona .
                OPTIONAL { ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/tipo_vehiculo> ?tipo_vehiculo }
                OPTIONAL { ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/min_edad> ?min_edad }
                OPTIONAL { ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/max_edad> ?max_edad }
                OPTIONAL { 
                    ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/tieneLesion> ?lesion .
                    OPTIONAL { ?lesion <http://smartcity.linkeddata.es/accidentes/ontologia/lesividad> ?lesividad_nombre }
                }
                OPTIONAL { ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/positiva_alcohol> ?alcohol }
                OPTIONAL { ?persona <http://smartcity.linkeddata.es/accidentes/ontologia/positiva_droga> ?droga }
            }
    """

    filter = ""

    if distrito != "None":
        filter += f'?distrito_nombre = "{distrito}" && '

    if fecha_desde != "":
        filter += f'?fecha >= "{fecha_desde}"^^xsd:date && '

    if fecha_hasta != "":
        filter += f'?fecha <= "{fecha_hasta}"^^xsd:date && '

    if tipo_accidente != "None":
        filter += f'?tipo_accidente = "{tipo_accidente}" && '

    if tipo_vehiculo != "None":
        filter += f'?tipo_vehiculo = "{tipo_vehiculo}" && '

    if edad_min != "":
        filter += f"?min_edad >= {edad_min} && "

    if edad_max != "":
        filter += f"?max_edad <= {edad_max} && "

    if lesividad != "None":
        filter += f'?lesividad_nombre = "{lesividad}" && '

    if estado_metereologico != "None":
        filter += f'?estado = "{estado_metereologico}" && '

    if alcohol != "None":
        filter += f"?alcohol = {alcohol} && "

    if droga != "None":
        filter += f"?droga = {droga} && "

    if filter != "":
        query = query + "FILTER(" + filter[:-4] + ")}"
    else:
        query = query + "}"

    # Prepare and execute the query
    q = prepareQuery(query)

    return g.query(q)

def get_distritos():
    get_districts_query = prepareQuery(
        """
            SELECT DISTINCT ?distrito
            WHERE {
                ?district a <http://smartcity.linkeddata.es/accidentes/ontologia/Distrito> ;
                        <http://smartcity.linkeddata.es/accidentes/ontologia/distrito> ?distrito .
            }
            ORDER BY ?distrito
            """
    )
    return [row.distrito for row in g.query(get_districts_query)]


def get_type_accident():
    get_type_accident = prepareQuery(
        """
        SELECT DISTINCT ?tipo_accidente
        WHERE {
            ?accident a <http://smartcity.linkeddata.es/accidentes/ontologia/Accidente> ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/tipo_accidente> ?tipo_accidente .
        }
        ORDER BY ?tipo_accidente
        """
    )
    return [row.tipo_accidente for row in g.query(get_type_accident)]


def get_tipo_vehiculo():
    get_tipo_vehiculo = prepareQuery(
        """
        SELECT DISTINCT ?tipo_vehiculo
        WHERE {
            ?persona a <http://smartcity.linkeddata.es/accidentes/ontologia/Persona> ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/tipo_vehiculo> ?tipo_vehiculo .
        }
        ORDER BY ?tipo_vehiculo
        """
    )
    return [row.tipo_vehiculo for row in g.query(get_tipo_vehiculo)]


def get_lesividad():
    get_lesividad = prepareQuery(
        """
        SELECT DISTINCT ?lesividades
        WHERE {
            ?Lesividad a <http://smartcity.linkeddata.es/accidentes/ontologia/Lesividad> ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/lesividad> ?lesividades .
        }
        ORDER BY ?lesividades
        """
    )
    return [row.lesividades for row in g.query(get_lesividad)]


def get_estado_meteorologico():
    get_estado_meteorologico = prepareQuery(
        """
        SELECT DISTINCT ?estado_meteorologico
        WHERE {
            ?accident a <http://smartcity.linkeddata.es/accidentes/ontologia/Accidente> ;
                    <http://smartcity.linkeddata.es/accidentes/ontologia/estado_meteorologico> ?estado_meteorologico .
        }
        ORDER BY ?estado_meteorologico
        """
    )
    return [row.estado_meteorologico for row in g.query(get_estado_meteorologico)]
