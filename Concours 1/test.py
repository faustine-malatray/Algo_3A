
graph_brute = open("./graphs/graph_01_100", 'r')
graph = {}
for ligne in graph_brute:

    # on ne veut pas traiter les 3 lignes d'intro
    if ligne[0] != "#":
        # on récupère l'id du sommet + de ses voisins
        chiffres = []
        chiffre_en_cours = ''
        for caractere in ligne:
            if caractere == ' ' or caractere == '\n':
                chiffres.append(chiffre_en_cours)
                chiffre_en_cours = ''
            else:
                chiffre_en_cours += caractere

        # print(chiffres)
        # on construit le dictionnaire: clés: sommets, valeurs: dict des voisins
        graph[int(chiffres[0])] = {int(chiffres[i])
                                   for i in range(1, len(chiffres))}
