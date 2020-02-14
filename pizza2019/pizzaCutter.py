# import matplotlib.pyplot as plt

class PizzaCutter:

    def __init__(self,path):
        self.path = path
        minIngredients, maxSize, matrix=self.read_input()
        self.matrix = matrix
        self.f = len(matrix)
        self.c = len(matrix[0])
        self.minIngredients = minIngredients
        self.maxSize = maxSize

    def read_input(self):
        with open(self.path, 'r') as file:
            header = file.readline()
            matrix = []
            for line in file:
                row = []
                for char in line:
                    if char == 'T':
                        row.append(0)
                    elif char == 'M':
                        row.append(1)
                matrix.append(row)
            data = header.split(' ')
            minIngredients = int(data[2])
            maxSize = int(data[3])

        return ((minIngredients, maxSize, matrix))

    def filetear(self,ID):
        totalScore=0
        totalTrozos=0
        totalIDs = []
        totaltrozos = []
        i=0
        for row in self.matrix:
            tmpRow = row.copy();
            accScore, mejorComb, mejorCorte,mejorestrozos =self.encontrarMejorFileteado(tmpRow);
            totalScore+=accScore;
            totalTrozos +=  len(mejorCorte)
            totaltrozos.append(mejorestrozos)

            for corte in mejorCorte:
                idEntrega = str(i)+" "+str(corte[0])+" "+str(i)+" "+str(corte[1])
                totalIDs.append(idEntrega)

            i+=1


        f = open('submit_'+ID+'.txt', 'w')
        f.write(str(totalTrozos)+"\n")
        for id in totalIDs:
            f.write(id + "\n")
        f.close()

        f = open('submit_trozos'+ID+'.txt', 'w')
        f.write("los trozos\n")
        for trozosPorfila in totaltrozos:
            f.write(str(trozosPorfila) + "\n")
        f.close()

        f = open('submit_filas' + ID + '.txt', 'w')
        f.write("las filas\n")
        for row in self.matrix:
            f.write(str(row) + "\n")
        f.close()

    def encontrarMejorFileteado(self,row):
        accScore=0
        mejorComb=2*self.minIngredients
        mejorCorte=[]
        mejorestrozos=[]
        # range(2*self.minIngredients,self.maxSize+1)
        for comb in range(2*self.minIngredients,self.maxSize+1):
            if(comb <= self.c):
                tmpRow=row.copy()
                tmpScore, cortes, trozostmp=self.cutYevaluate(comb,tmpRow)
                if(tmpScore > accScore):
                    accScore=tmpScore
                    mejorComb=comb
                    mejorCorte=cortes
                    mejorestrozos=trozostmp

        return(accScore,mejorComb,mejorCorte,mejorestrozos)

    def cutYevaluate(self,corte, row):
        trozos=[row[:corte]]
        cortes=[(0,corte-1)]
        pizza=row[corte:]
        #cortar
        while(len(pizza)>=corte):
            cortes.append(((len(trozos)*corte),(len(trozos)*corte)+corte-1))
            trozos.append(pizza[:corte])
            pizza = pizza[corte:]

        trozostmp = trozos.copy()
        trozos.reverse()
        #evaluar
        score=0;
        i=0
        for trozo in trozos:
            valido = False
            ingredientePrimero=trozo[0]
            cntIP=1
            cntIS=0
            for sigIngrediente in trozo[1:]:
                if not ingredientePrimero == sigIngrediente:
                    cntIS+=1
                else:
                    cntIP+=1

            if(cntIP>=self.minIngredients & cntIS>=self.minIngredients):
                valido=True

            if(valido):
                score += corte
            else:
                indx = len(trozos)-i-1
                trozostmp.pop(indx)
                cortes.pop(indx)
            i+=1

        return score,cortes,trozostmp;


if __name__ == '__main__':

    gestor = PizzaCutter("/input/d_big.in")
    gestor.filetear("D")

    gestor1 = PizzaCutter("/input/a_example.in")
    gestor1.filetear("A")

    gestor2 = PizzaCutter("/input/b_small.in")
    gestor2.filetear("B")

    gestor3 = PizzaCutter("/input/c_medium.in")
    gestor3.filetear("C")

    #plt.matshow(gestor.matrix)
    # plt.show()
