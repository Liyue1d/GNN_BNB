import numpy as np
import h5py
import time
import sys

debut=time.time()



#Calcul de la borne supérieure pour un graph de lenAdjacence noeuds
def Borne(lenAdjacence):
	borne=0
	for i in range(0,lenAdjacence):
		borne+=2**i				#la borne sera maximale si chaque noeud est un passage obligatoire. On obtient donc une valeur maximale des passages obligatoires par cette boucle
	a=(lenAdjacence-1)				#le noeud d'arrivée a a pour valeur maximale le noeud lenAdjacence-1 (car les noeuds vont de 0 à lenAdjacence)
	d=(lenAdjacence-1)				#le noeud de départ d a pour valeur maximale le noeud lenAdjacence-1

	#On a donc trois valeurs. Une pour les passages obligatoires, une pour le noeud d'arrivée et une pour le noeud de départ
	da=(a+d*lenAdjacence)*10**(len(str(borne)))	#On considère que les valeur a et d sont en base lenAdjacence (encodage lenAdjacence). On passe en base 10 par le calcul a+d*lenAdjacence. On multiplie alors la valeur obtenue par 10 puissance le nombre de chiffres de la borne. Cela permet de ne pas écraser les valeurs lors de l'addition suivante.
	borne=da+borne

	return borne


#fh est la fonction de hashage. Elle prend en arguments le nombre de noeuds lenAdjacence et une mission T. Elle renvoie le hash de la mission T
def fh(lenAdjacence,T):
	h=0
	for i in range(0,lenAdjacence):
		h+=T[3*i+2]*2**i			#On récupère une première valeur pour les noeuds de passage obligatoire par l'encodage binaire

	a=0
	for i in range(0,lenAdjacence):
		if T[3*i+1]==1:
			a=i				#On récupère le noeud d'arrivée a

	d=0
	for i in range(0,lenAdjacence):
		if T[3*i]==1:
			d=i				#On récupère le noeud de départ d

	da=(a+d*lenAdjacence)*10**(len(str(2**(lenAdjacence))))	#On obtient da par l'encodage lenAdjacence de a et d, et en multipliant par 10 puissance le nombre de chiffres de la valeur maximale obtenue pour les noeuds de passage obligatoire
	h=h+da
	return h


#Création de la liste de toutes les missions possibles du graph
def creerTemp(Adjacence,Missions):
	lenAdjacence=len(Adjacence)
	l=len(Missions)
	borne=Borne(lenAdjacence)			#Calcul de la borne supérieure de l'arbre de lenAdjacence noeuds

	#Création d'un nouveau dataset missionsTemp de taille (borne,1) que l'on remplie de 0. Chaque ligne représente une mission
	if 'missionsTemp' in f.keys():
		f.__delitem__('missionsTemp')
	f.create_dataset('missionsTemp', (borne,1), dtype='i8')
	MissionsTemp=f['missionsTemp']

	#Parcourt de la liste de missions à triées 'Missions'
	for i in range(0,l):
		T=Missions[i,0:3*lenAdjacence]
		h=fh(lenAdjacence,T)			#Calcul du hash de la mission
		MissionsTemp[h]=1			#On remplace 0 par 1 à l'indice h de MissionsTemp
	return(MissionsTemp)


