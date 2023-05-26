def portalEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Nombre": item["name"],
        "Apellido": item["Lastname"],
        "Titulo": item["Titulo"],
        "fecha": item["fecha"],
        "video": item["video"],
        "imagen": item["imagen"],
        "latitud": item["latitude"],
        "longitud": item["longitude"],
        "clasificacion": item["clasificacion"],
        "descripcion": item["descripcion"],
        "status": item["status"],
        "fuente": item["fuente"]
    }   
    
def portalsEntity(entity) -> list:
   return [portalEntity(item) for item in entity]


def instagramEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Nombre": item["Nombre"],
        "fecha": item["fecha"],
        "video": item["video"],
        "owner_username": item["owner_username"],
        'fuente': item['fuente'],
        "status": item["status"]
    }   
    
def instagramEsEntity(entity) -> list:
   return [instagramEntity(item) for item in entity]


def diarioEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Nombre": item["Nombre"],
        "fecha": item["fecha"],
        "video": item["video"],
        "owner_username": item["owner_username"],
        'fuente': item['fuente'],
        "status": item["status"],
        "imagen": item["imagen"]
    }

def diarioEsEntity(entity) -> list:
    return [diarioEntity(item) for item in entity]