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
        "fuente": item["fuente"],
        "url": item["url"] 
    }   
    
def portalsEntity(entity) -> list:
   return [portalEntity(item) for item in entity]





