from TabImages import TabImages
from Image import Image

if __name__ == "__main__":
    # Test Création de trois images
    image1 = Image(100.0, 100.0, "https://example.com/image1.jpg", 100)
    image2 = Image(460.0, 100.0, "https://example.com/image2.jpg", 150)
    image3 = Image(820.0, 100.0, "https://example.com/image3.jpg", 200)
    image4 = Image(1180.0, 100.0, "https://example.com/image4.jpg", 250)

    # Test Création du tableau de gestion
    gestionTableau = TabImages()

    # Test Ajout de ces images dans le tableau de gestion
    gestionTableau.addImgToList(image1)
    gestionTableau.addImgToList(image2)
    gestionTableau.addImgToList(image3)
    print("Test add : ")
    gestionTableau.toString()

    # Test du remove dans le tableau
    gestionTableau.removeImgToList(image3)
    print("\nTest remove : ")
    gestionTableau.toString()

    # Test getImagesFromCoord
    print("\nTest getImageFromCoord : ")
    print("Pour x = 0 et y = 0 : ")
    str(gestionTableau.getImageFromCoord(0.0, 0.0))
    print("\nPour x = 100 et y = 100 : ")
    gestionTableau.getImageFromCoord(100.0, 100.0).toString()
    print("\nPour x = 460 et y = 100 : ")
    gestionTableau.getImageFromCoord(460.0, 100.0).toString()

    # Test getAllPlaces
    print("\nTest getAllPlaces : ")
    listAllPLaces = gestionTableau.getAllPlaces()
    print(listAllPLaces)

    # Test isFree
    print("\nTest isFree : ")
    gestionTableau.addImgToList(image4)
    print(gestionTableau.isFree(100.0, 100.0))
    print(gestionTableau.isFree(460.0, 100.0))
    print(gestionTableau.isFree(820.0, 100.0))
    print(gestionTableau.isFree(1180.0, 100.0))

    # Test getFirstPlace
    print("\nTest closerFree : ")
    print("Résultat attendu : (820.0, 100.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image3)
    print("Résultat attendu : (100.0, 460.0)")
    print(gestionTableau.closerFree())
    gestionTableau.removeImgToList(image4)
    print("Résultat attendu : (1180.0, 100.0)")
    print(gestionTableau.closerFree())
    gestionTableau.removeImgToList(image2)
    print("Résultat attendu : (460.0, 100.0)")
    print(gestionTableau.closerFree())
    gestionTableau.removeImgToList(image1)
    print("Résultat attendu : (100.0, 100.0)")
    print(gestionTableau.closerFree())
