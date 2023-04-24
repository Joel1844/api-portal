def portalEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Nombre": item["name"],
        "fecha": item["date"],
        "video": item["video"],
        "latitud": item["latitude"],
        "longitud": item["longitude"]
    }   
    
def portalsEntity(entity) -> list:
   return [portalEntity(item) for item in entity]
