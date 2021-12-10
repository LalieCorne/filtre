## mails
def mail_recu () :
    """crée une liste de trois chaines de caractère contenant l'expediteur, le sujet et le corps d'un mail"""
    print ('expediteur : ', end ='')
    expediteur = str(input())
    print ('sujet : ', end = '')
    sujet = str(input())
    print ('corps :' , end = ' ')
    corps = str(input())
    return [expediteur, sujet, corps]

## analyse heuristique
def heuristique (mails,mots_interdits) :
    """prends une liste de mail à recevoir contenant les adresses mails ainsi que les messages qui nous sont destinés pour en retirer les message contenant des mots interdits"""
    n = len(mails)
    spams = []
    sujet = []
    message = []
    for k in range (n) :
        sujet.append(mails[k][1])
        message.append(mails[k][2])
    for k in range(len(message)) :
        for i in range(len(mots_interdits)) :
            if ((mots_interdits[i] in message[k]) or (mots_interdits[i] in sujet [k]))and (not(mails[k] in spams)):
                spams.append(mails[k])
    return spams

## liste blanche
def filtre_lb (spams,liste_blanche) :
    """prend une liste de spams et en retire les message vennant d'expediteurs appartenant à la liste blanche"""
    spams2 = []
    for k in range (len(spams)) :
        if not(spams[k][0] in liste_blanche) :
            spams2.append(spams[k])
    return spams2

## liste noire
def filtre_ln (mails,liste_noire) :
    """prend une liste de mails et renvoie les message vennant d'expediteurs appartenant à la liste noire, une liste de spams"""
    spams = []
    for k in range (len(mails)) :
        if (mails[k][0] in liste_noire) and not(mails[k] in spams) :
            spams.append(mails[k])
        return spams

## historique des transactions
def historique (mails, envoyé) :
    """decrete les adresses auxquelles un mail à été envoyé comme non spams"""
    clean = []
    for k in range(len(mails)) :
        if (mails[k][0] in envoyé) and not(mails[k][0] in clean) :
            clean.append(mails[k][0])
    return clean

## base collaborative de spams
def spams (mails,aspams) :
    passe_pas = []
    for k in range(len(mails)) :
        if (mails[k][0] in aspams) and not(mails[k] in passe_pas) :
            passe_pas.append(mails[k])
    return passe_pas

## autoadaptation
def liste_mots (char) :
    """prend une chaine de caractère et en renvoie une lsite de mots"""
    n = len (char)
    liste = []
    mot = ''
    for k in range(n) :
        if char[k] != ' ' :
            mot = mot + char[k]
        else :
            liste = liste + [mot]
            mot = ''
    liste = liste + [mot]
    return liste

def moyenne (L) :
    """prend une liste de nombre et en renvoie la moyenne"""
    n = len(L)
    S = 0
    for k in range (n) :
        S = S + L[k]
    return (S/n)

def Adresses (spams) :
    """renvoie un tuple de liste avec d'un coté l'adresse et de l'autre le nombre d'apparition de chaque adresse"""
    adresse = ([],[])
    for k in range (len(spams)) :
        if not(spams[k][0] in adresse[0]) :
            adresse[0].append(spams[k][0])
            adresse[1].append(1)
        else :
            for i in range(len(adresse)) :
                if spams[k][0] == adresse[0][i] :
                     adresse[0][i] = adresse[0][i]+1
    return adresse

def Mots (spams) :
    """renvoie un tuple de liste avec d'un coté les mots et de l'autre le nombre d'apparition de chaque mot"""
    mots = ([],[])
    for k in range(len(spams)) :
        mot = liste_mots (spams[k][1])
        for i in range (len(mot)) :
            if not(mot [i] in mots[0]) :
                mots[0].append(mot[i])
                mots[1].append(1)
            else :
                for j in range(len(mots)) :
                    if mot[i] == mots[0][j] :
                        mots[0][i] = mots[0][j]+1
    for k in range(len(spams)) :
        mot = liste_mots (spams[k][2])
        for i in range (len(mot)) :
            if not(mot [i] in mot[0]) :
                mots[0].append(mot[i])
                mots[1].append(1)
            else :
                for j in range(len(mots[0])) :
                    if mot[i] == mots[0][j] :
                        mots[0][i] = mots[0][j]+1
    return mots

def adapte (spams) :
    """renvoie les mots et les adresse qui ont plus de chances d'êtres des spams"""
    ln = []
    interdits = []
    adresses = Adresses(spams)
    mots = Mots(spams)
    MA = moyenne(adresses[1])
    MM = moyenne(mots[1])
    for k in range(len(adresses[0])) :
        if adresses[1][k] > (2*MA) :
            ln.append(adresses[0][k])
        if mots[1][k] > (2*MM) :
            interdits.append(mots[0][k])
    return ln , interdits

## mails
liste_blanche = ['A','C']
interdits =  ['$','%','reduction']
liste_noire = ['D','E']
envoyé = ['C','F']
mail1 = ['A', 'Salut', 'Bonjour, je suis Maurice']
mail2 = ['B', 'Reduc', 'Grosse reduction de 50%']
mail3 = ['C', 'Remboursement', 'Vous me devez 25$']
mail4 = ['D', 'reduction a ne pas manquer', 'Grosse baisse des prix ne la ratez pas']
mail5 = mail_recu()
mail6 = mail_recu()
mail7 = mail_recu()
mail8 = mail_recu()
mail9 = mail_recu()
mail10 = mail_recu()
reçu = [mail1 , mail2 , mail3 , mail4 , mail5, mail6, mail7, mail8, mail9, mail10]

##total

def Spams (mails,ln,lb,inter,histo) :
    spams = filtre_ln(mails,ln)
    #print(spams)
    spams2 = heuristique(mails,inter)
    #print(spams2)
    for k in range(len(spams)) :
        if not(spams[k] in spams2) :
            spams2.append(spams[k])
    #print(spams2)
    clean = historique(mails,histo)
    #print(clean)
    spams3 = filtre_lb(spams2,lb)
    #print(spams3)
    spams4 = []
    for k in range(len(spams3)) :
        if not(spams3[k] in clean) :
            spams4.append(spams3[k])
    #print(spams4)
    return spams4, adapte(spams4)

## fin

spams = Spams(reçu,liste_noire,liste_blanche,interdits,envoyé)[0]
interdits = interdits + Spams(reçu,liste_noire,liste_blanche,interdits,envoyé)[2]
liste_noire = liste_noire + Spams(reçu,liste_noire,liste_blanche,interdits,envoyé)[1]

#export des mails