import math


class Clasificador_Bayes:
    def __init__(self, archivo, formato):

        total = 0
        classes = {}
        counts = {}

        totals = {}  # Para atributos numericos
        numericValues = {}

        self.formato = formato.strip().split('\t')

        self.prior = {}
        self.conditional = {}

        f = open(archivo)
        lines = f.readlines()
        f.close()

        for line in lines:
            fields = line.strip().split('\t')
            # print(fields)
            vector = []
            nums = []
            for i in range(len(fields)):
                if self.formato[i] == 'num':
                    nums.append(float(fields[i]))
                elif self.formato[i] == 'attr':
                    vector.append(fields[i])
                elif self.formato[i] == 'class':
                    category = fields[i]

            total += 1
            classes.setdefault(category, 0)
            counts.setdefault(category, {})
            totals.setdefault(category, {})
            numericValues.setdefault(category, {})
            classes[category] += 1


            # Atributos no numericos
            col = 0
            for columnValue in vector:
                col += 1
                counts[category].setdefault(col, {})
                counts[category][col].setdefault(columnValue, 0)
                counts[category][col][columnValue] += 1

            # atributos numericos
            col = 0
            for columnValue in nums:
                col += 1
                totals[category].setdefault(col, 0)
                #totals[category][col].setdefault(columnValue, 0)
                totals[category][col] += columnValue
                numericValues[category].setdefault(col, [])
                numericValues[category][col].append(columnValue)

        # p(c)  #
        for (category, count) in classes.items():
            self.prior[category] = (float(count) / float(total))

        # p(c|D)  #
        for (category, columns) in counts.items():
            self.conditional.setdefault(category, {})
            for (col, valueCounts) in columns.items():
                self.conditional[category].setdefault(col, {})
                for (attrValue, count) in valueCounts.items():
                    self.conditional[category][col][attrValue] = (float(count) / float(classes[category]))

        self.tmp = counts

        # Media y desviacion estandar
        self.means = {}
        self.totals = totals
        for (category, columns) in totals.items():
            self.means.setdefault(category, {})
            for (col, cTotal) in columns.items():
                self.means[category][col] = (float(cTotal) / float(classes[category]))
        # Desviacion estandar
        self.ssd = {}
        for (category, columns) in numericValues.items():
            self.ssd.setdefault(category, {})
            for (col, values) in columns.items():
                sumOfSquareDifferences = 0
                theMean = self.means[category][col]
                for value in values:
                    sumOfSquareDifferences += (value - theMean) ** 2
                columns[col] = 0
                self.ssd[category][col] = math.sqrt(sumOfSquareDifferences / (classes[category] - 1))

    def clasificar(self, itemVector, numVector):
        results = []
        sqrt2pi = math.sqrt(2 * math.pi)
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]:
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            col = 1

            for x in numVector:
                mean = self.means[category][col]
                ssd = self.ssd[category][col]
                ePart = math.pow(math.e, -(x - mean) ** 2 / (2 * ssd ** 2))
                prob *= (1.0 / (sqrt2pi * ssd)) * ePart
                col += 1

            results.append((prob, category))
        return max(results)[1]

    def evaluar(self, archivo):

        clases = []
        aciertos = []
        c = 0;

        f = open(archivo)
        lines = f.readlines()
        f.close()

        for line in lines:
            l = line.strip().split('\t')
            clases.append(l[-1])

        total = len(clases)

        print("Numero de ejemplo: " + str(total))
        print (clases)


        vector = []
        for line in lines:
            l = line.strip().split('\t')
            l = l[:-1]
            for e in l:
                vector.append(float(e))
            res = self.clasificar([], vector)
            aciertos.append(res)
            vector = []

        #Calcular porcentaje de aciertos
        for e in range(len(clases)):
            if (clases[e] == aciertos[e]):
                c += 1
        #Regla se tres
        por = (c * 100) / len(clases)
        print"Porcentaje de aciertos: ", str(por)




c = Clasificador_Bayes("datos", "attr\tattr\tattr\tclass")
print(c.clasificar(['health', 'moderate', 'moderate'], []))
print(c.clasificar(['both', 'sedentary', 'moderate'], []))


c2 = Clasificador_Bayes("pima_e", "num\tnum\tnum\tnum\tnum\tnum\tnum\tnum\tclass")
print("Clase: " + str(c2.clasificar([], [3, 78, 50, 32, 88, 31.0, 0.248, 26])))
print("Clase: " + str(c2.clasificar([], [2, 197, 70, 45, 543, 30.5, 0.158, 53])))
print("Clase: " + str(c2.clasificar([], [3, 78, 50, 32, 88, 31.0, 0.248, 26])))
print("Clase: " + str(c2.clasificar([], [1, 91, 54, 25, 100, 25.2, 0.234, 23])))

c2.evaluar("pima_v")
c2.evaluar("pima_v2")
