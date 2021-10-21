import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert config

# -----------------------------------------------------
# API del TAD Catalogo de Películas
# -----------------------------------------------------

info = {
    "numelements" : 2000,
    "maptype" : 'CHAINING',
    "loadfactor": 1,
    "listtype" : 'ARRAY_LIST'
}

elements = info["numelements"]

def newCatalog():
    catalogo = {
        "movies" : None,
        "production_company" : None,
        'genres' : None,
        'actor' : None,
        'director_name': None,
        'production_countries': None
    }

    catalogo["movies"] = mp.newMap(
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareMoviesIds
                                    )
    catalogo["production_company"] = mp.newMap (
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareProductionCompanies
                                    )
    catalogo["genres"] = mp.newMap (
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareGenres
                                    )
    catalogo["actor"] = mp.newMap (
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareGenres
                                    )
    catalogo["director_name"] = mp.newMap (
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareGenres
                                    )  
    catalogo["production_countries"] = mp.newMap (
                                    numelements = info["numelements"],
                                    maptype=info["maptype"],
                                    loadfactor=info["loadfactor"],
                                    comparefunction=compareProductionCompanies
                                    )  
    
    return catalogo


def newProductionCompany():
    company = {
        "movies": lt.newList(info["listtype"]),
        "vote_average": 0
        }
    return company

def newGenres():
    genres = {
        "movies": lt.newList(info["listtype"]),
        "vote_count": 0
        }
    return genres

def newActor():
    actorDict = {
        'movies': lt.newList(info['listtype']),
        'vote_average': 0,
        'director': lt.newList(info['listtype'])
        }
    return actorDict

def newDirector():
    directorMov = {
        "movies": lt.newList(info["listtype"]),
        "vote_average": 0
        }
    return directorMov

def newCountry():
    countryMov = {
        "movies": lt.newList(info["listtype"]),
        "vote_average": 0
        }
    return countryMov

# ==============================
# Funciones de consulta
# ==============================


def getMovie(catalog, movieId):
    movie = mp.get(catalog["movies"], movieId)
    if movie:
        return me.getValue(movie)
    return None

def getMoviesByCompany(catalog, companyName):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    productionCompany = mp.get(catalog["production_company"], companyName)
    if productionCompany:
        companyData = me.getValue(productionCompany)
        companyMovies = lt.newList(info["listtype"])
        for i in range(lt.size(companyData["movies"])):
            movie = getMovie(catalog, lt.getElement(companyData["movies"], i))
            lt.addLast(companyMovies, movie)
        
        return (companyMovies,companyData["vote_average"])
        
    return (None,None)

def getMoviesByGenre(catalog, genre):
    """
    Retorna un autor con sus peliculas a partir del nombre del genero
    """
    genre = mp.get(catalog["genres"], genre)
    if genre:
        genreData = me.getValue(genre)
        genreMovies = lt.newList(info["listtype"])
        for i in range(lt.size(genreData["movies"])):
            movie = getMovie(catalog, lt.getElement(genreData["movies"], i))
            lt.addLast(genreMovies, movie)

        return (genreMovies,genreData["vote_average"])

    return (None,None)

def getMoviesByActor(catalog, actorn):
    """
    Retorna un autor con sus peliculas a partir del nombre del actor
    """
    actor= mp.get(catalog["actor"], actorn)
    if actor:
        actorData = me.getValue(actor)
        actorAvg = actorData['vote_average']
        actorMovies = lt.newList(info["listtype"])
        for i in range(lt.size(actorData["movies"])):
            movie = lt.getElement(actorData["movies"], i)
            lt.addLast(actorMovies, movie)

        mostDir = actorData['director']
        comun = []
        for i in range(lt.size(actorData['director'])):
            comun.append(lt.getElement(actorData['director'], i))
        actorDir = max(set(comun), key = comun.count)
        return (actorMovies,actorDir, actorAvg)
        
    return (None,None)

def getDirector(catalog, directorM):

    director= mp.get(catalog["director_name"], directorM)
    if director:
        directorData = me.getValue(director)
        directorAvg = directorData['vote_average']
        directorMovies = lt.newList(info["listtype"])
        for i in range(lt.size(directorData["movies"])):
            movie = lt.getElement(directorData["movies"], i)
            lt.addLast(directorMovies, movie)

        return (directorMovies, directorAvg)
        
    return (None,None)

