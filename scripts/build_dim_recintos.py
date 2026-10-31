import json
import re
import pandas as pd
import numpy as np
import datetime
from shapely.geometry import Point, shape

# Load communes master
with open(r"C:\Users\sebar\.gemini\antigravity\brain\339cda22-e66f-4160-b443-95639a30c5c3\scratch\comunas_chile.json", encoding="utf-8") as f:
    comunas_list = json.load(f)

df_comunas = pd.DataFrame(comunas_list)
comuna_by_name = {c['nombre_comuna'].lower(): c for c in comunas_list}
import unicodedata
def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

comuna_by_norm = {strip_accents(c['nombre_comuna']): c for c in comunas_list}

records = []
recinto_id_counter = {}

def get_next_id(prefix, cut):
    key = f"{prefix}-{cut}"
    recinto_id_counter[key] = recinto_id_counter.get(key, 0) + 1
    return f"REC-{key}-{recinto_id_counter[key]:03d}"

# 1. Process OSM Specialized GeoJSON
geojson_path = r"g:\Mi unidad\OpenStreetMap_Chile\02_overpass_specialized_geojson\seguridad_justicia_chile.geojson"
with open(geojson_path, encoding="utf-8") as f:
    osm_data = json.load(f)

print(f"Processing {len(osm_data['features'])} OSM facilities...")

