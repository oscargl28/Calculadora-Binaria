from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
import UI
import itertools
from sympy import *


setA = set()
setB = set()
setC = set()
setU = set()
setcompA = set()
setcompB = set()
setcompC = set()

quitar = ['A', 'B', 'C', '=', '{', '}', 'U']
dic = {"A": setA, "B": setB, "C": setC, "U": setU, "A'": setcompA, "B'": setcompB, "C'": setcompC}


def crear_conjunto(string, conjunto, operacion_text=''):
    for i in quitar:
        if i in string:
            string = string.replace(i, '')
    for i in string.split(','):
        conjunto.add(i)
    ui.operacion.setText(ui.operacion.text() + operacion_text)


def add_text(char):
    ui.operacion.setText(ui.operacion.text() + char)


def complemento():
    # Crear conjunto Universo
    crear_conjunto(str(ui.universo.text()), setU)
    try:
        # Encontrar conjunto por complementar
        conj = ui.operacion.text()[-1]
        if conj not in "ABC":
            all_clear()
            ui.resultado.setPlainText("Operacion Inválida")
            return 0
        # Agregar '
        ui.operacion.setText(ui.operacion.text() + "'")
        # Encontrar diferencia con U
        comp = setU.difference(dic.get(conj))
        # Cambiar conjunto a complemento del conjunto x --> x'
        conj = conj + "'"
        # Agregar los elementos al complemento correspondiente
        for i in comp:
            dic.get(conj).add(i)
        print(dic.get(conj))
    except Exception:
        return 0


def parentesis():
    if (ui.operacion.text().count("(") + ui.operacion.text().count(")")) % 2 == 0:
        add_text("(")
    else:
        add_text(")")


# CHECAR OPERACIONES CON COMPLEMENTOS (QUE SI DEN)
def op_parentesis(string):
    print(string)
    conjunto = set()
    # Ya no busca parentesis porque recibe un string sin parentesis ( )
    # op es el index de la operacion
    op = 1
    conj1 = string[0]
    # Para calcular el complemento de un solo conjunto sin otra operacion
    if len(string) == 2 and string[1] == "'":
        conj1 = conj1 + "'"
        conjunto = dic.get(conj1)
        print(dic.get(conj1))
    else:
        conj2 = string[-1]
        # si el primer conjunto es complemento
        if string[1] == "'":
            conj1 = conj1 + "'"
            # recorremos la posicion del parentesis ( porque ahora la operacion estará un indice despues
            op += 1
        # si el conjunto es complemento cambia el objeto
        if conj2 == "'":
            conj2 = string[-2] + "'"
        print(conj1)
        print(conj2)
        if string[op] == "∪":
            # se remplaza la clave dentro de var conj que esta dentro del diccionario por el objeto que le corresponde
            conjunto = dic.get(conj1).union(dic.get(conj2))
            print(conjunto)
        elif string[op] == '∩':
            conjunto = dic.get(conj1).intersection(dic.get(conj2))
            print(conjunto)
        elif string[op] == '-':
            conjunto = dic.get(conj1).difference(dic.get(conj2))
            print(conjunto)
        # Producto Cartesiano
        elif string[op] == 'x':
            conjunto = set(itertools.product(dic.get(conj1), dic.get(conj2)))
            print(conjunto)
    return conjunto