#La fonction depart renvoie le noeud de départ d'une mission T.
def depart(T):
	d=0
	for i in range(0,(len(T))//3):
		if T[3*i]==1:
			d=i
	return d



#La fonction arrivee renvoie le noeud d'arrivée d'une mission T.
def arrivee(T):
	a=0
	for i in range(0,(len(T))//3):
		if T[3*i+1]==1:
			a=i
	return a



#La fonction passages renvoie la liste des noeuds de passage obligatoire d'une mission T.
def passages(T):
	L=[]
	for i in range(0,(len(T))//3):
		if T[3*i+2]==1:
			L+=[i]
	return L



#La fonction surmissionpassageobligatoire prend en arguments une mission T, son noeud de départ d et un noeud adjacent j. Elle renvoie une surmission I ayant pour noeud de départ j et passant obligatoirement par d.
def surmissionpassageobligatoire(T,d,j):
	I=[]
	I+=list(T)
	I[3*d]=0
	I[3*d+2]=1
	I[3*j]=1
	return I



#La fonction surmissionsimple prend en arguments une mission T, son noeud de départ d et un noeud adjacent j. Elle renvoie une surmission J ayant pour noeud de départ j.
def surmissionsimple(T,d,j):
	J=[]
	J+=list(T)
	J[3*d]=0
	J[3*j]=1
	return J


#La fonction sousmission prend en arguments une mission T, son noeud de départ d et un noeud adjacent j. Elle renvoie une sousmission K ayant pour noeud de départ j en enlevant ce noeud j de ses passages obligatoires.
def sousmission(T,d,j):
	K=[]
	K+=list(T)
	K[3*d]=0
	K[3*j]=1
	K[3*j+2]=0
	return K

#La fonction trimissions prend en arguments une matrice d'Adjacence, une base de Missions, et la profondeur d'étude. Elle renvoie la base Missions triée.
def trimissions(Adjacence,Missions,profondeur):
	if profondeur>0:
		lenAdjacence=len(Adjacence)
		l=len(Missions)
		#On initialise la mission nulle Init
		Init=[]
		Init+=3*lenAdjacence*[0]
		#On applique la fonction creerTemp sur la matrice d'adjacence représentant le graph et la liste de missions entrées en arguments pour obtenir la liste de missions MissionsTemp
		MissionsTemp=creerTemp(Adjacence,Missions)

		#X, X2, Y et Y2 sont des variables de stockage de missions dont il faut étudier les surmissions à la prochaine itération de k
		#Parcourt des missions de la liste Missions
		for i in range(0,l):
			print("\i =  %d"%i)
			#Etude de la ième mission de la liste Missions
			T=Missions[i,0:3*lenAdjacence]
			dT=depart(T)
			aT=arrivee(T)
			LT=passages(T)
			indice=fh(lenAdjacence,T)			#hash de la mission T

			#On vérifie que la mission T n'est pas une surmission ou une sousmission d'une autre mission déjà étudiée en regardant si la ligne 'indice' de la liste MissionsTemp est égale à 1
			if MissionsTemp[indice]==1:
				#Etude des surmissions
				X=np.array([Init])
				for j in range(0,lenAdjacence):
					#On cherche les noeuds adjacents qui ne sont pas des noeuds de passage obligatoire
					if Adjacence[dT,j]==1 and j not in LT:
						#Si le noeud de départ est différent du noeud d'arrivée on peut créer une surmission I qui passe obligatoirement par le noeud dT
						if dT!=aT:
							I=surmissionpassageobligatoire(T,dT,j)
							h=fh(lenAdjacence,I)
							#On vérifie que le hash de la mission I soit différent de celui de la mission T qu'on étudie pour éviter de supprimer cette dernière de la base triée
							if h!=indice:
								X=np.concatenate((X,[I]))
								MissionsTemp[h]=0			#On remplace le 1 ou le 0 de la ligne h de la liste MissionsTemp par 0

						#Création de la surmission sans ajouter de noeud de passage obligatoire
						J=surmissionsimple(T,dT,j)
						h=fh(lenAdjacence,J)
						if h!=indice:
							X=np.concatenate((X,[J]))
							MissionsTemp[h]=0

				#La boucle permet d'étudier les surmissions de l'étage supérieur
				for k in range(1,profondeur):
					X2=np.array([Init])
					#Parcourt de la liste de surmissions X
					for h in range(0,len(X)):
						T2=X[h,:]
						d=depart(T2)
						a=arrivee(T2)
						L=passages(T2)

						for j in range(0,lenAdjacence):
							if Adjacence[d,j]==1 and j not in L:
								if d!=a:
									I=surmissionpassageobligatoire(T2,d,j)
									h=fh(lenAdjacence,I)
									if h!=indice:
										X2=np.concatenate((X2,[I]))
										MissionsTemp[h]=0

								J=surmissionsimple(T2,d,j)
								h=fh(lenAdjacence,J)
								if h!=indice:
									X2=np.concatenate((X2,[J]))
									MissionsTemp[h]=0

					X=np.copy(X2)

				#Etude des sousmissions
				Y=np.array([Init])
				#On vérifie que la mission étudiée ne soit pas une mission résolue
				if dT!=aT or LT!=[]:
					for j in range(0,lenAdjacence):
						#On cherche les noeuds adjacents
						if Adjacence[dT,j]==1:
							#Création de la sousmission
							K=sousmission(T,dT,j)
							h=fh(lenAdjacence,K)
							if h!=indice:
								Y=np.concatenate((Y,[K]))
								MissionsTemp[h]=0

				for k in range(1,profondeur):
					Y2=np.array([Init])
					#Parcourt de la liste de sousmissions Y
					for h in range(0,len(Y)):
						T2=Y[h,:]
						d=depart(T2)
						a=arrivee(T2)
						L=passages(T2)

						if d!=a or L!=[]:
							for j in range(0,lenAdjacence):
								if Adjacence[d,j]==1:
									K=sousmission(T2,d,j)
									h=fh(lenAdjacence,K)
									if h!=indice:
										Y2=np.concatenate((Y2,[K]))
										MissionsTemp[h]=0

					Y=np.copy(Y2)

		#Création d'un nouveau dataset filtered_data
		if 'filtered_data' in f.keys():
			f.__delitem__('filtered_data')

		f1.create_dataset('filtered_data', Missions.shape, dtype='i', maxshape=Missions.shape)
		filtered_data=f1['filtered_data']

		#On remplie ce nouveau dataset des missions de Missions
		compteur=0
		for i in range(0,len(Missions)):
			#On calcule le hash de ième missions de Missions et on vérifie si la ligne correspondante dans MissionsTemp est égale à 1
			if MissionsTemp[fh(lenAdjacence,Missions[i,0:3*lenAdjacence])]==1:
				#Si c'est le cas on copie la missions dans filtered_data et on incrémente le compteur
				filtered_data[compteur,:]=Missions[i,:]
				compteur+=1
		#On modifie la taille de filtered_data grâce au compteur
		filtered_data.resize((compteur,Missions.shape[1]))

		#On supprime le dataset missionsTemp pour réduire la taille du fichier hdf5
		if 'missionsTemp' in f.keys():
			f.__delitem__('missionsTemp')
	return filtered_data


#Matrice d'Adjacence à modifier selon le graphe étudié
exec(open("./../input/graph.py").read())

Adjacence = np.asarray(A>0)

#Ouverture en mode lecture du fichier .hdf5 entré en argument
f=h5py.File("../model_utils/raw_data.hdf5",'a')
f1=h5py.File("../model_utils/raw_data_1.hdf5",'w')
#Récupération de la base de missions Missions du fichier .hdf5
Missions=f["raw"]
#Exécution de la fonction trimissions et affichage de la base de missions Missions triée
filtered_data=trimissions(Adjacence,Missions,profondeur)
print(filtered_data)
#Fermeture du fichier Filename.hdf5
f.close()
f1.close()

fin=time.time()
print(fin-debut)
