class Fibonacci:
    """
    Ciąg Fibonacciego w wersji obiektowej:
        atrybuty: lista (wstępnie pusta)
        metody:
            add_number - dodaje do listy kolejny numer ciągu Fibonacciego
            substract_number - odejmuje z listy ostatni numer ciągu Fibonacciego
            add_several_numbers - dodaje do listy n kolejnych liczb ciągu Fibonacciego
            substract_several_numbers - usuwa z listy n ostatnich liczb ciągu Fibonacciego
    """

    __start_list = [0, 1]

    def __init__(self):
        self.list = []

    def add_number(self):
        if len(self.list) >= 2:
            self.list.append(self.list[-2] + self.list[-1])
        else:
            self.list = self.__start_list[:len(self.list) + 1]
        return self.list

    def substract_number(self):
        if len(self.list) >= 1:
            self.list.pop()
        return self.list

    def add_several_numbers(self, n):
        for __ in range(n):
            self.add_number()
        return self.list

    def substract_several_numbers(self, n):
        if n <= len(self.list):
            for __ in range(n):
                self.substract_number()
        return self.list



f1 = Fibonacci()
print(f"Obiekt f1: {f1.list}")
f1.add_number()
print(f"Obiekt f1: {f1.list}")
f1.add_number()
print(f"Obiekt f1: {f1.list}")
f1.add_number()
print(f"Obiekt f1: {f1.list}")
f1.substract_number()
print(f"Obiekt f1: {f1.list}")
f1.add_several_numbers(11)
print(f"Obiekt f1: {f1.list}")
f1.substract_several_numbers(5)
print(f"Obiekt f1: {f1.list}")