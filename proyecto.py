import copy
import math
import random
from scipy.spatial.distance import hamming as ham



class CHC:

    def __init__(self, archivo):

        f = open(archivo)

        self.tam_crom = int(f.readline())
        print ("Numero instancias: " + str(self.tam_crom))

        self.tip = f.readline()
        self.tip = self.tip.strip().split('\t')
        print("Tipo de atributos ")
        print(self.tip)
        f.readline()

        self.lines = f.readlines()
        f.close()

        self.crom_ini = []
        for i in range(self.tam_crom):
            self.crom_ini.append(1)

        print ("Cromosoma inicial ")
        print (self.crom_ini)


    def init_P(self, t):

        print("Poblacion Inicial ")
        self.pob = {}
        crom = []
        self.tam = t

        for i in range(self.tam):
            for e in range(self.tam_crom):
                crom.append(random.randrange(0,2))
            self.pob[i] = crom
            crom = []


        print (self.pob)
        return self.pob


    #Evalua a la poblacion
    def eval_P(self, p):
        self.eval = {}
        form = ""
        for e in range(len(self.tip[:-1])):
            if self.tip[e] == '0':
                form += 'num' + '\t'
            else:
                form += 'attr' + '\t'
        form += 'class'
        #print("Formato: " + form)

        c_i = 0
        for ip in range(len(p)):
            f_aux = open("aux.txt","w")
            c_e = 0
            v = p[c_i]

            for line in self.lines:
                if v[c_e] == 1:
                    f_aux.write(line)
                c_e += 1
            f_aux.close()
            fit = Clasificador_Bayes("aux.txt", form)
            r = fit.evaluar("T_V")
            self.eval[c_i] = r
            c_i += 1


        f_aux.close()
        print("Evaluaciones")
        print (self.eval)
        return self.eval


    #Evalua cromosoma inicial
    def eval_Crom(self):
        self.eval = {}
        form = ""

        for e in range(len(self.tip[:-1])):
            if self.tip[e] == '0':
                form += 'num' + '\t'
            else:
                form += 'attr' + '\t'
        form += 'class'
        print("Formato: " + form)

        f_aux = open("aux.txt","w")
        for line in self.lines:
            f_aux.write(line)
        f_aux.close()

        fit = Clasificador_Bayes("aux.txt", form)
        fit.evaluar("T_V")


    #HUX
    def hux(self, p, u = 0):
        if u == 0:
            u = self.tam_crom/4

        print ("Umbrar de apareamiento: " + str(u))


        self.p_d = {}
        aux = 0
        for n in range(int(self.tam/2)):

            p1 = p[random.randrange(0, len(p))]
            p2 = p[random.randrange(0, len(p))]

            if ( (ham(p1, p2) * self.tam_crom)  > u):
                m = (ham(p1, p2) * self.tam_crom) / 2
                m = int(m)
                h1 = p1
                h2 = p2

                while (m > 0):
                    bit_p = random.randrange(0, len(p1))
                    if (p1[bit_p] != p2[bit_p]) and (p1[bit_p] != h2[bit_p]):

                        # Crear decendiente de p1, p2
                        aux1 = p2[bit_p]
                        aux2 = p1[bit_p]
                        h1[bit_p] = aux1
                        h2[bit_p] = aux2
                        m -= 1
                self.p_d[aux] = h1
                self.p_d[aux + 1] = h2
                aux += 1

        print("Descendencia")
        print (self.p_d)
        return self.p_d


    #Seleccion elitista
    def sel_eti(self, p, h):
        self.p_n = {}

        print("Seleccion elitista")


        punt_p = g.eval_P(p)
        punt_h = g.eval_P(h)

        pob_total = {}
        l_aux = []
        cont = 0
        for key in p:
            l_aux.append(p[key])
            l_aux.append(punt_p[key])
            pob_total[cont] = l_aux
            l_aux = []
            cont += 1

        for key in h:
            l_aux.append(h[key])
            l_aux.append(punt_h[key])
            pob_total[cont] = l_aux
            l_aux = []
            cont += 1

        print("Poblacion total")
        print(pob_total)


        max = 0
        key_d = None

        for e in range(self.tam):
            for key in pob_total:
                if (pob_total[key][1] >= max):
                    max = pob_total[key][1]
                    key_d = key
            self.p_n[e] = pob_total[key_d]
            max = 0
            del (pob_total[key_d])

        print("Nueva poblacion")
        p_nueva = {}

        for key in self.p_n:
            p_nueva[key] = self.p_n[key][0]

        print (self.p_n)

        #-----------

        return p_nueva





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

        f = open(archivo)

        self.tip = f.readline()
        self.tip = self.tip.strip().split('\t')

        lines = f.readlines()
        f.close()

        for line in lines:
            l = line.strip().split('\t')
            clases.append(l[-1])

        total = len(clases)

        #print("Numero de ejemplo: " + str(total))
        #print (clases)


        vector_num = []
        vector_nom = []

        self.tip = self.tip[:-1]

        for line in lines:
            l = line.strip().split('\t')
            l = l[:-1]
            c = 0
            for e in l:
                if (self.tip[c] == '0'):
                    vector_num.append(float(e))
                else:
                    vector_nom.append(e)
                c += 1

            res = self.clasificar(vector_nom, vector_num)
            aciertos.append(res)
            vector_num = []
            vector_nom = []



        #print(aciertos)


        #Calcular porcentaje de aciertos
        c = 0
        for e in range(len(clases)):
            if (clases[e] == aciertos[e]):
                c += 1
        #Regla se tres
        por = (c * 100) / len(clases)
        #print"Porcentaje de aciertos: ", str(por)
        return por

#c = Clasificador_Bayes("datos", "attr\tattr\tattr\tclass")
#print(c.clasificar(['health', 'moderate', 'moderate'], []))
#print(c.clasificar(['both', 'sedentary', 'moderate'], []))


#c2 = Clasificador_Bayes("pima_e", "num\tnum\tnum\tnum\tnum\tnum\tnum\tnum\tclass")
#print("Clase: " + str(c2.clasificar([], [3, 78, 50, 32, 88, 31.0, 0.248, 26])))
#print("Clase: " + str(c2.clasificar([], [2, 197, 70, 45, 543, 30.5, 0.158, 53])))
#print("Clase: " + str(c2.clasificar([], [3, 78, 50, 32, 88, 31.0, 0.248, 26])))
#print("Clase: " + str(c2.clasificar([], [1, 91, 54, 25, 100, 25.2, 0.234, 23])))

#c2.evaluar("pima_v")
#c2.evaluar("pima_v2")

#c3 = Clasificador_Bayes("prueba", "num\tnum\tnum\tnum\tnum\tnum\tnum\tnum\tclass")
#c3.evaluar("pima_v3")

#c4 = Clasificador_Bayes("pima_e2", "num\tnum\tnum\tnum\tnum\tnum\tnum\tnum\tattr\tclass")
#print("Clase: " + str(c4.clasificar(['no'], [1, 91, 54, 25, 100, 25.2, 0.234,  23])))
#print("Clase: " + str(c4.clasificar(['yes'], [2, 197, 70, 45, 543, 30.5, 0.158, 53])))


g = CHC("T")
p = g.init_P(10)
#g.eval_Crom()
desc = g.hux(p)
p2 = g.sel_eti(p,desc)
#g.eval_P(p)

p_aux = copy.deepcopy(p2)
desc= g.hux(p2)
p3 = g.sel_eti(p_aux, desc)
