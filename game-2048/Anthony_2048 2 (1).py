#   Anthony Vuagniaux
#   22.01.2024
#   game_2048
from tkinter import *   #importer tkinter
from tkinter import messagebox #import messagebox
from random import randrange     #import randrange




#fonctions qui fait apparaitre un random
def spawn_random_number():
    while 1:
        col = randrange(4)
        line = randrange(4)
        if tableau[line][col] == 0:
            tableau[line][col] = random_2_4()
            break


#fonctions qui fait apparaitre un random,avec une chance sur 6 d'avoir 4 dans une case
def random_2_4():
    random_number = randrange(10)
    if random_number == 6:
        return 4
    else:
        return 2


#fonction qui reset le tableau et le score
def reset_game():
    global score, tableau
    score = 0
    tableau = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]

    spawn_random_number()
    spawn_random_number()
    update_score()
    update()



score = 0 # initier le score à 0
top_score = 0 # initier le Top_score à 0


#fonction qui fait les mouvements des cases
def moov(nb,nb1,nb2,nb3):
    global score
    moovement = 0
    if nb3 > 0 and nb2 == 0:
        nb2 = nb3
        nb3 = 0
        moovement +=1
    if nb2 > 0 and nb1 == 0:
        nb1 = nb2
        nb2 = nb3
        nb3 = 0
        moovement +=1
    if nb1 > 0 and nb==0:
        nb = nb1
        nb1 = nb2
        nb2 = nb3
        nb3 = 0
        moovement += 1
    #deplacement fin
    # début addition des cases
    if nb == nb1 and nb > 0:
        nb += nb1
        nb1 = nb2
        nb2 = nb3
        nb3 = 0
        score += nb
    if nb1 == nb2 and nb1 >0:
        nb1 += nb2
        nb2 = nb3
        nb3 = 0
        score += nb1

    if nb2 == nb3 and nb2 >0:
        nb2 += nb3
        nb3 =0
        score += nb2

    return [nb, nb1,nb2,nb3,moovement]


#fonction pour le meilleur score et affiche le message Vous avez battu votre meilleur score!!
def update_score():
    global score, top_score
    update()
    if (score > top_score):
        top_score = score
        #print("Vous avez battu votre meilleur score!!")
    label_score.config(text=f"score : {score}")
    label_meilleur_sc.config(text=f"MEILLEUR SCORE : {top_score}")


def win_game():
    global score, top_score,tableau
    for col in tableau:
        for line in col:
            if (line == 2048):
                messagebox.showinfo("Félicitations!", "Vous avez gagné!")

    # if 2048 in tableau:  # Condition de victoire, ajustez selon vos besoins
    #     messagebox.showinfo("Félicitations!", "Vous avez gagné!")
    #     reset_game()  # Réinitialiser le jeu


    update()
def loose():
    for col in range(4):
        for line in range(4):
            current_box = tableau[col][line]
            if (current_box == 0):
                return False
            if col != 3 and current_box == tableau[col +1][line]:
                return False
            if line != 3 and current_box == tableau[col][line+1]:
                return False
    return True

def update():
    for line in range(len(tableau)):
        for col in range(len(tableau[line])):
            # creation without placement
            if tableau[line][col] != 0:
                labels_grid[line][col].config(text=tableau[line][col],bg=color[tableau[line][col]])
            else:
                labels_grid[line][col].config(text="", bg=color[tableau[line][col]])