def resultado():
    if ui.mod_prop.isVisible():
        ui.operacion.setText(ui.operacion.text() + ui.btn_igual.text())
        conjunto = set()
        # Si no dio click en los botones, entonces no se crea el conjunto y se le notifica
        if ('A' in ui.operacion.text() and len(setA) == 0) or ('B' in ui.operacion.text() and len(setB) == 0) or \
                ('C' in ui.operacion.text() and len(setC) == 0) or ("'" in ui.operacion.text() and len(setU) == 0):
            ui.operacion.clear()
            return 0
        # Si a la operacion le hace falta un parentesis
        if (ui.operacion.text().count("(") + ui.operacion.text().count(")")) % 2 != 0:
            ui.resultado.setPlainText("Operación Inválida")
            return 0
        # Si se intenta calcular más de un producto cartesiano
        if ui.operacion.text().count("x") > 1:
            ui.resultado.setPlainText("Operación Inválida")
            return 0

        # Si se tiene una operación con más de un par de parentesis
        try:
            if ui.operacion.text().count("(") > 1:
                # si en los primeros indices encuentra ' se recorren las posiciones
                count = ui.operacion.text()[1:6].count("'")
                # Se crean substrings de las dos operaciones a realizar
                substring1 = ui.operacion.text()[1:4 + count]
                print(count)
                substring2 = ui.operacion.text()[7 + count:-2]
                x = op_parentesis(substring1)  # x y y se pueden quitar y llamar la función directo en las operaciones
                y = op_parentesis(substring2)
                # Se calculan los resultados de esas dos operaciones según la operación principal
                # Si es una unión
                if ui.operacion.text()[5 + count] == '∪':
                    # se remplaza la clave dentro de var conj que esta dentro del
                    # diccionario por el objeto que le corresponde
                    conjunto = x.union(y)
                    print(conjunto)
                # Si es una intersección
                elif ui.operacion.text()[5 + count] == '∩':
                    conjunto = x.intersection(y)
                    print(conjunto)
                # Si es una resta
                elif ui.operacion.text()[5 + count] == '-':
                    conjunto = x.difference(y)
                    print(conjunto)

            # Si es operación con un solo paréntesis
            elif "(" in ui.operacion.text():
                # Los pongo aquí aunque ya esten dentro de la función porque si no no los reconoce,
                # para quitar esto se pueden poner globales en la funcion op_parentesis (parentesis1, parentesis2)
                parentesis1 = ui.operacion.text().index("(")
                parentesis2 = ui.operacion.text().index(")")
                # Lo asignamos a una variable (se puede poner directo)
                conjunto = op_parentesis(ui.operacion.text()[parentesis1 + 1:parentesis2])
                # Si antes del parentesis esta la otra operación y es una unión
                if ui.operacion.text()[parentesis1 - 1] == '∪':
                    # Si es un complemento
                    if ui.operacion.text()[parentesis1 - 2] == "'":
                        conj1 = ui.operacion.text()[parentesis1 - 3] + "'"
                        conjunto = conjunto.union(dic.get(conj1))
                    # Si se unia con A con B o con C
                    else:
                        conj1 = ui.operacion.text()[parentesis1 - 2]
                        conjunto = conjunto.union(dic.get(conj1))
                    print(conjunto)

                # Si antes del parentesis esta la otra operación y es una intersección
                elif ui.operacion.text()[parentesis1 - 1] == '∩':
                    if ui.operacion.text()[parentesis1 - 2] == "'":
                        conj1 = ui.operacion.text()[parentesis1 - 3] + "'"
                        conjunto = conjunto.intersection(dic.get(conj1))
                    else:
                        conj1 = ui.operacion.text()[parentesis1 - 2]
                        conjunto = conjunto.intersection(dic.get(conj1))
                    print(conjunto)

                # Si antes del parentesis esta la otra operación y es una resta
                elif ui.operacion.text()[parentesis1 - 1] == '-':
                    # Si es un complemento
                    if ui.operacion.text()[parentesis1 - 2] == "'":
                        conj1 = ui.operacion.text()[parentesis1 - 3] + "'"
                        conjunto = conjunto.difference(dic.get(conj1))
                    else:
                        conj1 = ui.operacion.text()[parentesis1 - 2]
                        conjunto = conjunto.difference(dic.get(conj1))
                    print(conjunto)

                # Si despues del parentesis esta la otra operación y es una unión
                elif ui.operacion.text()[parentesis2 + 1] == '∪':
                    # Si es un complemento
                    if ui.operacion.text()[parentesis2 + 3] == "'":
                        conj1 = ui.operacion.text()[parentesis2 + 2] + "'"
                        conjunto = conjunto.union(dic.get(conj1))
                    else:
                        conj1 = ui.operacion.text()[parentesis2 + 2]
                        print(conj1)
                        conjunto = conjunto.union(dic.get(conj1))
                    print(conjunto)

                # Si despues del parentesis esta la otra operación y es una intersección
                elif ui.operacion.text()[parentesis2 + 1] == '∩':
                    # Si es un complemento
                    if ui.operacion.text()[parentesis2 + 3] == "'":
                        conj1 = ui.operacion.text()[parentesis2 + 2] + "'"
                        conjunto = conjunto.intersection(dic.get(conj1))
                    else:
                        conj1 = ui.operacion.text()[parentesis2 + 2]
                        conjunto = conjunto.intersection(dic.get(conj1))
                    print(conjunto)
                # Si despues del parentesis esta la otra operación y es una resta
                elif ui.operacion.text()[parentesis2 + 1] == '-':
                    # Si es un complemento
                    if ui.operacion.text()[parentesis2 + 3] == "'":
                        conj1 = ui.operacion.text()[parentesis2 + 2] + "'"
                        conjunto = conjunto.difference(dic.get(conj1))
                    else:
                        conj1 = ui.operacion.text()[parentesis2 + 2]
                        conjunto = conjunto.difference(dic.get(conj1))
                    print(conjunto)
            # Si son operaciones sin parentesis
            else:
                # calcular solo el complemento de un conjunto esta dentro de la funcion
                conjunto = op_parentesis(ui.operacion.text().replace("=", ""))
            # Muestra el resultado
            if len(conjunto) == 0:  # Si esta vacío
                ui.resultado.setPlainText(ui.operacion.text() + " { }")
            else:
                ui.resultado.setPlainText(ui.operacion.text() + " " + str(conjunto))
        except Exception:
            ui.resultado.setPlainText("Operación Inválida")
            ui.operacion.clear()
    ui.operacion.setText(ui.operacion.text().replace('=', ''))


