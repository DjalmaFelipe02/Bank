def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo) #A getattr()função retorna o valor do atributo especificado do objeto especificado.
        #SINTAXE: getattr(object, attribute, default)

    return total