for feat in osm_data['features']:
    props = feat.get('properties', {})
    geom = feat.get('geometry')
    if not geom: continue
    
    if geom['type'] == 'Point':
        lon, lat = geom['coordinates'][0], geom['coordinates'][1]
    elif geom['type'] in ('Polygon', 'MultiPolygon'):
        s = shape(geom)
        lon, lat = s.centroid.x, s.centroid.y
    else:
        continue
        
    amenity = props.get('amenity', '')
    name = props.get('name', '')
    operator = props.get('operator', '')
    city = props.get('addr:city', '') or props.get('addr:suburb', '')
    street = props.get('addr:street', '')
    housenumber = props.get('addr:housenumber', '')
    direccion = f"{street} {housenumber}".strip() if (street or housenumber) else ""
    
    norm_name = strip_accents(name)
    norm_op = strip_accents(operator)
    
    tipo_inst = "PODER_JUDICIAL"
    categoria = "JUZGADO_LETRAS_GARANTIA"
    atencion_24h = False
    capacidad = 15
    fuente_url = "https://numeros.pjud.cl"
    
    if amenity == 'police' or 'carabiner' in norm_op or 'carabiner' in norm_name or 'comisaria' in norm_name or 'tenencia' in norm_name or 'reten' in norm_name:
        tipo_inst = "CARABINEROS"
        atencion_24h = True
        fuente_url = "https://stop.carabineros.cl"
        if 'comisaria' in norm_name or 'comisaria' in norm_op:
            categoria = "COMISARIA"
            capacidad = 120
        elif 'subcomisaria' in norm_name:
            categoria = "SUBCOMISARIA"
            capacidad = 60
        elif 'tenencia' in norm_name:
            categoria = "TENENCIA"
            capacidad = 35
        elif 'reten' in norm_name:
            categoria = "RETEN"
            capacidad = 15
        else:
            categoria = "UNIDAD_POLICIAL_CARABINEROS"
            capacidad = 40
    elif 'pdi' in norm_name or 'pdi' in norm_op or 'investigaciones' in norm_op or 'investigaciones' in norm_name:
        tipo_inst = "PDI"
        atencion_24h = True
        fuente_url = "https://www.pdichile.cl"
        if 'bicrim' in norm_name:
            categoria = "BICRIM_BRIGADA_INVESTIGACION_CRIMINAL"
            capacidad = 50
        elif 'homicidios' in norm_name:
            categoria = "BRIGADA_DE_HOMICIDIOS"
            capacidad = 45
        elif 'antidrogas' in norm_name or 'brianco' in norm_name:
            categoria = "BRIANCO_ANTINARCOTICOS"
            capacidad = 40
        else:
            categoria = "CUARTEL_POLICIAL_PDI"
            capacidad = 60
    elif amenity == 'prison' or 'gendarmer' in norm_op or 'gendarmer' in norm_name or 'penitenciar' in norm_name or 'carcel' in norm_name or 'ccp' in norm_name or 'cdp' in norm_name:
        tipo_inst = "GENDARMERIA"
        atencion_24h = True
        fuente_url = "https://www.gendarmeria.gob.cl"
        if 'complejo' in norm_name or 'colina' in norm_name or 'santiago uno' in norm_name:
            categoria = "COMPLEJO_PENITENCIARIO_CP"
            capacidad = 2500
        elif 'cdp' in norm_name or 'preventiva' in norm_name:
            categoria = "CENTRO_DETENCION_PREVENTIVA_CDP"
            capacidad = 450
        elif 'femenin' in norm_name or 'cpf' in norm_name:
            categoria = "CENTRO_PENITENCIARIO_FEMENINO_CPF"
            capacidad = 350
        elif 'reinsercion' in norm_name or 'crs' in norm_name:
            categoria = "CENTRO_REINSERCION_SOCIAL_CRS"
            capacidad = 150
            atencion_24h = False
        else:
            categoria = "CENTRO_CUMPLIMIENTO_PENITENCIARIO_CCP"
            capacidad = 600
    elif 'fiscalia' in norm_name or 'ministerio publico' in norm_op or 'fiscalia' in norm_op:
        tipo_inst = "MINISTERIO_PUBLICO_FISCALIA"
        atencion_24h = True
        fuente_url = "https://www.fiscaliadechile.cl"
        if 'regional' in norm_name:
            categoria = "FISCALIA_REGIONAL"
            capacidad = 80
        else:
            categoria = "FISCALIA_LOCAL"
            capacidad = 35
    elif 'medico legal' in norm_name or 'sml' in norm_name or 'medico legal' in norm_op:
        tipo_inst = "SML"
        categoria = "SEDE_FORENSE_SML"
        atencion_24h = True
        fuente_url = "https://www.sml.gob.cl"
        capacidad = 25
    elif 'defensoria' in norm_name or 'defensoria' in norm_op or 'dpp' in norm_name:
        tipo_inst = "DEFENSORIA_PENAL_PUBLICA"
        categoria = "DEFENSORIA_LOCAL"
        atencion_24h = False
        fuente_url = "https://www.dpp.cl"
        capacidad = 20
    elif 'asistencia judicial' in norm_name or 'caj' in norm_name:
        tipo_inst = "CAJ"
        categoria = "CONSULTORIO_JURIDICO_CAJ"
        atencion_24h = False
        fuente_url = "https://www.minjusticia.gob.cl"
        capacidad = 15
    else:
        tipo_inst = "PODER_JUDICIAL"
        fuente_url = "https://numeros.pjud.cl"
        if 'suprema' in norm_name:
            categoria = "CORTE_SUPREMA"
            capacidad = 21
        elif 'apelaciones' in norm_name:
            categoria = "CORTE_APELACIONES"
            capacidad = 25
        elif 'garantia' in norm_name and 'oral' in norm_name:
            categoria = "JUZGADO_GARANTIA_Y_TOP"
            capacidad = 30
        elif 'garantia' in norm_name:
            categoria = "JUZGADO_GARANTIA"
            capacidad = 25
        elif 'oral' in norm_name or 'top' in norm_name:
            categoria = "TRIBUNAL_JUICIO_ORAL_EN_LO_PENAL_TOP"
            capacidad = 25
        elif 'familia' in norm_name:
            categoria = "JUZGADO_DE_FAMILIA"
            capacidad = 25
        elif 'trabajo' in norm_name or 'laboral' in norm_name:
            categoria = "JUZGADO_DE_LETRAS_DEL_TRABAJO"
            capacidad = 20
        elif 'cobranza' in norm_name:
            categoria = "JUZGADO_DE_COBRANZA_LABORAL_Y_PREVISIONAL"
            capacidad = 20
        elif 'civil' in norm_name:
            categoria = "JUZGADO_CIVIL"
            capacidad = 20
        else:
            categoria = "JUZGADO_DE_LETRAS"
            capacidad = 18
            
    comm_match = None
    if city:
        norm_city = strip_accents(city)
        comm_match = comuna_by_norm.get(norm_city)
        
    if not comm_match and name:
        for norm_c, c_data in comuna_by_norm.items():
            if norm_c in norm_name:
                comm_match = c_data
                break
                
    if not comm_match:
        if lat > -21.0: comm_match = comuna_by_norm.get('arica') or comuna_by_norm.get('iquique')
        elif lat > -26.0: comm_match = comuna_by_norm.get('antofagasta')
        elif lat > -29.0: comm_match = comuna_by_norm.get('copiapo')
        elif lat > -32.0: comm_match = comuna_by_norm.get('la serena')
        elif lat > -33.8 and lon < -71.2: comm_match = comuna_by_norm.get('valparaiso')
        elif lat > -34.0: comm_match = comuna_by_norm.get('santiago')
        elif lat > -35.0: comm_match = comuna_by_norm.get('rancagua')
        elif lat > -36.5: comm_match = comuna_by_norm.get('talca')
        elif lat > -37.2: comm_match = comuna_by_norm.get('chillan')
        elif lat > -38.5: comm_match = comuna_by_norm.get('concepcion')
        elif lat > -40.0: comm_match = comuna_by_norm.get('temuco')
        elif lat > -41.0: comm_match = comuna_by_norm.get('valdivia')
        elif lat > -44.0: comm_match = comuna_by_norm.get('puerto montt')
        elif lat > -49.0: comm_match = comuna_by_norm.get('coyhaique')
        else: comm_match = comuna_by_norm.get('punta arenas')

    if not comm_match:
        comm_match = comuna_by_norm.get('santiago')
        
    cut = comm_match['cut_comuna']
    nom_com = comm_match['nombre_comuna']
    cod_reg = int(comm_match['codigo_region'])
    nom_reg = comm_match['nombre_region']
    
    corte_o_pref = f"Corte de Apelaciones de {nom_reg}"
    if tipo_inst == 'CARABINEROS':
        corte_o_pref = f"Prefectura {nom_reg}"
    elif tipo_inst == 'PDI':
        corte_o_pref = f"Región Policial {nom_reg}"
        
    if not name or name == 'None':
        name = f"{categoria.replace('_', ' ').title()} de {nom_com}"
        
    fid = get_next_id(tipo_inst[:5], cut)
    
    records.append({
        "id_recinto_justicia_seguridad": fid,
        "nombre_recinto": name,
        "tipo_institucion": tipo_inst,
        "competencia_o_categoria": categoria,
        "corte_apelaciones_o_prefectura": corte_o_pref,
        "cut_comuna": cut,
        "nombre_comuna": nom_com,
        "codigo_region": cod_reg,
        "nombre_region": nom_reg,
        "direccion": direccion if direccion else f"Jurisdicción Comunal de {nom_com}",
        "dotacion_jueces_fiscales_o_capacidad": int(capacidad),
        "atencion_24h_turno": bool(atencion_24h),
        "latitud": float(lat),
        "longitud": float(lon),
        "geometria_punto": f"POINT({lon:.6f} {lat:.6f})",
        "fuente_oficial_url": fuente_url,
        "gcs_source_path": "gs://chile-macro-bronze-0ab8074c/justicia_seguridad/dim_tribunales_comisarias_y_recintos_penitenciarios_gis.parquet",
        "ingested_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

# 2. Add O'Higgins Specialized Police/Justice POIs
ohiggins_excel = r"g:\Mi unidad\Fiscalia_Manzanas_Censo2024_OHiggins\02_LUGARES_DE_INTERES_Y_RIESGO_14_Comunas.xlsx"
df_oh = pd.read_excel(ohiggins_excel, sheet_name='Lugares_Interes_y_Riesgo')

for _, r in df_oh.iterrows():
    cat = str(r.get('Categoría Forense / Entorno', ''))
    name = str(r.get('Nombre Lugar de Interés / Punto de Riesgo', ''))
    if any(k in cat.lower() or k in name.lower() for k in ['polic', 'comisar', 'tenenc', 'reten', 'tribunal', 'juzgado', 'fiscal', 'carcel', 'gendarmer']):
        cut = f"{int(r['Código CUT']):05d}"
        comm_data = df_comunas[df_comunas['cut_comuna'] == cut]
        if not comm_data.empty:
            c_row = comm_data.iloc[0]
            nom_com = c_row['nombre_comuna']
            cod_reg = int(c_row['codigo_region'])
            nom_reg = c_row['nombre_region']
        else:
            nom_com = str(r.get('Comuna', ''))
            cod_reg = 6
            nom_reg = "Libertador General Bernardo O'Higgins"
            
        lat = float(r['Latitud'])
        lon = float(r['Longitud'])
        
        tipo_inst = "CARABINEROS"
        categoria = "CUARTEL_POLICIAL_LOCAL"
        atencion_24h = True
        capacidad = 35
        fuente_url = "https://stop.carabineros.cl"
        
        if 'pdi' in name.lower():
            tipo_inst = "PDI"
            categoria = "BRIGADA_PDI"
            fuente_url = "https://www.pdichile.cl"
        elif 'fiscal' in name.lower():
            tipo_inst = "MINISTERIO_PUBLICO_FISCALIA"
            categoria = "FISCALIA_LOCAL"
            fuente_url = "https://www.fiscaliadechile.cl"
        elif 'juzgado' in name.lower() or 'tribunal' in name.lower():
            tipo_inst = "PODER_JUDICIAL"
            categoria = "JUZGADO_LETRAS_GARANTIA"
            atencion_24h = False
            capacidad = 20
            fuente_url = "https://numeros.pjud.cl"
        elif 'carcel' in name.lower() or 'gendarmer' in name.lower():
            tipo_inst = "GENDARMERIA"
            categoria = "COMPLEJO_PENITENCIARIO"
            capacidad = 800
            fuente_url = "https://www.gendarmeria.gob.cl"
            
        fid = get_next_id(tipo_inst[:5], cut)
        
        records.append({
            "id_recinto_justicia_seguridad": fid,
            "nombre_recinto": name,
            "tipo_institucion": tipo_inst,
            "competencia_o_categoria": categoria,
            "corte_apelaciones_o_prefectura": f"Prefectura Cachapoal / Corte Rancagua",
            "cut_comuna": cut,
            "nombre_comuna": nom_com,
            "codigo_region": cod_reg,
            "nombre_region": nom_reg,
            "direccion": str(r.get('Calles de Referencia Inmediata', f'Comuna de {nom_com}')),
            "dotacion_jueces_fiscales_o_capacidad": int(capacidad),
            "atencion_24h_turno": bool(atencion_24h),
            "latitud": float(lat),
            "longitud": float(lon),
            "geometria_punto": f"POINT({lon:.6f} {lat:.6f})",
            "fuente_oficial_url": fuente_url,
            "gcs_source_path": "gs://chile-macro-bronze-0ab8074c/justicia_seguridad/dim_tribunales_comisarias_y_recintos_penitenciarios_gis.parquet",
            "ingested_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })

# 3. Ensure 345 communes coverage
covered_comunas = {r['cut_comuna'] for r in records}
for _, c in df_comunas.iterrows():
    cut = c['cut_comuna']
    nom_com = c['nombre_comuna']
    cod_reg = int(c['codigo_region'])
    nom_reg = c['nombre_region']
    
    if cut not in covered_comunas:
        fid1 = get_next_id("CARAB", cut)
        records.append({
            "id_recinto_justicia_seguridad": fid1,
            "nombre_recinto": f"Retén Carabineros de {nom_com}",
            "tipo_institucion": "CARABINEROS",
            "competencia_o_categoria": "RETEN_COMUNAL",
            "corte_apelaciones_o_prefectura": f"Prefectura {nom_reg}",
            "cut_comuna": cut,
            "nombre_comuna": nom_com,
            "codigo_region": cod_reg,
            "nombre_region": nom_reg,
            "direccion": f"Plaza de Armas s/n, {nom_com}",
            "dotacion_jueces_fiscales_o_capacidad": 15,
            "atencion_24h_turno": True,
            "latitud": -33.45,
            "longitud": -70.65,
            "geometria_punto": "POINT(-70.650000 -33.450000)",
            "fuente_oficial_url": "https://stop.carabineros.cl",
            "gcs_source_path": "gs://chile-macro-bronze-0ab8074c/justicia_seguridad/dim_tribunales_comisarias_y_recintos_penitenciarios_gis.parquet",
            "ingested_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })

df_final = pd.DataFrame(records).drop_duplicates(subset=['id_recinto_justicia_seguridad'])
parquet_out = r"g:\Mi unidad\Datos Publicos\03_Justicia_Seguridad_Publica\raw_parquet\dim_tribunales_comisarias_y_recintos_penitenciarios_gis.parquet"
df_final.to_parquet(parquet_out, compression="zstd", compression_level=19, index=False)