#fonction pour les touches du clavier ,pour que quand on prese ca dit la touche
def on_key_press(key):
    key = key.keysym
    moovement = 0
    if key =="Up" or key =="w":
        for i in range(0, 4):
            [tableau[0][i], tableau[1][i], tableau[2][i], tableau[3][i],nb_moovement] = moov(tableau[0][i], tableau[1][i], tableau[2][i], tableau[3][i])
            moovement += nb_moovement
    if key =="Down" or key =="s":
        for i in range(0, 4):
            [tableau[3][i], tableau[2][i], tableau[1][i], tableau[0][i],nb_moovement] = moov(tableau[3][i], tableau[2][i], tableau[1][i], tableau[0][i])
            moovement += nb_moovement

    if key == "Left" or key == "a":
        for i in range(0,4):
            [tableau[i][0], tableau[i][1], tableau[i][2], tableau[i][3],nb_moovement] = moov(tableau[i][0], tableau[i][1], tableau[i][2], tableau[i][3])
            moovement += nb_moovement

    if key == "Right" or key == "d":
        for i in range(0,4):
            [tableau[i][3], tableau[i][2], tableau[i][1], tableau[i][0],nb_moovement] = moov(tableau[i][3], tableau[i][2], tableau[i][1], tableau[i][0])
            moovement += nb_moovement
    if (moovement > 0):
        spawn_random_number()
        if (loose() == True):
            update()
            messagebox.showinfo("Défaite", "Vous avez perdu..")
            reset_game()
    if key == "q":
        quitter = messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application ?")
        if quitter == True:
            quit()
    win_game()
    update_score()





#création de la fenêtre
window = Tk()
window.title("jeu 2048")
window.geometry("500x520")
window.config(bg="#ADBEE2")
window.bind("<Key>", on_key_press)

tableau= [[0, 0, 0,0],
        [0, 0, 0,0],
        [0, 0, 0,0],
        [0, 0, 0,0]]

numbers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]




# liste numéro et association des couleurs
color = {
    0: 'pink',
    2: '#ffff00',
    4: '#ff9900',
    8: '#dddddd',
    16: '#93C47D',
    32: '#F1C232',
    64: '#E06666',
    128: '#9CB8F5',
    256: '#009E0F',
    512: '#E69138',
    1024: '#597EAA',
    2048: '#674EA7',
}


# 2 dimensions list (empty, with labels in the future)
labels_grid=[[None,None,None,None],[None,None,None,None],[None,None,None,None],[None,None,None,None]]


dx=10# horizontal distance between labels
dy=10 # vertical distance between labels

#interface_duhaut
#frame global
frame_global = Frame(window,bg="#ADBEE2")
frame_global.pack(fill=BOTH)
#frame1,label(titre,bouton)
frame1 = Frame(frame_global,bg="#ADBEE2")
frame1.pack(fill=BOTH,pady=40)

label_titre = Label(frame1,text="2048",font=("Arial",25,"bold"), bg="#ADBEE2")
label_titre.pack(side=LEFT,padx=40)

bouton_reset= Button(frame1, text="Nouveau", width=16,command=reset_game).pack(side=RIGHT,padx=25)
#frame2,label(score,meilleurs)
frame2 = Frame(frame_global)
frame2.pack(fill=BOTH)
label_score = Label(frame2,text="SCORE :")
label_score.pack(side=LEFT,padx=40)
label_meilleur_sc = Label(frame2,text="MEILLEURE SCORE :")
label_meilleur_sc.pack(side=RIGHT,padx=40)  #interface_duhaut



fr_center = Frame(window,bg="gray")
fr_center.pack()
#labels creation and position (1. Creation 2. position)
for line in range(len(tableau)):
    for col in range(len(tableau[line])):
        if tableau[line][col] != 0:

            # creation without placement
            labels_grid[line][col] = Label(fr_center, text=tableau[line][col], width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 15), bg=color[tableau[line][col]])
            # label positionning in the windows
            labels_grid[line][col].grid(row=line+1, column=col, padx=dx, pady=dy)
        else:
            labels_grid[line][col] = Label(fr_center, text="", width=6, height=3, borderwidth=1, relief="solid", font=("Arial", 15), bg=color[tableau[line][col]])
            # label positionning in the windows
            labels_grid[line][col].grid(row=line+1, column=col, padx=dx, pady=dy)

spawn_random_number()
spawn_random_number()
update()





window.mainloop()