def delete():
    ui.operacion.setText(ui.operacion.text()[:-1])
    ui.resultado.clear()


def all_clear():
    setA.clear()
    setB.clear()
    setC.clear()
    setU.clear()
    setcompA.clear()
    setcompB.clear()
    setcompC.clear()
    ui.operacion.clear()
    ui.conjA.clear()
    ui.conjB.clear()
    ui.conjC.clear()
    ui.universo.clear()
    ui.resultado.clear()
    ui.tabla.setRowCount(1)
    ui.tabla.setColumnCount(0)


def modo(widget1, widget2):
    all_clear()
    ui.stackedWidget.setCurrentWidget(widget1)
    ui.stackedWidget_2.setCurrentWidget(widget2)


# PROPOSICIONES
##############################################################################
prop_symbols = {'¬': '~', 'v': '|', '^': '&', '→': '>>'}
global values, rows, variables, sorted_variables


def tf_values(expr_string):
    global values, rows, variables, sorted_variables

    # genera valores de verdad y almacena en arreglos
    expr = sympify(expr_string)
    variables = sorted(expr.free_symbols, key=default_sort_key)

    rows = 0
    sorted_values = []
    expr_truth_value = []
    for truth_values in cartes([True, False], repeat=len(variables)):
        values = dict(zip(variables, truth_values))
        sorted_values.append(sorted(values.items(), key=default_sort_key))
        expr_truth_value.append(expr.subs(values))
        rows += 1

    return sorted_values, expr_truth_value


def bicondicional_format(expr_string):
    if '↔' in expr_string:
        split_str = expr_string.split('↔')
        expr_string = "(" + "(" + split_str[0] + ")" + ">>" + "(" + split_str[1] + ")" + ")" + \
                      "&" + "(" + "(" + split_str[0] + ")" + "<<" + "(" + split_str[1] + ")" + ")"
    return expr_string


def is_equivalent(expr_string):
    split_str = expr_string.split('≡')
    split_str[0] = bicondicional_format(split_str[0])
    split_str[1] = bicondicional_format(split_str[1])

    try:
        tf_table_1, expr_truth_values1 = tf_values(split_str[0])
        tf_table_2, expr_truth_values2 = tf_values(split_str[1])
    except SympifyError:
        table_msg("Operación invalida")
        return

    ui.tabla.setColumnCount(3)
    ui.tabla.setRowCount(rows)
    split_op = ui.operacion.text().split('≡')
    ui.tabla.setHorizontalHeaderItem(0, QTableWidgetItem(split_op[0]))
    ui.tabla.setHorizontalHeaderItem(1, QTableWidgetItem(split_op[1]))
    ui.tabla.setHorizontalHeaderItem(2, QTableWidgetItem("Equivalente:"))

    for row in range(rows):
        ui.tabla.setItem(row, 0, QTableWidgetItem(str(expr_truth_values1[row])))
        ui.tabla.setItem(row, 1, QTableWidgetItem(str(expr_truth_values2[row])))

    if expr_truth_values1 == expr_truth_values2:
        ui.tabla.setItem(0, 2, QTableWidgetItem("True"))
    else:
        ui.tabla.setItem(0, 2, QTableWidgetItem("False"))


