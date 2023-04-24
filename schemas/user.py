def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "Nombre": item["name"],
        "Número de teléfono ": item["phone"],
        "Barrio": item["neighborhood"],
        "A qué se dedica": item["occupation"],
        "Nivel profesional": item["professional_level"],
        "Hace Ejercicio": item["exercise"],
        "Edad": item["age"],
        "Cuanta libra pesa": item["weight"],
        "Cuanta libra empezo": item["start_weight"],
        "Cuanta Libra Termino": item["end_weight"],
        "Cuanta libra quiere bajar": item["goal_weight"],
        "Sufre de alguna enfermedad": item["disease"],
        "Cual plan lleva": item["plan"],
        "Estatura": item["height"],
        "Sexo": item["sex"],
        "Más solicita(Jugo verde,yogurt)": item["more_request"],
        "Tiempo en plan": item["time_plan"],
    }   
    
def usersEntity(entity) -> list:
   return [userEntity(item) for item in entity]