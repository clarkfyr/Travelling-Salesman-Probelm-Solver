import random



for num in range(1, 4):
    file = open("../input/"+str(num)+".in", "w")
    n = random.randint(1, 500)
    file.write(str(n) + "\n")
    for i in range(n): # row
        for j in range(n): # column
            if i == j:
                utility = random.randint(0, 99)
                file.write(str(utility) + " ")
            else:
                if_edge = random.randint(0, 1)
                file.write(str(if_edge) + " ")

        file.write("\n")

    file.close()