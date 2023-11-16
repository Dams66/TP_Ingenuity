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

    # Test getOlderImage
    gestionTableau.addImgToList(image1)
    gestionTableau.addImgToList(image2)
    gestionTableau.addImgToList(image4)
    print("\nTest getOlderImage : ")
    print("L'image la plus ancienne est :")
    gestionTableau.getOlderImage().toString()
    print("Parmis :")
    gestionTableau.toString()

    # Test CloserFree
    print("\nTest closerFree : ")
    image5 = Image(100.0, 460.0, "https://example.com/image5.jpg", 300)
    image6 = Image(460.0, 460.0, "https://example.com/image6.jpg", 350)
    image7 = Image(820.0, 460.0, "https://example.com/image7.jpg", 400)
    image8 = Image(1180.0, 460.0, "https://example.com/image8.jpg", 450)
    image9 = Image(100.0, 820.0, "https://example.com/image9.jpg", 500)
    image10 = Image(460.0, 820.0, "https://example.com/image10.jpg", 550)
    image11 = Image(820.0, 820.0, "https://example.com/image11.jpg", 600)
    image12 = Image(1180.0, 820.0, "https://example.com/image12.jpg", 650)
    image13 = Image(100.0, 100.0, "https://example.com/image13.jpg", 700)
    gestionTableau.addImgToList(image5)
    print("Résultat attendu : Emplacement 6(460.0, 460.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image6)
    print("Résultat attendu : Emplacement 7(820.0, 460.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image7)
    print("Résultat attendu : Emplacement 8(1180.0, 460.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image8)
    print("Résultat attendu : Emplacement 9(100.0, 820.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image9)
    print("Résultat attendu : Emplacement 10(460.0, 820.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image10)
    print("Résultat attendu : Emplacement 11(820.0, 820.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image11)
    print("Résultat attendu : Emplacement 12(1180.0, 820.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image12)
    print("Résultat attendu : Emplacement 1(100.0, 100.0)")
    print(gestionTableau.closerFree())
    gestionTableau.addImgToList(image13)
    print("Résultat attendu : Emplacement 2(460.0, 100.0)")
    print(gestionTableau.closerFree())

    # Test Ordering
    print("\nTest Ordering : ")
    print("Before ordering : ")
    gestionTableau.toString()
    gestionTableau.order()
    print("After ordering : ")
    gestionTableau.toString()

    gestionTableau.listImages.clear()

    print("\nTest Ordering 2 : ")
    image14 = Image(820.0, 100.0, "https://example.com/image14.jpg", 300)
    image15 = Image(460.0, 100.0, "https://example.com/image15.jpg", 350)
    gestionTableau.addImgToList(image14)
    gestionTableau.addImgToList(image15)
    print("Before ordering : ")
    gestionTableau.toString()
    gestionTableau.order()
    print("After ordering : ")
    gestionTableau.toString()
