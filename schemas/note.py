#for mongodb obj to python dict
def noteEntity(item) -> dict:
    return {
        "id": item["_id"],
        "title" : item["title"],
        "desc" : item["desc"],
        "important" : item["important"],

    }

def notesEntity(items) -> list[dict]:
    return [noteEntity(item) for item in items]

async def formEnitity(request) -> dict:
    form =await request.form()
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    return formDict