def getMoviesByCountry(catalog, countryName):
    countryM = mp.get(catalog["production_countries"], countryName)
    if countryM:
        countryData = me.getValue(countryM)
        countryMovies = lt.newList(info["listtype"])
        for i in range(lt.size(countryData["movies"])):
            movie = getMovie(catalog, lt.getElement(countryData["movies"], i))
            lt.addLast(countryMovies, movie)
        
        return (countryMovies,countryData["vote_average"])
        
    return (None,None)

# Funciones para agregar informacion al catalogo

def addMovie(catalogo, dataD: dict, dataC: dict):
    if mp.contains(catalogo["movies"], dataD["id"]):
        movie = mp.get(catalogo["movies"], dataD["id"])
        movie = me.getValue(movie)
        movie.update(dataD)
        movie.update(dataC)
        
    else:
        mp.put(catalogo["movies"], dataD["id"], dataD)
        addProductionCompany(catalogo,dataD)
        addGenres(catalogo, dataD)
        addActor(catalogo, dataC, dataD)
        addDirector(catalogo, dataC, dataD)
        addCountry(catalogo,dataD)

def addProductionCompany (catalogo, movie) :
    companies = catalogo["production_company"]
    movieId = movie["id"]
    name = movie["production_companies"]
    existauthor = mp.contains(companies, name)
    if existauthor:
        entry = mp.get(companies, name)
        company = me.getValue(entry)
    else:
        company = newProductionCompany()
        mp.put(companies, name, company)
    lt.addLast(company['movies'], movieId)

    companyAvg = company["vote_average"]
    movieAvg = movie["vote_average"]
    if (movieAvg == 0.0):
        company["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(company["movies"])
        company["vote_average"] = ((companyAvg*(moviesNum-1)) + float(movieAvg)) / moviesNum

def addGenres (catalogo, movie) :
    companies = catalogo["genres"]
    movieId = movie["id"]
    name = movie["genres"]
    existauthor = mp.contains(companies, name)
    if existauthor:
        entry = mp.get(companies, name)
        company = me.getValue(entry)
    else:
        company = newProductionCompany()
        mp.put(companies, name, company)
    lt.addLast(company['movies'], movieId)

    companyAvg = company["vote_average"]
    movieAvg = movie["vote_average"]
    if (movieAvg == 0.0):
        company["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(company["movies"])
        company["vote_average"] = ((companyAvg*(moviesNum-1)) + float(movieAvg)) / moviesNum

def addActor (catalog, movie, details) :
    actorCatalog = catalog['actor']
    movieId = movie['id']
    nameActor1Value, nameActor2Value, nameActor3Value, nameActor4Value, nameActor5Value = (movie["actor1_name"],movie["actor2_name"],movie["actor3_name"],movie["actor4_name"],movie["actor5_name"])
    
    movieAvg = details["vote_average"]
    
    #A1
    existActor1 = mp.contains(actorCatalog, nameActor1Value)
    if existActor1:
        entry = mp.get(actorCatalog, nameActor1Value)
        actorsD = me.getValue(entry)
    else:
        actorsD = newActor()
        mp.put(actorCatalog, nameActor1Value, actorsD)
    lt.addLast(actorsD['movies'], details['original_title'])
    lt.addLast(actorsD['director'], movie['director_name'])
    actorAvg1 = actorsD["vote_average"] 
    if (movieAvg == 0.0):
        actorsD["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(actorsD["movies"])
        actorsD["vote_average"] = ((actorAvg1*(moviesNum-1)) + float(movieAvg)) / moviesNum

    #A2
    existActor2 = mp.contains(actorCatalog, nameActor2Value)
    if existActor2:
        entry = mp.get(actorCatalog, nameActor2Value)
        actorsD = me.getValue(entry)
    else:
        actorsD = newActor()
        mp.put(actorCatalog, nameActor2Value, actorsD)
    lt.addLast(actorsD['movies'], details['original_title'])
    lt.addLast(actorsD['director'], movie['director_name'])
    actorAvg2 = actorsD["vote_average"]
    if (movieAvg == 0.0):
        actorsD["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(actorsD["movies"])
        actorsD["vote_average"] = ((actorAvg2*(moviesNum-1)) + float(movieAvg)) / moviesNum

    #A3
    existActor3 = mp.contains(actorCatalog, nameActor3Value)
    if existActor3:
        entry = mp.get(actorCatalog, nameActor3Value)
        actorsD = me.getValue(entry)
    else:
        actorsD = newActor()
        mp.put(actorCatalog, nameActor3Value, actorsD)
    lt.addLast(actorsD['movies'], details['original_title'])
    lt.addLast(actorsD['director'], movie['director_name'])
    actorAvg3 = actorsD["vote_average"]
    if (movieAvg == 0.0):
        actorsD["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(actorsD["movies"])
        actorsD["vote_average"] = ((actorAvg3*(moviesNum-1)) + float(movieAvg)) / moviesNum

    #A4
    existActor4 = mp.contains(actorCatalog, nameActor4Value)
    if existActor4:
        entry = mp.get(actorCatalog, nameActor4Value)
        actorsD = me.getValue(entry)
    else:
        actorsD = newActor()
        mp.put(actorCatalog, nameActor4Value, actorsD)
    lt.addLast(actorsD['movies'], details['original_title'])
    lt.addLast(actorsD['director'], movie['director_name'])
    actorAvg4 = actorsD["vote_average"]
    if (movieAvg == 0.0):
        actorsD["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(actorsD["movies"])
        actorsD["vote_average"] = ((actorAvg4*(moviesNum-1)) + float(movieAvg)) / moviesNum

    #A5
    existActor5 = mp.contains(actorCatalog, nameActor5Value)
    if existActor5:
        entry = mp.get(actorCatalog, nameActor5Value)
        actorsD = me.getValue(entry)
    else:
        actorsD = newActor()
        mp.put(actorCatalog, nameActor5Value, actorsD)
    lt.addLast(actorsD['movies'], details['original_title'])
    lt.addLast(actorsD['director'], movie['director_name'])
    actorAvg5 = actorsD["vote_average"]
    if (movieAvg == 0.0):
        actorsD["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(actorsD["movies"])
        actorsD["vote_average"] = ((actorAvg5*(moviesNum-1)) + float(movieAvg)) / moviesNum
  
def addDirector (catalog, movie, details) :
    companies = catalog["director_name"]
    movieId = movie["id"]
    name = movie["director_name"]
    existauthor = mp.contains(companies, name)
    if existauthor:
        entry = mp.get(companies, name)
        company = me.getValue(entry)
    else:
        company = newDirector()
        mp.put(companies, name, company)
    lt.addLast(company['movies'], details['original_title'])

    companyAvg = company["vote_average"]
    movieAvg = details["vote_average"]
    if (movieAvg == 0.0):
        company["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(company["movies"])
        company["vote_average"] = ((companyAvg*(moviesNum-1)) + float(movieAvg)) / moviesNum

def addCountry (catalogo, movie) :
    companies = catalogo["production_countries"]
    movieId = movie["id"]
    name = movie["production_countries"]
    existauthor = mp.contains(companies, name)
    if existauthor:
        entry = mp.get(companies, name)
        company = me.getValue(entry)
    else:
        company = newCountry()
        mp.put(companies, name, company)
    lt.addLast(company['movies'], movieId)

    companyAvg = company["vote_average"]
    movieAvg = movie["vote_average"]
    if (movieAvg == 0.0):
        company["vote_average"] = float(movieAvg)
    else:
        moviesNum = lt.size(company["movies"])
        company["vote_average"] = ((companyAvg*(moviesNum-1)) + float(movieAvg)) / moviesNum
        
# ==============================
# Funciones de Comparacion
# ==============================

def compareMoviesIds(id, entry):
    """
    Compara dos ids de peliculas
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return - 1
        
def compareProductionCompanies(id, entry):
    """
    Compara dos ids de compañias productoras
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareGenres(id, entry):
    """
    Compara dos ids de compañias productoras
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

# ___________________________________________________
#  Requerimientos
# ___________________________________________________

def descubrirProductoras(catalogo, Productora):
    movies = getMoviesByCompany(catalogo, Productora)
    try:
        moviesNum = lt.size(movies[0])
    except:
        moviesNum = 0
    
    return (movies[0],movies[1],moviesNum)

def entenderGenero(catalogo, genero):
    movies = getMoviesByGenre(catalogo, genero)
    try:
        moviesNum = lt.size(movies[0])
    except:
        moviesNum = 0
    
    return (movies[0],movies[1],moviesNum)

def entenderActor(catalogo, actor):
    movies = getMoviesByActor(catalogo, actor)
    try:
        moviesNum = lt.size(movies[0])
    except:
        moviesNum = 0
    
    return (movies[0], movies[1], movies[2], moviesNum)

def entenderDirector(catalogo, director):
    movies = getDirector(catalogo, director)
    try:
        moviesNum = lt.size(movies[0])
    except:
        moviesNum = 0
    
    return (movies[0], movies[1], moviesNum)

def entenderPais(catalogo, pais):
    movies = getMoviesByCountry(catalogo, pais)
    try:
        moviesNum = lt.size(movies[0])
    except:
        moviesNum = 0
    
    return (movies[0],movies[1],moviesNum)