def resultado_tablas():
    if ui.mod_conj.isVisible():
        stylesheet = "::section{Background-color:rgb(250,250,250)}"
        ui.tabla.horizontalHeader().setStyleSheet(stylesheet)
        ui.tabla.horizontalHeader().show()
        expr_string = ui.operacion.text()

        # reemplaza simbolos para que la expresión pueda ser leida por sympy
        for symbol, replacement in prop_symbols.items():
            expr_string = expr_string.replace(symbol, replacement)

        # busca equivalencia
        if '≡' in expr_string:
            is_equivalent(expr_string)
            return

        # busca bicondicional
        expr_string = bicondicional_format(expr_string)

        # genera valores de verdad
        try:
            sorted_values, expr_truth_value = tf_values(expr_string)
        except SympifyError:
            table_msg("Operación invalida")
            return

        # determina la cantidad de columnas
        ui.tabla.setColumnCount(len(values) + 1)
        ui.tabla.setRowCount(rows)

        # pone encabezados en columnas
        column = 0
        for variable in variables:
            ui.tabla.setHorizontalHeaderItem(column, QTableWidgetItem(str(variable)))
            column += 1

        # pone la operacion en el encabezado de la ultima columna
        ui.tabla.setHorizontalHeaderItem(column, QTableWidgetItem(ui.operacion.text()))

        # llena la tabla
        row = 0
        for value in sorted_values:
            for column in range(0, len(value)):
                ui.tabla.setItem(row, column, QTableWidgetItem(str(value[column][1])))
            ui.tabla.setItem(row, len(value), QTableWidgetItem(str(expr_truth_value[row])))
            row += 1

        # ajusta el tamaño de la tabla
        for column in range(0, ui.tabla.columnCount()):
            ui.tabla.setColumnWidth(column, int(ui.tabla.width() / ui.tabla.columnCount()))


def table_msg(message):
    ui.tabla.setColumnCount(1)
    ui.tabla.setRowCount(1)
    ui.tabla.horizontalHeader().hide()
    ui.tabla.setItem(0, 0, QTableWidgetItem(message))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UI.Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.setFixedWidth(461)
    main_window.setFixedHeight(553)
    ui.stackedWidget.setCurrentWidget(ui.conjuntos)
    ui.stackedWidget_2.setCurrentWidget(ui.mod_prop)

    # FUNCIONES
    ##############################################################################

    # CONJUNTOS
    ui.btn_conjA.clicked.connect(lambda: crear_conjunto(ui.conjA.text(), setA, 'A'))
    ui.btn_conjB.clicked.connect(lambda: crear_conjunto(ui.conjB.text(), setB, 'B'))
    ui.btn_conjC.clicked.connect(lambda: crear_conjunto(ui.conjC.text(), setC, 'C'))

    ui.btn_parentesis.clicked.connect(parentesis)
    ui.btn_union.clicked.connect(lambda: add_text('∪'))
    ui.btn_interseccion.clicked.connect(lambda: add_text('∩'))
    ui.btn_resta.clicked.connect(lambda: add_text('-'))
    ui.btn_producto.clicked.connect(lambda: add_text('x'))
    ui.btn_a.clicked.connect(complemento)

    # PROPOSICIONES
    ui.btn_p.clicked.connect(lambda: add_text("p"))
    ui.btn_q.clicked.connect(lambda: add_text("q"))
    ui.btn_r.clicked.connect(lambda: add_text("r"))

    ui.btn_equiv.clicked.connect(lambda: add_text("≡"))
    ui.btn_birelaccional.clicked.connect(lambda: add_text("↔"))
    ui.btn_relacional.clicked.connect(lambda: add_text("→"))

    ui.btn_and.clicked.connect(lambda: add_text("^"))
    ui.btn_or.clicked.connect(lambda: add_text("v"))
    ui.btn_not.clicked.connect(lambda: add_text("¬"))

    ui.btn_par2.clicked.connect(parentesis)

    # OTRAS FUNCIONES
    ui.btn_modConj.clicked.connect(lambda: modo(ui.conjuntos, ui.mod_prop))
    ui.btn_modProp.clicked.connect(lambda: modo(ui.proposiciones, ui.mod_conj))
    ui.tabla.horizontalHeader().show()
    main_window.setWindowIcon(QtGui.QIcon('Recursos/icon.ico'))

    # BORRAR
    ui.btn_del.clicked.connect(delete)
    ui.btn_ac.clicked.connect(all_clear)

    # RESULTADO
    ui.btn_igual.clicked.connect(resultado)
    ui.btn_igual.clicked.connect(resultado_tablas)

    ##############################################################################

    main_window.show()
    sys.exit(app.exec_())
